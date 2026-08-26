;KNDL_AP_v0.asm
;This patch applies custom code to do the following:
;Check for doors locked/unlocked
;Detect Items (1ups, tomatos and pep brews)
;Apply Items

.gba
.open "KNDL/KNDL_AP_v0.gba", 0x08000000

; ============================
;LABELS
; ============================

.definelabel FreeROM, 0x087E4000

.definelabel DoorLockControlByte, 0x030078A0
.definelabel DoorLockSFXControl, 0x030078A3
.definelabel ItemAwardControlByte, 0x030078A8
.definelabel HealCounter, 0x030078A9
.definelabel DoorLock_ControlPanel, 0x030078B0

.definelabel ScreenModifier, 0x030023D8
.definelabel Max_Health_EW, 0x02005580
.definelabel Kirby_Health_EW, 0x02005588
.definelabel LifeCounter_EW, 0x02007D48

.definelabel Pos_Update_Hook_Start, 0x08026266
.definelabel Kirby_Xpos_IW, 0x030023CC
.definelabel Kirby_Ypos_IW, 0x03002388

.definelabel Life_Change_Hook_Start, 0x08009E6A
.definelabel Life_Change_Fun_End, 0x08009EAA

.definelabel Pickup_Handler_Skip_Start, 0x0806A16E
.definelabel Pickup_Handler_Skip_End, 0x0806A250

.definelabel Door_Handler_Hook, 0x08024E4C
.definelabel DoorHandlerEnd, 0x08025008 
.definelabel DoorHandlerStart, 0x08024E56 
.definelabel DoorID, 0x02000030

.definelabel WorldLevel_Modifier, 0x030023EC


;All functions below end with bx rN, so set lr before calling them
.definelabel Heal_Tomato_Start, 0x080B429C ;no input
.definelabel Change_Lives_Start, 0x08009E60 ;r0 = lives to add (1). r1 = player number (0)
.definelabel Make_Invincible_Start, 0x0803E1B8 ;r0 = player value to alter? (5). r1, r2 uncertain use, but should be 0
.definelabel Change_Music_Start, 0x08003110 ;r0 = ID of music track (NOT the sound test Number)
.definelabel Play_SFX_Start, 0x080031B8 ;r0 = Number of SFX in Sound test + 100

; ============================
;ROM HEADER REPLACEMENT FOR VALIDATION
; ============================
.org 0x080000A0
.ascii "APR KIRBY DX"   ;APR - ArchiPelago Randomizer



; ============================
;HOOKS
; ============================

;Hook to all code that needs to run "every frame"
.org Pos_Update_Hook_Start
    ldr r2, =FreeROM_ClientCheck+1
    bx r2
    .pool 
;The function we are totally replacing starts with the X position to update in r0, Y in r1
;It has no push/pop usage except for a standard bx lr at the end, so keep track of lr

;Hook the puckup handler to skip all behaviour except setting the collection flag and unloading the entity (probably what the last function does...)
;This disables the usual behavior of all pickup items, including the Arena rewards. Hence, Arenas now MUST be checks
.org Pickup_Handler_Skip_Start
    b Pickup_Handler_Skip_End

;Hook the door handler function at the moment it changes 0x0200 0030 to 0xFF
.org Door_Handler_Hook
    ;Need to ldr and use bx because it's too far for b. Also +1 to keep the interpreter in thumb mode, or something
    ldr r2, =FreeROM_DoorLock+1 ;r2 should be doing nothing here
    bx r2
    .pool 



; ============================
; CUSTOM CODE
; ============================
.org FreeROM
.area 0x4000 ;make it bigger if we need, I guess
FreeROM_ClientCheck:
    push {r0, r1, lr} ;Store these from the original position update function

    ;Manage the Door SFX control byte
    ldr r2, =DoorLockSFXControl
    ldrb r0,[r2]
    cmp r0, #0x0 ;If the value is 0, do nothing. Else, decrement the value by 1. The SFX will only play again once the value is 0
    beq @@Continue_Client_Check_1
    sub r0, r0, #1
    strb r0, [r2]

