from typing import TYPE_CHECKING

from NetUtils import ClientStatus

import worlds._bizhawk as bizhawk
#from .Options import KNIDLOptions
from worlds._bizhawk.client import BizHawkClient
import Utils

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext
    from .world import KirbyNIDLWorld

from .locations import LOCATION_NAME_TO_ID
from .items import ITEM_NAME_TO_ID, SIDE_DOORS_PER_WORLD, SIDE_DOOR_MAP
import copy, logging, time

logger = logging.getLogger(__name__)
logger.setLevel(logging.CRITICAL) #Set to CRITICAL for release

###DATA
##APWORLD STUFF
KNIDL_BASE_ID = 2742740


#Table (list) of what index in each world's bit array each door type corresponds to
DOOR_NAME_TO_BIT_MAP = [
    'Prev', #The prev door will never be locked
    'Level 1','Level 2','Level 3','Level 4','Level 5','Level 6', #levels 1-6 = index 1-6
    'Bomb Rally','Air Grind','Quick Draw', #Minigames 7-9 in order of first appearence
    'Arena','Museum','Unused1','Unused2','Warp Station','Boss' #A is for Arena, followed by B Museum. Warp Station E and Boss F are last
]

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
#Number of big switches in world {index}
BIGSWITCHES_PER_WORLD_INDEX = (0,0,2,3,4,6,2)
#List of all abilities with their in-game ID and bit index. ie, list[1] = fire
ABILITY_LIST_INDEXED = [
    '','Fire','Spark','Cutter',
    'Sword','Burning','Laser','Mike',
    'Wheel','Hammer','Parasol','Sleep',
    'Needle','Ice','Freeze','Hi-Jump',
    'Beam','Stone','Ball','Tornado',
    'Crash','Light','Backdrop','Throw',
    'UFO'
]


##ROM ADDRESSES
ROM_HEADER_ADR = 0x0A0 #As it is for all GBA games
##EWRAM ADDRESSES
SYNC_ADR_BASE = 0xE6FC #+ 0x100n for file 2, file 3
FILE_NUMBER_ADR = 0xB074 #Also the sound vs music variable in the sound test
KIRBY_HP_EW_ADR = 0x5588
KIRBY_MAX_HP_ADR = 0x5580
PICKUP_FLAG_ADR = 0x7BF0
EW_CLEAR_FLAGS_START = 0xE628
EW_SWITCHEXISTS_BITARR = 0xE620
WARP_STATION_BITARR = 0xB04C
##IWRAM ADDRESSES
BGM_ID_ADR = 0x0490
SCREEN_MOD_ADR = 0x23D8 
OW_MOD_ADR = 0x23B8
WORLD_MOD_ADR = 0x238C
LEVEL_MOD_ADR = 0x1F20
ROOM_MOD_ADR = 0x2468
IW_CLEAR_FLAGS_START = 0x2400 
IW_SWITCHEXISTS_BITARR = 0x23C8 #, 0x23C9, 0x23CA
KIRBY_X_ADR = 0x23CC
KIRBY_Y_ADR = 0x2388
MOUTH_ADR = 0x217B
BOSS_HP_ADR = 0x3A08
LEVELS_CLEARED_ADR = 0x2384
WORLDS_CLEARED_IW = 0x23E0
KIRBY_ACTIONABLE = 0x1F34
KIRBY_HP_IW = 0x2808
#CUSTOM IWRAM (the "control panel")
DOOR_LOCK_ADR = 0x78A0
ITEM_AWARD_ADR = 0x78A8
DOOR_LOCK_BITARR = 0x78B0 #+2,4,6 for each world's doors, until W7 at BC
ABILITY_LOCK_BITARR = 0x78C0

###Some Helper Functions and classes

class DeathLinkCtx: #stolen from WL4 apworld
    enabled: bool = False
    update_pending: bool = False
    pending: bool = False
    sent_this_death: bool = False

def cmd_toggle_deathlink(self):
    """Toggle death link from client. Overrides default setting. Works right out of the box like this?"""

    client_handler = self.ctx.client_handler
    client_handler.death_link.client_override = True
    client_handler.death_link.enabled = not client_handler.death_link.enabled
    logger.info('Death Link Toggle Function was called')
    Utils.async_start(
        self.ctx.update_death_link(client_handler.death_link.enabled),
        name="Update Death Link"
    )

#List of custom commands allowed by the client
knidl_client_commands = {
    "deathlink": cmd_toggle_deathlink,
    # "kill": cmd_receive_death,
}

