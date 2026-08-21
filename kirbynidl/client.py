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
import copy, logging, time

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

###DATA - Abstract to other files LATER
##APWORLD STUFF
KNIDL_BASE_ID = 2742740
KIRBY_BASE_HP = 3



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
    (0,0xA,0xD) : 'Vegetable Valley Bomb Rally',
    (0,0xE,0x9) : 'Vegetable Valley Museum',
    (0,0x1B,0x3) : 'Vegetable Valley Warp Station',

    (1,0x6,0x6) : 'Ice Cream Island Air Grind',
    (1,0x15,0xE) : 'Ice Cream Island Bomb Rally',
    (1,0x17,0x4) : 'Ice Cream Island Museum',
    (1,0x1E,0x6) : 'Ice Cream Island Arena',
    (1,0x28,0xD) : 'Ice Cream Island Warp Station',
    (1,0x2B,0x6) : 'Ice Cream Island Boss',

    (2,0xC,0x28) : 'Butter Building Arena',
    (2,0x2,0x1B) : 'Butter Building Bomb Rally',
    (2,0xC,0x12) : 'Butter Building Quick Draw',
    (2,0x2,0xD) : 'Butter Building Air Grind',
    (2,0xC,0x9) : 'Butter Building Warp Station',
    (2,0x7,0x6) : 'Butter Building Boss',

    (3,0x3,0x8) : 'Grape Garden Bomb Rally',
    (3,0xC,0x3) : 'Grape Garden Quick Draw',
    (3,0x11,0xE) : 'Grape Garden Museum',
    (3,0x1C,0xF) : 'Grape Garden Arena',
    (3,0x2B,0x8) : 'Grape Garden Warp Station',
    (3,0x2B,0x4) : 'Grape Garden Boss',

    (4,0x2,0xC) : 'Yogurt Yard Bomb Rally',
    (4,0xA,0x10) : 'Yogurt Yard Air Grind',
    (4,0x15,0x4) : 'Yogurt Yard Museum',
    (4,0x1A,0xE) : 'Yogurt Yard Arena',
    (4,0x24,0x4) : 'Yogurt Yard Quick Draw',
    (4,0x2B,0xD) : 'Yogurt Yard Warp Station',
    (4,0x2A,0x8) : 'Yogurt Yard Boss',

    (5,0x7,0xB) : 'Orange Ocean Museum',
    (5,0xD,0x3) : 'Orange Ocean Arena',
    (5,0x12,0x14) : 'Orange Ocean Bomb Rally',
    (5,0x16,0x6) : 'Orange Ocean Air Grind',
    (5,0x24,0x10) : 'Orange Ocean Quick Draw',
    (5,0x26,0x3) : 'Orange Ocean Warp Station',
    (5,0x2C,0x8) : 'Orange Ocean Boss',

    (6,0x5,0x6) : 'Rainbow Resort Bomb Rally',
    (6,0x1B,0x3) : 'Rainbow Resort Warp Station',
    (6,0xF,0x5) : 'Rainbow Resort Boss',

}
#Flesh out the above table with the right block of each door, and many surrounding blocks (including diagonals)
for k in list(OW_WXY_TO_DOOR_NAME.keys()):
    for dx in [-3,-2,-1,0,1,2,3,4]:
        for dy in [-3,-2,-1,0,1,2,3]:
            OW_WXY_TO_DOOR_NAME[(k[0], k[1]+dx, k[2]+dy)] = OW_WXY_TO_DOOR_NAME[k]

#Table for item ID to name (since AP client sends ID's not names, it seems)
ITEM_ID_TO_NAME = dict()
for k in ITEM_NAME_TO_ID.keys():
    ITEM_ID_TO_NAME[ITEM_NAME_TO_ID[k]] = k
#Same for locations -- it's handy to have
LOCATION_ID_TO_NAME = dict()
for k in LOCATION_NAME_TO_ID.keys():
    LOCATION_ID_TO_NAME[str(LOCATION_NAME_TO_ID[k])] = k


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
#Number of levels in world {[index]+1}
LEVELS_PER_WORLD_INDEX = (4,5,6,6,6,6,6)