@@Continue_Client_Check_1:
    ;Check control byte for what item it is, then the Screen Modifier to see if now is a good time to award the item
    ldr r2, =ScreenModifier
    ldrb r0,[r2]
    cmp r0, #0x8 ;Normal level or Boss
    beq @@Continue_Client_Check_2
    cmp r0, #0x13 ;Arena
    beq @@Continue_Client_Check_2
    b @@MakeUp_and_Resume_OGFunction ;Kirby is not in a level or arena, nothing happens

@@Continue_Client_Check_2:
    ldr r2, =ItemAwardControlByte
    ldrb r0,[r2]
    cmp r0, #0x0
    beq @@MakeUp_and_Resume_OGFunction ;Control byte 0, do nothing

    ;Clear the control byte
    mov r1, #0x0
    strb r1, [r2]

    ;Switch block for each item case
    cmp r0, #0x1
    beq @@Finally_Call_Heal;Control byte 1 = 1 HP Segment
    cmp r0, #0x2
    beq @@Set_Heal_SFX ;Control byte 2 = Healing Item (added to bank, play SFX only)
    cmp r0, #0x3
    beq @@Change_Lives ;Control byte 3 = 1up
    cmp r0, #0x4
    beq @@Make_Invincible ;Control byte 4 = Candy
    cmp r0, #0x5
    beq @@Set_Star_Rod_SFX ;Control byte 5 = Star Rod
    cmp r0, #0x6
    beq @@Set_Ability_SFX ;Control byte 6 = Copy Ability Unlock
    cmp r0, #0x7
    beq @@Set_Vitality_SFX ;Control byte 7 = Vitality Unlock
    cmp r0, #0x8
    beq @@Set_DoorUnlock_SFX ;Control byte 8 = Door Key Unlock

@@Finally_Call_Heal:
    mov r0, #0x1
    ;Assign custom code location to the lr to get correct jumpback (quasi-bl). Though, I'm not entirely sure this callback ever gets called back
    ldr r1, =@@MakeUp_and_Resume_OGFunction+1 ;Keep healing if the counter isn't 0 (assuming this is ever even called back)
    mov lr, r1
    ldr r3, =Heal_Tomato_Start+1 
    bx r3

@@Set_Heal_SFX:
    ;Assign custom code location to the lr to get correct jumpback (quasi-bl)
    ldr r1, =@@MakeUp_and_Resume_OGFunction+1
    mov lr, r1
    ;Set r0 to correct SFX value
    mov r0, #0x79
    ;Call SFX function
    b @@Call_Play_SFX

@@Set_Star_Rod_SFX:
    ;Assign custom code location to the lr to get correct jumpback (quasi-bl)
    ldr r1, =@@MakeUp_and_Resume_OGFunction+1
    mov lr, r1
    ;Set r0 to correct SFX value
    mov r0, #0x87
    ;Call SFX function
    b @@Call_Play_SFX

@@Set_Ability_SFX:
    ;Assign custom code location to the lr to get correct jumpback (quasi-bl)
    ldr r1, =@@MakeUp_and_Resume_OGFunction+1
    mov lr, r1
    ;Set r0 to correct SFX value
    mov r0, #0x08
    ;Call SFX function
    b @@Call_Play_SFX

@@Set_Vitality_SFX:
    ;Assign custom code location to the lr to get correct jumpback (quasi-bl)
    ldr r1, =@@MakeUp_and_Resume_OGFunction+1
    mov lr, r1
    ;Set r0 to correct SFX value
    mov r0, #0x84
    ;Call SFX function
    b @@Call_Play_SFX

@@Set_DoorUnlock_SFX:
    ;Assign custom code location to the lr to get correct jumpback (quasi-bl)
    ldr r1, =@@MakeUp_and_Resume_OGFunction+1
    mov lr, r1
    ;Set r0 to correct SFX value
    mov r0, #0x7A
    ;Call SFX function
    b @@Call_Play_SFX

@@Call_Play_SFX:
    add r0, #0x64
    ldr r3, =Play_SFX_Start+1 
    bx r3

@@Change_Lives:
    ;Assign custom code location to the lr to get correct jumpback (quasi-bl)
    ;Note that because we are going to actually modify the life counter, this is not the same as other "pure SFX" items
    ldr r1, =@@Change_Lives_Post_LifeSFX+1
    mov lr, r1
    ;Call SFX function with the 1up SFX
    mov r0, #0x78
    b @@Call_Play_SFX

