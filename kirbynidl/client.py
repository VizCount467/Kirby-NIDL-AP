from typing import TYPE_CHECKING

from NetUtils import ClientStatus

import worlds._bizhawk as bizhawk
#from .Options import KNIDLOptions
from worlds._bizhawk.client import BizHawkClient

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext
    from .world import KirbyNIDLWorld

from .locations import LOCATION_NAME_TO_ID
from .items import ITEM_NAME_TO_ID
import copy

###DATA - Abstract to other files LATER
##APWORLD STUFF
KNIDL_BASE_ID = 2742740
#Table for items that are alone in their rooms and can be mapped to a single location from WLR alone
#For multi-items rooms, will make a separate data table later from the master data source and do something more involved
WLR_TO_LOCATION_NAME_SOLO = {
    (0,0,2) : "Vegetable Valley 1 - Tomato (Waterfall)",
    (0,1,3) : "Vegetable Valley 2 - Tomato (Cave)",
    (0,1,5) : "Vegetable Valley 2 - 1up (Hidden Room)",
    (0,2,3) : "Vegetable Valley 3 - Tomato (Hotheads)",
    (0,3,3) : "Vegetable Valley 4 - 1up (Shotzos)"
}
#Table of door coordinates (XY of left block) (doors are 2x1 blocks) 
#If kirby is in front of the door blocks, the lock byte will be set. 
#Only World 1 for now
#If we enable locking side doors, level doors, define this dict in parts with ref to options
#also maybe abstract the world to an additional layer to make this a list of dicts or something?
OW_WXY_TO_DOOR_NAME = {
    # (0,0x6,0x10) : 'Vegetable Valley 1 Level', ##commented out until level keys are implemented (if ever)
    # (0,0xE,0x12) : 'Vegetable Valley 2 Level',
    # (0,0x13,0xC) : 'Vegetable Valley 3 Level',
    # (0,0x18,0xF) : 'Vegetable Valley 4 Level',
    (0,0x1B,0x7) : 'Vegetable Valley Boss',
    # (0,0xA,0xD) : 'Vegetable Valley Bomb Rally',
    # (0,0xE,0x9) : 'Vegetable Valley Museum',
    # (0,0x1B,0x3) : 'Vegetable Valley Warp Station',
}
#Flesh out the above table with the right block of each door, and all possible surrounding blocks (including diagonals)
for k in list(OW_WXY_TO_DOOR_NAME.keys()):
    for dx in [-1,0,1,2]:
        for dy in [-1,0,1]:
            OW_WXY_TO_DOOR_NAME[(k[0], k[1]+dx, k[2]+dy)] = OW_WXY_TO_DOOR_NAME[k]

#Table for item ID to name (since AP client sends ID's not names, it seems)
ITEM_ID_TO_NAME = dict()
for k in ITEM_NAME_TO_ID.keys():
    ITEM_ID_TO_NAME[ITEM_NAME_TO_ID[k]] = k

#Helper Table that lists all the worlds in order. Can probably abstract this later
WORLD_NAMES_INDEXED = [
    'Vegetable Valley',
    'Ice Cream Island',
    'Butter Building',
    'Grape Garden',
    'Yogurt Yard',
    'Orange Ocean',
    'Rainbow Resort'
]


##ROM ADDRESSES
ROM_HEADER_ADR = 0x0A0 #As it is for all GBA games
##EWRAM ADDRESSES
SYNC_ADR_BASE = 0xE6FC #+ 0x100n for file 2, file 3
FILE_NUMBER_ADR = 0xB074 #Also the sound vs music variable in the sound test
##IWRAM ADDRESSES
SCREEN_MOD_ADR = 0x23D8 
OW_MOD_ADR = 0x23B8
LEVEL_MOD_ADR = 0x1F20
ROOM_MOD_ADR = 0x2468
IW_CLEAR_FLAGS_W1 = [0x2400,0x2401,0x2402,0x2403]
KIRBY_X_ADR = 0x23CC
KIRBY_Y_ADR = 0x2388
#CUSTOM IWRAM (the "control panel")
DOOR_LOCK_ADR = 0x78A0
FOOD_DETECT_ADR = 0x78A1
ONEUP_DETECT_ADR = 0x78A2
ITEM_AWARD_ADR = 0x78A8


