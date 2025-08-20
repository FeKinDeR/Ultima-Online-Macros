# SampireBot for Doom Gauntlet  
# Made by KinDeR           
 
try:
    import requests
except ModuleNotFoundError:
    print("No 'requests' module found. Install it using 'pip install requests' ")
    exit()
try:
    from discord_webhook import DiscordWebhook, DiscordEmbed
except ModuleNotFoundError:
    print("No 'discord_webhook' module found. Install it using 'pip install discord_webhook' ")
    exit()

try:
    import PySimpleGUI as sg
except ModuleNotFoundError:
    print("No 'PySimpleGUI' module found. Install it using 'pip install PySimpleGUI' to access the GUI interface.")
    sg = None 
 
try:
    from doom_config import *
except ModuleNotFoundError:
    print("No 'doom-config' module found.")
    exit()
   
try:
    from autoloot import *
except ModuleNotFoundError:
    print("No 'autoloot.py' module found.")                
    
    
URL_API = ''

from datetime import datetime, timedelta
from time import sleep
from py_stealth import *
import json
from pprint import pprint
import re
import threading                    
import ctypes

#################################################################################################################################################
############# **DO NOT CHANGE**  ############ **DO NOT CHANGE ** ############## **DO NOT CHANGE**  ############ **DO NOT CHANGE ** ##############
############# **DO NOT CHANGE**  ############ **DO NOT CHANGE ** ############## **DO NOT CHANGE**  ############ **DO NOT CHANGE ** ##############
# ==============================================================================================================================================#
#                                                               GLOBAL VARIABLES                                                                #
# ==============================================================================================================================================#
WAV_AFK  =  StealthPath() + 'Scripts\afk.wav'                                                    # Sound for afk gump
WAIT_TIME = 500                                                                                  # Default Wait Time
WAIT_LAG_TIME = 10000                                                                            # Default Wait Lag Time
TITHING_POINTS_WARNLEVEL = 1000                                                                  # Default amount of low TITHING points to warn
TITHING_POINTS_ABORTLEVEL = 150                                                                  # Default amount of low TITHING points to abort
TITHING_COOLDOWN_IN_MINUTES = 1                                                                  # Default Cooldown time for check TITHING points 
timer_evasion = datetime.now()- timedelta(seconds=20)
timer_start_boss = datetime.now()
timer_apple = datetime.now()- timedelta(seconds=120)
last_tithingpoints_check = datetime.now() - timedelta(minutes=TITHING_COOLDOWN_IN_MINUTES)
timer_deaths_in_a_row_check = datetime.now() - timedelta(minutes=5)
timer_gm_check = datetime.now() - timedelta(seconds=5)
timer_dispel_mobs = datetime.now()
deaths_in_a_row = 0

#################################################################################################################################################
############# **DO NOT CHANGE**  ############ **DO NOT CHANGE ** ############## **DO NOT CHANGE**  ############ **DO NOT CHANGE ** ##############
############# **DO NOT CHANGE**  ############ **DO NOT CHANGE ** ############## **DO NOT CHANGE**  ############ **DO NOT CHANGE ** ##############
#Item type/Qtd
ITEMS_TO_BUY = {
    0x0F8A: 100,    #pigiron
    0x0F78: 1,      #batwing
    0x0F8E: 1,      #noxcrystal
}

#################################################################################################################################################
############# **DO NOT CHANGE**  ############ **DO NOT CHANGE ** ############## **DO NOT CHANGE**  ############ **DO NOT CHANGE ** ##############
############# **DO NOT CHANGE**  ############ **DO NOT CHANGE ** ############## **DO NOT CHANGE**  ############ **DO NOT CHANGE ** ##############
PLAYER_TYPES = [0x029A, 0x029B, 0x0190, 0x0191, 0x025d, 0x025e, 0x0192, 0x0193, 0x025f, 0x0260, 0x02ea, 0x02ec, 0x02ed, 0x084, 0x0f6, 0x019, 0x0db, 0x051, 0x07a, 0x02ee, 0x02e8, 0x02e9, 0x02eb, 0x0117, 0x0116, 0x0115]
BossNames = ["Darknight Creeper","Fleshrenderer","Impaler","Shadow Knight","Abyssmal Horror","demon knight"] 
MOB_TYPES = [0x003A, 0x139, 0x13b, 0x132, 0x137, 0x138, 0x13e]
BONE_TYPES = [0x0ECA, 0x0ECB, 0x0ECC, 0x0ECD, 0x0ECE, 0x0ECF, 0x0ED0, 0x0ED1, 0x0ED2, 0x0ED3, 0x0ED4]
# TRAPS! #hole: 0x1b71 | #gas trap south: 0x1147 | #gas trap north: 0x113C | #trap red: 0x11ac | #triple red trap: 0x11a0 0x119a | #mushroom :0x1125 | #trap white 0x11b1 
TRAPS_TYPES = [0x1b71, 0x1147, 0x113C, 0x11ac, 0x11a0, 0x119a, 0x1125, 0x11b1]
# a ghoul - 0x99 #a bone knight - 0x39 #a lich lord - 0x4f #a rotting corpse - 0x9b
DISPEL_TYPES = [0x99, 0x9a, 0x9b, 0x1a, 0x93, 0x39, 0x4f, 0x18]

#################################################################################################################################################
############################################# ** --->>    ARTIFACTS RARITY 11    << -- ** #######################################################
############################################# ** These are the artifacts to be insured ** #######################################################
# ----------------------------------------------------------------------- #
INSURE_TYPES = [0x13c7, 0x108a, 0x1547, 0x1412, 0x13b2, 0x1086, 0x1545, 0x143b, 0xf4d, 0x13db, 0x1413, 0x1718, 0x1b78, 0x13be, 0x1086, 0x13d2, 0x1b76, 0x26BB, 0x13eb, 0xe89, 0x1405, 0x144e, 0xf4b, 0x1549, 0x1415, 0x1451, 0x1400, 0x13bf, 0x13b1, 0x26c0, 0x1406, 0x13FF, 0x1F06, 0x1F09, 0x0DF0, 0x13C6, 0x13CC, 0x13CD, 0x13CB]

#################################################################################################################################################
############# **DO NOT CHANGE**  ############ **DO NOT CHANGE ** ############## **DO NOT CHANGE**  ############ **DO NOT CHANGE ** ##############
############# **DO NOT CHANGE**  ############ **DO NOT CHANGE ** ############## **DO NOT CHANGE**  ############ **DO NOT CHANGE ** ##############
# ==============================================================================================================================================#
#                                                                DRESSING UTILS                                                                 #
# ==============================================================================================================================================#

# Defining global variables for reequip suit
ARMOR_ITEM_LIST = []
ARMOR_ITEM_LAYERS  = [HatLayer(),NeckLayer(),ArmsLayer(),TorsoLayer(),PantsLayer(),GlovesLayer(),LhandLayer(),RingLayer(),BraceLayer(),RobeLayer(),ShoesLayer(),TalismanLayer(),CloakLayer(),EarLayer(),RhandLayer(),WaistLayer(),TorsoHLayer(),ShirtLayer(),EggsLayer()]

def save_set():
    global ARMOR_ITEM_LIST
    hat = neck = sleeves = chest = legs = gloves = lhand = ring = brace = robe = shoes = talisman = cloak = ear = rhand = waist = torsoH = shirt = eggs = 0
    ARMOR_ITEM_LIST = [hat,neck,sleeves,chest,legs,gloves,lhand,ring,brace,robe,shoes,talisman,cloak,ear,rhand,waist,torsoH,shirt,eggs]
     
    for layer_i in range(len(ARMOR_ITEM_LAYERS)):
        if ObjAtLayer(ARMOR_ITEM_LAYERS[layer_i]) > 0:
            ARMOR_ITEM_LIST[layer_i] = ObjAtLayer(ARMOR_ITEM_LAYERS[layer_i]) 
    return                                                                                                                                                                                                                                                                                                 
                      
def dress_lrc_set():
    for key, val in LRC_SET.items():
        if val != 0:    
            eqp_found = False
            if GetCliloc(val) == '':
                ClickOnObject(val)
                Wait(500)
                
            if FindType(GetType(val),Backpack()):
                for item in GetFindedList():
                    if item == val:  
                        eqp_found = True
             
            if not eqp_found:
                continue               
            while (ObjAtLayer(key()) != val):
                # if item to be equiped is a two-hand weapon, we must clear both hands to equip it
                #print(GetCliloc(val))
                if 'two-handed' in GetCliloc(val):
                    if key() == LhandLayer() or key() == RhandLayer(): 
                        if ObjAtLayer(LhandLayer()) != 0:
                            if UnEquip(LhandLayer()):
                                wait_lag(1000) 
                        if ObjAtLayer(RhandLayer()) != 0:
                            if UnEquip(RhandLayer()):
                                wait_lag(1000) 
                                
                # if item is one-handed must check if a two-handed weap is equipped or simply unequip rhand
                elif 'one-handed' in GetCliloc(val): 
                    # check if two-handed is equiped, unequip it
                    if 'two-handed' in GetCliloc(ObjAtLayer(LhandLayer())):
                        if UnEquip(LhandLayer()):
                            wait_lag(1000)  
                    # else unequip right hand
                    elif ObjAtLayer(RhandLayer()) != 0:
                        if UnEquip(RhandLayer()):
                            wait_lag(1000) 
                            
                                    
                elif (ObjAtLayer(key()) != val):
                    if UnEquip(key()):
                        wait_lag(1000)
                                 
                print('EQUIPING. Item: '  + GetCliloc(val).split('|')[0] )
                if not Equip(key(),val):          
                    pass
                else:                                                             
                    wait_lag(1000)

def dress_main_set():
    for j in range(len(ARMOR_ITEM_LAYERS)):  
        while (ObjAtLayer(ARMOR_ITEM_LAYERS[j]) != ARMOR_ITEM_LIST[j]):
            # if item to be equiped is a two-hand weapon, we must clear both hands to equip it
            if 'two-handed' in GetCliloc(ARMOR_ITEM_LIST[j]):
                if ARMOR_ITEM_LAYERS[j] == LhandLayer() or ARMOR_ITEM_LAYERS[j] == RhandLayer():
                    if ObjAtLayer(LhandLayer()) != 0:
                        if UnEquip(LhandLayer()):
                            wait_lag(1000)           
                    if ObjAtLayer(RhandLayer()) != 0:
                        if UnEquip(RhandLayer()):
                            wait_lag(1000)
            # if item is one-handed must check if a two-handed weap is equipped or simply unequip rhand
            elif 'one-handed' in GetCliloc(ARMOR_ITEM_LIST[j]): 
                # check if two-handed is equiped
                if 'two-handed' in GetCliloc(ObjAtLayer(LhandLayer())):
                    if UnEquip(LhandLayer()):
                        wait_lag(1000)  
                # else unequip right hand
                elif ObjAtLayer(RhandLayer()) != 0:
                    if UnEquip(RhandLayer()):
                        wait_lag(1000)  
            # else unequip the item on that layer
            elif ObjAtLayer(ARMOR_ITEM_LAYERS[j]) != 0:
                # unequip item
                if UnEquip(ARMOR_ITEM_LAYERS[j]):
                    wait_lag(1000) 
            print('EQUIPING. Item: '  + GetCliloc(ARMOR_ITEM_LIST[j]).split('|')[0] )
            if not Equip(ARMOR_ITEM_LAYERS[j], ARMOR_ITEM_LIST[j]):
                pass
            else:                
                wait_lag(1000) 
    return

def undress_all():
    for j in range(len(ARMOR_ITEM_LAYERS)):                                                                                                      
        print('UNEquiping Item: ' + GetCliloc(ARMOR_ITEM_LIST[j]).split('|')[0] )
        if UnEquip(ARMOR_ITEM_LAYERS[j]):
            Wait(1000)  
    return 
    
def get_pieces_together():
    if FindTypesArrayEx(ITEMS_TO_BUY ,[0xFFFF],[Backpack()],False): 
        founds = GetFindedList()
        if len(founds) <= len(ITEMS_TO_BUY):
            return            
        for found in founds: 
            if GetType(found) in ITEMS_TO_BUY:     
                ClientPrintEx(Self(), 66, 1, 'moving..' + GetTooltip(found))   
                MoveItem(found, -1, Backpack(), 0, 0, 0)   
                Wait(600)       

def security_equip_weapon():
    # if disconnected or hand layers are not empty
    if not Connected() or ObjAtLayer(RhandLayer()) != 0 or (ObjAtLayer(LhandLayer()) != 0 and 'two-handed' in GetCliloc(ObjAtLayer(LhandLayer()))):    
        return                                        
    if 'two-handed' in GetCliloc(QSTAFF_AUX) or 'two-handed' in GetCliloc(DEMON_SLAYER) or 'two-handed' in GetCliloc(UNDEAD_SLAYER):   
        layer = LhandLayer()                                                                                                      
    else:
        layer = RhandLayer()                                                                                                      
               
    if (ObjAtLayer(layer) == 0): 
        Equip(LhandLayer(), QSTAFF_AUX)
        Wait(1000)
        if (ObjAtLayer(layer) == 0): 
            Equip(LhandLayer(), DEMON_SLAYER)
            Wait(1000)    
            if (ObjAtLayer(layer) == 0):  
                Equip(LhandLayer(), UNDEAD_SLAYER)
                Wait(1000)
                  
    if (ObjAtLayer(LhandLayer()) == 0 and ObjAtLayer(RhandLayer()) == 0):      
        print('SECURITY BREAK!! DID NOT EQUIP THE WEAPON!!')  
        go_to_safe_and_logout()

def equip_weapon(weap):
    count = 0
    # if layer is two-hand (left or right) must clear both hands to equip a two-hand weapon  
    if 'two-handed' in GetCliloc(weap):
        while (ObjAtLayer(LhandLayer()) != weap): 
            if ObjAtLayer(LhandLayer()) != 0:
                if UnEquip(LhandLayer()):
                    wait_lag(1000) 
            if ObjAtLayer(RhandLayer()) != 0:
                if UnEquip(RhandLayer()):
                    wait_lag(1000)    
            Equip(LhandLayer(), weap)
            Wait(1000)    
            count = count + 1
            if count > 5:
                print('***-----SECURITY BREAK!! DID NOT EQUIP THE WEAPON!!')
                break    
                
    else:
        # try to equip a one hand weapon and a shield if it exists
        while (ObjAtLayer(RhandLayer()) != weap):
            if 'two-handed' in GetCliloc(ObjAtLayer(LhandLayer())) or 'two-handed' in GetCliloc(ObjAtLayer(RhandLayer())):     
                if ObjAtLayer(LhandLayer()) != 0:
                    if UnEquip(LhandLayer()):
                        wait_lag(1000) 
                if ObjAtLayer(RhandLayer()) != 0:
                    if UnEquip(RhandLayer()):
                        wait_lag(1000)                  
            elif UnEquip(RhandLayer()):
                wait_lag(1000)
            Equip(RhandLayer(), weap)
            Wait(1000)
            Equip(LhandLayer(), SHIELD)
            Wait(1000) 
             
            count = count + 1
            if count > 5:
                print('SECURITY BREAK!! DID NOT EQUIP THE WEAPON!!')
                break   

