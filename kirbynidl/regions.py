from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .world import KirbyNIDLWorld
#See locations.py for explanation of this boilerplate

from BaseClasses import Region #,Entrance

ENEMY_LIST_INDEXED = [
    'Drop Star',
    'Mr. Bright Laser Star',
    'Waddle Dee',
    'Parasol Waddle Dee',
    'Pengy',
    'Bomber',
    'Sparky',
    'Sword Knight',
    'Blade Knight',
    'Needlous',
    'UFO',
    'Parasol',
    'Rocky',
    'Sir Kibble',
    'Cappy Cap',
    'Capless Cappy',
    'Cool Spook',
    'Kabu',
    'Twister',
    'Starman',
    'Hot Head',
    'Poppy Bros. Jr.',
    'Poppy Bros. Jr. Roller (Apple)',
    'Poppy Bros. Jr. Roller (Tomato)',
    'Poppy Bros. Jr. Apple',
    'Wheelie',
    'Flamer',
    'Noddy',
    'Chilly',
    'Waddle Doo',
    'Parasol Waddle Doo',
    'Bronto Burt',
    'Twizzy',
    'Squishy',
    'Bubbles',
    'Glunk',
    'Slippy',
    'Blipper',
    'Gip',
    'Broom Hatter',
    'Laser Ball',
    'Coconut',
    'Coner',
    'Bonkers',
    'Poppy Bros. Sr.',
    'Bugsy',
    'Bonkers Coconut',
    'Poppy Bros. Sr. Bomb',
    'Bugsy Ladybug',
    'Grand Wheelie',
    'Fire Lion',
    'Phan Phan',
    'Grand Wheelie Wheelie',
    'Phan Phan Apple',
    'Mr. Frosty',
    'Mr. Tick-Tock',
    'Mr. Frosty Ice Block',
    'Mr. Tick-Tock Note',
    'Axe Knight',
    'Mace Knight',
    'Trident Knight',
    'Javelin Knight',
    'Mr. Shine Falling Star',
    'Kracko Starman',
    'Paint Roller Car',
    'Paint Roller Fake Kirby',
    'Paint Roller Waddle Dee',
    'Paint Roller Mike',
    'Paint Roller Baseball',
    'Paint Roller Bomb',
    'Paint Roller Cloud',
    'Paint Roller Parasol',
    'Heavy Mole Gold Missile',
    'Heavy Mole Red Missile',
    'Whispy Woods Apple',
]