@@Change_Lives_Post_LifeSFX:
    ;Put lr on the stack again because the last function "used up" our callback
    ldr r1, =@@MakeUp_and_Resume_OGFunction+1
    mov lr, r1
    ;prep and do the change lives function
    mov r0, #0x1 ;lives to add = 1
    mov r1, #0x0 ;player number = 0 (player 1)
    ldr r3, =Change_Lives_Start+1 
    bx r3 
    b @@MakeUp_and_Resume_OGFunction

@@Make_Invincible:
    ;Assign custom code location to the lr to get correct jumpback (quasi-bl)
    ldr r1, =@@Make_Invincible_Post_Music+1
    mov lr, r1
    ;Before calling the make invincible function, call the music change function to trigger the invincibility theme
    mov r0, #0x13 ;Move ID of invincibility theme to r0
    ldr r3, =Change_Music_Start+1 
    bx r3
@@Make_Invincible_Post_Music:
    ;Put lr on the stack again because the last function "used up" our callback
    ldr r1, =@@MakeUp_and_Resume_OGFunction+1
    mov lr, r1
    ;Prep and Do the Make Invincible Call 
    mov r0, #0x5 ;which sub-function to call (5 as determined by debugging)
    mov r1, #0x0 ;no clue 1 
    mov r2, #0x0 ;...and no clue 2
    ldr r3, =Make_Invincible_Start+1 
    bx r3 
    b @@MakeUp_and_Resume_OGFunction

@@MakeUp_and_Resume_OGFunction:
    pop {r0, r1} ;Get these back from the stack storage earlier
    ;Update kirby X and Y position in IW from r0/r1 exactly how the OG function did it
    ldr r2, =Kirby_Xpos_IW
    strh r0, [r2]
    ldr r0, =Kirby_Ypos_IW
    strh r1, [r0]
    pop {r0} ;this is the original lr. Note that you can't pop {lr}; this is an invalid instruction.
    mov lr, r0
    bx lr ;jump back to whatever called the OG function    

    .pool ;pretty sure each block needs its own .pool


FreeROM_DoorLock:
    ;Fulfill the OG function: move r0 > r5 and r1 > r6
    add r5,r0,#0x0
    add r6,r1,#0x0

    ;fulfill the OG function: write 0xFF to the door id address
    ldr r1, =DoorID
    mov r0, #0xFF
    strb r0,[r1]

    ;Read Kirby's coordinates, floor round to nearest block, and combine in a single halfword
    ldr r1, =Kirby_Xpos_IW
    ldrh r0, [r1]
    lsr r2, r0, 4
    ldr r1, =Kirby_Ypos_IW
    ldrh r0, [r1]
    lsr r0, r0, 4
    lsl r3, r0, 8
    add r3, r2, r3 ;halfword code for kirby's current coords now set at r3

    ;Set index pointer r2 to the correct spot in the coordinate table based on the world number
    ;This table is 1 halfword for each door, each world taking up 32 (0x20) bytes
    ldr r1, =WorldLevel_Modifier
    ldrb r0, [r1]
    lsl r0, r0, 5 ;
    ldr r1, =@@Door_XY_Table
    add r2, r1, r0

    ;Iterate counter r1 through the entire world's door coords, stopping when we get a match
    mov r1, #0x0
@@Door_Coord_Loop:
    ldrh r0, [r2, r1]
    cmp r0, r3
    beq @@Door_Index_Found
    ;Since the value in the table is the LEFT block of the door, try adding 0x1 to the value and check that also
    add r0, r0, #0x1
    cmp r0, r3
    beq @@Door_Index_Found
    add r1, r1, #0x2 ;inc counter by 2 (halfword byte size)
    cmp r1, #0x20 ;check if overflow (32 bytes / 16 halfwords)
    bhi @@GoToDoorHandlerStart ;overflowed table without finding a match; just let kirby through the door by default
    b @@Door_Coord_Loop

    ;Read the bit corresponding to the located door from the correct control panel address
    ;In this control panel, each world gets 16 bits (2 bytes)