#################################################################################################################################################
############# **DO NOT CHANGE**  ############ **DO NOT CHANGE ** ############## **DO NOT CHANGE**  ############ **DO NOT CHANGE ** ##############
############# **DO NOT CHANGE**  ############ **DO NOT CHANGE ** ############## **DO NOT CHANGE**  ############ **DO NOT CHANGE ** ##############
# ==============================================================================================================================================#
#                                                              MOVING UTILS                                                                     #
# ==============================================================================================================================================#
def move_thru_doors(Xdst, Ydst, Zdst, AccuracyXY, AccuracyZ, Running, _beforeStepCallback = None):
    def debug(msg):
        if MoveXYZ.debug:
            AddToSystemJournal('MoveXYZ: ' + msg)

    def step(dir, run):
        while 42:  # while True
            step = StepQ(dir, run)
            if step == -2 or step >= 0:                                                                                                                     
                return step >= 0

    if not hasattr(MoveXYZ, 'debug'):
        MoveXYZ.debug = False

    find_path = True
    while 42:  # while True     
        # pause while not connected
        while not Connected():
            Wait(1000)          
        if is_bufficon_activated('Paralyze') or (not Dead() and GetStam(Self()) < 3):
            Wait(200)
            continue
        # try to find a path if required
        if find_path:
            find_path = False   
            #ClientPrintEx(Self(),55,0,'111getpatharray!!!!')
            path = GetPathArray3D(PredictedX(), PredictedY(), PredictedZ(),
                                  Xdst, Ydst, Zdst,
                                  WorldNum(), AccuracyXY, AccuracyZ, Running)
            #ClientPrintEx(Self(),55,0,'222getpatharray!!!!')
            # there is no path to a target location
            if len(path) <= 0:
                debug('There is no path to a target location.')
                return False
            debug('Path found. Length = ' + str(len(path)))
        # check path passability for a few steps
        cx, cy, cz = PredictedX(), PredictedY(), PredictedZ()
        for i in range(3):
            try:
                x, y, z = path[i]
                if IsWorldCellPassable(cx, cy, cz, x, y, WorldNum()):
                    cx, cy, cz = x, y, z
                else:
                    debug('Point ({0}, {1}, {2}) is not passable.'.format(x, y, z))
                    find_path = True
                    break
            except IndexError:
                break
        if find_path:
            continue
        # stamina check   
        if not Dead() and Stam() < GetMoveCheckStamina():
            Wait(100)
        # lets walk :)
        mx, my = PredictedX(), PredictedY()
        x, y, z = path.pop(0)
        dx = mx - x
        dy = my - y
        dir = CalcDir(mx, my, x, y)
        # if something wrong
        if (dx == 0 and dy == 0) or (abs(dx) > 1 or abs(dy) > 1) or dir == 100:
            debug('dx = {0}, dy = {1}, dir = {2}'.format(dx, dy, dir))
            find_path = True
            continue
        # try to turn if required
        if PredictedDirection() != dir:  
            #ClientPrintEx(Self(),75,0,'here')
            _beforeStepCallback()
            if not step(dir, Running):
                find_path = True
                continue
        # try to do a step                   
        #ClientPrintEx(Self(),25,0,'walking')
        _beforeStepCallback()
        if not step(dir, Running):
            find_path = True
            continue
        # looks like it is done
        if not path:
            mx, my = PredictedX(), PredictedY()
            # ensure this
            if abs(mx - Xdst) <= AccuracyXY and abs(my - Ydst) <= AccuracyXY:            
                #print('Location reached!' + str(mx) + ' ' + str(my))
                #print('Location reached!' + str(GetX(Self())) + ' ' + str(GetY(Self())))
                return True
            # nope (
            debug('Wtf? Recompute path.')
            find_path = True          
        #Wait(30)
             
def leave_room(room):
    if GOTOSAFEANDLOGOUT:
        go_to_safe_and_logout()
    return
    print('LeaveROOM '+str(room))
    if room == 1:         
        print('LEAVING SALA 1')
        #NewMoveXY(481,432, False,0,True)    
        #UseObject(0x407A35EB)
        #NewMoveXY(462,433, False,1,True)
        move_thru_doors(462, 433, 0, 0, 4, True, open_doors)
    if room == 2:  
        print('LEAVING SALA 2')
        #NewMoveXY(468,497, False,0,True)
        #UseObject(0x407A35F8)
        #NewMoveXY(469,484, False,1,True)                               
        move_thru_doors(469, 484, 0, 0, 4, True, open_doors)
    if room == 3:  
        print('LEAVING SALA 3')
        #NewMoveXY(409,510, False,0,True)  
        #UseObject(0x407A3605)
        #NewMoveXY(403,451, False,1,True) 
        move_thru_doors(403, 451, 0, 0, 4, True, open_doors)
    if room == 4: 
        print('LEAVING SALA 4')       
        #NewMoveXY(361,483, False,0,True) 
        #UseObject(0x407A3611)
        #NewMoveXY(393,444, False,0,True)  
        move_thru_doors(393, 444, 0, 0, 4, True, open_doors)
    if room == 5: 
        print('LEAVING SALA 5')
        #NewMoveXY(359,429, False,0,True)    
        #UseObject(0x407A361E)
        #NewMoveXY(381,429, False,1,True)    
        #NewMoveXY(391,429, False,0,True)
    if room == 6:        
        print('LEAVING SALA DF')
        #NewMoveXY(423,430, False,1,True) 
        move_thru_doors(423, 430, 0, 0, 4, True, open_doors)
                
def go_to_room(room): 
    global KILL_DF_CENTER
    reached = False     
    if GetGlobal('char','Room') == 'Logout':
        return     
    if GOTOSAFEANDLOGOUT:
        go_to_safe_and_logout()
    tries = 0
    while not reached:   
        ClearBadLocationList()
        if room == 1 or room > 6:
            print('-------------------------------------------------------------') 
            print('----------------- ROOM 1 - Darknight Creeper ----------------')   
            #NewMoveXY(470,428, False,0,True)  
            SetBadLocation(456,424)
            SetBadLocation(456,425)   
            SetBadLocation(456,426)
            SetBadLocation(456,427)    
            SetBadLocation(453,424)
            SetBadLocation(454,424)  
            SetBadLocation(455,424)  
            SetBadLocation(453,424) 
            SetBadLocation(453,423)  
            SetBadLocation(453,422)
            SetBadLocation(459,438)
            SetBadLocation(458,439)
            SetBadLocation(457,440)
            for i in range(458,463):   
                SetBadLocation(i,428)
            move_thru_doors(470, 428, 0, 0, 4, True, open_doors)
            move_steps_direction(2,2)    
            
            if(NewMoveXY(490,452, False,1,True)):
                reached = True   
            else:
                tries = tries + 1
        if room == 2:  
            print('-------------------------------------------------------------') 
            print('----------------- ROOM 2 - Fleshrenderer --------------------')   
            SetBadLocation(479,437)   
            SetBadLocation(479,436) 
            SetBadLocation(479,435)
            SetBadLocation(478,437) 
            SetBadLocation(478,436) 
            SetBadLocation(477,436)      
            for i in range(436,449):  
                SetBadLocation(480, i)   
            for i in range(437,449):  
                SetBadLocation(481, i)
            for i in range(480,485):
                SetBadLocation(i, 440)  
                SetBadLocation(i, 439)   
                SetBadLocation(i-1, 438)    
                SetBadLocation(i-2, 437)
                SetBadLocation(i-2, 436)                    
            move_thru_doors(462, 493, 0, 0, 4, True, open_doors)
            move_steps_direction(2,4)
             
            if(NewMoveXY(477,514, False,1,True)):
                reached = True   
            else:
                tries = tries + 1
        if room == 3:  
            print('-------------------------------------------------------------') 
            print('----------------- ROOM 3 - Impaler --------------------------')  
            SetBadLocation(403,496)
            SetBadLocation(403,495)
            SetBadLocation(404,497) 
            SetBadLocation(470,497) 
            for i in range(470,472):   
                SetBadLocation(i, 498)  
                SetBadLocation(i, 499)
            for i in range(484,493):   
                SetBadLocation(409, i)         
            move_thru_doors(403, 501, 0, 0, 4, True, open_doors) 
            move_steps_direction(2,4)    
            
            if(NewMoveXY(399,533, False,1,True) ):
                reached = True   
            else:
                tries = tries + 1
        if room == 4:   
            print('-------------------------------------------------------------') 
            print('----------------- ROOM 4 - Shadow Knight --------------------')  
            SetBadLocation(407,506)
            SetBadLocation(407,507)
            SetBadLocation(407,508)          
            #NewMoveXY(357,475, False,0,True)
            move_thru_doors(357, 475, 0, 0, 4, True, open_doors) 
            move_steps_direction(2,4)       
                                                                           
            if(NewMoveXY(340,507, False,1,True)   ):
                reached = True   
            else:
                tries = tries + 1
        if room == 5: 
            print('-------------------------------------------------------------') 
            print('----------------- ROOM 5 - Abyssmal Horror ------------------')   
            #NewMoveXY(361,432, False,0,True)
            for i in range(350,359): 
                SetBadLocation(i,479)
                SetBadLocation(i,480) 
                SetBadLocation(i,481)  
            move_thru_doors(361, 432, 0, 0, 4, True, open_doors) 
            move_steps_direction(2,4)                          
            if(NewMoveXY(328,434, False,1,True)):
                reached = True   
            else:
                tries = tries + 1
        if room == 6:       
            print('-------------------------------------------------------------') 
            print('----------------- ROOM 6 - The Dark Father ------------------') 
            if move_thru_doors(413, 429, 0, 0, 4, True, open_doors):
                reached = True   
            else:
                tries = tries + 1
        if tries >= 1:
            return False
    return True

def move_steps_direction(steps,direction):
    d = 0
    while d < steps and steps > 0:
        StepQ(direction,True)
        d += 1
        Wait(50)

def move_to_corner_if_not_there(corner_x = 453, corner_y = 419):
    mx, my = GetX(Self()), GetY(Self()) 
    
    if is_in_danger():
        return False
    
    if (mx != corner_x or my != corner_y): 
        path = GetPathArray3D(PredictedX(), PredictedY(), PredictedZ(), corner_x, corner_y, GetZ(Self()) , WorldNum(), 0, 0, False)         
        # there is no path to a target location
        if len(path) <= 0:
            print('There is no path to a target location. trap on my way?')         
            ClearBadLocationList()
            return False 
        else: 
            for i in range(2):
                try:
                    # lets walk :)
                    x, y, z = path[i]
                    mx, my = PredictedX(), PredictedY()
                    dx = mx - x
                    dy = my - y
                    dir = CalcDir(mx, my, x, y)   
                    StepQ(dir, True)
                    StepQ(dir, True)          
                except IndexError:                                          
                    break
            Wait(1000)
        return True 
    else:
        return False

def approach_helper_bot():
    if (find_helper_bot(find_players(16)) >= 0) and (find_helper_bot(find_players(16)) <= 16):
        list_of_players = find_players(16)
        for player in list_of_players:
            if player in HELPER_BOT_LIST:
                print('Approaching helper bot on ' + str(GetX(player)) + ' ' + str(GetY(player)))
                NewMoveXY(GetX(player),GetY(player), False,0,True)   
                return player
    return None

def go_to_safe_and_logout():
    global deaths_in_a_row
    print('Going to safe room to logout.')
    ClearBadLocationList()  
    move_thru_doors(423, 431, 0, 0, 4, True, open_doors)
    NewMoveXY(423,370, False,1,True)  #Antes de Virar
    NewMoveXY(431,371, False,1,True)  #Começo da Parede
    wait_lag(600)  
    move_steps_direction(3,2)
    wait_lag(600)
    ClearBadLocationList() #Tem q ter esse segundo clearBadLocation se não da pau
    move_steps_direction(55,2) #healer coord!!! 

    if check_low_tithing_points():
        print('Logging you out! Disconnecting! Low on TITHINGPOINTS.') 
        send_discord_message(DISCORD_WEBHOOK,'******** (TTPOINTS) '+ get_user_id(DISCORD_ID) +' Tithing points too low! Char: '+ str(CharName()) +' ********')
    elif (ObjAtLayer(LhandLayer()) == 0): 
        print('Logging you out! Disconnecting! Unarmed.') 
        send_discord_message(DISCORD_WEBHOOK,'******** (NOWEP) '+ get_user_id(DISCORD_ID) +' Cannot equip weapon! Char: '+ str(CharName()) +' ********')
    elif deaths_in_a_row >= 5:    
        send_discord_message(DISCORD_WEBHOOK,'******** (X__X) '+ get_user_id(DISCORD_ID) +' Too many deaths in a row! Char: '+ str(CharName()) +' ********')
    else:
        print('Logging you out! Disconnecting!') 
        send_discord_message(DISCORD_WEBHOOK,'******** (OFF) '+ get_user_id(DISCORD_ID) +' Logging out Char: '+ str(CharName()) +' ********')
        
    SetARStatus(False)     
    Disconnect()
    exit()
    
def go_to_safe_and_fix_equipment():
    SetGlobal('char','Room','Fix')
    print('Going to safe to fix equipment')
    ClearBadLocationList()
    move_thru_doors(423, 431, 0, 0, 4, True, open_doors)
    NewMoveXY(423,370, False,1,True)  #Antes de Virar
    NewMoveXY(431,371, False,1,True)  #Começo da Parede
    wait_lag(600)
    move_steps_direction(3,2)
    wait_lag(600)
    ClearBadLocationList() #Tem q ter esse segundo clearBadLocation se não da pau
    move_steps_direction(55,2) #healer coord!!! 
    
    ClearBadLocationList()     
    fixed = False
    eqp_with_low_durability = check_low_durability_equip()
    if eqp_with_low_durability: 
        helper_bot = approach_helper_bot() 
        if helper_bot is not None:
            fixed = fix_equipament(eqp_with_low_durability, helper_bot)
            if fixed:
                dress_main_set()
        else:
            print('Could not find HelperBot.')

    
    if eqp_with_low_durability is False or fixed is False:
        print('Could not fix equipment! Disconnecting') 
        send_discord_message(DISCORD_WEBHOOK,'******** (FIX) '+ get_user_id(DISCORD_ID) +' Could not fix equipment! Char: '+ str(CharName()) +' ********')
        SetARStatus(False)
        Disconnect()
        exit()
        
    UOSay('Cheers Quaker! Thank you, sir!')
    return
    print('Exiting safe room and going to center')
    move_steps_direction(55,6)           
    while is_in_hallway():   
        move_steps_direction(1,6)
    ClearBadLocationList() #Tem q ter esse segundo clearBadLocation se não da pau
    move_steps_direction(5,6)
    wait_lag(600)
    ClearBadLocationList() #Tem q ter esse segundo clearBadLocation se não da pau
    print('antes de virar')
    NewMoveXY(423,371, False,1,True)  #Antes de Virar
    print('indo para o centro')
    NewMoveXY(423,431, False,1,True)  #Centro

charX = 0
charY = 0
charZ = 0

def find_destination(coordsToCheck):
    #print(coordsToCheck)
    #print(charX)
    for coord in coordsToCheck:
        if IsWorldCellPassable (charX, charY, charZ, coord[0], coord[1], WorldNum())[0]:
            #Checking if there's a trap on the destination coord.
            objOnCoord = FindAtCoord(coord[0], coord[1])
            if not GetType(objOnCoord) in TRAPS_TYPES:
                return coord[0], coord[1]
    return -1, -1


def keep_distance(boss_serial, min_distance = 10):
    global charX 
    global charY 
    global charZ
    ClearBadLocationList()
    SetMoveBetweenTwoCorners(0)
    SetMoveCheckStamina(0)
    SetMoveThroughCorner(0)
    SetMoveThroughNPC(0)
    ClickOnObject(boss_serial)
    found_destination = False
    distance = GetDistance(boss_serial)
    while not Dead() and distance < min_distance and GetHP(Self()) <= GetMaxHP(Self())*0.4: 
        if is_bufficon_activated('Blood Oath'):
            SetWarMode(False)
        else:
            mob_nearby = get_mobs_nearby()  
            if mob_nearby != 0:
                Attack(mob_nearby)
                if GetType(mob_nearby) in MOB_TYPES:
                    boss_serial = mob_nearby                              
                
        found_destination=False
        ClearBadLocationList()
        ClearBadObjectList()
        #checking for traps and setting it as bad locations
        set_traps_as_bad_locations()

        objX = GetX(boss_serial)
        objY = GetY(boss_serial)
        if objX <=0 and objY <=0:
            #ClientPrintEx(Self(), 66, 1, 'object not found. returning')
            return
        charX = GetX(Self())
        charY = GetY(Self())
        charZ = GetZ(Self())
        
        while not found_destination:
            if min_distance < 1:
                print('ABORT! Could not keep a minimal distance!')
                return
            circunference_coords = sort_by_distance(generate_circunference_coords_array(objX,objY,min_distance))
            destX, destY = find_destination(circunference_coords)
            if destX > -1:
                found_destination = True
            else:
                print('Can\'t keep min distance of '+str(min_distance)+'. Trying distance '+str(min_distance-1))
                min_distance = min_distance - 1
        
        #ClientPrintEx(Self(), 66, 1, 'toX:'+str(destX)+'. toY:'+str(destY))
        #ClientPrintEx(Self(), 66, 1, 'HP:'+str(GetHP(Self())))
        if found_destination:
            print('DANGER!! MOVING AWAY!')
            NewMoveXY(destX, destY, True, 0, True)
            #ClientPrintEx(Self(), 66, 1, 'currDistance:'+str(GetDistance(boss_serial)))
        #ClientPrintEx(Self(), 66, 1, '--------------------')
        distance = GetDistance(boss_serial)
        cast_curse_weapon(0.2,0.95,5)