ENEMY_ABILITY_MAP = {
    'Drop Star' : ['None',0x0873F670,0], #0:Ability (text), 1:ROM VALUE ADR, 2: Index / ID.
    'Mr. Bright Laser Star' : ['Fire',0x0873F69C,0],
    'Waddle Dee' : ['None',0x08740BE0,0],
    'Parasol Waddle Dee' : ['Parasol',0x08740C0C,0],
    'Pengy' : ['Ice',0x08740C38,0],
    'Bomber' : ['Crash',0x8740C64,0],
    'Sparky' : ['Spark',0x08740C90,0],
    'Sword Knight' : ['Sword',0x08740CE8,0], 
    'Blade Knight' : ['Sword',0x08740D14,0], 
    'Needlous' : ['Needle',0x08740D6C,0], 
    'UFO' : ['UFO',0x08740D98,0],
    'Parasol' : ['Parasol',0x08740DC4,0], 
    'Rocky' : ['Stone',0x087417C4,0], 
    'Sir Kibble' : ['Cutter',0x087417F0,0], 
    'Cappy Cap' : ['None',0x0874181C,0], 
    'Capless Cappy' : ['None',0x08741848,0], 
    'Cool Spook' : ['Light',0x087418A0,0], 
    'Kabu' : ['None',0x087418CC,0], 
    'Twister' : ['Tornado',0x087418F8,0],
    'Starman' : ['Hi-Jump',0x08741924,0],
    'Hot Head' : ['Fire',0x08741950,0], 
    'Poppy Bros. Jr.' : ['None',0x0874197C,0], 
    'Poppy Bros. Jr. Roller (Apple)' : ['None',0x087419A8,0], 
    'Poppy Bros. Jr. Roller (Tomato)' : ['None',0x087419D4,0], 
    'Poppy Bros. Jr. Apple' : ['None',0x08741A00,0], 
    'Wheelie' : ['Wheel',0x08741A58,0], 
    'Flamer' : ['Burning',0x08741A84,0], 
    'Noddy' : ['Sleep',0x087429F4,0], 
    'Chilly' : ['Freeze',0x08742A20,0], 
    'Waddle Doo' : ['Beam',0x08742A4C,0], 
    'Parasol Waddle Doo' : ['Parasol',0x08742A78,0], 
    'Bronto Burt' : ['None',0x08742AA4,0], 
    'Twizzy' : ['None',0x08742AD0,0], 
    'Squishy' : ['None',0x08742AFC,0], 
    'Bubbles' : ['Ball',0x08742B28,0],
    'Glunk' : ['None',0x08742B54,0], 
    'Slippy' : ['None',0x08742B80,0], 
    'Blipper' : ['None',0x08742BAC,0], 
    'Gip' : ['None',0x08742BD8,0], 
    'Broom Hatter' : ['None',0x08743318,0], 
    'Laser Ball' : ['Laser',0x08743344,0], 
    'Coconut' : ['None',0x08743370,0], 
    'Coner' : ['None',0x087433C8,0], 
    'Bonkers' : ['Hammer',0x08743B58,0], 
    'Poppy Bros. Sr.' : ['Crash',0x08743B84,0], 
    'Bugsy' : ['Backdrop',0x08743BB0,0], 
    'Bonkers Coconut' : ['None',0x087441E4,0], 
    'Poppy Bros. Sr. Bomb' : ['None',0x08744210,0], 
    'Bugsy Ladybug' : ['None',0x0874423C,0], 
    'Grand Wheelie' : ['Wheel',0x08744970,0], 
    'Fire Lion' : ['Burning',0x0874499C,0],
    'Phan Phan' : ['Throw',0x087449C8,0],
    'Grand Wheelie Wheelie' : ['None',0x0874553C,0],
    'Phan Phan Apple' : ['None',0x08745568,0],
    'Mr. Frosty' : ['Freeze',0x0874581C,0],
    'Mr. Tick-Tock' : ['Mike',0x08745848,0],
    'Mr. Frosty Ice Block' : ['None',0x08745B3C,0],
    'Mr. Tick-Tock Note' : ['None',0x08745B94,0],
    'Axe Knight' : ['None',0x08747D68,0],
    'Mace Knight' : ['None',0x08747DC0,0],
    'Trident Knight' : ['None',0x08747E18,0],
    'Javelin Knight' : ['None',0x08747E70,0],
    'Mr. Shine Falling Star' : ['Cutter',0x08748B40,0],
    'Kracko Starman' : ['Hi-Jump',0x08749C24,0],
    'Paint Roller Car' : ['Wheel',0x0874B978,0],
    'Paint Roller Fake Kirby' : ['None',0x0874B9A4,0],
    'Paint Roller Waddle Dee' : ['None',0x0874B9D0,0],
    'Paint Roller Mike' : ['Mike',0x0874B9FC,0],
    'Paint Roller Baseball' : ['Ball',0x0874BA28,0],
    'Paint Roller Bomb' : ['Crash',0x0874BA54,0],
    'Paint Roller Cloud' : ['Spark',0x0874BA80,0],
    'Paint Roller Parasol' : ['Parasol',0x0874BAAC,0],
    'Heavy Mole Gold Missile' : ['Hammer',0x0874BB30,0],
    'Heavy Mole Red Missile' : ['Sleep',0x0874BB5C,0],
    'Whispy Woods Apple' : ['None',0x0874C384,0],

}
for i,e in enumerate(ENEMY_LIST_INDEXED):
    ENEMY_ABILITY_MAP[e][2] = i