class KirbyNIDLClient(BizHawkClient):
    game = "Kirby Nightmare in Dream Land"
    system = "GBA"
    patch_suffix = ".apkirbynidl"

    def __init__(self):
        super().__init__()

        #Internal data setup
        self.last_received_index = 0 #index of last item received; needed so we don't apply filler pickup items multiple times
        self.detected_goal_game = False #flag to prevent repeated send of level clear check during a goal game
        self.ow_wxy_to_locked_doors = copy.copy(OW_WXY_TO_DOOR_NAME)
        self.door_locked = False
        self.clear_flags_written = False
        self.sync_counter = 0
        self.consumable_queue = []

    #Helper function to determine what to write to the control panel and where for consumable items
    def determine_panel_award_write(self, item_award_id):
        panel_adr = None; panel_id = 0
        if item_award_id == 1 or item_award_id == 2:
            panel_adr = FOOD_DETECT_ADR
        elif item_award_id == 3:
            panel_adr = ONEUP_DETECT_ADR
        if item_award_id == 1:
            panel_id = 3
        elif item_award_id == 2 or item_award_id == 3:
            panel_id = 2
        return panel_adr, panel_id
    
    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        try:
            print('INFO: Init KNIDL client validate_rom function')
            # Check ROM name/patch version
            rom_name = ((await bizhawk.read(ctx.bizhawk_ctx, [(ROM_HEADER_ADR, 12, "ROM")]))[0]).decode("ascii")
            if not rom_name.endswith('KIRBY DX'):
                await ctx.send_msgs([
                            {"cmd": "Say", "text": "Incompatible ROM. Check if ROM is a US Kirby NiDL ROM."},
                        ])
                return False
            elif rom_name == 'AGB KIRBY DX':
                await ctx.send_msgs([
                            {"cmd": "Say", "text": "Tried to use unpatched Kirby NiDL ROM. The client is only compatible with the patched US ROM!"},
                        ])
                return False
            elif rom_name == "APR KIRBY DX":
                
                await ctx.send_msgs([
                            {"cmd": "Say", "text": "DEBUG: Recognized patched US Kirby NiDL ROM!"},
                        ])
                print('INFO: KNIDL client recognized and validated rom')
                #Client Context Setup Stuff
                ctx.game = self.game
                ctx.items_handling = 0b011 # gets items from other worlds and OWN world
                ctx.want_slot_data = True
                return True 
            else:
                return False
        except bizhawk.RequestFailedError:
            return False  # Not able to get a response, say no for now
    
    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        try:
            #Check Game State
            #NOTE the bizhawk.read command returns a list of bytes (size 1) or bytearrays (size 1+)
            screen_modb, = await bizhawk.read(ctx.bizhawk_ctx, [
                (SCREEN_MOD_ADR,1, "IWRAM")       
            ])
            screen_mod = int.from_bytes(screen_modb)
            #print(f'INFO: Screen mod is {screen_mod}')

            # Don't do anything if the game is not in a specific state (list all states we will actually use here)
            # For now, we only care about 5 (OW lobby), 7 (World Intro Cutscene), 8 (Normal Level or Boss) and A (Goal Game)
            if not screen_mod in (0x5,0x7,0x8,0xA):
                return
            
            #During the Level Intro Cutscene or any normal level, force all level clear flags to 02 to open the entire OW
            # For now, only set them for World 1
            # This strategy is a problem if savestates are used, but that's whatever for now
            if (not self.clear_flags_written) and (screen_mod == 0x7 or screen_mod == 0x8):
                print(f'INFO: Attempting to write clear flags to unlock all levels')
                clear_flag_writes = []
                for f in IW_CLEAR_FLAGS_W1:
                    clear_flag_writes.append((f, [0x2], "IWRAM"))
                await bizhawk.write(
                    ctx.bizhawk_ctx, clear_flag_writes
                )
                self.clear_flags_written = True
            
            #while in a level or the OW, check to see if there are items to award
            if self.sync_counter != len(ctx.items_received) and (screen_mod == 0x5 or screen_mod == 0x8):
                print(f'INFO: init item sync sequence. Current sync counter is {self.sync_counter}. Number of items received is {len(ctx.items_received)}')
                file_numberb, = await bizhawk.read(ctx.bizhawk_ctx, [
                    (FILE_NUMBER_ADR, 1, "IWRAM")       
                ])
                file_number = int.from_bytes(file_numberb)
                sync_adr = SYNC_ADR_BASE + file_number*0x100
                sync_counterb, = await bizhawk.read(ctx.bizhawk_ctx, [
                    (sync_adr, 1, "IWRAM")       
                ])
                sync_counter = int.from_bytes(sync_counterb, "little")
                #sync counter doesn't match, award items
                if self.sync_counter != len(ctx.items_received):
                    if self.sync_counter > len(ctx.items_received): #Case when sync counter is fresh (FF) or somehow greater than items received
                        self.sync_counter = 0
                    #Loop from latest sync counter to get new items
                    for i in range(sync_counter, len(ctx.items_received)):
                        received_item = ctx.items_received[i]
                        print(f'INFO: newly received item is {ITEM_ID_TO_NAME[received_item.item]}')
                        item_id_readable = received_item.item - KNIDL_BASE_ID 
                        #Consumable Item; hit the item award control byte
                        if item_id_readable in [11,12,13,14]:
                            item_award_id = item_id_readable - 10 #1=drink, 2=tomato, 3=1up, 4=candy

                            #Determine what to write to the control panel so that AP-awarded items don't trigger a pickup check
                            panel_adr, panel_id = self.determine_panel_award_write(item_award_id)
                            
                            print(f'INFO: attempting to write consumable item id {item_award_id} to control panel')
                            #check if the item award control byte is 0. If not, add the consumable to the conumable queue
                            item_award_panelb = await bizhawk.read(ctx.bizhawk_ctx, [
                                (ITEM_AWARD_ADR, 1, "IWRAM")       
                            ])
                            item_award_panel = int.from_bytes(item_award_panelb)
                            if item_award_panel != 0:
                                print(f'INFO: item to award sent to panel, sent item to consumable queue')
                                self.consumable_queue.append(item_award_id)
                            else:
                                item_award_writes = [(ITEM_AWARD_ADR, [item_award_id], "IWRAM")]
                                if panel_adr and panel_id:
                                    item_award_writes.append((panel_adr,[panel_id],"IWRAM"))
                                await bizhawk.write(
                                    ctx.bizhawk_ctx,
                                    item_award_writes
                                )
                        #TODO: Door key or star rod; play the appropriate sound effect
                    #Having awarded new one-off items, update the sync counter
                    self.sync_counter = len(ctx.items_received)

                    #Loop through all items to check for door key items
                    for received_item in ctx.items_received:
                        received_item_name = ITEM_ID_TO_NAME[received_item.item]
                        if received_item_name.endswith('Key'):
                            #Remove the corresponding entry of the Key item from the list of locked doors
                            print(f'INFO: removing lock for Key item {ITEM_ID_TO_NAME[received_item.item]}')
                            for k in list(self.ow_wxy_to_locked_doors.keys()):
                                if self.ow_wxy_to_locked_doors[k] == received_item_name[:-4]:
                                    del self.ow_wxy_to_locked_doors[k]

                    #Look at the number of star rod pieces and unlock the corresponding boss doors
                    star_rod_pieces_received = sum(1 for i in ctx.items_received if ITEM_ID_TO_NAME[i.item] == 'Star Rod Piece')
                    boss_doors_to_unlock = [wn + ' Boss' for wn in WORLD_NAMES_INDEXED[:star_rod_pieces_received]]
                    print(f'INFO: removing lock for following boss doors: {boss_doors_to_unlock}')
                    for k in list(self.ow_wxy_to_locked_doors.keys()):
                        if self.ow_wxy_to_locked_doors[k] in boss_doors_to_unlock:
                            del self.ow_wxy_to_locked_doors[k]

                    #Set the sync counter now that any needed items have been awarded
                    #Note we may need a two-byte write if we ever have more than 254 max possible checks/items (since FF 255 is the default)
                    print(f'INFO: attempting to write new sync counter {self.sync_counter}')
                    await bizhawk.write(
                        ctx.bizhawk_ctx, [(sync_adr, [self.sync_counter], "IWRAM")]
                    )

            if self.consumable_queue != 0:
                #Note this is duplicated code from the standard sync check
                #Determine what to write to the control panel so that AP-awarded items don't trigger a pickup check
                panel_adr, panel_id = self.determine_panel_award_write(self.consumable_queue[0])

                #check if the item award control byte is 0. If not, add the consumable to the conumable queue. 
                print(f'INFO: attempting to award queued item {self.consumable_queue[0]}')
                item_award_panelb = await bizhawk.read(ctx.bizhawk_ctx, [
                    (ITEM_AWARD_ADR, 1, "IWRAM")       
                ])
                item_award_panel = int.from_bytes(item_award_panelb)
                if item_award_panel != 0:
                    print(f'INFO: item to award already paneled, do nothing')
                else:
                    item_award_writes = [(ITEM_AWARD_ADR, self.consumable_queue[0], "IWRAM")]
                    if panel_adr and panel_id:
                        item_award_writes.append((panel_adr,[panel_id],"IWRAM"))
                    await bizhawk.write(
                        ctx.bizhawk_ctx,
                        item_award_writes
                    )
                    self.consumable_queue = self.consumable_queue[1:]

                    
            
            #If a goal game is detected, send the level clear check. 
            #TODO: Not sure if it's fine to attempt the send the check when it's already checked, but this does not check for the location already being sent
            #A similar pattern will be followed for big switches (screen mod = 9)
            if screen_mod == 0xA and not self.detected_goal_game:
                print(f'INFO: Begin Goal Game Check Sequence')
                self.detected_goal_game = True
                (world_numb, level_numb) = await bizhawk.read(ctx.bizhawk_ctx, [
                    (OW_MOD_ADR, 1, "IWRAM"),   
                    (LEVEL_MOD_ADR, 1, "IWRAM"),     
                ])
                world_num = int.from_bytes(world_numb)
                level_num = int.from_bytes(level_numb)
                print(f'INFO: Detected World {world_num}, Level {level_num}')
                level_clear_loc_id = KNIDL_BASE_ID + world_num*100 + level_num*10
                #For now, use the fact that level clear location ID's follow the pattern of WL0 + BASE
                print(f'INFO: Attempting to send location id {level_clear_loc_id}')
                await ctx.send_msgs([{
                        "cmd": "LocationChecks",
                        "locations": [level_clear_loc_id]
                    }])
            if not screen_mod == 0xA:
                self.detected_goal_game = False

                
            #If an item pickup is detected, send the item check
            if screen_mod == 0x8:
                sent_check = False
                #TODO: abstract the repeated pattern of bizhawk.read + int.from_bytes into a function that can handle 1 or multiple var reads
                #Note that we only need the trailing comma syntax
                (food_detectedb, oneup_detectedb) = await bizhawk.read(ctx.bizhawk_ctx, [
                    (FOOD_DETECT_ADR, 1, "IWRAM"),   
                    (ONEUP_DETECT_ADR, 1, "IWRAM"),     
                ])
                food_detected = int.from_bytes(food_detectedb) 
                oneup_detected = int.from_bytes(oneup_detectedb)
                if food_detected == 0x1 or oneup_detected == 0x1:
                    print(f'INFO: detected 1up or food pickup')
                    (world_numb, level_numb, room_numb, x_coordb, y_coordb) = await bizhawk.read(ctx.bizhawk_ctx, [
                        (OW_MOD_ADR, 1, "IWRAM"),   
                        (LEVEL_MOD_ADR, 1, "IWRAM"),
                        (ROOM_MOD_ADR, 1, "IWRAM"),
                        (KIRBY_X_ADR, 2, "IWRAM"),  
                        (KIRBY_Y_ADR, 2, "IWRAM")   
                    ])
                    wlr = (int.from_bytes(world_numb,'little'), int.from_bytes(level_numb,'little'), int.from_bytes(room_numb,'little'))
                    print(f'INFO: calculated WLR is {wlr}')
                    if wlr in WLR_TO_LOCATION_NAME_SOLO.keys():
                        loc_name = WLR_TO_LOCATION_NAME_SOLO[wlr]
                        print(f'INFO: attempting to send location {loc_name}, id {LOCATION_NAME_TO_ID[loc_name]}')
                        await ctx.send_msgs([{
                            "cmd": "LocationChecks",
                            "locations": [LOCATION_NAME_TO_ID[loc_name]]
                        }])
                        sent_check = True

                    #else: TODO: do math on the coordiantes to get the location name, when that becomes necessary

                    #After sending the check, it's the client's responsibility to reset the byte
                    if sent_check:
                        print(f'INFO: Attempting to reset 1up and food triggers in control panel after sending pickup check')
                        await bizhawk.write(
                            ctx.bizhawk_ctx, [(FOOD_DETECT_ADR, [0], "IWRAM"),(ONEUP_DETECT_ADR, [0], "IWRAM")]
                        )
            
            #If Kirby is in the OW, set the door lock control byte if we are near any doors
            if screen_mod == 0x5:
                (world_numb, x_coordb, y_coordb) = await bizhawk.read(ctx.bizhawk_ctx, [
                    (OW_MOD_ADR, 1, "IWRAM"),   
                    (KIRBY_X_ADR, 2, "IWRAM"),  
                    (KIRBY_Y_ADR, 2, "IWRAM")   
                ])
                world_num = int.from_bytes(world_numb,'little')
                x_coord_round = int(int.from_bytes(x_coordb,'little')/16)
                y_coord_round = int(int.from_bytes(y_coordb,'little')/16)
                print(f"INFO: Client detecting Kirby in the OW Lobby (World {world_num}) with rounded coords {x_coord_round}, {y_coord_round}")
                if not self.door_locked and \
                    (world_num,x_coord_round,y_coord_round) in self.ow_wxy_to_locked_doors.keys():
                    self.door_locked = True
                    print('INFO: attempting to lock door')
                    await bizhawk.write(
                            ctx.bizhawk_ctx, [(DOOR_LOCK_ADR, [1], "IWRAM")]
                        )
                elif self.door_locked and not \
                    (int.from_bytes(world_numb,'little'),x_coord_round,y_coord_round) in self.ow_wxy_to_locked_doors.keys():
                    self.door_locked = False
                    print('INFO: attempting to unlock door')
                    await bizhawk.write(
                            ctx.bizhawk_ctx, [(DOOR_LOCK_ADR, [0], "IWRAM")]
                        )

        except bizhawk.RequestFailedError:
            print('ERROR: bizhawk request failed error')
            pass