import math
def normal_round_based_on_coords(centerX,centerY,nX,nY):
    #round number for a 'outer coord' using center coord as reference.
    if nX < centerX and nY < centerY:
        return math.floor(nX),math.floor(nY)
    if nX < centerX and nY > centerY:
        return math.floor(nX),math.ceil(nY)
    if nX > centerX and nY > centerY:
        return math.ceil(nX),math.ceil(nY)
    if nX > centerX and nY < centerY:
        return math.ceil(nX),math.floor(nY)
    #print('nao retornou. cx:'+str(centerX)+'. cy:'+str(centerY)+'. nx:'+str(nX)+'. ny:'+str(nY))
    return round(nX),round(nY)


def generate_circunference_coords_array(centerX,centerY,radius):
    #BUG:
    #Alguns pontos são mais longes (principalmente nos cantos) deveriam são considerados como distância maior, mais aqui estão como se estivessem como a distância certa. Isso fica evidente para raio 3 ou 4.
    #Se eu removo os da ponta, funciona para raio 3, mas não funciona para raio 4 pra cima.
    #Para corrigir, talvez tenha que ser levado em consideração a diferença entre coords X e Y usando a função abs. Similar ao que tem no stealth na função Dist
    array_of_points = []
    top_left     = 0
    top_right    = 0
    bottom_left  = 0
    bottom_right = 0
    arrays_of_rounded_points = []
    arrays_of_invalid_distance = []

    number_of_points = radius * 8
    for i in range(0, number_of_points+1):

        #xt= radius * math.cos(angle) + Xinicial
        #yt= radius * math.sin(angle) + Yinicial

        xt= radius * math.cos(2*math.pi/number_of_points*i) + centerX
        yt= radius * math.sin(2*math.pi/number_of_points*i) + centerY
        #For debug purpose
        #print ('X:'+str(xt)+'. Y:'+str(yt) + '. roundX:'+str(math.ceil(xt))+' roundY:'+str(math.ceil(yt)))
        tempArray = [xt, yt]
        array_of_points.append(tempArray)
        #For debug purpose
  
        roundedX, roundedY = normal_round_based_on_coords(centerX,centerY,xt,yt)
        temp_rounded_array = [roundedX, roundedY]
        if temp_rounded_array not in arrays_of_rounded_points:
            if Dist(roundedX,roundedY,centerX,centerY) == radius:
                arrays_of_rounded_points.append(temp_rounded_array)
            #For debug Purpose
            else:
                arrays_of_invalid_distance.append(temp_rounded_array)

    return arrays_of_rounded_points

#For Python 3
def cmp_to_key(mycmp):
    'Convert a cmp= function into a key= function'
    class K(object):
        def __init__(self, obj, *args):
            self.obj = obj
        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0
        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0
        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0
        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0
        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0
        def __ne__(self, other):
            return mycmp(self.obj, other.obj) != 0
    return K

def sort_by_stealth_distance(x, y):
    p = [charX, charY]
    q = [x[0], x[1]]
    first_distance = math.dist(p, q)
    p = [charX, charY]
    q = [y[0],y[1]]
    second_distance = math.dist(p, q)
    #print('SORT. first:'+str(firstDistance)+'. second:'+str(secondDistance))
    return first_distance - second_distance

def sort_by_distance(array_of_points):
    #array_of_points.sort(key = lambda p: sqrt((p.centerX - centerX)**2 + (p.centerY - centerY)**2))
    #Python 2:
    #return sorted(array_of_points, cmp=sort_by_stealth_distance)
    #Ptyhon 3:
    from functools import cmp_to_key
    return sorted(array_of_points, key=cmp_to_key(sort_by_stealth_distance))


#################################################################################################################################################
############# **DO NOT CHANGE**  ############ **DO NOT CHANGE ** ############## **DO NOT CHANGE**  ############ **DO NOT CHANGE ** ##############
############# **DO NOT CHANGE**  ############ **DO NOT CHANGE ** ############## **DO NOT CHANGE**  ############ **DO NOT CHANGE ** ##############
# ==============================================================================================================================================#
#                                                           RESSURRECTING UTILS                                                                 #
# ==============================================================================================================================================#
                                                                           
def go_to_saferoom_and_ress(room = 0):
    SetGlobal('char','Room','Ress')
    send_discord_message(DISCORD_WEBHOOK,'******** (DEAD) '+ get_user_id(DISCORD_ID) +' Char: '+ str(CharName()) + ' @ Room: ' + str(room) +' ********') 
    print('-------------- GOING TO SAFE ROOM -> RESS!!! ----------------')
    ClearBadLocationList() 
    move_thru_doors(423, 431, 0, 0, 4, True, open_doors) 
    NewMoveXY(423, 371, False, 1, True)  #Antes de Virar
    NewMoveXY(431, 371, False, 1, True)  #Começo da Parede
    wait_lag(600)
    move_steps_direction(3,2)
    wait_lag(600)
    ClearBadLocationList() #Tem q ter esse segundo clearBadLocation se não da pau
    #while is_in_hallway():   
        #move_steps_direction(1,2)
    
    move_steps_direction(55,2)
    ClearBadLocationList() 
    helper_bot = approach_helper_bot()
    SetWarMode(True)
    starttime = datetime.now()
    while Dead():
        Wait(1000)
        if check_gump_exists(2957810225):
            waitgumpid_press(2957810225,1,5)
        if datetime.now() >= starttime+timedelta(minutes=2):
            print('SECURITY BREAK RESS!!! COULD NOT RESS! QUITING!')
            send_discord_message(DISCORD_WEBHOOK,'******** (DEAD) '+ get_user_id(DISCORD_ID) +' Could not ress! Char: '+ str(CharName()) + ' @ Room: ' + str(room) +' ********') 
            SetARStatus(False)
            Disconnect()
            exit()
    
    SetARStatus(True)
    SetPauseScriptOnDisconnectStatus(False)
    Wait(100)
    print('Disconnected')
    Disconnect()     
    Wait(4000)  
    
    while( not Connected()):
        Connect()
        Wait(4000)   
    Wait(1000)
    SetWarMode(False)

    UOSay('all follow me')

    if GetSkillValue('Necromancy') >= 99:
        dress_lrc_set()
    
    handle_pet()    
    buy_items_after_ress()    
    cast_vampiric_embrace()
    dress_main_set()    
    check_mount_before_leave()
    
    ClearBadLocationList()
    SetPauseScriptOnDisconnectStatus(True)
    check_number_of_deaths_playable()
    honor_self()         
    
    # LEAVE SAFE ROOM
    NewMoveXY(489, 371, False, 0, True)  # Center of safe room  
    move_steps_direction(55,6)
    while is_in_hallway():   
        move_steps_direction(1,6)
    ClearBadLocationList() #Tem q ter esse segundo clearBadLocation se não da pau
    move_steps_direction(5,6)
    wait_lag(600)
    ClearBadLocationList() #Tem q ter esse segundo clearBadLocation se não da pau
    NewMoveXY(423, 371, False, 1, True)  #Antes de Virar
    NewMoveXY(423, 431, False, 1, True)  #Centro


def get_body_corpse_back(room, x, y):
    if room != 6:
        go_to_room(room)
    NewMoveXY(x, y, False, 0, True)
    # FINDING CORPSE SELF     
    CORPSE_TYPES = [0x2006, 0x0ED0, 0x0ED1, 0x0ED2, 0xECB, 0xECC, 0xECD, 0x0ECE, 0xECF]   
    gotit = False
    if FindTypesArrayEx(CORPSE_TYPES ,[0xFFFF],[Ground()],False): 
        ClientPrintEx(Self(), 66, 1, 'Found a corpse.')
        founds = GetFindedList()
        for found in founds:
            if(GetTooltip(found).lower().find(GetName(Self()).lower()) >= 0): 
                ClientPrintEx(Self(), 66, 1, "Oh, that's my body! Let me get my stuff back.")
                NewMoveXY(GetX(found),GetY(found), False,0,True)
                Wait(500)
                for i in range(1, 4):
                    UseObject(found)
                    if WaitJournalLine(datetime.now(), 'You quickly gather all of your belongings', 600): 
                        ClientPrintEx(Self(), 66, 1, 'GOT IT!!!')        
                        gotit = True
                        break  
                if gotit:
                    break 
              
    if not gotit:
        ClientPrintEx(Self(), 66, 1, 'Did not find a body corpse. :(')  
        send_discord_message(DISCORD_WEBHOOK,'******** (LOOT) Could not find my body corpse. '+ get_user_id(DISCORD_ID) +' Char: '+ str(CharName()) + ' @ Room: ' + str(room) +' ********') 

    check_deaths_in_a_row() 
    return

    
def wait_lag(wait_time=WAIT_TIME, lag_time=WAIT_LAG_TIME):
    Wait(wait_time)
    CheckLag(lag_time)
    return
    

def find_players(distance = 2, vdistance = 10):
    SetFindDistance(distance)
    SetFindVertical(vdistance)
    findedList = FindTypesArrayEx(PLAYER_TYPES ,[0xFFFF],[Ground()],False)
    list_of_finded = GetFindedList()
    return list_of_finded


def find_helper_bot(list_of_players):
    for player in list_of_players:
        if player in HELPER_BOT_LIST:
            return GetDistance(player)
    return -1

def set_auto_buy():
    AutoBuy(0, 0, 0)
    for key, val in ITEMS_TO_BUY.items():
        AutoBuy(key,0xFFFF,val)
        wait_lag(600)

def buy_items_after_ress():
    set_auto_buy()
    starttime = datetime.now()
    SetFindDistance(25)
    # try to find NPC around
    NPC_TYPES = [0x0190, 0x0191]
    if FindTypesArrayEx(NPC_TYPES ,[0x8835],[Ground()],False):
        founds = GetFindedList()
        for found in founds:
            if GetNotoriety(found) != 7:
                continue            
            ClickOnObject(found)
            wait_lag(100)                
            vendor_name = GetAltName(found)
            if (vendor_name.find('Variety Dealer') != -1):
                VENDOR_CONTEXT = found
                wait_lag(100)
                SetContextMenuHook(VENDOR_CONTEXT, 1)
                wait_lag(100)
                RequestContextMenu(VENDOR_CONTEXT)
                wait_lag(200)
                break
    #RESET CONTEXT
    SetContextMenuHook(0, 0)
    AutoBuy(0, 0, 0)
    wait_lag(50)
    return

def get_number_of_deaths_playable():
    number_of_deaths_playable = 0
    SetContextMenuHook(Self(), 2)
    WaitGump(1000)
    RequestContextMenu(Self())
    wait_lag(1)
    # reset the context! important!
    SetContextMenuHook(0, 0)
    waitgumpid_without_use_object(3465474465)

    for gump in range(GetGumpsCount()):
        idd = GetGumpID(gump)
        if idd == 3465474465:
            # gump do insurance menu
            infogump = GetGumpInfo(gump)
            number_of_deaths_playable = int(infogump['Text'][2][0])
        else:
            break

    close_gumps()
    wait_lag(1)
    close_gumps()
    return number_of_deaths_playable

def waitgumpid_without_use_object(gumpid, timeout=15):
    maxcounter = 0
    while maxcounter < timeout * 10:
        if IsGump():
            for currentgumpnumb in range(0, (GetGumpsCount())):
                currentgump = GetGumpInfo(currentgumpnumb)
                if ('GumpID' in currentgump):  # got to check if key exists or we might get an error
                    if currentgump['GumpID'] == gumpid:
                        return True
                if IsGumpCanBeClosed(currentgumpnumb):
                    CloseSimpleGump(currentgumpnumb)
        maxcounter += 1
        CheckLag(100000)
    return False

def check_deaths_in_a_row():
    global deaths_in_a_row
    global timer_deaths_in_a_row_check 
    deaths_in_a_row = deaths_in_a_row + 1                                    
    print('Current deaths in a row ' + str(deaths_in_a_row))  
    if datetime.now() <= timer_deaths_in_a_row_check + timedelta(minutes=30):   
        if deaths_in_a_row >= 5:
            print('Too many deaths in a row!!')   
            print('Logging you out! Disconnecting!') 
            go_to_safe_and_logout()
    else:                                    
        timer_deaths_in_a_row_check = datetime.now()
        deaths_in_a_row = deaths_in_a_row - 1 
        if deaths_in_a_row <= 0:  
            deaths_in_a_row = 0

def check_number_of_deaths_playable():
    nodp = get_number_of_deaths_playable()
    if nodp:
        if nodp < 10:
            print('Out of gold!! Current gold balance only give you ' + str(nodp) + ' deaths playable')   
            print('Logging you out! Disconnecting!') 
            send_discord_message(DISCORD_WEBHOOK,'******** ($$$) '+ get_user_id(DISCORD_ID) +' OUT OF GOLD FOR INSURE! Char: '+ str(CharName()) +' ********')
            SetARStatus(False)
            Disconnect() 
            exit()
        else:
            print('Current gold balance give you ' + str(nodp) + ' deaths playable') 

#################################################################################################################################################
############# **DO NOT CHANGE**  ############ **DO NOT CHANGE ** ############## **DO NOT CHANGE**  ############ **DO NOT CHANGE ** ##############
############# **DO NOT CHANGE**  ############ **DO NOT CHANGE ** ############## **DO NOT CHANGE**  ############ **DO NOT CHANGE ** ##############
# ==============================================================================================================================================#
#                                                                 GENERAL UTILS                                                                 #
# ==============================================================================================================================================#

#
def ping_user():
    print("trying to ping")
    try:
        # api-endpoint
        URL = URL_API + DISCORD_ID.replace(' ','%20').replace('#','%23')
        #URL = 'http://127.0.0.1:8000/' + DISCORD_ID.replace(' ','%20').replace('#','%23')
    
        # defining a params dict for the parameters to be sent to the API
        PARAMS = {'char_name': CharName()}  
  
        # sending get request and saving the response as response object
        r = requests.get(url = URL, params = PARAMS)
      
        # extracting data in json format
        data = r.json() 
        #print(data)
    except:         
        print('exception')
        pass    

def post_user():
    #print("trying to post")

    try:     
        
        url = URL_API + 'post_char_info'
        player = {
            'serial' : Self()  ,
            'info': {
                "name": CharName(),
                "last_arty": '',
                "arty_count": 0,
                "online"    : True,
                "last_seen": '', 
                "last_room": GetGlobal('char','Room'),
            }
        }             

        r = requests.post(url, json = player)
        
        # extracting data in json format
        data = r.json() 
        #print(data)
    except:         
        print('exception')
        pass  

def post_new_artifact(artifact):
    #print("trying to post")

    try:                                             
        url = URL_API + 'post_new_artifact'
        player = {
            'serial' : Self()  ,
            'info': {
                "name": CharName(),
                "last_arty": artifact,
                "arty_count": 1,
                "online"    : True,
                "last_seen": '', 
                "last_room": GetGlobal('char','Room'),
            }
        }             

        r = requests.post(url, json = player, timeout = 3)
        
        # extracting data in json format
        data = r.json() 
        #print(data)
    except:         
        print('exception')
        pass  
    
# associate each user discord to its dev discord id 
def get_user_id(user):
    users = {     
        'Marcos Guerine#4564': '283404359289667595',
        'C O V I D#2754': '471488170224123904',
        'ferrari#4280': '475945772714819584',
        'Peter Griffin#5996': '200217498354712576',      
        'Vitin#6883': '710940695703322676',
        'gusta#9691': '699761314746335264',
        'Mauruto#1707': '133723531312758784',
        'Henriqu#1980': '759855695351906316',
        'LeoO#2569': '130188083357286400',
        'Renan Alves#2261' : '695823823538356265',
        'HAGNOK#0768' : '256959516107603968',
        'Grifo#5642' : '116007443380699144',
        'Maicossuel#2737' : '788110650853163058',
        'caioandre#8449' : '495966324510687258',
        'Ciro#7619' : '218502256562143232',
        'thiagoPC#7835' : '542470901531279386',
        'Riann#1517' : '654477892058873876',
        'Ziuul#6626' : '264024952150163456',
        'Gandalf_Zica#5142' : '940416836686712872',
        'rodolphodimas#0757' : '352222468926078997',
        'Gui#2692' : '274640824711774208',
        'Rafa L#2629' : '933118553694031962',
        'Dozen#1351' : '773290280395735060',
        'Cap0#0675' : '474274307623747584',
        'Andinhow#3963' : '437086138100875275',
        'Loverboy#6771' :  '387444238734065665',
        'Tairone Reis#9222' : '355474079974817802',
        'Christian Portugal#6228' : '712461094136053772',
        'Cunnana#9052' : '116302878636900359',
        'flocris#7433' : '261869160634646529',
        'zephyr#3336' : '115909954417721350',
        'paulopaulo#6114' : '346483487068389389',
        'kindermvp' : '291700776823291915'

    }

    if user in users:
        return '<@'+users[user]+'>'
    else:
        return '@unknown' 