ENEMIES_IN_LEVEL = [
    ###WORLD 1
    [
        ['Bronto Burt','Hot Head','Poppy Bros. Jr.','Sparky','UFO','Waddle Dee','Waddle Doo'],
        ['Bronto Burt','Broom Hatter','Cappy','Hot Head','Poppy Bros. Jr.','Poppy Bros. Jr. Apple','Sir Kibble','Sparky','Sword Knight','Waddle Dee','Waddle Doo','Poppy Bros. Sr.','Poppy Bros Sr. Bomb'],
        #1-3: all aquatic enemies are inhalable
        ['Blipper','Bronto Burt','Broom Hatter','Cappy Cap','Capless Cappy','Coner','Flamer','Glunk','Hot Head','Kabu','Poppy Bros. Jr.','Slippy','Sparky','Waddle Dee','Waddle Doo'],
        ['Blade Knight','Bronto Burt','Broom Hatter','Cappy','Kabu','Poppy Bros. Jr.','Sparky','Sword Knight','Needlous','Twizzy','Waddle Dee','Waddle Doo']
    ],
    ###WORLD 2
    [
        ['Bomber','Cappy','Coconut','Coner','Hot Head','Parasol','Waddle Doo','Sword Knight','Twister','Waddle Dee'],
        ['Gip','Coner','Hot Head','Parasol','Poppy Bros. Jr.','Poppy Bros. Jr. Apple','Sparky','Sword Knight','Needlous','Waddle Dee','Wheelie','Grand Wheelie','Grand Wheelie Wheelie'],
        #2-3: Blipper is reachable from water's surface
        ['Blipper','Bronto Burt','Cappy Cap','Capless Cappy','Kabu','Parasol','Sword Knight','Waddle Dee','Axe Knight','Mace Knight','Trident Knight'],
        ['Gip','Bronto Burt','Cappy Cap','Capless Cappy','Glunk','Hot Head','Laser Ball','Parasol','Rocky','Sparky','Waddle Dee','Waddle Doo','Mr. Tick-Tock','Mr. Tick-Tock Note'],
        ['Bomber','Bronto Burt','Flamer','Kabu','Laser Ball','Noddy','Parasol','Poppy Bros. Jr.','Poppy Bros. Jr. Apple','Sir Kibble','Starman','Sword Knight','Wadddle Dee','Waddle Doo','Wheelie'],
    ],
    ###WORLD 3
    [
        ['Bomber','Bronto Burt','Flamer','Laser Ball','Sword Knight','Parasol','Rocky','Waddle Dee','Mr. Tick-Tock','Mr. Tick-Tock Note'],
        ['Blade Knight','Gip','Glunk','Hot Head','Pengy','Poppy Bros. Jr.','Rocky','Sir Kibble','Sparky','Needlous','Twizzy','Waddle Dee','Waddle Doo','Bugsy','Bugsy Ladybug'],
        ['Blade Knight','Bronto Burt','Broom Hatter','Coner','Flamer','Hot Head','Pengy','Starman','Sword Knight','Needlous','Waddle Dee'],
        ['Broom Hatter','Kabu','Parasol','Sword Knight','Waddle Doo','Axe Knight','Mace Knight','Javelin Knight'],
        ['Blade Knight','Bomber','Chilly','Laser Ball','Sir Kibble','Sparky','Sword Knight','Twizzy','Waddle Dee','Bonkers','Drop Star','Bonkers Coconut'],
        ['Blade Knight','Bomber','Hot Head','Laser Ball','Pengy','Poppy Bros. Jr.','Rocky','Sir Kibble','Slippy','Starman','Twizzy','Waddle Dee']
    ],
    ###WORLD 4
    [
        ['Blade Knight','Bubbles','Glunk','Hot Head','Laser Ball','Noddy','Parasol','Sir Kibble','Sparky','Twister','Twizzy','Waddle Dee','Wadle Doo'],
        ['Hot Head','Parasol','Poppy Bros. Jr.','Poppy Bros. Jr. Apple','Sparky','Squishy','Waddle Dee','Poppy Bros. Sr.','Poppy Bros Sr. Bomb'],
        ['Bomber','Gip','Bronto Burt','Broom Hatter','Cappy Cap','Cappy Cap','Hot Head','Kabu','Laser Ball','Parasol','Sir Kibble','Starman','Sword Knight','Waddle Dee'],
        ['Blade Knight','Bronto Burt','Bubbles','Coner','Sparky','Twizzy','Waddle Dee','Waddle Doo','Wheelie','Phan Phan','Phan Phan Apple'],
        ['Gip','Bronto Burt','Broom Hatter','Chilly','Flamer','Kabu','Sparky','Sword Knight','Waddle Dee','Axe Knight','Mace Knight','Trident Knight','Javelin Knight'],
        #4-6 Blipper is in the stage, but is stuck underwater and cannot be inhaled
        ['Blade Knight','Bronto Burt','Glunk','Hot Head','Kabu','Parasol','Rocky','Sir Kibble','Slippy','Starman','Sword Knight','Waddle Dee','Waddle Doo','Mr. Tick-Tock','Mr. Tick-Tock Note']
    ],
    ###WORLD 5
    [
        ['Bomber','Bronto Burt','Cappy Cap','Capless Cappy','Chilly','Kabu','Parasol','Pengy','Rocky','Starman','Sword Knight','Needlous','Waddle Dee','Waddle Doo'],
        #5-2: There is a blippper that CAN be lured to the surface
        ['Blade Knight','Blipper','Gip','Bubbles','Coconut','Coner','Flamer','Kabu','Sparky','Waddle Dee','Bonkers','Drop Star','Bonkers Coconut'],
        ['Gip','Hot Head','Laser Ball','Parasol','Poppy Bros. Jr.','Poppy Bros. Jr. Apple','Rocky','Sparky','Starman','Sword Knight','Twizzy','Waddle Dee','Wheelie'],
        #5-4: all enemies are available outside water
        ['Blade Knight','Blipper','Gip','Bubbles','Flamer','Glunk','Poppy Bros. Jr.','Poppy Bros. Jr. Apple','Sparky','Squishy','Waddle Dee','Waddle Doo','Axe Knight','Trident Knight'],
        ['Gip','Bronto Burt','Flamer','Hot Head','Laser Ball','Parasol','Poppy Bros. Jr.','Poppy Bros. Jr. Apple','Sir Kibble','Starman','Sword Knight','Waddle Dee','Fire Lion','Drop Star'],
        #5-6 Blipper is stuck in the water this time
        ['Blade Knight','Rocky','Waddle Dee','Wheelie'],
    ],
    ###WORLD 6
    [
        #6-1. Blipper and slippy can be surfaced. There is a glunk and a coner outside water
        ['Blade Knight','Blipper','Gip','Coner','Flamer','Glunk','Hot Head','Slippy','Sparky','Twizzy','Phan Phan','Phan Phan Apple'],
        #6-2 Blipper and slippy OK. Glunk is outside water
        ['Blade Knight','Blipper','Bomber','Bronto Burt','Broom Hatter','Cappy Cap','Capless Cappy','Flamer','Glunk','Kabu','Parasol','Poppy Bros. Jr.','Rocky','Sir Kibble','Slippy','Sparky'
         'Starman','Sword Knight','Twister','Waddle Dee','Waddle Doo'],
        #6-3. Only noting enemies available outside the metal block-locked areas
        #There are blippers here, but they cannot be eaten safely
        ['Waddle Dee','Sparky','Bonkers','Bonkers Coconut','Drop Star','Flamer','Poppy Bros. Jr.','Coner','Bronto Burt','Broom Hatter','Glunk','Coconut','Slippy','Kabu','Hot Head'],
        #6-4: Coner, Slippy, and Glunk out of water. Blipper stuck in the water
        ['Blade Knight','Bomber','Broom Hatter','Coner','Glunk','Parasol','Sir Kibble','Slippy','Sword Knight','Twizzy','Waddle Dee','Waddle Doo'],
        #6-5: Water-locked blipper
        ['Blade Knight','Bomber','Bronto Burt','Chilly','Hot Head','Laser Ball','Pengy','Poppy Bros. Jr.','Poppy Bros. Jr. Apple','Sparky','Needlous','Waddle Dee','Waddle Doo'],
        #6-6 Blipper, Glunk and Slippy all OK
        ['Blade Knight','Blipper','Bronto Burt','Cappy Cap','Capless Cappy','Flamer','Glunk','Hot Head','Laser Ball','Pengy','Slippy','Sparky','Waddle Dee','Waddle Doo',
         'Mr. Frosty','Mr. Frosty Ice Block','Poppy Bros. Sr.','Poppy Bros. Sr. Bomb','Axe Knight','Mace Knight','Trident Knight','Javelin Knight']
    ],
    ###WORLD 7
    [
        ['Blade Knight','Chilly','Flamer','Hot Head','Laser Ball','Noddy','Rocky','Sir Kibble','Sparky','Waddle Dee','Waddle Doo'],
        ['Blade Knight','Mr. Frosty','Mr. Frosty Ice Block','Mr. Tick-Tock','Mr. Tick-Tock Note','Poppy Bros. Sr.','Poppy Bros. Sr. Bomb','Bonkers','Bonkers Coconut','Drop Star',
         'Bugsy','Bugsy Ladybug','Phan Phan','Phan Phan Apple','Fire Lion'],
        #7-3: Blipper comes out of the water, coner OK
        ['Blade Knight','Blipper','Bronto Burt','Broom Hatter','Chilly','Coner','Noddy','Sir Kibble','Waddle Dee','Waddle Doo'],
        ['Bomber','Bronto Burt','Bubbles','Gip','Flamer','Hot Head','Noddy','Laser Ball','Poppy Bros. Jr.','Sir Kibble','Sparky','Twister','Twizzy','Waddle Dee'],
        #7-5: There is a wheelie, but it's inaccessible under the midboss
        ['Bomber','Gip','Flamer','Hot Head','Laser Ball','Sparky','Grand Wheelie','Grand Wheelie Wheelie'],
        #7-6: The blippers can be surface-skimmed
        ['Blipper','Bronto Burt','Broom Hatter','Cappy Cap','Capless Cappy','Coconut','Coner','Kabu','Parasol','Poppy Bros. Jr.','Poppy Bros. Jr. Apple','Sir Kibble','Squishy','Twizzy',
        'Waddle Dee','Waddle Doo']
    ]
]

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