@@Door_Index_Found:
    lsr r1, #0x1 ; divide r1 by 2 since we were counting by 2 before
    ldr r3, =WorldLevel_Modifier
    ldrb r2, [r3]
    lsl r2, r2, 1
    ldr r3, =DoorLock_ControlPanel
    ldrh r2, [r3, r2] ;relavent bitarray halfword for the world now in r2
    ;Following code to test 1 bit given by AI
    mov r0, #0x1
    cmp r1, #0x0
    beq @@door_bit_set
@@door_shift_loop: ; loop lsl r0 "r1 times", since lsl with a register as the shift amount is invalid
    lsl r0, r0, #0x1
    sub r1, #0x1
    cmp r1, #0x0
    bne @@door_shift_loop
@@door_bit_set:
    tst r2, r0 ;does a bitwise AND, True/False if any bit is 1, apparently
    beq @@GoToDoorHandlerStart ; Bit is 0, door is UNLOCKED. Play out the function as normal
    ;Otherwise, check the Lock SFX

    ;Check the Door Lock Control Panel Var so that the SFX doesn't play EVERY FRAME
    ldr r1, =DoorLockSFXControl
    ldrb r0,[r1]
    cmp r0, #0x0 ;If the SFX byte is anything other than zero, skip playing the SFX
    bne @@Continue_Post_LockSFX
    mov r0, #0x1E ;Set the refresh timer now that the SFX will be played 30 frames = 1/2 second
    strb r0, [r1]

    ;Play a SFX if the door is locked to cue the player
    ldr r1, =@@Continue_Post_LockSFX+1
    mov lr, r1
    ;Call SFX function with a certain SFX that sounds like banging on a door (the stone ability "thump")
    mov r0, #0x89
    add r0, #0x64
    ldr r3, =Play_SFX_Start+1 
    bx r3

@@Continue_Post_LockSFX:
    mov r2,#0x0 ;fulfill the OG function: set r2 to 0 just in case
    mov r0,#0x0 ;If 1, set r0 to 0 (door handler output) and jump to the end of the door handler function
    ldr r1, =DoorHandlerEnd+1 ;+1, see note above
    bx r1

@@GoToDoorHandlerStart:
    mov r2,#0x0 ;fulfill the OG function: set r2 to 0 just in case
    ldr r1, =DoorHandlerStart+1
    bx r1