def check_journal(word, clear = True):
    for i in range(LowJournal(), HighJournal() +1) :
        if i < 0:
            continue
        line = Journal(i)     
        #print(line + ' ' + str(i) + ' checking')
        if word in line:                   
            if clear: ClearJournal()
            return True
    if clear: ClearJournal()     
    return False

def trunc(num, digits):
    sp = str(num).split('.')  
    inteiro = sp[0]
    decimal = sp[1]
    return (str(sp[0]) + '.' + str(decimal[:digits]))


def honor_self():
    UseVirtue('Honor')
    WaitForTarget(2000)
    if TargetPresent():
        WaitTargetObject(Self())
        Wait(500)
    if IsGump():
        if GetGumpsCount() > 0:
            gump_id = GetGumpID(GetGumpsCount()-1)
            gumpInfo = GetGumpInfo(GetGumpsCount()-1) 
            for text in gumpInfo['Text']:
                if 'Are you sure you want to use honor points on yourself?' in text:
                    waitgumpid_press(gump_id, 1, True, 1)

 
def insure_items(room = 0):
    item_to_insure = []
    has_item_to_insure = False

    FindTypesArrayEx(INSURE_TYPES ,[0xFFFF],[Backpack()],False)
    founds = GetFindedList()
    for found in founds:
        if GetType(found) == '': 
            ClickOnObject(found)
            Wait(500)
        if GetType(found) in INSURE_TYPES:
            tooltip = str(GetTooltip(found))
            if tooltip == '':
                ClickOnObject(found)
                Wait(500)
            tooltip = str(GetTooltip(found))
            if tooltip.find('Insured') < 0:
                if tooltip.find('Blessed') < 0:
                    #print(tooltip)
                    print('###FOUND ARTY##### Non Insured and non blessed wearable found! item id: ' +str(found) + '. Tooltip:'+str(tooltip) + '. Insured:'+str(tooltip.find('Insured')) + '. Blessed: '+str(tooltip.find('Blessed')))
                    item_to_insure.append(found)
                    has_item_to_insure = True
                    if 'artifact rarity' in str(tooltip):
                        send_discord_message(DISCORD_WEBHOOK,'******** (ARTY) '+ get_user_id(DISCORD_ID) +' Arty: ' + str(tooltip).split('|')[0] + ' | Char: '+ str(CharName()) + ' @ Room: ' + str(room) +' ********')                            
                        post_new_artifact(str(tooltip).split('|')[0])
                        UOSay('AEEEEEEEEE!!')   
                        Wait(50)
                        UOSay('ARTY!! ARTY!! ARTY!! ARTY!! ARTY!! ARTY!! '+ str(tooltip).split('|')[0])
                        Wait(50)                  
                    elif 'ring' in str(tooltip) or 'brace' in str(tooltip) or 'Assassin' in str(tooltip):
                        if 'Assassin' in str(tooltip):
                            if GetType(found) == 0x13CC:
                                piece = 'Tunic'
                            elif GetType(found) == 0x13CD:
                                piece = 'Sleeves'
                            elif GetType(found) == 0x13CB:
                                piece = 'Leggings'
                            elif GetType(found) == 0x13C6:
                                piece = 'Gloves'
                            else:
                                piece = 'None'
                            send_discord_message(DISCORD_WEBHOOK,'******** (LOOT) '+ get_user_id(DISCORD_ID) +' Item: ' + str(tooltip).split('|')[0] + ' (' +  piece + ') | Char: '+ str(CharName()) + ' @ Room: ' + str(room) +' ********' + str('```') )
                        else:
                            score = trunc(calculate_value(found), 2)
                            if float(score) > 30:
                                send_discord_message(DISCORD_WEBHOOK,'******** (LOOT) '+ get_user_id(DISCORD_ID) +' Item: ' + str(tooltip).split('|')[0] + ' | Char: '+ str(CharName()) + ' @ Room: ' + str(room) +' ********' + str('```') + tooltip + str(' | score: '+ str(score) + '```'))
                    

    if has_item_to_insure is True: 
        CancelTarget()
        ClearContextMenu  
        SetContextMenuHook(0, 0)
        RequestContextMenu(Self())
        SetContextMenuHook(Self(), 3) 
        WaitForTarget(2000)
        if TargetPresent():
            for item in item_to_insure:
                TargetToObject(item)
                Wait(500)   
                
        CancelTarget()
        ClearContextMenu()  
        SetContextMenuHook(0, 0)
        Wait(500)  
    
def find_loot_and_ignore_dead_corpses(room, _loot = True):
    # FINDING AND IGNORING DEAD BOSS CORPSES  
    if (FindType(0x2006,Ground()) > 0):
        founds = GetFindedList()
        for found in founds:
            corpse = found
            if GetType(corpse) == 0x2006 and (GetTooltip(corpse).lower().find(BossNames[room-1].lower()) >= 0):
                try:
                    if _loot and GetDistance(corpse) <= 2:
                        ClientPrintEx(Self(), 13, 0, "LOOTING..." + str(GetTooltip(corpse)))
                        loot(corpse, 25, False)
                except:
                    pass    
                Ignore(corpse)
                return True
    else:
        return False     

def set_traps_as_bad_locations():
    # FINDING TRAPS AND SETTING AS BAD LOCATION                     
    if FindTypesArrayEx(TRAPS_TYPES ,[0xFFFF],[Ground()],False): 
        founds = GetFindedList()
        for found in founds:  
            if GetType(found) in TRAPS_TYPES: 
                SetBadLocation(GetX(found),GetY(found))  
                    
def bone_cutter():
    if BONECUTTER is False:
        return
    if FindTypesArrayEx(BONE_TYPES ,[0xFFFF],[Ground()],False):
        founds = GetFindedList()
        for found in founds:   
            if GetType(found) in BONE_TYPES and GetDistance(found) <= 2 and 'remains of' not in GetCliloc(found):
                bone = found 
                if FindType(BLADE_TYPE,Backpack()):   
                    kata = FindItem()
                    UseObject(kata)
                    WaitForTarget(700)
                    if TargetPresent():     
                        WaitTargetObject(bone)
                        TargetToObject(bone)   


#################################################################################################################################################
############# **DO NOT CHANGE**  ############ **DO NOT CHANGE ** ############## **DO NOT CHANGE**  ############ **DO NOT CHANGE ** ##############
############# **DO NOT CHANGE**  ############ **DO NOT CHANGE ** ############## **DO NOT CHANGE**  ############ **DO NOT CHANGE ** ##############
# ==============================================================================================================================================#
#                                                                 CASTING UTILS                                                                 #
# ==============================================================================================================================================#
BuffIcons = {
    'Dismount Prevention': 1001,
    'Dismount': 1001,
    'NoRearm': 1002,
    'Night Sight': 1005,
    'Death Strike': 1006,
    'Evil Omen': 1007,
    'Honored': 1008,
    'Achieve Perfection': 1009,
    'Divine Fury': 1010,
    'Enemy Of One': 1011,
    'HidingAndOrStealth': 1012,
    'Active Meditation': 1013,
    'Blood Oath Caster': 1014,
    'Blood Oath Curse': 1015,
    'Blood Oath': 1015,
    'Corpse Skin': 1016,
    'Mindrot': 1017,
    'PainS pike': 1018,
    'Strangle': 1019,
    'Gift Of Renewal': 1020,
    'Attune Weapon': 1021,
    'Thunderstorm': 1022,
    'Essence Of Wind': 1023,
    'Ethereal Voyage': 1024,
    'Gift Of Life': 1025,
    'Arcane Empowerment': 1026,
    'Mortal Strike': 1027,
    'Reactive Armor': 1028,
    'Protection': 1029,
    'Arch Protection': 1030,
    'Magic Reflection': 1031,
    'Incognito': 1032,
    'Disguised': 1033,
    'Animal Form': 1034,
    'Polymorph': 1035,
    'Invisibility': 1036,
    'Paralyze': 1037,
    'Poison': 1038,
    'Bleed': 1039,
    'Clumsy': 1040,
    'Feeblemind': 1041,
    'Weaken': 1042,
    'Curse': 1043,
    'Mass Curse': 1044,
    'Agility': 1045,
    'Cunning': 1046,
    'Strength': 1047,
    'Bless': 1048,
    'Sleep': 1049,
    'Stone Form': 1050,
    'Spell Plague': 1051,
    'Gargoyle Berserk': 1052,
    'Fly': 1054,
    'Inspire': 1055,
    'Invigorate': 1056,
    'Resilience': 1057,
    'Perseverance': 1058,
    'Tribulation': 1059,
    'Despair': 1060,
    'Arcane Empowerment2': 1061,
    'Magic Fish Buff': 1062,
    'Hit Lower Attack': 1063,
    'Hit Lower Defense': 1064,
    'Hit Dual Wield': 1065,
    'Block': 1066,
    'Defense Mastery': 1067,
    'Despair Bard': 1068,
    'Healing Skill': 1069,
    'Spell Focusing': 1070,
    'Spell Focusing Debuff': 1071,
    'Rage Focusing Debuff': 1072,
    'Rage Focusing': 1073,
    'Warding': 1074,
    'Tribulation Bard': 1075,
    'Force Arrow': 1076,
    'Disarm': 1077,
    'Surge': 1078,
    'Feint': 1079,
    'Talon Strike': 1080,
    'Psychic Attack': 1081,
    'Consecrate': 1082,
    'Consecrate Weapon': 1082,
    'Grapes Of Wrath': 1083,
    'Enemy Of One Debuff': 1084,
    'Horrific Beast': 1085,
    'Lich Form': 1086,
    'Vampiric Embrace': 1087,
    'Curse Weapon': 1088,
    'Reaper Form': 1089,
    'Immolating Weapon': 1090,
    'Enchant': 1091,
    'Honorable Execution': 1092,
    'Confidence': 1093,
    'Evasion': 1094,
    'Counter Attack': 1095,
    'Lightning Strike': 1096,
    'Momentum Strike': 1097,
    'Orange Petals': 1098,
    'Rose Of Trinsic Petals': 1099,
    'Poison Resistance': 1100,
    'Veterinary': 1101,
    'Perfection': 1102,
    'Honored2': 1103,
    'Honor': 1103,
    'Mana Phase': 1104,
    'Fandancer Fan Fire': 1105,
    'Rage': 1106,
    'Webbing': 1107,
    'Medusa Stone': 1108,
    'Dragon Slasher Fear': 1109,
    'Aura Of Nausea': 1110,
    'Howl Of Cacophony': 1111,
    'Gaze Despair': 1112,
    'Hiryu Physical Resistance': 1113,
    'Rune Beetle Corruption': 1114,
    'Bloodworm Anemia': 1115,
    'Rotworm Blood Disease': 1116,
    'Skill Use Delay': 1117,
    'Faction Stat Loss': 1118,
    'Heat Of Battle': 1119,
    'Criminal': 1120,
    'Armor Pierce': 1121,
    'Splintering': 1122,
    'Swing Speed Debuff': 1123,
    'Wraith Form': 1124,
    'Honorable Execution2': 1125,
    'City Trade Deal': 1126
}

def is_bufficon_activated(spell,timer_start=datetime.now()):    
    bufficon = BuffIcons.get(spell)
    info = GetBuffBarInfo() 
    for icon in info: 
        if(icon.get('Attribute_ID') == bufficon):  
            if(bufficon == 1082):   
                consecrate_start = icon.get('TimeStart')                                                                                                                                                       
                if (timer_start > consecrate_start + timedelta(seconds=8) ):
                    return False
                else:
                    return True
            if(bufficon == 1011):
                enemy_of_one_start = icon.get('TimeStart')  
                if (enemy_of_one_start < timer_start):
                    return False
                else:
                    return True
            else:
                return True
    return False  

def journal_status(journalStates, clear=True):                     
    for state in journalStates:
        texts = journalStates[state]
        for text in texts:
            if check_journal(text, False):
                if clear: ClearJournal()
                return state
    return None    
    
def wait_for_target(timeout = None, target = None):
    ClearJournal() 
    if timeout is None: timeout = 5000
    if target != None:
        WaitTargetObject(target)
    #'casting':  ['You are already casting'],
    jStatus = {
        'reags': ['More reagents are needed for this spell'],
        'mana': ['Mana to use this ability.', 'Insufficient mana.'],        
        'fizzle':  ['The spell fizzles'],
        'disturb': ['Your concentration is disturbed, thus ruining thy spell.'],
        'recov': ['You have not yet recovered from casting a spell.'],                  
        'cant': ['You cannot heal that target in their current state.'],
        'away': ['This is too far away']
    }
    start_mana = GetMana(Self())
    endtime = datetime.now() + timedelta(seconds=timeout/1000)
    #i = 0        
    #print('* CASTING started: ', end ='')
    #print(str(datetime.now().time()))  

    while datetime.now() < endtime: 
        Wait(200)   
        found = journal_status(jStatus, False)
        
                        
        if GetMana(Self())  < start_mana:
            #print('[success?] MANA')  
            return 'mana'

        if found in jStatus.keys(): 
            #if found == 'casting':
            #    continue            
            ClientPrintEx(Self(), 33, 0, '[FAIL: ' + str(found) + ']' )
            #print('[FAIL: ' + str(found) + ']')    
            if str(found) == 'recov':
                Wait(100)
            #print(str(datetime.now().time())) 
            return None


        if TargetPresent():  
            ClientPrintEx(Self(), 72, 0, '[TARGET SUCCESS]') 
            if target != None and target == 'self':
                TargetToObject(Self())
            elif target != None and target == 0:
                TargetToObject(LastTarget())
            elif target != None and target > 0:
                TargetToObject(target)
            break
    if datetime.now() > endtime and not TargetPresent():
        #print('[FAIL: timeout?]') 
        ClientPrintEx(Self(), 33, 0, '[FAIL: timeout?]' )
    #    print(str(datetime.now().time()))
    #else:
    #    print('[FAIL: timeout?] : ' , end ='')
    #    print(str(datetime.now().time()))     
    return 'success' if datetime.now() < endtime else None

def cast_heal_cure_self(confidence = True):
    if GetSkillValue('Bushido') < 60:
        confidence = False        
    if not IsPoisoned(Self()) and confidence and not is_bufficon_activated('Confidence'):
        cast_confidence(0.5, True)          
    elif not confidence:
        cast_heal_cure_target(Self()) 

def cast_heal_cure_target(target, _lb = 0.8):
    if GetMana(Self()) < 7:
        return
    if not IsPoisoned(target) and GetHP(target) < GetMaxHP(target)*_lb and GetDistance(target) <= 2:
        Cast('Close Wounds')    
        if wait_for_target(3500, target):
            TargetToObject(target) 
            Wait(300)
    elif IsPoisoned(target):
        Cast('Cleanse by Fire')
        if wait_for_target(2500, target):
            TargetToObject(target)  
            Wait(300)


def cast_holy_light(): 
    if GetSkillValue('Chivalry') >= 60 and GetMana(Self()) >= 15: 
        Cast('Holy Light')   
        Wait(2000)     

def cast_enemy_of_one(timer = datetime.now()):
    # ENEMY OF ONE   
    if GetSkillValue('Chivalry') >= 60 and GetMana(Self()) >= 14: 
        #ClientPrintEx(Self(),13,0, 'LastAttack: ' + str(LastAttack()))
        #ClientPrintEx(Self(),13,0, 'Notoriety: ' + str(GetNotoriety(LastAttack()))) 
        if LastAttack() == 0 and not is_bufficon_activated('Enemy Of One', timer):  
            Cast('Enemy Of One')   
            Wait(300)         
        elif GetNotoriety(LastAttack()) != 5 and not IsHidden(LastAttack()) and GetHP(LastAttack()) > 0 and GetDistance(LastAttack()) < 2 and GetType(LastAttack()) in MOB_TYPES:
            Cast('Enemy Of One')   
            Wait(300)
                                                                                    

