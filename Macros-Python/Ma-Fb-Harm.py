if not TimerExists("magicarrow"):
    CreateTimer("magicarrow")
    SetTimer("magicarrow", 1000)
if GetAlias("Enemy") == GetAlias("self"): 
    UnsetAlias("enemy")
elif TargetExists('harmful') and InRange('enemy',10):
    Target('enemy')
elif InRange('enemy',1) :
    Cast('Harm')
    if WaitForTargetOrFizzle(1000):
        if InRange('enemy', 10):
            Target('enemy')
            #Pause(100)
else:
    if Timer("magicarrow") > 900:  
        SetTimer("magicarrow",0)
        Cast('Magic Arrow')
        if WaitForTargetOrFizzle(700):
            if InRange('enemy', 10):
                Target('enemy')
                #Pause(130)
    else:
        Cast('Fireball')
        if WaitForTargetOrFizzle(1200):
            if InRange('enemy', 10):
                Target('enemy')
                #Pause(180)