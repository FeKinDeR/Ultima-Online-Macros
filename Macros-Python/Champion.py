// Version: 6.0
// Description: Champ with Friends
// Authors: KinDeR
// Instructions:
// Marque a opcao Loop
// Crie um perfil no agents -> dress com todo seu set e renomeie para: MageSuit
// Se voce quiser ser o guia, use o target em voce mesmo.
if not listexists 'foods'
  createlist 'foods'
  @pushlist 'foods' 0x97d
  @pushlist 'foods' 0x9c0
  @pushlist 'foods' 0x9eb
  @pushlist 'foods' 0x97b
  @pushlist 'foods' 0x9f2
  @pushlist 'foods' 0x9d2
  @pushlist 'foods' 0x9b7
  @pushlist 'foods' 0x9d3
  @pushlist 'foods' 0x9d1
  @pushlist 'foods' 0x9d0
endif
if not listexists 'replicas'
  createlist 'replicas'
  @pushlist! 'replicas' 0x1413
  @pushlist! 'replicas' 0x1540
  @pushlist! 'replicas' 0x1f03
  @pushlist! 'replicas' 0x2684
  @pushlist! 'replicas' 0x170b
  @pushlist! 'replicas' 0x1f0b
endif
if not @findobject 'tanker'
  headmsg 'Selecione o Tanker' 55
  promptalias 'tanker'
endif
// Timers
if not timerexists 'renewal'
  @settimer 'renewal' 190000
endif
if not timerexists 'attunement'
  @settimer 'attunement' 280000
endif
// Resurrect
while dead 'self'
  @warmode 'on'
  if @replygump 2957810225 1
    pause 300
  endif
endwhile
// Corpse or Dress
if @findtype 0x2006 'any' 'ground' 748 2 or @findtype 0x2006 'any' 'ground' 747 2
  @useobject! 'found'
  pause 800
  @ignoreobject 'found'
else
  @dress 'MageSuit'
  while dressing
  endwhile
endif
// Transform: wraith form
if @graphic 'self' != 0x2eb and @graphic 'self' != 0x2ec
  if mana >= 16
    @clearjournal
    cast 'wraith form'
    waitforjournal 'disturbed' 'system' 800
    pause 1000
  endif
endif
// Check food
if @findalias 'eat'
  @clearjournal
  cast 'create food'
  waitforjournal 'disturbed' 'self' 500
  @unsetalias 'eat'
elseif stam <= 5
  @setalias 'eat' 'self'
  for 0 to 'foods'
    if @usetype! 'foods[]'
      @unsetalias 'eat'
      break
    endif
  endfor
endif
// Check for replicas
for 0 to 'replicas'
  while @findtype 'replicas[]' 'any' 'backpack'
    if @color 'found' != 0
      waitforproperties 'found' 1500
      if @property 'replica' 'found'
        if not @property 'insured' 'found' and not @property 'blessed' 'found'
          waitforcontext 'self' 3 1500
          waitfortarget 1500
          if @target! 'found'
            waitforproperties 'found' 1500
          endif
        endif
      endif
    endif
    ignoreobject 'found'
  endwhile
endfor
// Actions
@getenemy 'criminal' 'gray' 'innocent' 'closest' //'murderer'
if diffhits 'self' >= 30 or poisoned 'self'
  miniheal 'self'
  while waitingfortarget
  endwhile
elseif hits 'tanker' <= 40 and @inrange 'tanker' 2
  miniheal 'tanker'
  while waitingfortarget
  endwhile
elseif not @inrange 'tanker' 1
  if dead
    break
  elseif @x 'tanker' > x 'self' and @y 'tanker' > y 'self'
    run 'southeast'
  elseif @x 'tanker' < x 'self' and @y 'tanker' > y 'self'
    run 'southwest'
  elseif @x 'tanker' > x 'self' and @y 'tanker' < y 'self'
    run 'northeast'
  elseif @x 'tanker' < x 'self' and @y 'tanker' < y 'self'
    run 'northwest'
  elseif @x 'tanker' > x 'self' and @y 'tanker' == y 'self'
    run 'east'
  elseif @x 'tanker' < x 'self' and @y 'tanker' == y 'self'
    run 'west'
  elseif @x 'tanker' == x 'self' and @y 'tanker' > y 'self'
    run 'south'
  elseif @x 'tanker' == x 'self' and @y 'tanker' < y 'self'
    run 'north'
  endif
elseif @inrange 'enemy' 3 and @inrange 'tanker' 2
  if @findtype 0x3155 0 'backpack'
    if not buffexists 'attune weapon' and mana >= 50
      @clearjournal
      if timer 'attunement' >= 280000
        cast 'attunement'
        waitforjournal 'disturbed' 'system' 100
        @settimer 'attunement' 0
      endif
    endif
    if mana >= 80
      cast 'thunderstorm'
    elseif mana >= 20
      cast 'wither'
    endif
  elseif mana >= 14
    cast 'wither'
  endif
elseif not @inrange 'enemy' 3 and @inrange 'tanker' 2
  if skill 'spellweaving' >= 80 and @findtype 0x3155 0 'backpack'
    if mana >= 70 and not @buffexists 'gift of life'
      cast 'gift of life' 'self'
      while waitingfortarget
      endwhile
    endif
    if mana >= 30 and not buffexists 'gift of renewal'
      if timer 'renewal' >= 190000
        cast 'gift of renewal' 'self'
        while waitingfortarget
        endwhile
        @settimer 'renewal' 0
      endif
    endif
  endif
endif