def cast_vampiric_embrace():
    VAMPIRIC_EMBRACE_SCROLL = 0x226C
    starttime = datetime.now()   
    if GetColor(Self()) != 33918 and GetSkillValue('Necromancy') >= 99:
        while GetMana(Self()) <= 20:
            if datetime.now() >= starttime+timedelta(seconds=10):
                print('Waiting for mana to cast Vampiric Embrace')
                starttime = datetime.now()
            Wait(1000)
        while GetColor(Self()) != 33918:                         
            if datetime.now() >= starttime+timedelta(minutes=2):
                print('Security break. Could not turn to vampiric form.')  
                break
            print('Char is not in Vampire form! Turning...')                           
            if count_lrc() <= 0:
                dress_lrc_set()
            if FindType(VAMPIRIC_EMBRACE_SCROLL, Backpack()):
                UseType(VAMPIRIC_EMBRACE_SCROLL)
                Wait(3000)
            else:
                Cast('Vampiric Embrace')
                Wait(3000)
    if GetColor(Self()) == 33918:
        print('Turned into Vampire.')                                                    

def cast_remove_curse():
    if GetSkillValue('Chivalry') >= 60 and GetMana(Self()) > 16:                                                                                                                                                                      
        if (is_bufficon_activated('Blood Oath') or is_bufficon_activated('Corpse Skin') or is_bufficon_activated('Curse') or is_bufficon_activated('Clumsy') or is_bufficon_activated('Weaken')):
            Cast('Remove Curse')
            if wait_for_target(3000):
                TargetToObject(Self())  
            Wait(500)

def cast_divine_fury(_lb = 90):
    if GetSkillValue('Chivalry') >= 60 and GetMana(Self()) >= 12:
        if not is_bufficon_activated('Divine Fury') and GetHP(LastAttack()) > 0 and GetDistance(LastAttack()) < 3: 
            Cast('Divine Fury')
            Wait(300)  
        elif GetStam(Self()) < _lb and GetStam(Self()) < GetMaxStam(Self()) and GetHP(LastAttack()) > 0 and GetDistance(LastAttack()) < 3:
            Cast('Divine Fury')
            Wait(300)    
        elif GetHP(LastAttack()) <= 0  and GetStam(Self()) < 30:
            Cast('Divine Fury')
            Wait(300)    
  
 
def cast_consecrate_weapon(force = False, wait = True):
    if GetSkillValue('Chivalry') >= 60 and GetMana(Self()) >= 8:  
        if (not is_bufficon_activated('Consecrate Weapon', datetime.now()) and GetHP(LastAttack()) > 0 and GetDistance(LastAttack()) < 3 and not IsHidden(LastAttack())) or force :
            Cast('Consecrate Weapon')   
            if wait:
                Wait(200)       
    if is_bufficon_activated('Consecrate Weapon', datetime.now()):
        return True
    else:
        return False
    

def cast_dispel_evil():
    global timer_dispel_mobs
    if is_bufficon_activated('Blood Oath') or GetSkillValue('Chivalry') < 60:
        return False
    achei = False  
    #Dispeling renavant
    if (FindType(0x190,Ground()) > 0): 
        founds = GetFindedList()  
        for found in founds:
            if GetType(found) == 0x190 and (GetName(found).find('a revenant') >= 0):
                Cast('Dispel Evil')
                Wait(200)
                achei = True
    #Dispeling other mobs
    if FindTypesArrayEx(DISPEL_TYPES ,[0xFFFF],[Ground()],False): 
        founds = GetFindedList()
        for found in founds:
            if GetType(found) in DISPEL_TYPES and GetDistance(found) <= 2 and datetime.now() >= timer_dispel_mobs + timedelta(seconds=10):
                timer_dispel_mobs = datetime.now()   
                Cast('Dispel Evil') 
                Wait(200) 
                achei = True
    return achei
        
def cast_confidence(_lb = 0.8, force = False):
    if GetSkillValue('Bushido') >= 65 and GetMana(Self()) >= 8 and GetHP(Self()) < GetMaxHP(Self())*_lb and (not is_bufficon_activated('Confidence')  or force):  
        Cast('Confidence')
        Wait(500)

def cast_counter_attack():
    if GetHP(Self()) > GetMaxHP(Self())*0.8 and GetSkillValue('Bushido') >= 80 and GetSkillValue('Parrying') >= 80 and not is_bufficon_activated('Counter Attack') and not is_bufficon_activated('Evasion') and not is_bufficon_activated('Blood Oath') and GetHP(LastAttack()) > 0  and GetDistance(LastAttack()) < 3:
        Cast('Counter Attack')
        Wait(500)    

def cast_curse_weapon(_lb = 0.3, _ub = 0.85, _mana = 5):
    if not is_bufficon_activated('Curse Weapon') and GetHP(LastAttack()) > 0 and not IsHidden(LastAttack()) > 0:
        if GetHP(Self()) > GetMaxHP(Self())*_lb and GetHP(Self()) < GetMaxHP(Self())*_ub and GetMana(Self()) > _mana:
            if FindType(0x2263,Backpack()):
                UseType(0x2263,0x0000)
            elif FindType(0x0F8A,Backpack()) or count_lrc() >= 40:  
                Cast('Curse Weapon')  

def count_lrc():
    lrc_total = 0  
    for layer_i in range(len(ARMOR_ITEM_LAYERS)):
        if ObjAtLayer(ARMOR_ITEM_LAYERS[layer_i]) > 0:
            item = ObjAtLayer(ARMOR_ITEM_LAYERS[layer_i])
            item_details_str = GetTooltip(item)
            item_details_array = item_details_str.split('|')
            for item_name, item_props in enumerate(item_details_array):
                item_props_array = item_props.split(',')
                for property_str in item_props_array:
                    prop_array = re.split('(-?\d*\.?\d+)', property_str)
                    if 'lower reagent cost ' in prop_array:
                        lrc_total += int(prop_array[1])
    return lrc_total


def get_mobs_nearby():
    #Finding other mobs nearby and return the closest
    if FindTypesArrayEx(DISPEL_TYPES ,[0xFFFF],[Ground()],False): 
        founds = GetFindedList()
        for found in founds:
            if GetType(found) in DISPEL_TYPES and GetDistance(found) < 2:
                return found   
    return 0
 
def check_low_tithing_points():
    tp = GetExtInfo()['Tithing_points']
    global last_tithingpoints_check
    if datetime.now() >= last_tithingpoints_check + timedelta(minutes=TITHING_COOLDOWN_IN_MINUTES):
        last_tithingpoints_check = datetime.now()
        if tp < TITHING_POINTS_ABORTLEVEL:
            ClientPrintEx(Self(), 66, 1, '### ABORTING!!! TITHING POINTS TOO LOW! ABORTING!!! Current: '+str(tp)+' ###')
        if tp < TITHING_POINTS_WARNLEVEL:
            ClientPrintEx(Self(), 66, 1, 'WARNING!!! LOW ON TITHING POINTS!!! Current: '+str(tp))
    if tp < TITHING_POINTS_ABORTLEVEL:
        return True
    elif tp < TITHING_POINTS_WARNLEVEL:
        return False
    return False     


def check_low_durability_equip(limit = 20):
    for j in range(len(ARMOR_ITEM_LAYERS)):
        eqp = ObjAtLayer(ARMOR_ITEM_LAYERS[j])
        tooltip = GetTooltip(eqp)
        regex_search = re.search('durability\s+(\d+).*',tooltip)
        if regex_search is not None:  
            durability = str(regex_search.group(0)).replace(' / ','/').split(' ')[1]
            first = durability.split('/')[0]
            second = durability.split('/')[1] 
            if int(first) < limit and int(first) != int(second):
                print('Found equipment with low durability!!! Going to safe! Eqp:' + tooltip)
                if FindType(0x1006, Backpack()) and int(second) < 255:
                    if 'Replica' not in tooltip:
                        use_powder_of_fortication_at(eqp)
                        return False
                return eqp 
            if int(second) < 20:
                ClientPrintEx(Self(), 66, 1, 'WARNING!!! EQUIPAMENT LOW DURABILITY!! ')
    return False


def use_powder_of_fortication_at(item):
    pof = {'type': 0x1006, 'color': 0x0973} 
    if not item:
        return    
    if FindType(pof['type'], Backpack()) and UseType(pof['type'], pof['color']):
        WaitForTarget(800)
        TargetToObject(item) 
        ClientPrintEx(Self(),52,0,'* POF *')
    #else:
    #    print('* No POF *')  
        
def fix_equipament(eqp, helper_bot):
    countTradeWaitLimit = 120
    count = 0
    print('Trying to fix equipment!')
    MoveItem(eqp, 65000, helper_bot, 0, 0, 0)
    while True:
        Wait(1000)
        count = count + 1
        if count > countTradeWaitLimit:
            return False
        if IsTrade() and not TradeCheck(TradeCount()-1,1): 
            print('Accept Trade')
            ConfirmTrade(TradeCount()-1)
            Wait(600)
        if FindType(GetType(eqp),Backpack()):
            for item in GetFindedList():
                if item == eqp:  
                    return True    
    return True

 


def honor_mob(honored_list):
    starttime = datetime.now()
    
    messages_not_honor = 'Somebody else is|You cannot honor'
    SetFindDistance(16)
    if FindTypesArrayEx(MOB_TYPES ,[0xFFFF],[Ground()],False):
        SetFindDistance(25)
        founds = GetFindedList()
        qnt = len(founds)
        for found in founds:
            if GetType(found) in MOB_TYPES and found not in honored_list:                     
                ClearJournal()   
                CancelWaitTarget()
                UseVirtue('Honor')
                WaitForTarget(3000)
                if TargetPresent():
                    WaitTargetObject(found) 
                    boss = found
                    Wait(1500) # Precisa desse wait para dar tempo de aparecer no journal
                    if InJournalBetweenTimes(messages_not_honor, starttime, datetime.now()) > -1:
                    #if InJournal('Somebody else is') >= 0 or InJournal('You cannot honor') >= 0:
                        honored_list.append(boss)   
                        #print('ignoring: ' + str(boss))
                    else:
                        #HONORED (or ate least tried but didn't have enough points)
                        #print('sucessfully honored?')     
                        if is_bufficon_activated('Honor'):
                            print('I honored the creature!!')
                            ClientPrintEx(Self(), 66, 1, 'I honored the creature!!')
                            ClientPrintEx(Self(), 66, 1, 'I honored the creature!!')
                            ClientPrintEx(Self(), 66, 1, 'I honored the creature!!')
                            honored_list.append(boss)
                        return 0
    else:
        SetFindDistance(25)
        return 1
    return 1   

def is_in_hallway():
    #x 434 - 477
    #y 371 - 372  
    return GetX(Self()) >= 434 and GetX(Self()) <= 477 and GetY(Self()) >= 371 and GetY(Self()) <= 372


#################################################################################################################################################
############# **DO NOT CHANGE**  ############ **DO NOT CHANGE ** ############## **DO NOT CHANGE**  ############ **DO NOT CHANGE ** ##############
############# **DO NOT CHANGE**  ############ **DO NOT CHANGE ** ############## **DO NOT CHANGE**  ############ **DO NOT CHANGE ** ##############
# ==============================================================================================================================================#
#                                                            AFK GUMP, GM and JAIL Utils                                                        #
# ==============================================================================================================================================#
InJail = False
GMGumpFound = False
GMGumpAnswered = False
AFK_GUMP = 0xc37345f3
GUMP_DEBUG_FILE = '/Scripts/gump-debug.txt'
JAIL_X_TOP_LEFT = 5270
JAIL_Y_TOP_LEFT = 1160
JAIL_X_BOTTOM_RIGHT = 5310
JAIL_Y_BOTTOM_RIGHT = 1190

DEMISE_GMS = {
    'Dysis':  0x450C2,
    'Astraeus': 0x53380,
    'Marshall': 0x48D25,
    'Forseti': 0xBC45C,
    'Samael': 0xDEBA0,
    'Tetra': 0xB741C,
    'Selene' : 0x94C42,
    'Larson' : 0x7A251,
    'Tycho' : 0x18622A, 
}

DEMISE_GM_DISGUISE_TYPES = {
    0x31D: 0,  # Ancient Wyrm Verde
    0x2DF: 0,  # navrey
    0xBD: 33,  # red orc brute
    0xAF: 1194,  # anjo tetra (WTF ???)
}

gm_names = [
    'EOS:',
    'Larson:',
    'Selene:',
    'GM controlling:',
    'GM Tetra:',
    'Anjo Tetra:',
    'Tycho:',
    'Navrey:',
    'Ancient Wyrm Verde',
    'ORC BRUTE VERMELHO',
    'Samael:',
    'John:',
    'Styx:',
    'Lyane:',
    'Marshall:',
    'Forseti:',
    'Dysis:',
    'Astraeus:',  
]

gm_msgs = [
    'here?',
    'attending',
    'ATTENDANCE CHECK!! IF YOU ARE ATTENDED', 
    'attended',  
    'AFK', 
    'H3R3',
    'STOP',   
    'Hitting' 
    'Stop hitting',  
    'Stop H1t1ng'
]
                  
def is_gm_present():
    global timer_gm_check
    if datetime.now() >= timer_gm_check +timedelta(seconds=5):
        timer_gm_check = datetime.now()                       
    else:
        return False
    #print('Checking....')   
    for name in gm_names:              
        if InJournal(name) > -1:
            ClearJournal()  
            send_discord_message(DISCORD_WEBHOOK,'******** (GM.ON?) by name: ' + name + ' @everyone ALERT! GM ONLINE? Char: '+ str(CharName()) +' ********') 
            return True
    for msg in gm_msgs:              
        if InJournal(msg) > -1:
            ClearJournal()   
            send_discord_message(DISCORD_WEBHOOK,'******** (GM.ON?) by msg: ' + msg + ' @everyone ALERT! GM ONLINE? Char: '+ str(CharName()) +' ********')
            return True
     
    for gm_name in DEMISE_GMS.keys():
        gm_serial = DEMISE_GMS[gm_name] 
        if IsObjectExists(gm_serial) or GetDistance(gm_serial) != -1:
            send_discord_message(DISCORD_WEBHOOK,'******** (GM.ON!!) by serial: ' + gm_name + ' @everyone ALERT! GM ONLINE!! Char: '+ str(CharName()) +' ********')
            return True

    # try to find disguised gm
    for disguise_graphic in DEMISE_GM_DISGUISE_TYPES.keys():    
        disguise_color = DEMISE_GM_DISGUISE_TYPES[disguise_graphic]
        if FindTypeEx(disguise_graphic, disguise_color, Ground(), True):
            send_discord_message(DISCORD_WEBHOOK,'******** (GM.ON!!) GM Transfigurado: ' + gm_name + ' @everyone ALERT! GM ONLINE!! Char: '+ str(CharName()) +' ********')
            return True
            
    return False

def check_afk_gump(charFunction = ''):
    global GMGumpFound
    if IsGump():
        if GetGumpsCount() > 0:
            id = GetGumpID(GetGumpsCount()-1)
            if id == AFK_GUMP:
                try:
                    PlayWav(WAV_AFK)
                except:
                    pass
                if GMGumpFound is not True:
                    print('Found GUMP')
                    print ('######FOUND AFK CHECK GUMP ID#########')
                    send_discord_message(DISCORD_WEBHOOK,'******** (AFKGUMP) @everyone WARNING! AFK GUMP DETECTED!! Char: '+ str(CharName()) +'. '+str(charFunction)+' ********')
                    GMGumpFound = True

                    #superDebug('Gumps Count:' + str(GetGumpsCount()))
                    #id = GetGumpID(GetGumpsCount()-1)
                    #superDebug('Gump Id:' + str(id))
                    #gumpFullInfo = GetGumpFullInfo(GetGumpsCount()-1)
                    gumpInfo = GetGumpInfo(GetGumpsCount()-1)
                    #with open('gump-debug.txt','w') as file:
                    debugGumpFile = open(StealthPath()+GUMP_DEBUG_FILE, 'a+')
                    #print(gumpInfo)
                    debugGumpFile.writelines('\n\n\n---------------GUMP FOUND! Char:'+ str(CharName()) +'----------------')
                    debugGumpFile.writelines('\n-------'+str(datetime.now())+'-------\n')
                    json.dump(gumpInfo, debugGumpFile)
                
                    gumpFullLines = GetGumpFullLines(GetGumpsCount()-1)
                    print(gumpFullLines)
                    debugGumpFile.writelines('\n-------FULL LINES-------\n')
                    json.dump(gumpFullLines, debugGumpFile)
                    for gump in range(GetGumpsCount()-1):
                        idd = GetGumpID(gump)
                    
                        debugGumpFile.writelines('\n-------ID - for-------\n')
                        gumpInfo = GetGumpInfo(idd)
                        json.dump(gumpInfo, debugGumpFile)

                        gumpFullLines = GetGumpFullLines(idd)
                        debugGumpFile.writelines('\n-------FULL LINES - for-------\n')
                        json.dump(gumpFullLines, debugGumpFile)

                    debugGumpFile.close()
            if id == AFK_GUMP:
               

                if GMGumpFound is not True:
                    #TRYING TO PRESS CHECKBOX
                    print ('PRESSING CHECKBOX')
                    Wait (5000) #waiting 5 seconds just to pretend
                    button = gumpInfo['GumpButtons'][0]['ReturnValue']
                    waitgumpid_press(id, int(button), True, 5)
                    #Wait (600000) # Wait for 10 Minutes
            #else:
                #close_gumps()