region_names = []
for i, world_name in enumerate(WORLD_NAMES_INDEXED):
    region_names.append(world_name)
    for j in range(LEVELS_PER_WORLD_INDEX[i]):
        region_names.append(world_name + ' ' + str(j+1))
#region_names = ["Vegetable Valley","Vegetable Valley 1","Vegetable Valley 2","Vegetable Valley 3","Vegetable Valley 4"] ...

def create_and_connect_regions(world: KirbyNIDLWorld) -> None:
    create_all_regions(world)
    connect_regions(world)

def create_all_regions(world: KirbyNIDLWorld) -> None:
    #Regions are invoked through their constructor
    knidl_regions = [Region(rn, world.player, world.multiworld) for rn in region_names]
    # We now need to add these regions to multiworld.regions so that AP knows about their existence.
    world.multiworld.regions += knidl_regions
    #Create the special "Warp Station" region if the option for it is on
    if world.options.warp_station_skips:
        world.multiworld.regions.append(Region('Warp Star Station', world.player, world.multiworld))

def connect_regions(world: KirbyNIDLWorld) -> None:
    #Connections to region are made by the region.connect helper function
    #You can add a rule to the entrance as the final argument, but this is not required
    #You can also init an entrance object and use entrance.connect(region)
    #Note that entrances are 1-way, but logic assumes you can always get to an earlier if you go to a later region (ie, game reset)

    #Connect all level regions to their parent world region via connections named like "Vegetable Valley 1 Door". These connections have no requirements
    for world_name in WORLD_NAMES_INDEXED:
        w = world.get_region(world_name)
        for rn in region_names:
            if rn.startswith(world_name + ' '):
                r = world.get_region(rn)
                w.connect(r, rn + " Door") 

    #Connect all world regions to each other in sequence with Star Rod Pieces as the requirement
    #Do the Star Rod calculation from options
    if world.options.req_pieces_prc == 0:
        req_pieces = world.options.req_pieces_num
    else:
        req_pieces = int(world.options.req_pieces_prc/100 * world.options.pieces_in_pool)
    if req_pieces > world.options.pieces_in_pool:
        raise Exception('Error in Star Rod Piece Options: number of required pieces cannot be greater than amount in pool')
    if req_pieces < 7:
        raise Exception('Error in Received Star Rod Piece Options: number of required pieces is less than 7 (percent set too low)')
    #Calculate the required pieces for each boss
    req_pieces_per_boss = int(req_pieces/7)

    for i, world_name in enumerate(WORLD_NAMES_INDEXED[:-1]):
        w_current = world.get_region(world_name)
        w_next = world.get_region(WORLD_NAMES_INDEXED[i+1])
        req_pieces_i = req_pieces_per_boss*(i+1)
        ##PYTHON PITFALL: if a lambda references iteration variable i, it will "look up" the value of i when called, which is the END VALUE of the loop (ie, 6)
        ##SOLUTION: use the extra "rp" variable in the lambda with the "req pieces" value defined in the loop. Notice how the "rp" var turns color in VS code
        ##This applies to ALL rule functions
        w_current.connect(w_next,world_name + ' Next Door', lambda state, rp=req_pieces_i: state.has("Star Rod Piece", world.player, rp))

    #Connect the special warp station region if option is set
    if world.options.warp_station_skips:
        print('Regions.py Warp Station skips called!')
        ws_region = world.get_region('Warp Star Station')
        for i, world_name in enumerate(WORLD_NAMES_INDEXED):
            w_current = world.get_region(world_name)
            w_current.connect(ws_region, world_name + ' Warp Station Door', lambda state, wn = world_name: state.has(wn+ ' Warp Station Key', world.player))
            ws_region.connect(w_current, world_name + ' Warp Station Exit Door', lambda state, wn = world_name: state.has(wn + ' Warp Station Key', world.player))

        
    


  