@@Door_XY_Table:
    ;;Because of little-endian-ness, I'm pretty sure these must be listed out as YYXX (since we made Y the higher digits)
    ;;World 1
    .halfword 0x0000 ;0=prev
    .halfword 0x1006 ;1=level 1
    .halfword 0x120E ;2=level 2
    .halfword 0x0C13 ;3=level 3
    .halfword 0x0F18 ;4=level 4
    .halfword 0x0000 ;5=level 5
    .halfword 0x0000 ;6=level 6
    .halfword 0x0D0A ;7=Bomb Rally
    .halfword 0x0000 ;8=Air Grind
    .halfword 0x0000 ;9=Quick Draw
    .halfword 0x0000 ;A=Arena
    .halfword 0x090E ;B=Museum
    .halfword 0x0000 ;C=None
    .halfword 0x0000 ;D=None
    .halfword 0x031B ;E=Warp Station
    .halfword 0x071B ;F=Boss/next

    ;;World 2
    .halfword 0x0000 ;0=prev
    .halfword 0x0000 ;1=level 1
    .halfword 0x0000 ;2=level 2
    .halfword 0x0000 ;3=level 3
    .halfword 0x0000 ;4=level 4
    .halfword 0x0000 ;5=level 5
    .halfword 0x0000 ;6=level 6
    .halfword 0x0E15 ;7=Bomb Rally
    .halfword 0x0606 ;8=Air Grind
    .halfword 0x0000 ;9=Quick Draw
    .halfword 0x0000 ;A=Arena
    .halfword 0x0417 ;B=Museum
    .halfword 0x0000 ;C=None
    .halfword 0x0000 ;D=None
    .halfword 0x0D28 ;E=Warp Station
    .halfword 0x062B ;F=Boss/next

    ;;World 3
    .halfword 0x0000 ;0=prev
    .halfword 0x0000 ;1=level 1
    .halfword 0x0000 ;2=level 2
    .halfword 0x0000 ;3=level 3
    .halfword 0x0000 ;4=level 4
    .halfword 0x0000 ;5=level 5
    .halfword 0x0000 ;6=level 6
    .halfword 0x0000 ;7=Bomb Rally
    .halfword 0x0D02 ;8=Air Grind
    .halfword 0x120C ;9=Quick Draw
    .halfword 0x280C ;A=Arena
    .halfword 0x1B02 ;B=Museum
    .halfword 0x0000 ;C=None
    .halfword 0x0000 ;D=None
    .halfword 0x090C ;E=Warp Station
    .halfword 0x0607 ;F=Boss/next

    ;;World 4
    .halfword 0x0000 ;0=prev
    .halfword 0x0000 ;1=level 1
    .halfword 0x0000 ;2=level 2
    .halfword 0x0000 ;3=level 3
    .halfword 0x0000 ;4=level 4
    .halfword 0x0000 ;5=level 5
    .halfword 0x0000 ;6=level 6
    .halfword 0x0803 ;7=Bomb Rally
    .halfword 0x0000 ;8=Air Grind
    .halfword 0x030C ;9=Quick Draw
    .halfword 0x0F1C ;A=Arena
    .halfword 0x0E11 ;B=Museum
    .halfword 0x0000 ;C=None
    .halfword 0x0000 ;D=None
    .halfword 0x082B ;E=Warp Station
    .halfword 0x042B ;F=Boss/next

    ;;World 5
    .halfword 0x0000 ;0=prev
    .halfword 0x0000 ;1=level 1
    .halfword 0x0000 ;2=level 2
    .halfword 0x0000 ;3=level 3
    .halfword 0x0000 ;4=level 4
    .halfword 0x0000 ;5=level 5
    .halfword 0x0000 ;6=level 6
    .halfword 0x0C02 ;7=Bomb Rally
    .halfword 0x100A ;8=Air Grind
    .halfword 0x0424 ;9=Quick Draw
    .halfword 0x0E1A ;A=Arena
    .halfword 0x0415 ;B=Museum
    .halfword 0x0000 ;C=None
    .halfword 0x0000 ;D=None
    .halfword 0x0D2B ;E=Warp Station
    .halfword 0x082A ;F=Boss/next

    ;;World 6
    .halfword 0x0000 ;0=prev
    .halfword 0x0000 ;1=level 1
    .halfword 0x0000 ;2=level 2
    .halfword 0x0000 ;3=level 3
    .halfword 0x0000 ;4=level 4
    .halfword 0x0000 ;5=level 5
    .halfword 0x0000 ;6=level 6
    .halfword 0x1412 ;7=Bomb Rally
    .halfword 0x0616 ;8=Air Grind
    .halfword 0x1024 ;9=Quick Draw
    .halfword 0x030D ;A=Arena
    .halfword 0x0B07 ;B=Museum
    .halfword 0x0000 ;C=None
    .halfword 0x0000 ;D=None
    .halfword 0x0326 ;E=Warp Station
    .halfword 0x082C ;F=Boss/next

    ;;World 7
    .halfword 0x0000 ;0=prev
    .halfword 0x0000 ;1=level 1
    .halfword 0x0000 ;2=level 2
    .halfword 0x0000 ;3=level 3
    .halfword 0x0000 ;4=level 4
    .halfword 0x0000 ;5=level 5
    .halfword 0x0000 ;6=level 6
    .halfword 0x0605 ;7=Bomb Rally
    .halfword 0x0000 ;8=Air Grind
    .halfword 0x0000 ;9=Quick Draw
    .halfword 0x0000 ;A=Arena
    .halfword 0x0000 ;B=Museum
    .halfword 0x0000 ;C=None
    .halfword 0x0000 ;D=None
    .halfword 0x031B ;E=Warp Station
    .halfword 0x050F ;F=Boss/next

    ;this .pool instruction is required to correctly parse the ldr instructions when the value is 32 bits 
    ;(normally instructions are 16 bits)
    .pool 

.endarea

.close