def check_if_in_jail(charFunction = ''):
    currentX = GetX(Self())
    currentY = GetY(Self())
    global InJail

    if (currentX >= JAIL_X_TOP_LEFT) and (currentX <= JAIL_X_BOTTOM_RIGHT):
        if (currentY >= JAIL_Y_TOP_LEFT) and (currentY <= JAIL_Y_BOTTOM_RIGHT):
            if InJail is not True:
                try:
                    PlayWav(WAV_AFK)
                except:
                    pass
                print('########IN JAIL!!!########')
                send_discord_message(DISCORD_WEBHOOK,'******** (JAIL) @everyone WARNING!!! CHAR NA JAIL!!!!!! Char: '+ str(CharName()) +'. '+str(charFunction)+' ********')
                InJail = True

def check_gump_exists(gumpid):
    for i in range(GetGumpsCount()):  
        if gumpid and gumpid == GetGumpID(i):
            return True
    return False    

def waitgumpid_press(gumpid, number=0, pressbutton=True, timeout=15):
    maxcounter = 0
    while maxcounter < timeout * 10:
        if IsGump():
            for currentgumpnumb in range(0, (GetGumpsCount())):
                currentgump = GetGumpInfo(currentgumpnumb)
                if 'GumpID' in currentgump:  # got to check if key exists or we might get an error
                    if currentgump['GumpID'] == gumpid:
                        if pressbutton:
                            NumGumpButton(currentgumpnumb, number)
                        else:
                            return currentgump
                        return True
                if IsGumpCanBeClosed(currentgumpnumb):
                    CloseSimpleGump(currentgumpnumb)
        maxcounter += 1
        CheckLag(100000)
    return False

def close_gumps():
    while IsGump():
        if not Connected():
            return False
        if not IsGumpCanBeClosed(GetGumpsCount() - 1):
            return False
            #WaitGump('0')
        else:
            CloseSimpleGump(GetGumpsCount() - 1)
    return True
                                               

def send_full_discord_message(webhook_url, user, discord_id ,room, message):
    # colors: https://gist.github.com/thomasbnt/b6f455e2c7d743b796917fa3c205f812
    # test-server webhook
    webhook_url='https://discord.com/api/webhooks/855048334115864618/eOOnHkuc7hd3ojROkoxq8DggBaOZ8wfo7XZD3tAn2c6mHqnNZ57I7RxiNuEWUeb4lSgB'
    
    embed = DiscordEmbed(title=(' Char: '+user), description='', color='0x212')
    # set author
    embed.set_author(name='**** ARTIFACT *****', icon_url='https://www.uoguide.com/images/thumb/8/8d/Doom-gauntle.png/700px-Doom-gauntle.png')

    # set image
    #embed.set_image(url='https://www.uoguide.com/images/1/11/Ornament_Of_The_Magician.png')

    # set thumbnail
    embed.set_thumbnail(url='https://www.uoguide.com/images/1/11/Ornament_Of_The_Magician.png')

    # set footer
    #embed.set_footer(text='For your valor in defeating the fallen creature, you have been rewarded with a special artifact.')

    # set timestamp (default is now)
    embed.set_timestamp()

    # add fields to embed                                       
    embed.add_embed_field(name='Artifact: ',value='Ornament of the Magician')
    embed.add_embed_field(name=('Room: '+str(room)), value='Darknight Creeper') 
    value = 12235
    embed.add_embed_field(name='Tithing points: ', value=f'{value:,}'   )


    webhook = DiscordWebhook(url=webhook_url)
    webhook.add_embed(embed)
    webhook.execute()
    return 
 
def send_temp_discord_message(webhook_url, message):
    webhook_url='https://discord.com/api/webhooks/855048334115864618/eOOnHkuc7hd3ojROkoxq8DggBaOZ8wfo7XZD3tAn2c6mHqnNZ57I7RxiNuEWUeb4lSgB'
    webhook = DiscordWebhook(url=webhook_url, content=str(message))
    sent_webhook = webhook.execute() 
    sleep(1)  
    webhook.delete(sent_webhook)

    return 
   
def send_discord_message(webhook_url, message):
    try:
        webhook = DiscordWebhook(url=webhook_url, content=str(message))
        webhook.execute()
    except:
        print('Something else went wrong')
    return 

                     
#################################################################################################################################################
############# **DO NOT CHANGE**  ############ **DO NOT CHANGE ** ############## **DO NOT CHANGE**  ############ **DO NOT CHANGE ** ##############
############# **DO NOT CHANGE**  ############ **DO NOT CHANGE ** ############## **DO NOT CHANGE**  ############ **DO NOT CHANGE ** ##############
# ==============================================================================================================================================#
#                                                               ATTACK ROUTINES                                                                 #
# ==============================================================================================================================================#

def honorable_execution():  
    WEAK_MOBS = [0x03, 0x99, 0x001A, 0xEE,0xd0,0xcb,0xed,0x122,0xcd,0x6,0xd9,0xcf,0xc9,0xee,0xd8,0xe7,0xd1,0x33,0x27,0x34]
    enemy = 0 
    if FindTypesArrayEx(WEAK_MOBS ,[0xFFFF],[Ground()],False):
        founds = GetFindedList()  
        if(len(founds) > 0):
            for found in founds:
                if GetType(found) in WEAK_MOBS:
                    enemy = found
                    if GetDistance(enemy) < 2: 
                        ClientPrintEx(Self(), 66, 1, 'Honorable Execution')  
                        print('Honorable Execution')
                        ClientPrintEx(enemy, 16, 1, '** KILL ME **')
                        break
                    else:  
                        ClientPrintEx(enemy, 5, 1, '** LURE **')
                        Attack(enemy)

    
            if (enemy != 0 and GetDistance(enemy) < 2): 
                if not is_bufficon_activated('Honorable Execution'):
                    Cast('Honorable Execution')
                       
      
def handle_blood_oath():
    global timer_apple     
    timer_blood_oath = datetime.now()
    while is_bufficon_activated('Blood Oath'):  
        SetWarMode(False)   
        if is_bufficon_activated('Counter Attack'):
            cast_confidence(1,True)  
        for i in range(1,3): 
            if FindType(0x2FD8,Backpack()):
                print('Usando APPLE')
                UseType(0x2FD8,0x0488)
                Wait(100)
            if not is_bufficon_activated('Blood Oath'):
                break
        cast_remove_curse()  
        if datetime.now() >= timer_blood_oath+timedelta(seconds=12):  
            # sera que eh bom deixar o buff curse weapon ativo? vou testar castar mais para o final do tempo do BO, caso nao tenha sido retirado 
            cast_curse_weapon()      
    timer_apple = datetime.now()  

def check_mount_before_leave():
    global pet_dead
    global PET
    tries = 0
    ########### CHECK FOR DISMOUNT BEFORE LEAVING ROOM ############# 
    while ObjAtLayer(HorseLayer()) == 0:
        if Dead() or not Connected():
            return
        if not is_bufficon_activated('Dismount'):
            # if pet is dead, try to ress
            if GetHP(PET) <= 0 and GetDistance(PET) >= 0:
                pet_dead = True
                if check_gump_exists(0x4DA72C0):         
                    waitgumpid_press(0x4DA72C0,1,2) 
                    pet_dead = False
                    if ObjAtLayer(HorseLayer()) != 0:
                        UseObject(Self())
                        Wait(600)
            # if pet is alive, try to mount
            if GetHP(PET) > 0:
                pet_dead = False
                if GetDistance(PET) >= 2:
                    NewMoveXY(GetX(PET), GetY(PET), False, 1, True)
                if ObjAtLayer(HorseLayer()) != 0:
                    UseObject(Self())
                    Wait(600)
                cast_heal_cure_target(PET)
                UseObject(PET)
                Wait(100)                                          
            elif ObjAtLayer(HorseLayer()) == 0:        
                if ETHY != 0:
                    pet_dead = True
                    UseObject(ETHY)
                    Wait(1000)
            tries += 1
            if tries > 10:
                break
        Wait(50) 

def handle_pet():
    global BOSS
    global pet_dead  
    # if pet is dead, try to ress
    if GetHP(PET) <= 0 and GetDistance(PET) >= 0:
        pet_dead = True
        if check_gump_exists(0x4DA72C0):         
            waitgumpid_press(0x4DA72C0,1,2) 
            pet_dead = False
            if ObjAtLayer(HorseLayer()) != 0:
                UseObject(Self())
                Wait(1000)
            
    # if pet is alive, try to mount
    if GetHP(PET) > 0 and not IsPoisoned(PET) and (GetHP(PET) < GetMaxHP(PET)*0.6 or GetHP(BOSS) < GetMaxHP(BOSS)*0.1):
        if ObjAtLayer(HorseLayer()) != 0:
            UseObject(Self())
            Wait(600)
        if not is_bufficon_activated('Dismount'):
            if GetDistance(PET) >= 2:
                NewMoveXY(GetX(PET), GetY(PET), False, 1, True)
            UseObject(PET)  
            Wait(600)
            
    # Lesser Hiryu
    if PET_TYPE == 0x0F3:
        if GetHP(PET) > 0:
            pet_dead = False
            cast_heal_cure_target(PET, 0.8)              
            
    

BOSS = 0
pet_dead = False
def unmount_and_attack(enemy):
    global BOSS
    global pet_dead        
    #print('pet dead ? ' + str(pet_dead))
    if ObjAtLayer(HorseLayer()) != 0 and PET_TYPE == 0x0F3 and enemy != BOSS and GetDistance(enemy) < 2 and not pet_dead:
        UseObject(Self())
        Wait(500)

    if PET_TYPE == 0x0F3 and enemy != BOSS and GetDistance(enemy) < 2 and not pet_dead and GetType(enemy) in MOB_TYPES:
        UOSay("All Kill")
        WaitForTarget(500)
        TargetToObject(enemy)

def use_conflag():
    # FINDING IF THERES ALREADY A CONFLAG     
    if (FindType(0x398C, Ground()) <= 0):   
        if FindType(0x0F06, Backpack()):    
            print('Using CONFLAG') 
            UseType(0x0F06, 0x0489)
            WaitForTarget(1000)
            if TargetPresent:
                TargetToObject(Self())  
                Wait(200)     

def is_in_danger():
    return GetHP(Self()) < GetMaxHP(Self())*0.5 and not is_bufficon_activated('Curse Weapon') and not Dead() 
 
def find_boss_or_traps(boss, room, double_check = False):
    # FINDING BOSS 
    enemy = 0                       
    traps_found = False
    mob_nearby = get_mobs_nearby()  
    if mob_nearby != 0:
        enemy = mob_nearby
        ClientPrintEx(Self(), 5, 1, 'ATACCKING MOBS NEARBY') 
    elif FindTypesArrayEx([boss], [0xFFFF], [Ground()], False):
        founds = GetFindedList()  
        if len(founds) > 0:
            enemy = founds[0]
            if(not is_in_danger() and room != 4):
                mobhp = GetHP(enemy)  
                for found in founds:
                    if GetHP(found) < mobhp: 
                        enemy = found
                        mobhp = GetHP(found) 
                        
            else:
                mindistance = GetDistance(enemy)  
                for found in founds:
                    if GetDistance(found) < mindistance: 
                        enemy = found
                        mindistance = GetDistance(found)          
    else:
        # FINDING TRAPS
        ClearBadObjectList()
        ClearBadLocationList() 
        #if room == 4 or double_check:
        #    Wait(600)
        SetFindDistance(18) 
        if FindTypesArrayEx(TRAPS_TYPES, [0xFFFF], [Ground()], False):   
            SetFindDistance(25)
            traps = GetFindedList() 
            for trap in traps:
                if GetType(trap) not in TRAPS_TYPES:
                    if GetType(trap) not in MOB_TYPES:
                        Ignore(trap)         
                    continue
                elif IsObjectExists(trap):  
                    if room == 6:
                        if GetX(trap) >= 475:
                            traps_found = False 
                            print('NAO ACHOU TRAP PELO GETX')
                            break
                    if room == 4 or double_check:  
                        # DOUBLE CHECK FOR TRAPS  
                        ClearJournal()
                        ClickOnObject(trap)
                        Wait(600)
                        tooltip = str(GetTooltip(trap))
                        if GetTooltip(trap) != '' and check_journal(tooltip): 
                            traps_found = True #SE ACHAR PELO MENOS UMA TRAP NO JOURNAL 
                            break                  
                    else:
                        traps_found = True
                        break
                else:       
                    print('NAO ACHOU TRAP PELO OBJETO NAO EXISTE')
                    if GetType(trap) not in [boss]:
                        Ignore(trap)              
                    traps_found = False
                    break
        SetFindDistance(25)

    if enemy:
        return enemy
    elif traps_found:
        return 0
    else:
        return -1


def set_ability_or_ls(timer_sm):
    if (datetime.now() >= timer_sm+timedelta(seconds=3) or GetMana(Self()) >= 20) and GetActiveAbility() != 'Double Strike' and is_bufficon_activated('Consecrate Weapon', datetime.now()):   
        UsePrimaryAbility() 
        return True  
    elif not is_bufficon_activated('Lightning Strike') and GetMana(Self()) >= 10 and GetActiveAbility() != 'Double Strike':  
        Cast('Lightning Strike')
        return False
    else:
        UsePrimaryAbility() 
        return True   

def print_boss_lifebar(enemy):
    if GetHP(enemy) > 0:
        if GetHP(enemy)*4 > 10:
            print('[' + str(GetHP(enemy)*4) + '%] [', end='')
        else:
            print('[' + ' ' + str(GetHP(enemy)*4) + '%] [', end='')
        print('*'*(GetHP(enemy)), end='')
        print('-'*(25-GetHP(enemy)), end='')
        print(']')
        
        