##ROM ADDRESSES
ROM_HEADER_ADR = 0x0A0 #As it is for all GBA games
##EWRAM ADDRESSES
SYNC_ADR_BASE = 0xE6FC #+ 0x100n for file 2, file 3
FILE_NUMBER_ADR = 0xB074 #Also the sound vs music variable in the sound test
KIRBY_HP_EW_ADR = 0x5588
KIRBY_MAX_HP_ADR = 0x5580
PICKUP_FLAG_ADR = 0x7BF0
##IWRAM ADDRESSES
BGM_ID_ADR = 0x0490
SCREEN_MOD_ADR = 0x23D8 
OW_MOD_ADR = 0x23B8
LEVEL_MOD_ADR = 0x1F20
ROOM_MOD_ADR = 0x2468
IW_CLEAR_FLAGS_START = 0x2400 
IW_SWITCHEXISTS_BITARR = [0x23C8, 0x23C9, 0x23CA]
KIRBY_X_ADR = 0x23CC
KIRBY_Y_ADR = 0x2388
MOUTH_ADR = 0x217B
BOSS_HP_ADR = 0x3A08
#CUSTOM IWRAM (the "control panel")
DOOR_LOCK_ADR = 0x78A0
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
        self.initial_flags_written = False
        self.init_startup = True
        self.sync_counter = 0
        self.item_queue = []
        self.hp_bank = 0
        self.kirby_max_hp = KIRBY_BASE_HP
        self.hp_trickle_timestamp = 0
        self.HEAL_TIME_DELAY = 1 #time to wait in seconds between healing kirby HP segments (otherwise, client will heal kirby before previous HP gain registered)
        self.current_world = -1 #indexed to 0, Vegetable Valley = 0
        self.current_level = -1 #also indexed to 0
        self.current_pickup_bitarr = 0
        self.current_pickup_flag_adr = 0x7BF0
        self.sent_boss_check = False
        self.sent_bigswitch_check = False
        self.prev_boss_hp = 0
        self.sent_arena_check = False
        self.locked_ability_ids = [a for a in range(1,25)] #1-24 inclusive
    
    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        try:
            logger.info('Init KNIDL client validate_rom function')
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
                logger.info('KNIDL client recognized and validated rom')
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
            #logging.debug(f'Screen mod is {screen_mod}')

            # Don't do anything if the game is not in a specific state (list all states we will actually use here)
            # For now, we only care about 5 (OW lobby), 7 (World Intro Cutscene), 8 (Normal Level or Boss), 9 (Big Switch cutscene), A (Goal Game)
            # and also 12 (Museum) and 13 (Arena) because kirby can gain abilities in these scenes
            if not screen_mod in (0x5,0x7,0x8,0x9,0xA,0x12,0x13):
                return
            
            # During the Level Intro Cutscene or any normal level, force all level clear flags to 02 to open the entire OW
            # Also set the big switch exists array to all 0 so that all big switches appear
            # Also set Kirby's max vitality here too
            # This strategy is a problem if savestates are used, but that's whatever for now
            if (not self.initial_flags_written) and (screen_mod == 0x7 or screen_mod == 0x8):
                logger.info(f'Attempting to write clear flags to unlock all levels and big switches')
                clear_flag_writes = []
                for world_num, level_count in enumerate(LEVELS_PER_WORLD_INDEX):
                    for offset in range(level_count):
                        clear_flag_writes.append((IW_CLEAR_FLAGS_START + world_num*6 + offset, [0x2], "IWRAM"))

                for f in IW_SWITCHEXISTS_BITARR:
                    clear_flag_writes.append((f,[0],"IWRAM"))
                await bizhawk.write(
                    ctx.bizhawk_ctx, clear_flag_writes
                )
                logger.info(f"Attempting to set Kirby's current Max Health to {self.kirby_max_hp} segments (initial flag setting)")
                hp_val = int(self.kirby_max_hp*8)
                await bizhawk.write(ctx.bizhawk_ctx, 
                    [(KIRBY_HP_EW_ADR,[hp_val],'EWRAM'),
                     (KIRBY_MAX_HP_ADR,[hp_val],'EWRAM')
                     ]
                )
                self.initial_flags_written = True

            # Ability Lock: if Kirby is in a gameplay state, always be checking his "Mouth" value. 
            # If the mouth contains a locked ability, set the Mouth to 0
            if screen_mod in (0x5,0x8,0x12,0x13):
                mouth_idb, = await bizhawk.read(ctx.bizhawk_ctx, [
                    (MOUTH_ADR, 1, "IWRAM")       
                ])
                mouth_id = int.from_bytes(mouth_idb)
                if mouth_id in self.locked_ability_ids:
                    logger.info(f'Locked mouth id {mouth_id} detected, setting mouth to 0')
                    await bizhawk.write(ctx.bizhawk_ctx, 
                                        [(MOUTH_ADR, [0], "IWRAM")]
                    )

            
            #while in a level or the OW, check to see if there are items to award
            if (self.sync_counter != len(ctx.items_received) or self.init_startup) and (screen_mod == 0x5 or screen_mod == 0x8 or screen_mod == 0x13):
                logger.info(f'init item sync sequence. Current sync counter is {self.sync_counter}. Number of items received is {len(ctx.items_received)}')
                file_numberb, = await bizhawk.read(ctx.bizhawk_ctx, [
                    (FILE_NUMBER_ADR, 1, "EWRAM")       
                ])
                file_number = int.from_bytes(file_numberb)
                sync_adr = SYNC_ADR_BASE + file_number*0x100
                sync_counterb, = await bizhawk.read(ctx.bizhawk_ctx, [
                    (sync_adr, 1, "EWRAM")       
                ])
                sync_counter_ingame = int.from_bytes(sync_counterb, "little")
                logger.info(f'Sync counter according to game RAM is {self.sync_counter}')
                if sync_counter_ingame <= self.sync_counter: #When the in-game (last registered) sync counter is less than the current items, give the items that were received since
                    self.sync_counter = sync_counter_ingame
                #sync counter doesn't match, award items
                if self.sync_counter != len(ctx.items_received):
                    if self.sync_counter > len(ctx.items_received): 
                        logger.warning('sync counter is somehow greater than number of items received!')
                        self.sync_counter = 0
                    #Loop from latest sync counter to get new items
                    for i in range(self.sync_counter, len(ctx.items_received)):
                        received_item = ctx.items_received[i]
                        logger.info(f'newly received item is {ITEM_ID_TO_NAME[received_item.item]}')
                        item_id_readable = received_item.item - KNIDL_BASE_ID 
                        self.item_queue.append(item_id_readable)
                        logger.info(f'Added readable item id {item_id_readable} to item queue')
                        logger.info(f'Item queue is {self.item_queue}')
                    #Having awarded new one-off items, update the sync counter
                    self.sync_counter = len(ctx.items_received)

                #Loop through all items to check for all the client-side locks: door key, ability unlock items, and vitality upgrades
                for received_item in ctx.items_received:
                    received_item_name = ITEM_ID_TO_NAME[received_item.item]
                    received_item_id_readable = received_item.item - KNIDL_BASE_ID

                    if received_item_name.endswith(' Key'):
                        #Remove the corresponding entry of the Key item from the list of locked doors
                        logger.info(f'removing lock for Key item {ITEM_ID_TO_NAME[received_item.item]}')
                        for k in list(self.ow_wxy_to_locked_doors.keys()):
                            if self.ow_wxy_to_locked_doors[k] == received_item_name[:-4]:
                                del self.ow_wxy_to_locked_doors[k]

                    if received_item_id_readable > 50 and received_item_id_readable < 75:
                        ability_id = received_item_id_readable - 50
                        logger.info(f'removing lock for Copy Ability {ITEM_ID_TO_NAME[received_item.item]}, ability id {ability_id}')
                        if ability_id in self.locked_ability_ids:
                            self.locked_ability_ids.remove(ability_id)

                #Set kirby's max hp based off the number of vitality items
                extra_hp = sum([1 for i in ctx.items_received if ITEM_ID_TO_NAME[i.item] == 'Vitality'])
                new_kirby_max_hp = KIRBY_BASE_HP + extra_hp
                if new_kirby_max_hp != self.kirby_max_hp:
                    self.kirby_max_hp = new_kirby_max_hp
                    logger.info(f"Attempting to set Kirby's current Max Health to {self.kirby_max_hp} (vitality recalculation)")
                    hp_val = int(self.kirby_max_hp*8)
                    await bizhawk.write(ctx.bizhawk_ctx, 
                        [(KIRBY_HP_EW_ADR,[hp_val],'EWRAM'),
                        (KIRBY_MAX_HP_ADR,[hp_val],'EWRAM')
                        ]
                    )

                #Look at the number of star rod pieces and unlock the corresponding boss doors
                star_rod_pieces_received = sum(1 for i in ctx.items_received if ITEM_ID_TO_NAME[i.item] == 'Star Rod Piece')
                boss_doors_to_unlock = [wn + ' Boss' for wn in WORLD_NAMES_INDEXED[:star_rod_pieces_received]]
                logger.info(f'removing lock for following boss doors: {boss_doors_to_unlock}')
                for k in list(self.ow_wxy_to_locked_doors.keys()):
                    if self.ow_wxy_to_locked_doors[k] in boss_doors_to_unlock:
                        del self.ow_wxy_to_locked_doors[k]

                #Set the sync counter now that any needed items have been awarded
                #Note we may need a two-byte write if we ever have more than 254 max possible checks/items (since FF 255 is the default)
                logger.info(f'attempting to write new sync counter {self.sync_counter}')
                await bizhawk.write(ctx.bizhawk_ctx, 
                    [(sync_adr, [self.sync_counter], "EWRAM")]
                )
                self.init_startup = False

            #Handle the in-game effects of all items (mainly playing SFX)
            #May need to put a delay timer on this
            if len(self.item_queue) != 0:
                #check if we're free to award the item
                item_award_panelb, = await bizhawk.read(ctx.bizhawk_ctx, [
                    (ITEM_AWARD_ADR, 1, "IWRAM")       
                ])
                item_award_panel = int.from_bytes(item_award_panelb)
                if item_award_panel != 0:
                    logger.debug(f'Item to award already paneled, do nothing')

                else:    
                    #Calc id to put in the item award control panel address, if any
                    current_item = self.item_queue[0] #This will be the readable item id
                    item_award_id = 0
                    if current_item == 13: #1up
                        item_award_id = 3
                    elif current_item == 14: #Candy
                        item_award_id = 4
                    elif current_item == 12: #Tomato
                        #calc how many segments to add to the HP bank
                        self.hp_bank += self.kirby_max_hp - 1 #TODO: calc this from vitality + vitality pieces when implemented
                        logger.info(f'Added {self.kirby_max_hp - 1} HP to Bank')
                        item_award_id = 2
                    elif current_item == 11: #Pep Drink
                        if self.kirby_max_hp <= 3:
                            hp = 1
                        else:
                            hp = 2
                        self.hp_bank += hp
                        logger.info(f'Added {hp} HP to Bank')
                        item_award_id = 2
                    elif current_item == 1: #Star Rod
                        item_award_id = 5
                    elif current_item > 50 and current_item < 75: #Ability unlock
                        item_award_id = 6
                    elif current_item == 5: #Vitality
                        item_award_id = 7

                    if item_award_id:
                        logger.info(f'attempting to award queued item {current_item}')
                        await bizhawk.write(ctx.bizhawk_ctx,
                            [(ITEM_AWARD_ADR, [item_award_id], "IWRAM")]
                        )
                        self.item_queue = self.item_queue[1:]

            #If there's hp in the hp bank and Kirby has less than full health AND enough time has expired so that we don't overheal kirby, award a health segment
            if self.hp_bank > 0 and screen_mod == 0x8:
                kirby_hpb, = await bizhawk.read(ctx.bizhawk_ctx, [
                    (KIRBY_HP_EW_ADR, 1, "EWRAM")       
                ])
                kirby_hp = int(int.from_bytes(kirby_hpb) / 8)
                now = time.time()
                if kirby_hp < self.kirby_max_hp and now - self.hp_trickle_timestamp > self.HEAL_TIME_DELAY: 
                    logger.info(f'Detected kirby HP is {kirby_hp} with HP bank at {self.hp_bank}. Awarding 1 HP segment')
                    await bizhawk.write(ctx.bizhawk_ctx,
                            [(ITEM_AWARD_ADR, [1], "IWRAM")]
                    )
                    self.hp_bank -= 1
                    self.hp_trickle_timestamp = now
                    
      
            
            #If a goal game is detected, send the level clear check. 
            #TODO: Not sure if it's fine to attempt the send the check when it's already checked, but this does not check for the location already being sent
            #A similar pattern will be followed for big switches (screen mod = 9)
            if screen_mod == 0xA and not self.detected_goal_game:
                logger.info(f'Begin Goal Game Check Sequence')
                self.detected_goal_game = True
                (world_numb, level_numb) = await bizhawk.read(ctx.bizhawk_ctx, [
                    (OW_MOD_ADR, 1, "IWRAM"),   
                    (LEVEL_MOD_ADR, 1, "IWRAM"),     
                ])
                world_num = int.from_bytes(world_numb) + 1 #+1 because World / Level 1 is readable ID 11X
                level_num = int.from_bytes(level_numb) + 1
                logger.info(f'Detected World {world_num}, Level {level_num}')
                level_clear_loc_id = KNIDL_BASE_ID + world_num*100 + level_num*10
                #For now, use the fact that level clear location ID's follow the pattern of WL0 + BASE
                logger.info(f'Attempting to send location id {level_clear_loc_id}')
                await ctx.send_msgs([{
                        "cmd": "LocationChecks",
                        "locations": [level_clear_loc_id]
                    }])
            #Reset various "send check only once" switches once we're out of their screen mod context
            if not screen_mod == 0xA:
                self.detected_goal_game = False
            if not screen_mod == 0x8:
                self.sent_boss_check = False
            if not screen_mod == 0x9:
                self.sent_bigswitch_check = False
            if not screen_mod == 0x13:
                self.sent_arena_check = False
                self.prev_boss_hp = 0

                
            #In-Level Checks
            if screen_mod == 0x8:

                #Pickup Item checks via the flags starting at EW 7BF0
                #TODO: abstract the repeated pattern of bizhawk.read + int.from_bytes into a function that can handle 1 or multiple var reads
                #Note that we only need the trailing comma syntax
                (world_numb,level_numb, bgm_idb) = await bizhawk.read(ctx.bizhawk_ctx, [
                    (OW_MOD_ADR, 1, "IWRAM"),   
                    (LEVEL_MOD_ADR, 1, "IWRAM"),
                    (BGM_ID_ADR, 1, "IWRAM")     
                ])
                world_num = int.from_bytes(world_numb,'little')
                level_num = int.from_bytes(level_numb,'little')
                bgm_id = int.from_bytes(bgm_idb)
                if self.current_world != world_num or self.current_level != level_num:
                    self.current_world = world_num; self.current_level = level_num
                    self.current_pickup_flag_adr = PICKUP_FLAG_ADR + world_num*0x20 + level_num*4
                    self.current_pickup_bitarr = -1
                    logger.info(f'New level {world_num+1}-{level_num+1} detected, changing pickup array window')


                pickup_bitarrb, = await bizhawk.read(ctx.bizhawk_ctx, [
                    (self.current_pickup_flag_adr, 2, "EWRAM")       
                ])
                pickup_bitarr = int.from_bytes(pickup_bitarrb,'little')
                if self.current_pickup_bitarr == -1: #freshly entered a new level (which may have pickups already in the array). Set current bitarr to the read value and do nothing else
                    self.current_pickup_bitarr = pickup_bitarr
                    new_bit = 0
                else:
                    new_bit = pickup_bitarr ^ self.current_pickup_bitarr

                if new_bit != 0: #The bit array changed, send the check now
                    self.current_pickup_bitarr = pickup_bitarr
                    if world_num + 1 == 6 and level_num + 1 == 6: #Carve out for level 6-6, where 8 UFOs take up the first 8 item id slots
                        pickup_id = new_bit.bit_length() - 8
                    else:
                        pickup_id = new_bit.bit_length() #1st item id = 1, effectively 1-indexed
                    loc_id_readable = (world_num+1)*100 + (level_num+1)*10 + pickup_id 
                    loc_id = loc_id_readable + KNIDL_BASE_ID
                    loc_name = None #Technically we don't need to find the location name here, but it's convenient for logging 
                    try:
                        loc_name = LOCATION_ID_TO_NAME[str(loc_id)]
                    except IndexError:
                        logger.warning(f'Attempted to find location name for nonexistent id: {loc_id_readable} (readable). Pass')
                    if loc_name: 
                        logger.info(f'Attempting to send location {loc_name}, id {LOCATION_NAME_TO_ID[loc_name]}')
                        await ctx.send_msgs([{
                            "cmd": "LocationChecks",
                            "locations": [LOCATION_NAME_TO_ID[loc_name]]
                        }])


                ##Boss Checks -- look for the Kirby Dance BGM ID
                if bgm_id == 0x0D and not self.sent_boss_check: #0x0D = Kirby Dance 
                    logger.info('Detected Kirby Dance')
                    world_numb, = await bizhawk.read(ctx.bizhawk_ctx, [
                        (OW_MOD_ADR, 1, "IWRAM")       
                    ])
                    world_num = int.from_bytes(world_numb) + 1
                    loc_id = int(KNIDL_BASE_ID + world_num*100 + 99)
                    logger.info(f'Attempting to send location ID {loc_id}, Boss check from World {world_num}')
                    await ctx.send_msgs([{
                        "cmd": "LocationChecks",
                        "locations": [loc_id]
                    }])
                    self.sent_boss_check = True

            #Big Switch Checks -- look for a specific screen mod        
            if screen_mod == 0x9 and not self.sent_bigswitch_check:
                logger.info('Detected Big Switch cutscene')
                (world_numb, level_numb) = await bizhawk.read(ctx.bizhawk_ctx, [
                    (OW_MOD_ADR, 1, "IWRAM"),   
                    (LEVEL_MOD_ADR, 1, "IWRAM"),   
                ])
                world_num = int.from_bytes(world_numb) + 1
                level_num = int.from_bytes(level_numb) + 1
                loc_id = int(KNIDL_BASE_ID + world_num*100 + level_num*10 + 9) #Pattern is WL9
                logger.info(f'Attempting to send Boss check from World {world_num}')
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [loc_id]
                }])
                self.sent_bigswitch_check = True

            #Arena Checks -- look for Boss HP going to 0
            if screen_mod == 0x13:
                (boss_hpb, world_numb) = await bizhawk.read(ctx.bizhawk_ctx, [  
                    (BOSS_HP_ADR, 1, "IWRAM"),
                    (OW_MOD_ADR, 1, "IWRAM")   
                ])
                boss_hp = int.from_bytes(boss_hpb)
                world_num = int.from_bytes(world_numb) + 1
                if not self.sent_arena_check and boss_hp == 0 and self.prev_boss_hp > 0: #Boss was defeated
                    logger.info(f'Attempting to send check for Arena boss defeated in world {world_num}')
                    loc_id = world_num*100 + 89 + KNIDL_BASE_ID
                    await ctx.send_msgs([{
                        "cmd": "LocationChecks",
                        "locations": [loc_id]
                    }])
                    self.sent_arena_check = True
                self.prev_boss_hp = boss_hp


            
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
                logger.debug(f"Client detecting Kirby in the OW Lobby (World {world_num}) with rounded coords {x_coord_round}, {y_coord_round}")
                if not self.door_locked and \
                    (world_num,x_coord_round,y_coord_round) in self.ow_wxy_to_locked_doors.keys():
                    self.door_locked = True
                    logger.info('attempting to lock door')
                    await bizhawk.write(ctx.bizhawk_ctx, 
                                    [(DOOR_LOCK_ADR, [1], "IWRAM")]
                    )
                elif self.door_locked and not \
                    (int.from_bytes(world_numb,'little'),x_coord_round,y_coord_round) in self.ow_wxy_to_locked_doors.keys():
                    self.door_locked = False
                    logger.info('attempting to unlock door')
                    await bizhawk.write(ctx.bizhawk_ctx, 
                                    [(DOOR_LOCK_ADR, [0], "IWRAM")]
                    )

        except bizhawk.RequestFailedError:
            print('ERROR: bizhawk request failed error')
            pass