#From the list of all currently checked location ids (+ the location just collected), derive the array of bytes that should be written to the level clear flags
def get_door_color_bytes(missing_location_ids, last_loc_id=None, last_loc_ids = []):
    #derive initial array of all "02" for "complete"
    color_array = []
    for w in range(7):
        color_array.append([])
        level_count = LEVELS_PER_WORLD_INDEX[w]
        for _ in range(level_count):
            color_array[w].append(2)
    #Remove the last location we checked (if there was one) from the set of missing ID's
    if last_loc_id:
        all_missing_location_ids = copy.copy(missing_location_ids)
        all_missing_location_ids.discard(last_loc_id)
    elif last_loc_ids:
        all_missing_location_ids = copy.copy(missing_location_ids)
        all_missing_location_ids.difference_update(last_loc_ids)
    else:
        all_missing_location_ids = missing_location_ids
    #go through all missing locations, derive world and level, and set the corresponding byte to "01" for "not complete"
    for m in all_missing_location_ids:
        #Exploit the fact the X## is the world, #X# is the level of the location id
        m_readable = m - KNIDL_BASE_ID
        world = m_readable // 100
        level = (m_readable // 10) % 10 #int divide by ten to "shift right 1", mod 10 to extract last digit
        if world <= 7 and level <= 6:
            color_array[world-1][level-1] = 1
    return color_array



class KirbyNIDLClient(BizHawkClient):
    game = "Kirby Nightmare in Dream Land"
    system = "GBA"
    patch_suffix = ".apknidl"

    def __init__(self):
        super().__init__()

        self.deathLink = DeathLinkCtx()

        #Obtain a list of every door that can possibly be locked at startup (then remove them as items come in)
        self.locked_door_names = []
        for i in range(len(WORLD_NAMES_INDEXED)):
            self.locked_door_names.append(f'{WORLD_NAMES_INDEXED[i]} Boss')
            for sd in SIDE_DOORS_PER_WORLD[i]:
                self.locked_door_names.append(f'{WORLD_NAMES_INDEXED[i]} {SIDE_DOOR_MAP[int(sd)-1]}') #ie, "Vegetable Valley Museum"

        #Internal data setup
        self.last_received_index = 0 #index of last item received; needed so we don't apply filler pickup items multiple times
        self.detected_goal_game = False #flag to prevent repeated send of level clear check during a goal game
        self.initial_flags_written = False
        self.init_startup = True
        self.sync_counter = 0
        self.item_queue = []
        self.hp_bank = 0
        self.kirby_max_hp = None
        self.hp_trickle_timestamp = 0
        self.HEAL_TIME_DELAY = 1 #time to wait in seconds between healing kirby HP segments (otherwise, client will heal kirby before previous HP gain registered)
        self.current_world = -1 #indexed to 0, Vegetable Valley = 0
        self.current_level = -1 #also indexed to 0
        self.current_pickup_bitarr = 0
        self.current_pickup_flag_adr = 0
        self.sent_boss_check = False
        self.sent_bigswitch_check = False
        self.sent_victory_check = False
        self.prev_boss_hp = 0
        self.sent_arena_check = False
        self.locked_abilities = copy.copy(ABILITY_LIST_INDEXED)[1:] #Exclude the starting index of 0, which is a blank string
        self.req_pieces = None
        self.worlds_cleared = 0
        self.level_status_updated = True
        self.switchexists_bitarr = 0
        self.file_number = 0
        self.detected_death = False
    
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
                ctx.command_processor.commands.update(knidl_client_commands) #Allows client to accept custom commands (?)
                return True 
            else:
                return False
        except bizhawk.RequestFailedError:
            return False  # Not able to get a response, say no for now

    def on_package(self, ctx, cmd: str, args: dict): #A sort of handler for packets. TY WL4 again. 
        if cmd == 'Connected':
            if args["slot_data"].get("death_link"):
                logger.info('Death Link found in slot data. Death link enabled')
                self.deathLink.enabled = True
                self.deathLink.update_pending = True
        if cmd == 'Bounced':
            tags = args.get("tags", [])
            try:
                if "DeathLink" in tags and args["data"]["source"] != ctx.auth:
                    logger.info('Death Link incoming, set death pending to True')
                    self.deathLink.pending = True
            except KeyError:
                pass

    ### Self Helper Function
    def get_color_flag_writes(self, ctx: "BizHawkClientContext", last_loc_id=None, last_loc_ids=[]):
        color_flag_writes = []
        color_array = get_door_color_bytes(ctx.missing_locations, last_loc_id, last_loc_ids)
        for i in range(self.worlds_cleared+1): #write for W1 with 0 bosses cleared, W7 with 6 bosses cleared
            level_count = LEVELS_PER_WORLD_INDEX[i]
            for offset in range(level_count):
                color_flag_writes.append((IW_CLEAR_FLAGS_START + i*7 + offset, [color_array[i][offset]], "IWRAM"))
                color_flag_writes.append((EW_CLEAR_FLAGS_START + self.file_number*0x100 + i*7 + offset, [color_array[i][offset]], "EWRAM"))
        return color_flag_writes
    
    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        try:
            #Early short circuit for when slot data hasn't loaded yet?
            if not ctx.slot_data:
                return
            
            #Check Game State
            #NOTE the bizhawk.read command returns a list of bytes (size 1) or bytearrays (size 1+)
            screen_modb, = await bizhawk.read(ctx.bizhawk_ctx, [
                (SCREEN_MOD_ADR,1, "IWRAM")       
            ])
            screen_mod = int.from_bytes(screen_modb)
            #logging.debug(f'Screen mod is {screen_mod}')
            
            #Before anything, reset the init flag if we see the title screen (handles emu refreshes, I think)
            if screen_mod in (0x3,0x4):
                logger.info('Detected title screen, setting flag to recalculate initial flags')
                self.init_startup = True
                self.initial_flags_written = False
                return 

            #Also before anything, set the required star rod pieces now that we have options access
            #Do the Star Rod calculation from options
            if not self.req_pieces:
                if ctx.slot_data.get('req_pieces_prc') == 0:
                    req_pieces = ctx.slot_data.get('req_pieces_num')
                else:
                    req_pieces = int(ctx.slot_data.get('req_pieces_prc')/100 * ctx.slot_data.get('pieces_in_pool'))
                if req_pieces > ctx.slot_data.get('pieces_in_pool'):
                    raise Exception('Error in Received Star Rod Piece Options: number of required pieces cannot be greater than amount in pool')
                if req_pieces < 7:
                    raise Exception('Error in Received Star Rod Piece Options: number of required pieces is less than 7 (percent set too low)')
                #Calculate the required pieces for each boss
                self.req_pieces_per_boss = int(req_pieces/7)
                self.req_pieces = req_pieces

            #If death link Option is true, enable death link
            if ctx.slot_data.get('death_link') == True:
                self.deathLink.enabled = True
                self.deathLink.update_pending = True

            #If a death link UPDATE is pending, handle the update
            if self.deathLink.update_pending:
                await ctx.update_death_link(self.deathLink.enabled)
                self.deathLink.update_pending = False

            # Don't do anything if the game is not in a specific state (list all states we will actually use here)
            #We only care about 5 (OW lobby), 7 (World Intro Cutscene), 8 (Normal Level or Boss), 9 (Big Switch cutscene), A (Goal Game, B (Final Cutscene)
            # and also 12 (Museum) and 13 (Arena) because kirby can gain abilities in these scenes
            if not screen_mod in (0x5,0x7,0x8,0x9,0xA,0XB,0x12,0x13):
                return
            
            # During the Level Intro Cutscene or any normal level, force all level clear flags to 02 to open the entire OW
            # And also the levels cleared variable to 06 (all) to make door sprites show up
            # Also set the big switch exists array to all 0 so that all big switches appear
            # Also set Kirby's max vitality here too
            # This strategy is a problem if savestates are used, but that's whatever for now
            if (not self.initial_flags_written) and (screen_mod == 0x7 or screen_mod == 0x8):
                #Find the File number
                (file_numberb, worlds_clearedb) = await bizhawk.read(ctx.bizhawk_ctx, [
                    (FILE_NUMBER_ADR, 1, "EWRAM"),
                    (WORLDS_CLEARED_IW, 1, "IWRAM")       
                ])
                self.file_number = int.from_bytes(file_numberb)
                self.worlds_cleared = int.from_bytes(worlds_clearedb)
                #set the level clear flags for levels in all CLEARED worlds to 02
                logger.debug(ctx.checked_locations)
                logger.info(f'Attempting to write clear flags to unlock all levels and big switches. Worlds Cleared count is {self.worlds_cleared}')
                clear_flag_writes = self.get_color_flag_writes(ctx)
                #Set Big Switch array (switches pressed) to True for UNLOCKED worlds
                n_switches = sum(BIGSWITCHES_PER_WORLD_INDEX[:(self.worlds_cleared+1)])
                self.switchexists_bitarr = (1 << n_switches) - 1
                switchexists_bytes = self.switchexists_bitarr.to_bytes(3,byteorder='little')
                logger.info(f'Switch Exists bit array is {hex(self.switchexists_bitarr)}')
                clear_flag_writes += [(IW_SWITCHEXISTS_BITARR,[switchexists_bytes[0]],'IWRAM'),
                                    (IW_SWITCHEXISTS_BITARR+1,[switchexists_bytes[1]],'IWRAM'),
                                    (IW_SWITCHEXISTS_BITARR+2,[switchexists_bytes[2]],'IWRAM'),
                                    (EW_SWITCHEXISTS_BITARR +self.file_number*0x100,[switchexists_bytes[0]],'EWRAM'), #bit padding is different in EWRAM. Probably a cleaner way to do this, but eh
                                    (EW_SWITCHEXISTS_BITARR+1 +self.file_number*0x100,[switchexists_bytes[1]],'EWRAM'),
                                    (EW_SWITCHEXISTS_BITARR+2 +self.file_number*0x100,[switchexists_bytes[2]],'EWRAM')
                                    ]
                #Finally, set the Warp Station bitarray to the correct value for unlocked worlds
                ws_bitarr = 2**(self.worlds_cleared+1)-1
                clear_flag_writes.append((WARP_STATION_BITARR, [ws_bitarr], 'EWRAM'))
                # logger.info(f'Clear Flags Write List is')
                # logger.info(clear_flag_writes)
                await bizhawk.write(
                    ctx.bizhawk_ctx, clear_flag_writes
                )
                #Boss Clear Failsafe: Check the bosses count, and award the checks for any boss locations that were "skipped".
                #This handles the scenario of a client disconnecting, fighting a boss without getting their check, then losing that check because no boss refights
                checked_boss_ids = [l for l in ctx.checked_locations if ' - Boss' in LOCATION_ID_TO_NAME[str(l)]]
                expected_boss_ids = [(i+1)*100+99+KNIDL_BASE_ID for i in range(self.worlds_cleared)] #Boss ID is always X99
                missing_boss_ids = [i for i in expected_boss_ids if not i in checked_boss_ids]
                if missing_boss_ids:
                    await ctx.send_msgs([{
                        "cmd": "LocationChecks",
                        "locations": missing_boss_ids
                    }])

                #Set Kirby's Health Bar
                if not self.kirby_max_hp:
                    extra_hp = sum([1 for i in ctx.items_received if ITEM_ID_TO_NAME[i.item] == 'Vitality'])
                    self.kirby_max_hp = ctx.slot_data.get("starting_vitality",3) + extra_hp
                hp_val = int(self.kirby_max_hp*8)
                logger.info(f"Attempting to set Kirby's current Max Health to {self.kirby_max_hp} segments (initial flag setting)")
                await bizhawk.write(ctx.bizhawk_ctx, 
                    [(KIRBY_HP_EW_ADR,[hp_val],'EWRAM'),
                     (KIRBY_MAX_HP_ADR,[hp_val],'EWRAM')
                     ]
                )
                self.initial_flags_written = True
                self.level_status_updated = True

            #If on the world intro cutscene, update level and switch clear flags based on the number of bosses beaten
            ##Note on checked locations: checked_locations is the server state variable, locations_checked is the local state variables. Yes, that's terrible
            if screen_mod == 0x7 and not self.level_status_updated:
                worlds_clearedb, = await bizhawk.read(ctx.bizhawk_ctx, [
                    (WORLDS_CLEARED_IW, 1, "IWRAM")       
                ])
                self.worlds_cleared = int.from_bytes(worlds_clearedb)
                logger.info(f'Attempting to write clear flags to unlock all levels and big switches. Worlds Cleared is {self.worlds_cleared}')
                clear_flag_writes = self.get_color_flag_writes(ctx)
                #Set Big Switch array (switches pressed) to True for UNLOCKED worlds
                n_switches = sum(BIGSWITCHES_PER_WORLD_INDEX[:(self.worlds_cleared+1)])
                self.switchexists_bitarr = (1 << n_switches) - 1 
                switchexists_bytes = self.switchexists_bitarr.to_bytes(3,byteorder='little')
                logger.debug(f'Switch Exists bit array is {hex(self.switchexists_bitarr)}')
                clear_flag_writes += [(IW_SWITCHEXISTS_BITARR,[switchexists_bytes[0]],'IWRAM'),
                                    (IW_SWITCHEXISTS_BITARR+1,[switchexists_bytes[1]],'IWRAM'),
                                    (IW_SWITCHEXISTS_BITARR+2,[switchexists_bytes[2]],'IWRAM'),
                                    (EW_SWITCHEXISTS_BITARR +self.file_number*0x100,[switchexists_bytes[0]],'EWRAM'), #bit padding is different in EWRAM. Probably a cleaner way to do this, but eh
                                    (EW_SWITCHEXISTS_BITARR+1 +self.file_number*0x100,[switchexists_bytes[1]],'EWRAM'),
                                    (EW_SWITCHEXISTS_BITARR+2 +self.file_number*0x100,[switchexists_bytes[2]],'EWRAM')
                                    ]
                #Finally, set the Warp Station bitarray to the correct value for unlocked worlds
                ws_bitarr = 2**(self.worlds_cleared+1)-1
                clear_flag_writes.append((WARP_STATION_BITARR, [ws_bitarr] , 'EWRAM'))
                # logger.info(f'Clear Flags Write List is')
                # logger.info(clear_flag_writes)
                await bizhawk.write(
                    ctx.bizhawk_ctx, clear_flag_writes
                )
                self.level_status_updated = True

            
            #while in a level or the OW, check to see if there are items to award
            if (self.sync_counter != len(ctx.items_received) or self.init_startup) and (screen_mod == 0x5 or screen_mod == 0x8 or screen_mod == 0x13):
                logger.info(f'init item sync sequence. Current sync counter is {self.sync_counter}. Number of items received is {len(ctx.items_received)}')
                file_numberb, = await bizhawk.read(ctx.bizhawk_ctx, [
                    (FILE_NUMBER_ADR, 1, "EWRAM")       
                ])
                self.file_number = int.from_bytes(file_numberb)
                sync_adr = SYNC_ADR_BASE + self.file_number*0x100
                sync_counterb, = await bizhawk.read(ctx.bizhawk_ctx, [
                    (sync_adr, 1, "EWRAM")       
                ])
                sync_counter_ingame = int.from_bytes(sync_counterb, "little")
                logger.info(f'Sync counter according to game RAM is {sync_counter_ingame} (file number {self.file_number}) (ADR {hex(SYNC_ADR_BASE + self.file_number*0x100)})')
                if sync_counter_ingame == 0xFF: #value should start at 0xFF on a new file 
                    self.sync_counter = 0
                else:
                    self.sync_counter = sync_counter_ingame
                #sync counter doesn't match, award items
                if self.sync_counter != len(ctx.items_received):
                    if self.sync_counter > len(ctx.items_received): #This can happen; don't worry about it too much. Progress will be unlocked regardless
                        self.sync_counter = len(ctx.items_received)
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

                #Loop through all items to check for all the client-made locks: door key, ability unlock items, and vitality upgrades
                for received_item in ctx.items_received:
                    received_item_name = ITEM_ID_TO_NAME[received_item.item]
                    received_item_id_readable = received_item.item - KNIDL_BASE_ID

                    if received_item_name.endswith(' Key'):
                        #Remove the corresponding entry of the Key item from the list of locked doors
                        logger.debug(f'removing lock for Key item {ITEM_ID_TO_NAME[received_item.item]}')
                        dn = received_item_name[:-4] #minus Key, ie 'Vegetable Valley Bomb Rally'
                        if dn in self.locked_door_names:
                            self.locked_door_names.remove(dn)

                    if received_item_id_readable > 50 and received_item_id_readable < 75:
                        ability_id = received_item_id_readable - 50
                        ability_name = ABILITY_LIST_INDEXED[ability_id]
                        logger.debug(f'removing lock for Copy Ability {ability_name}, ability id {ability_id}')
                        if ability_name in self.locked_abilities:
                            self.locked_abilities.remove(ability_name)

                #Set kirby's max hp based off the number of vitality items
                extra_hp = sum([1 for i in ctx.items_received if ITEM_ID_TO_NAME[i.item] == 'Vitality'])
                new_kirby_max_hp = ctx.slot_data.get("starting_vitality",3) + extra_hp
                if self.init_startup or new_kirby_max_hp != self.kirby_max_hp:
                    self.kirby_max_hp = new_kirby_max_hp
                    logger.info(f"Attempting to set Kirby's current Max Health to {self.kirby_max_hp}")
                    hp_val = int(self.kirby_max_hp*8)
                    await bizhawk.write(ctx.bizhawk_ctx, 
                        [(KIRBY_HP_EW_ADR,[hp_val],'EWRAM'),
                        (KIRBY_MAX_HP_ADR,[hp_val],'EWRAM')
                        ]
                    )
                #reset the current world and level if we're in the OW
                if screen_mod == 0x5:
                    self.current_world = -1
                    self.current_level = -1
                    self.current_pickup_flag_adr = 0

                if ctx.slot_data.get('lock_bonus_doors') == False: #If side doors are not locked, refresh the list with just the boss doors
                    self.locked_door_names = []
                    for i in range(len(WORLD_NAMES_INDEXED)):
                        self.locked_door_names.append(f'{WORLD_NAMES_INDEXED[i]} Boss')

                #Look at the number of star rod pieces and unlock the corresponding boss doors
                star_rod_pieces_received = sum(1 for i in ctx.items_received if ITEM_ID_TO_NAME[i.item] == 'Star Rod Piece')
                boss_door_count = min(
                    int(star_rod_pieces_received / self.req_pieces_per_boss),6 #never unlock more than 6 boss doors in the loop
                )
                boss_doors_to_unlock = [wn + ' Boss' for wn in WORLD_NAMES_INDEXED[:boss_door_count]]
                if star_rod_pieces_received >= self.req_pieces:
                    boss_doors_to_unlock.append('Rainbow Resort Boss') 
                logger.info(f'removing lock for following boss doors: {boss_doors_to_unlock}')
                for dn in boss_doors_to_unlock:
                    if dn in self.locked_door_names:
                        self.locked_door_names.remove(dn)

                #based on the doors in the locked door list, calculate what to write to the locked door bit array
                locked_door_writes = []
                for i,w in enumerate(WORLD_NAMES_INDEXED):
                    door_bits = []
                    logger.debug(f'locked door names before write is {self.locked_door_names}')
                    for ldn in self.locked_door_names:
                        if w in ldn:
                            door_type = ldn.split(w)[1].strip() #Map the door in the locked door list to its index in the bit array
                            door_bitarr_index = DOOR_NAME_TO_BIT_MAP.index(door_type)
                            door_bits.append(door_bitarr_index)
                    door_bitarr = sum(1 << b for b in door_bits) #compile the bit indexes in a single bit array number
                    assert door_bitarr <= 0xFFFF
                    door_bitarr_list = [door_bitarr & 0xFF, door_bitarr >> 8] #split the bit array number into a list of two byte numbers, the bigger one second (little-endian)
                    locked_door_writes.append((DOOR_LOCK_BITARR+2*i, door_bitarr_list, 'IWRAM')) #Write the bit array number to the control panel with correct offset (2 bytes per world)
                #logger.debug(locked_door_writes)

                #Similarly, based on the abilities in the locked abilities list, calculate what to write to the "mouthguard" bit array
                #This is simpler since the entire thing fits in <=4 bytes
                if ctx.slot_data.get('lock_copy_abilities') == False: #If copy abilities are not locked, write all 0's
                    ability_bits = [0 for _ in ABILITY_LIST_INDEXED]
                else:
                    ability_bits = [1 if a in self.locked_abilities else 0 for a in ABILITY_LIST_INDEXED] 
                #because empty string is in the master list but never the locked abilities, the first bit is always 0
                ability_bits.reverse() #Reverse because the first bit will become the highest "place" in the bitarr
                ability_bitarr = 0
                for b in ability_bits:
                    ability_bitarr = (ability_bitarr << 1) | b #Left shift 1 and "add" the next bit to the tail with bitwise OR
                assert ability_bitarr <= 0xFFFFFFFF #starting value with all abilities locked should be 0x1FFFFFE (ability "0" is always unlocked)
                ability_bitarr_list = [ability_bitarr & 0xFF, ability_bitarr >> 8 & 0xFF, ability_bitarr >> 16 & 0xFF, ability_bitarr >> 24 & 0xFF] 
                #Split the full word into 4 byte numbers, bigger places last because little-endian again
                ability_lock_writes = [(ABILITY_LOCK_BITARR, ability_bitarr_list, 'IWRAM')]

                #Set the sync counter now that any needed items have been awarded
                #Note we may need a two-byte write if we ever have more than 254 max possible checks/items (since FF 255 is the default) (currently it's 201)
                #Also, write the correct byte string to the locked door bit array and ability lock array
                sync_writes = locked_door_writes + ability_lock_writes + [(sync_adr, [self.sync_counter], "EWRAM")]
                logger.info(f'attempting to write new sync counter {self.sync_counter}, and locked door bit array')
                logger.debug(sync_writes)
                await bizhawk.write(ctx.bizhawk_ctx, sync_writes
                )
                #NOTE: The sync counter can be written whenever, but will only be actually saved by Bizhawk when the game itself saves. This is out of the client's control
                #So, if a player connects, receives items, then leaves without the game saving (ie, on level complete), the sync counter will not update and the items will be received again
                self.init_startup = False

            #Handle the in-game effects of all items (mainly playing SFX). don't do anything if a death is pending
            if len(self.item_queue) != 0 and self.deathLink.pending == False:
                #check if we're free to award the item
                (item_award_panelb, world_numb, bgm_idb) = await bizhawk.read(ctx.bizhawk_ctx, [
                    (ITEM_AWARD_ADR, 1, "IWRAM"),
                    (WORLD_MOD_ADR, 1, "IWRAM"),
                    (BGM_ID_ADR, 1, "IWRAM")       
                ])
                item_award_panel = int.from_bytes(item_award_panelb)
                world_num = int.from_bytes(world_numb) + 1
                bgm_id = int.from_bytes(bgm_idb)
                if world_num == 8 and not bgm_id == 0x22:
                    logger.debug('In Nightmare Fight and not in Wizard phase, do nothing')
                elif item_award_panel != 0:
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
                        self.hp_bank += self.kirby_max_hp - 1 
                        logger.info(f'Added {self.kirby_max_hp - 1} HP to Bank. Bank at {self.hp_bank}')
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
                    elif current_item >= 100: #Door Unlock
                        item_award_id = 8

                    if item_award_id:
                        logger.info(f'attempting to award queued item {current_item}')
                        await bizhawk.write(ctx.bizhawk_ctx,
                            [(ITEM_AWARD_ADR, [item_award_id], "IWRAM")]
                        )
                        self.item_queue = self.item_queue[1:]

            #If there's hp in the hp bank and Kirby has less than full health AND enough time has expired so that we don't overheal kirby, award a health segment
            #Also don't heal if he's at 0 hp (ie, pit death) or if a deathLink is pending, or during the nightmare orb phase
            if self.hp_bank > 0 and screen_mod in (0x8, 0x13) and self.deathLink.pending == False:
                (kirby_hpb, kirby_actionableb, world_numb, bgm_idb) = await bizhawk.read(ctx.bizhawk_ctx, [
                    (KIRBY_HP_EW_ADR, 1, "EWRAM"), 
                    (KIRBY_ACTIONABLE, 1, "IWRAM"),
                    (WORLD_MOD_ADR, 1, "IWRAM"),
                    (BGM_ID_ADR, 1, "IWRAM") 
                ])
                kirby_hp = int(int.from_bytes(kirby_hpb) / 8)
                kirby_actionable = int.from_bytes(kirby_actionableb)
                world_num = int.from_bytes(world_numb) + 1 #FoD = W8
                bgm_id = int.from_bytes(bgm_idb)
                nightmare_filter = world_num != 8 or (world_num == 8 and bgm_id == 0x22) #Not in FoD or in FoD with Wizard phase active
                now = time.time()
                if kirby_actionable == 0 and nightmare_filter and kirby_hp < self.kirby_max_hp and kirby_hp > 0 and now - self.hp_trickle_timestamp > self.HEAL_TIME_DELAY: 
                    logger.info(f'Detected kirby HP is {kirby_hp} with HP bank at {self.hp_bank}. Awarding 1 HP segment')
                    await bizhawk.write(ctx.bizhawk_ctx,
                            [(ITEM_AWARD_ADR, [1], "IWRAM")]
                    )
                    self.hp_bank -= 1
                    self.hp_trickle_timestamp = now

            #If a death link is pending, kill Kirby at first available opportunity 
            if self.deathLink.enabled and self.deathLink.pending and screen_mod in (0x8, 0x13):
                logger.info('Death Link: Checking to see if Kirby is killable now')
                (kirby_hpb, kirby_actionableb) = await bizhawk.read(ctx.bizhawk_ctx, [
                    (KIRBY_HP_EW_ADR, 1, "EWRAM"), 
                    (KIRBY_ACTIONABLE, 1, "IWRAM"), 
                ])
                kirby_hp = int(int.from_bytes(kirby_hpb) / 8)
                kirby_actionable = int.from_bytes(kirby_actionableb)
                if kirby_hp > 0 and kirby_actionable == 0: #Only attempt to kill if Kirby is in a normal gameplay state
                    logger.info('Death Link: Attempting to kill Kirby because of Death Link')
                    await bizhawk.write(ctx.bizhawk_ctx,
                            [(KIRBY_HP_IW, [0], "IWRAM")]
                    )
                    self.deathLink.sent_this_death = True #Next kirby death will be a Death Link death. 

            #If death link is enabled, look to see if Kirby is Dead
            if self.deathLink.enabled and screen_mod in (0x8, 0x13):
                kirby_hpb, = await bizhawk.read(ctx.bizhawk_ctx, [
                    (KIRBY_HP_EW_ADR, 1, "EWRAM"), 
                ])
                kirby_hp = int(int.from_bytes(kirby_hpb) / 8)
                if kirby_hp == 0 and not self.detected_death:
                    self.deathLink.pending = False #Confirmed that we killed kirby via death link, death no longer pending
                    self.detected_death = True #Flag to confirm this is a new death and not the same death detected multiple times
                    logger.info('Death Link: Detected Kirby Death')
                    if self.deathLink.sent_this_death == False: #The death was not a death link death, send a signal
                        logger.info('Death Link: Death was not from Death Link, Sending Death Link death')
                        self.deathLink.sent_this_death = True
                        await ctx.send_death()
                    else: #The death was a Death Link death, reset the "sent this death" flag
                        logger.info('Death Link: Death was from Death Link, resetting sent death flag')
                        self.deathLink.sent_this_death = False
                elif kirby_hp > 0:
                    self.detected_death = False
            
            #If a goal game is detected, send the level clear check. 
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
                #Also update the door colors
                color_flag_writes = self.get_color_flag_writes(ctx,last_loc_id=level_clear_loc_id)
                await bizhawk.write(
                    ctx.bizhawk_ctx, color_flag_writes
                )

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
            if not screen_mod == 0x7: #assume we need to update the level clear status every time we see a world intro cutscene (ie, beat a boss)
                self.level_status_updated = False

                
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
                if level_num <= 5 and (self.current_world != world_num or self.current_level != level_num):
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
                    new_bits = 0
                else:
                    new_bits = pickup_bitarr ^ self.current_pickup_bitarr
                    self.current_pickup_bitarr = pickup_bitarr

                #calculate the "1's" in the new bit array by checking each smallest digit and right shifting until empty
                new_ids = []; p = 0
                while new_bits:
                    if new_bits & 1:
                        new_ids.append(p+1) #+1 because ID's are 1-indexed, position is 0-indexed
                    new_bits >>= 1
                    p+= 1

                loc_ids = []
                for new_id in new_ids:
                    if world_num + 1 == 6 and level_num + 1 == 6: #Carve out for level 6-6, where 8 UFOs take up the first 8 item id slots
                        if new_id > 8:
                            pickup_id = new_id - 8
                        else:
                            break ##if id is 1-8, it's one of the UFO's
                    else:
                        pickup_id = new_id #1st item id = 1, effectively 1-indexed
                    loc_id_readable = (world_num+1)*100 + (level_num+1)*10 + pickup_id 
                    loc_id = loc_id_readable + KNIDL_BASE_ID
                    loc_name = None #Technically we don't need to find the location name here, but it's convenient for logging 
                    try:
                        loc_name = LOCATION_ID_TO_NAME[str(loc_id)]
                    except KeyError:
                        logger.warning(f'Attempted to find location name for nonexistent id: {loc_id_readable} (readable). Pass') #This will happen for UFO "locations"
                    if loc_name: 
                        logger.info(f'Attempting to send location {loc_name}, id {LOCATION_NAME_TO_ID[loc_name]}')
                        loc_ids.append(LOCATION_NAME_TO_ID[loc_name])
                #For every location id, check to see if it was already collected. If it was (2nd time collecting after a reset), award its "vanilla" in-game item
                for l in loc_ids:
                    if l in ctx.checked_locations:
                        loc_name = LOCATION_ID_TO_NAME[str(l)]
                        logger.info(f'Already found location {loc_name}, awarding in-game item')
                        if 'Pep Drink' in loc_name:
                            self.item_queue.append(11)
                        elif 'Tomato' in loc_name:
                            self.item_queue.append(12)
                        elif '1up' in loc_name:
                            self.item_queue.append(13)
                        elif 'Candy' in loc_name:
                            self.item_queue.append(14) 
                if loc_ids:
                    await ctx.send_msgs([{
                        "cmd": "LocationChecks",
                        "locations": loc_ids
                    }])
                    #Also update the door colors
                    color_flag_writes = self.get_color_flag_writes(ctx,last_loc_ids=loc_ids)
                    await bizhawk.write(
                        ctx.bizhawk_ctx, color_flag_writes
                    )


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
                    
            ##Victory  -- look for the final cutscene BGM
            if screen_mod == 0xB and not self.sent_victory_check:
                logger.info('Detected Nightmare Defeated Game End Cutscene')
                logger.info(f'Attempting to send Victory Event')
                await ctx.send_msgs([{
                    "cmd": "StatusUpdate",
                    "status": ClientStatus.CLIENT_GOAL
                }])
                self.sent_victory_check = True

            #Big Switch Checks -- look for a specific screen mod        
            if screen_mod == 0x9 and not self.sent_bigswitch_check:
                logger.info('Detected Big Switch cutscene')
                #Note that DURING the big switch cutscene, the level mod adr always changes to 0x10, so don't read it fresh!
                #Instread, we use the value we already stored for changing the pickup flag window
                loc_id_readable = int((self.current_world+1)*100 + (self.current_level+1)*10 + 9) 
                loc_id = int(KNIDL_BASE_ID + loc_id_readable) #Pattern is WL9
                logger.info(f'Attempting to send Big Switch check from World {self.current_world+1}, level {self.current_level+1}, id (readable) {loc_id_readable}')
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [loc_id]
                }])
                #Also update the door colors
                color_flag_writes = self.get_color_flag_writes(ctx,last_loc_id=loc_id)
                await bizhawk.write(
                    ctx.bizhawk_ctx, color_flag_writes
                )
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

        except bizhawk.RequestFailedError:
            print('ERROR: bizhawk request failed error')
            pass