def attack_room_one_two_three_five(mob, room):
    if Dead():
        return GetX(Self()), GetY(Self())
    # reset corpse ids
    #IgnoreReset() 
    # timer for enemy_of_one
    global timer_start_boss
    # timer for evasion
    global timer_evasion  
    # timer for apple
    global timer_apple
    # timer for special move
    timer_sm = datetime.now()
    # timer for search boss
    timer_search_boss = datetime.now() 
    # global boss variable 
    global BOSS                                              
    
    ########### SECURITY CHECK FOR WEAPON ############                
    security_equip_weapon() 
    find_loot_and_ignore_dead_corpses(room, False)
    set_traps_as_bad_locations()
     
    rail = {
        1 : [[491,450], [490,424]] , 
        2 : [[481,514], [460,520], [492,524], [486,505], ],
        3 : [[408,532], [389,536], [424,538],], 
        5 : [[326,429], [313,440], [321,419],],
    }                                                              

    if find_boss_or_traps(mob, room) > 0: 
        cast_consecrate_weapon(force = True, wait = False)
        
    priority = True  
    tries = 0  
    enemy = 0  
    
    while True: 
        if Dead():
            break   
            
        if is_bufficon_activated('Paralyze'):
            Wait(200)
            continue                            
            
        if find_loot_and_ignore_dead_corpses(room):
            insure_items(room)
            
        
        enemy = find_boss_or_traps(mob, room, datetime.now() >= timer_search_boss+timedelta(seconds=15))   
         
        if (enemy == 0):
            if datetime.now() >= timer_search_boss+timedelta(seconds=5):
                print('Enemy = 0, trying to find him, room: ' + str(room))
                pos = rail[room][tries]                
                print('going to rail pos: ' + str(pos[0]) + ' ' + str(pos[1]) + ' try: ' + str(tries))
                NewMoveXY(pos[0], pos[1], False, 1, True)
                tries += 1
                if tries >= len(rail[room]):
                    tries = 0
                    break
            
        
        elif (enemy > 0):  
            cast_dispel_evil() 
            timer_search_boss = datetime.now()
            tries = 0
            if (datetime.now() >= timer_sm+timedelta(seconds=3) or GetMana(Self()) >= 20) and GetActiveAbility() != 'Double Strike' and is_bufficon_activated('Consecrate Weapon', datetime.now()):   
                UsePrimaryAbility() 
                timer_sm = datetime.now()   
            elif not is_bufficon_activated('Lightning Strike') and GetMana(Self()) >= 10 and GetActiveAbility() != 'Double Strike':  
                Cast('Lightning Strike')
                        
            if (FOLLOW and not is_in_danger() and IsObjectExists(enemy) and GetHP(enemy) > 0 and GetDistance(enemy) > 0):
                NewMoveXY(GetX(enemy),GetY(enemy), False, 1, True)

            handle_blood_oath() 
            if IsObjectExists(enemy): 
                Attack(enemy)            
                unmount_and_attack(enemy) 
                #print_boss_lifebar(enemy)
                if BOSS != enemy and GetDistance(enemy) < 2:    
                    BOSS = enemy
                    ClientPrintEx(enemy, 33, 0, '* BOSS *')  
                    ClientPrintEx(enemy, 33, 0, '* BOSS *')
                    ClientPrintEx(enemy, 33, 0, '* BOSS *')
                                 

            ########### DANGER -> MOVE AWAY? ############
            if is_in_danger():
                if MOVEAWAY: 
                    keep_distance(enemy)
                    cast_heal_cure_self()
                priority = False   
                
            ########### CHIVALRY SPELLS ############
            # ENEMY OF ONE
            if ENEMYOFONE:  
                cast_enemy_of_one(timer_start_boss)
                                                                           
            if not is_in_danger():
                cast_remove_curse()

            priority = not(cast_consecrate_weapon())                                                             
            # DIVINE FURY
            if not priority:
                cast_divine_fury()  
             
            ########### CURSE WEAPON ############
            if CURSEWEAPON and GetDistance(enemy) < 2:    
                cast_curse_weapon()      
            
            ########### BUSHIDO SPELLS #############
            cast_confidence(0.6)
            cast_counter_attack()                     
            cast_confidence(0.4,True)

        else:   
            break # NO BOSS FOUND AND NO TRAP FOUND             

        ########### DISMOUNT #############
        handle_pet()      
    
    ########### CHECK FOR HP AND CURE/HEAL SELF BEFORE LEAVING ROOM #############  
    if GetHP(Self()) < GetMaxHP(Self())*0.8 or (CURE_AFTER_ROOM_ONE and IsPoisoned(Self()) ):
        while IsPoisoned(Self()):
            if is_bufficon_activated('Blood Oath'):
                SetWarMode(False)
            else:
                mob_nearby = get_mobs_nearby() 
                if mob_nearby != 0 and IsObjectExists(mob_nearby): 
                    Attack(mob_nearby)
            cast_heal_cure_self(confidence = False)
        cast_confidence(1, True)

    check_mount_before_leave()
    ClearBadLocationList()
    find_loot_and_ignore_dead_corpses(room)
    insure_items(room)
    return GetX(Self()), GetY(Self())                            

def attack_room_four(mob):
    room = 4             
    if Dead():
        return GetX(Self()), GetY(Self())
    # reset corpse ids
    #IgnoreReset() 
    # timer for enemy_of_one
    global timer_start_boss
    # timer for evasion
    global timer_evasion   
    # timer for conflag
    timer_conflag = datetime.now()- timedelta(seconds=30)
    # timer for special move
    timer_sm = datetime.now()
    # timer for warning messages
    timer_messages = datetime.now() - timedelta(seconds=10)  
    # global boss variable 
    global BOSS        
    
    ########### SECURITY CHECK FOR WEAPON ############                
    security_equip_weapon() 
    
    find_loot_and_ignore_dead_corpses(room, False)
    set_traps_as_bad_locations()                      
 
    boss4_hidden = False      
    priority = True
    
    if find_boss_or_traps(mob, room) > 0: 
        cast_consecrate_weapon(force = True, wait = False)
    
    rail = [
        [338,508],
        [331,519],
        [345,519],    
        [345,495], 
        [328,495],
    ] 
    
    n = 0
    enemy = 0            
    
    while True:        
        if Dead():
            return GetX(Self()), GetY(Self())
        if is_bufficon_activated('Paralyze'):
            Wait(200)
            continue
        
        if find_loot_and_ignore_dead_corpses(room):
            insure_items(room)                
            
        enemy = find_boss_or_traps(mob, room, boss4_hidden) 

        if (enemy == 0):                          
            #BUG FOR SEARCH FOR HIDDEN BOSS
            if(not boss4_hidden): 
                timer_boss4 = datetime.now()  
         
            if(not is_bufficon_activated('Enemy Of One', timer_boss4+timedelta(seconds=10))) and GetMana(Self()) > 14:
                #n = tries // len(rail)
                pos = rail[n]                
                #print('going to rail pos: ' + str(pos[0]) + ' ' + str(pos[1]) + ' n: ' + str(n))
                NewMoveXY(pos[0], pos[1], False, 1, True)
                timer_boss4 = datetime.now()
                mana_before = GetMana(Self())   
                Cast('Enemy Of One')   
                Wait(1000)                   
                if GetMana(Self()) < mana_before :
                    n = n + 1
                if n >= len(rail):
                    n = 0    
                    break
            boss4_hidden = True
        
        elif (enemy > 0):   
            cast_consecrate_weapon() 
            boss4_hidden = False
            cast_dispel_evil()
            n = 0
            if (IsHidden(enemy) and GetDistance(enemy) < 2):
                if datetime.now() >= timer_conflag+timedelta(seconds=30):
                    use_conflag()                                       
                    timer_conflag = datetime.now()
                cast_holy_light()    
             
            if (datetime.now() >= timer_sm+timedelta(seconds=3) or GetMana(Self()) >= 20) and GetActiveAbility() != 'Double Strike' and is_bufficon_activated('Consecrate Weapon',datetime.now()):   
                UsePrimaryAbility()
                timer_sm = datetime.now()   
            elif not is_bufficon_activated('Lightning Strike') and GetMana(Self()) >= 10 and GetActiveAbility() != 'Double Strike': 
                Cast('Lightning Strike')
            
            if IsObjectExists(enemy):
                Attack(enemy)   
                #unmount_and_attack(enemy)
                if BOSS != enemy and GetDistance(enemy) < 2:    
                    BOSS = enemy
                    ClientPrintEx(enemy, 33, 0, '* BOSS *')  
                    ClientPrintEx(enemy, 33, 0, '* BOSS *')
                    ClientPrintEx(enemy, 33, 0, '* BOSS *')
            
            if (FOLLOW and not is_in_danger()):
                NewMoveXY(GetX(enemy), GetY(enemy), False, 1, True) 
            
            ########### DANGER -> MOVE AWAY? ############
            if is_in_danger():
                if MOVEAWAY: 
                    keep_distance(enemy)  
                    cast_heal_cure_self()
                priority = False
                
            ########### CHIVALRY SPELLS ############ 
            if not is_in_danger():
                cast_remove_curse()
            
            if GetDistance(enemy) <= 4 and not IsHidden(enemy):
                if ENEMYOFONE:  
                    cast_enemy_of_one(timer_start_boss)
            
            priority = not(cast_consecrate_weapon())         

            if not priority:
                cast_divine_fury()  
                 
            ########### CURSE WEAPON ############    
            if CURSEWEAPON and GetDistance(enemy) < 2:    
                cast_curse_weapon()       
            
            ########### BUSHIDO SPELLS #############
            cast_confidence(0.6)
            cast_counter_attack()                   
            cast_confidence(0.4, True)
        else:
            break        
        ########### DISMOUNT #############
        handle_pet()  

    check_mount_before_leave()
    ClearBadLocationList()
    find_loot_and_ignore_dead_corpses(room)
    insure_items(room)
    return GetX(Self()), GetY(Self())          

 
def is_at_corner():
    return GetX(Self()) == 453 and GetY(Self()) == 419                  
        
def attack_df(mob):
    room = 6
    if Dead():
        return GetX(Self()), GetY(Self())
    # reset corpse ids
    #IgnoreReset() 
    # timer for enemy_of_one
    global timer_start_boss 
    # timer for evasion
    global timer_evasion    
    # timer for apple
    global timer_apple       
    # global variable to kill df at center
    global KILL_DF_CORNER
    # timer for special move
    timer_sm = datetime.now() 
    # timer for warning messages
    timer_messages = datetime.now() - timedelta(seconds=10)   
    # timer for search boss
    timer_search_boss = datetime.now() 
    # global boss variable 
    global BOSS        
        
    ########### SECURITY CHECK FOR WEAPON ############                
    security_equip_weapon()  
    
    find_loot_and_ignore_dead_corpses(room, False)           
    set_traps_as_bad_locations() 
    
    #if find_boss_or_traps(mob, room, True) > 0: 
        #cast_consecrate_weapon(True)    

    priority = True
                    
    rail = [    
        [453,419],
        [432,419],
        [412,431],
        [454,439],    
        [401,412],
        [424,394], 
    ] 

    enemy = 0        
    tries = 0   
    lure_tries = 0 
    timer_lure_boss = datetime.now() - timedelta(seconds=30)
    
    SetGoodLocation(454,419) 
    SetGoodLocation(453,419)
    SetGoodLocation(452,419)
    SetGoodLocation(452,420)                               
    while True:  
        bone_cutter()
        
        if Dead():
            return GetX(Self()), GetY(Self())  
            
        if is_bufficon_activated('Paralyze'):
            Wait(200)
            continue
        
        if find_loot_and_ignore_dead_corpses(room):
            insure_items(room)
        
        enemy = find_boss_or_traps(mob, room, True)

        if (enemy == 0):
            if datetime.now() < timer_search_boss+timedelta(seconds=10) and not is_at_corner(): 
                print('Enemy = 0, lure him to corner at ' + str(rail[tries][0]) + ", " + str(rail[tries][1]))                
                move_thru_doors(rail[tries][0],rail[tries][1], 0, 0, 4, False, open_doors) 
                move_to_corner_if_not_there() # double check 
            elif datetime.now() >= timer_search_boss+timedelta(seconds=15):
                ClearBadLocationList()     
                pos = rail[tries]                
                print('Enemy = 0, trying to find him at '+ str(pos[0]) + ' ' + str(pos[1]) + ' try: ' + str(tries))
                NewMoveXY(pos[0], pos[1], False, 1, True)
                tries += 1
                if tries >= len(rail):
                    tries = 0
            elif GetHP(Self()) < GetMaxHP(Self()):
                cast_heal_cure_self(confidence = False)
                                          
        elif (enemy > 0):   
            cast_dispel_evil()
            timer_search_boss = datetime.now()  
            tries = 0
            if (datetime.now() >= timer_sm+timedelta(seconds=3) or GetMana(Self()) >= 20) and GetActiveAbility() != 'Double Strike' and is_bufficon_activated('Consecrate Weapon',datetime.now()):   
                UsePrimaryAbility()  
                timer_sm = datetime.now()   
            elif not is_bufficon_activated('Lightning Strike') and GetMana(Self()) >= 10 and GetActiveAbility() != 'Double Strike':  
                Cast('Lightning Strike')
                        
            handle_blood_oath()     
            
            if IsObjectExists(enemy): 
                Attack(enemy)    
                if is_at_corner():
                    unmount_and_attack(enemy)
                if BOSS != enemy and GetDistance(enemy) < 2:    
                    BOSS = enemy
                    ClientPrintEx(enemy, 33, 0, '* BOSS *')  
                    ClientPrintEx(enemy, 33, 0, '* BOSS *')
                    ClientPrintEx(enemy, 33, 0, '* BOSS *')
                
            if (FOLLOW and not is_in_danger() and GetType(enemy) in [mob]):
                # chase boss condition:
                # 1) if DF hp is low enough
                # 2) or next to corner
                # 3) or KILL_DF_CORNER disabled 
                if GetHP(enemy) < GetMaxHP(enemy)*0.95 or (GetX(enemy) >= 452 and GetY(enemy) >= 419) or not KILL_DF_CORNER:
                    boss_pos_x = GetX(enemy)
                    boss_pos_y = GetY(enemy)      
                    NewMoveXY(GetX(enemy),GetY(enemy), False,1,True)  
                    if boss_pos_x != GetX(enemy) or boss_pos_y != GetY(enemy):  
                        lure_tries = 0
                    if(KILL_DF_CORNER):                                                                                   
                        if lure_tries <= 3 and datetime.now() >= timer_lure_boss+timedelta(seconds=30) and move_to_corner_if_not_there():
                            ClearBadLocationList()
                            if boss_pos_x == GetX(enemy) and boss_pos_y == GetY(enemy):
                                lure_tries += 1  
                                if lure_tries >= 3:
                                    lure_tries = 0
                                    ClientPrintEx(Self(), 66, 1, 'STOP LURING FOR 30 SECONDS')
                                    timer_lure_boss = datetime.now()    
                            else:
                                ClientPrintEx(Self(), 66, 1, 'BOSS MOVEED!')
                                Wait(500) 
                                lure_tries = 0 
                # if DF is full HP and we're not at corner, lure him to corner 
                elif not is_at_corner():  
                    print('Enemy != 0, lure him to corner at ' + str(rail[tries][0]) + ' ' + str(rail[tries][1]) + ' try: ' + str(tries))
                    Attack(enemy)
                    SetWarMode(True) 
                    SetWarMode(False)                 
                    move_thru_doors(rail[tries][0],rail[tries][1], 0, 0, 4, False, open_doors)    
                # if DF is full HP and we're at corner, heal self 
                elif GetHP(Self()) < GetMaxHP(Self())*0.9:
                    cast_heal_cure_self(confidence = False)
                # if DF is full HP and we're at corner and full HP, cast evasion if we can
                elif GetDistance(enemy) > 3 and datetime.now() > timer_evasion+timedelta(seconds=20):
                    Cast('Evasion')
                    Wait(600)                                            
                    timer_evasion = datetime.now()      
                                                    
            ########### DANGER -> MOVE AWAY? ############
            if is_in_danger():
                if MOVEAWAY: 
                    keep_distance(enemy) 
                    cast_heal_cure_self()
                priority = False
                
                
            ########### CHIVALRY SPELLS ############
            # ENEMY OF ONE
            if ENEMYOFONE and GetType(enemy) in [mob]: 
                cast_enemy_of_one(timer_start_boss)
                                                                           
            if not is_in_danger():
                cast_remove_curse()

            priority = not(cast_consecrate_weapon())         
            
            if not priority:
                cast_divine_fury()  
             
            ########### CURSE WEAPON ############    
            if CURSEWEAPON and GetDistance(enemy) < 2:    
                cast_curse_weapon(0.2,0.95,5)         
            
            ########### BUSHIDO SPELLS #############
            cast_confidence(0.6)
            cast_counter_attack()                     
            cast_confidence(0.4,True)
        else:
            break
        
        ########### DISMOUNT #############
        handle_pet()  
            
    check_mount_before_leave()
    ClearBadLocationList()   
    find_loot_and_ignore_dead_corpses(room)
    insure_items(room)
    return GetX(Self()), GetY(Self())



def set_global_room_status(room):
    if room == 1 or room > 6:   
        SetGlobal('char','Room','One')
    elif room == 2: 
        SetGlobal('char','Room','Two')
    elif room == 3:                   
        SetGlobal('char','Room','Three')
    elif room == 4:
        SetGlobal('char','Room','Four')
    elif room == 5:                   
        SetGlobal('char','Room','Five')
    elif room == 6:                   
        SetGlobal('char','Room','DF')
    

def start_sampire_bot_at_room(room):
    global timer_start_boss
     
    tries = 0
    while True:  
        ########### ATTACK ROUTINES FOR EACH ROOM #############
        if room == 0:
            room = 6      
        if room == 1:   
            lastx, lasty = attack_room_one_two_three_five(0x139,1)
        elif room == 2:
            lastx, lasty = attack_room_one_two_three_five(0x13b,2) 
        elif room == 3:       
            lastx, lasty = attack_room_one_two_three_five(0x132,3)  
        elif room == 4:    
            lastx, lasty = attack_room_four(0x137) 
        elif room == 5: 
            lastx, lasty = attack_room_one_two_three_five(0x138,5)
        else:      
            lastx, lasty = attack_df(0x13e)   
        
        SetWarMode(False)  
        
        ########### DEATH CHECK AND RESS #############                    
        if Dead():          
            x, y = GetX(Self()), GetY(Self())
            go_to_saferoom_and_ress(room)
            set_global_room_status(room) 
            get_body_corpse_back(room, x, y)
            return  
            
        ########### DURABILITY CHECK    #############
        if check_low_durability_equip():
            go_to_safe_and_fix_equipment() 
            return

        ########### TITHINGPOINTS CHECK #############
        if check_low_tithing_points():
            go_to_safe_and_logout()

        set_global_room_status(room + 1)             
        
        ########### SECURITY CHECK ############# 
        if tries >= 2 and tries < 10:
            print('SECURITY BREAK GOTOROOM!!!')
            send_discord_message(DISCORD_WEBHOOK,'******** (STUCK) ALERT '+ get_user_id(DISCORD_ID) +' GM ONLINE? ' + ' | Char: '+ str(CharName()) + ' STUCK @ Room: ' + str(room) +' ********')                                                                                              
                                         
        ########### TRY TO LEAVE ROOM #############
        timer_start_boss = datetime.now() 
        leave_room(room)               
        if not go_to_room(room + 1):
            tries = tries + 1   
            print('Going to last position - ' + str(lastx) + ' ' +   str(lasty))
            NewMoveXY(lastx, lasty, False,0,True)  # Back to the center of room in case the door is closed 
            continue      
            
        tries = 0   
        room = room + 1
        if room > 6:
            room = 1          
        
def search_boss_or_go_to_center():
    SetFindDistance(25)
    SetFindVertical(10)
    enemy = 0        
    while True:         
        if Dead():
            go_to_saferoom_and_ress()
            return
        ########### TITHINGPOINTS CHECK #############
        if check_low_tithing_points():
            go_to_safe_and_logout()
        if FindTypesArrayEx(MOB_TYPES ,[0xFFFF],[Ground()],False): 
            founds = GetFindedList()
            for found in founds:   
                tipo = GetType(str(found))
                if tipo == 0x139:     
                    SetGlobal('char','Room','One')
                    start_sampire_bot_at_room(1)
                    break
                elif tipo == 0x13b:  
                    SetGlobal('char','Room','Two')
                    start_sampire_bot_at_room(2)
                    break
                elif tipo == 0x132:  
                    SetGlobal('char','Room','Three')
                    start_sampire_bot_at_room(3)
                    break
                elif tipo == 0x137: 
                    SetGlobal('char','Room','Four')
                    start_sampire_bot_at_room(4)
                    break
                elif tipo == 0x138: 
                    SetGlobal('char','Room','Five')
                    start_sampire_bot_at_room(5)
                    break
                elif tipo == 0x13e:        
                    SetGlobal('char','Room','DF')
                    start_sampire_bot_at_room(6)
                    break 
                else:
                    break
        else: 
            if (find_helper_bot(find_players(15)) >= 0):
                print('Exiting safe room and going to center')
                NewMoveXY(489,371, False,0,True)  # Center of safe room
                move_steps_direction(55,6)
                ClearBadLocationList() #Tem q ter esse segundo clearBadLocation se não da pau
                move_steps_direction(5,6)  
                wait_lag(600)
                ClearBadLocationList() #Tem q ter esse segundo clearBadLocation se não da pau
                NewMoveXY(423,371, False,1,True)  #Antes de Virar
            while is_in_hallway():   
                move_steps_direction(1,6)
            #GO TO CENTER  
            move_thru_doors(423, 430, 0, 0, 4, True, open_doors)
            room = 0
            if (GetColor(0x407A35F1) == 1654):
                room = 1
                SetGlobal('char','Room','One')
            elif (GetColor(0x407A35FE) == 1654):
                room = 2
                SetGlobal('char','Room','Two')
            elif (GetColor(0x407A360B) == 1654):
                room = 3
                SetGlobal('char','Room','Three')
            elif (GetColor(0x407A3618) == 1654):
                room = 4
                SetGlobal('char','Room','Four')
            elif (GetColor(0x407A3625) == 1654):
                room = 5
                SetGlobal('char','Room','Five')
            else:
                SetGlobal('char','Room','DF')
                room = 6
            if room > 0:
                go_to_room(room)
                start_sampire_bot_at_room(room)

# Background thread to ease the sampire. Checks for AFK GUMP, GM appearance, swap weapons, honor and more
def background_helper():
    global last_tithingpoints_check
    global timer_deaths_in_a_row_check 
    honored = False
    room = GetGlobal('char','Room')
    timer_start = datetime.now()      
    SetGlobal('char','Room','Next')
    honored_list = []
    while True:
        if not Dead() and Connected(): 
            while( not Connected()):
                SetARStatus(True)
                SetPauseScriptOnDisconnectStatus(False)
                Wait(1000)
            
            if GetGlobal('char','Room') == 'Ress':
                Wait(2000)
                continue                  
                
            ########### TITHINGPOINTS CHECK #############
            check_low_tithing_points()           
                            
            if GetGlobal('char','Room') == 'One' or GetGlobal('char','Room') == 'Four':
                equip_weapon(UNDEAD_SLAYER)           
                Wait(1000)
            elif GetGlobal('char','Room') == 'Two':
                equip_weapon(QSTAFF_AUX)
                Wait(1000)
            elif GetGlobal('char','Room') == 'Five' or GetGlobal('char','Room') == 'Three'  or GetGlobal('char','Room') == 'DF':
                equip_weapon(DEMON_SLAYER)
                Wait(1000)     
                
            if GetGlobal('char','Room') != 'Next': 
                timer_start = datetime.now()
                post_user() 
                SetGlobal('char','Room','Next') 
                honored = False
                honored_list = []
                # organize reagents in backpack          
                get_pieces_together()
                                          
            
            cast_enemy_of_one(timer_start)
            
            cast_divine_fury(40)

            if is_bufficon_activated('Blood Oath'):
                SetWarMode(False)

            cast_confidence(0.7)    

            #### HONOR ##### 
            if USEHONOR and not honored: 
                if honor_mob(honored_list) == 0:
                    honored = True

            check_afk_gump('Doom')
            check_if_in_jail('Doom')                
            is_gm_present()

            Wait(300)


class VerifyTraps(threading.Thread):
    def __init__(self):
        super(VerifyTraps, self).__init__(daemon=True)
        self._running = False
        self._finded = None  
        self._timer_start_check_traps = datetime.now() - timedelta(minutes=1)
         
    def finded(self):
        return self._finded

    def active(self):
        return self._running
    
    def feedback(self, changed = False):
        if changed or datetime.now() >= self._timer_start_check_traps + timedelta(seconds=1):
            self._timer_start_check_traps = datetime.now()
            if self._finded:
                print('--------------- ACHEI TRAPS ---------------')
            else:
                print('--------------- SUMIRAM TRAPS -------------')

    def run(self):
        SetFindDistance(12)
        self._running = True
        while self._running is True:
            last = self._finded
            if FindTypesArrayEx(TRAPS_TYPES, [0xFFFF], [Ground()], False) > 0:    
                self._finded = True
            else:                 
                self._finded = False
            Wait(100)           
            r = (last != self._finded)
            self.feedback(r)
    
    def terminate(self):
        self._running = False
        self._finded = None


class SampireWindow(threading.Thread):
    def __init__(self):
        global sg
        super(SampireWindow, self).__init__(daemon=True)
        self._running = False
        self._window = None  
        if sg is None: 
            self.terminate() 

         
    def finded(self):
        return self._finded
    
    def active(self):
        return self._running 
                 
    def modify_flags(self,event):
        if self._window is None:
            return
        global KILL_DF_CORNER
        global CURE_AFTER_ROOM_ONE
        global FOLLOW     
        global MOVEAWAY 
        global BONECUTTER
        global GOTOSAFEANDLOGOUT
        if event == '1':
            if KILL_DF_CORNER:   
                self._window['1'].Update(button_color=('black', 'red'))
                self._window['1'].Update('OFF')  
                KILL_DF_CORNER = False
            else:
                self._window['1'].Update(button_color=('black', 'green'))
                self._window['1'].Update('ON') 
                KILL_DF_CORNER = True     
        elif event == '2':
            if CURE_AFTER_ROOM_ONE:
                self._window['2'].Update(button_color=('black', 'red'))
                self._window['2'].Update('OFF')  
                CURE_AFTER_ROOM_ONE = False
            else:
                self._window['2'].Update(button_color=('black', 'green'))
                self._window['2'].Update('ON') 
                CURE_AFTER_ROOM_ONE = True   
        elif event == '3':
            if FOLLOW:
                self._window['3'].Update(button_color=('black', 'red'))
                self._window['3'].Update('OFF')  
                FOLLOW = False
            else:
                self._window['3'].Update(button_color=('black', 'green'))
                self._window['3'].Update('ON') 
                FOLLOW = True    
        elif event == '4':
            if MOVEAWAY:
                self._window['4'].Update(button_color=('black', 'red'))
                self._window['4'].Update('OFF')  
                MOVEAWAY = False
            else:
                self._window['4'].Update(button_color=('black', 'green'))
                self._window['4'].Update('ON') 
                MOVEAWAY = True  
        elif event == '5':
            if BONECUTTER:
                self._window['5'].Update(button_color=('black', 'red'))
                self._window['5'].Update('OFF')  
                BONECUTTER = False
            else:
                self._window['5'].Update(button_color=('black', 'green'))
                self._window['5'].Update('ON') 
                BONECUTTER = True    
        elif event == '6':
            if GOTOSAFEANDLOGOUT:
                self._window['6'].Update(button_color=('black', 'gray'))
                self._window['6'].Update('-')  
                GOTOSAFEANDLOGOUT = False
            else:
                self._window['6'].Update(button_color=('black', 'navy'))
                self._window['6'].Update('GO') 
                GOTOSAFEANDLOGOUT = True 
        else:
            return
        
    def run(self):
        if sg is None:
            return         
        self._running = True  
        sg.ChangeLookAndFeel('GreenTan')

		# ------ Menu Definition ------ #
        #menu_def = [['&File', ['&Open', '&Save', 'E&xit', 'Properties']], ['&Edit', ['Paste', ['Special', 'Normal', ], 'Undo'], ],	['&Help', '&About...'], ]    
        

		# ------ Column Definition ------ #
        column1 = [[sg.Text('Column 1', background_color='lightblue', justification='center', size=(10, 1))],
				   [sg.Spin(values=('Spin Box 1', '2', '3'), initial_value='Spin Box 1')],
				   [sg.Spin(values=('Spin Box 1', '2', '3'), initial_value='Spin Box 2')],
				   [sg.Spin(values=('Spin Box 1', '2', '3'), initial_value='Spin Box 3')]]

        layout = [
            #[sg.Menu(menu_def, tearoff=True)],
			[sg.Text('Sampirebot for Doom Gauntlet', size=(30, 1), justification='center', font=('Helvetica', 16), relief=sg.RELIEF_RIDGE)],  
            [sg.Text('by Mark and Quaker', size=(32, 1), justification='right', font=('Helvetica', 10))],
			[sg.Frame(layout=[
			    [sg.Text('Kill DF at the corner (ON recommended)', size=(36, 1)), sg.Button('ON' if KILL_DF_CORNER else 'OFF', button_color=('black', 'green' if KILL_DF_CORNER else 'red'), size=(4, 1), font=('Helvetica', 10) , key='1', tooltip='Enable to lure and kill the DF at the corner position') ], 
                [sg.Text('Cure self before next room (ON recommended)', size=(36, 1)), sg.Button('ON' if CURE_AFTER_ROOM_ONE  else 'OFF', button_color=('black', 'green' if CURE_AFTER_ROOM_ONE else 'red'), size=(4, 1), font=('Helvetica', 10), key='2', tooltip='Enable to heal/cure yourself before leaving rooms')], 
                [sg.Text('Follow and Chase Boss position', size=(36, 1)), sg.Button('ON' if FOLLOW else 'OFF', button_color=('black', 'green' if FOLLOW else 'red'), size=(4, 1), font=('Helvetica', 10), key='3', tooltip='Enable to keep chasing boss')],  
                [sg.Text('Move away from boss when in danger', size=(36, 1)), sg.Button('ON' if MOVEAWAY else 'OFF', button_color=('black', 'green' if MOVEAWAY else 'red'), size=(4, 1), font=('Helvetica', 10), key='4', tooltip='Enable to move away from boss position when your HP is low')], 
                [sg.Text('Cut bones thrown by the Dark Father', size=(36, 1)), sg.Button('ON' if BONECUTTER else 'OFF', button_color=('black', 'green' if BONECUTTER else 'red'), size=(4, 1), font=('Helvetica', 10), key='5', tooltip='Enable bonecutter') ], 
                [sg.Text('Check this to go to safe room and logout', size=(36, 1)), sg.Button('GO' if GOTOSAFEANDLOGOUT else '-', button_color=('black', 'navy' if GOTOSAFEANDLOGOUT else 'gray'), size=(4, 1), font=('Helvetica', 10), key='6', tooltip='Go to safe room and logout after next boss') ],
            ], title=' Flag Options ',title_color='black', relief=sg.RELIEF_SUNKEN)],
            [sg.Text('_' * 50)],
        ]                         
        icone = str(StealthPath())+'Scripts\Dark_Father.ico'                                                                                                         
        self._window = sg.Window('Sampirebot | Char: '+str(CharName()), layout, default_element_size=(40, 1), grab_anywhere=False, icon=icone)  
        # Event Loop to process 'events' and get the 'values' of the inputs
        while True:
            event, values = self._window.read()      
            if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
                break
            elif event is not None:
                self.modify_flags(event)
            else:
                Wait(500)
        self.terminate()

    def terminate(self):     
        print('Closing window')
        self._running = False
        if self._window is not None:
            self._window.close()
        self.__del__()      
    
    def __del__(self):
        print('Thread finished..')  
        

def open_doors():
    DOORS = [0x0675, 0x067, 0x077, 0x0677, 0x067D, 0x067F]    
    DOORS_COLORS = [0x0455, 0x0000]
    SetFindDistance(3)
    SetFindVertical(10)   
    #ClientPrintEx(Self(), 66, 1, 'Trying')
    if FindTypesArrayEx(DOORS, DOORS_COLORS ,[Ground()],False): 
        founds = GetFindedList()
        for found in founds:
            if GetDistance(found) < 3:
                ClientPrintEx(found, 66, 1, 'Door')
                UseObject(found)

    SetFindDistance(25)
    SetFindVertical(10)
    return

def initial_check_and_configs():
    IgnoreReset() 
    SetMoveOpenDoor(True) 
  
    SetFindDistance(25)
    SetFindVertical(10)


    SetMoveThroughNPC(0)
    SetMoveCheckStamina(0)            
    SetARStatus(True)
  
    # DF corner location
    SetGoodLocation(454,419) 
    
    # setting doors as good locations to work properly            
    # doors room #1
    SetGoodLocation(473,432)
    SetGoodLocation(473,433)
    
    # doors room #2
    SetGoodLocation(469,496)
    SetGoodLocation(468,496)
    
    # doors room #3
    SetGoodLocation(408,504)
    SetGoodLocation(409,504)
    
    # doors room #4
    SetGoodLocation(360,478)
    SetGoodLocation(361,478)
    
    # doors room #5
    SetGoodLocation(360,429)
    SetGoodLocation(360,430) 
    
    if GetColor(Self()) != 33918 and not Dead(): 
        dress_lrc_set()
        buy_items_after_ress()
        Wait(1000)
        #Casting Vampiric Embrace 
        cast_vampiric_embrace()    
        dress_main_set()
    
    handle_pet()
    check_mount_before_leave()
    


if __name__ == '__main__':
    print('-------------------------------------------------------------')
    print('-------------------------------------------------------------')
    print('----------- Running SAMPIREBOT by Mark and Quaker -----------')
    print('-------------------------------------------------------------')
    print('-------------------------------------------------------------')
    
    # GUI interface with a few options
    menu_thread = SampireWindow()
    menu_thread.start()

    # background thread to check a few things
    background_helper_thread = threading.Thread(target=background_helper, daemon=True)
    background_helper_thread.start()
    
    # save current set to reequip when die
    save_set()        
    
    # set some configs and also check for vampiric embrace and pet
    initial_check_and_configs()

    # search for alive boss, or go to the main hall and check for active room
    search_boss_or_go_to_center()                  
                