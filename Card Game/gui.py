import pygame as pg
from random import randint, uniform, choice
from numpy.random import choice as ch
from math import sin, cos, pi, sqrt, floor
import time
from classes import particleEffect

def renderArrows(hud, mouse, keys, map, win, width, height, mapArrows, mapLocations, clickables, startPos, rotation, player):
    print('Walking')
    particles = []
    numOfArrows = randint(4,12)
    spacer = 40
    dx, dy = 0, 0
    tooLarge=sqrt((width)**2 + (height)**2)
    choices = ['battle', 'cross', 'fire', 'tent', 'town']
    if not player.skip:
        timeBetween = 0.5
    else:
        timeBetween = 0.25
    endTime = numOfArrows*timeBetween
    n=0
    location = startPos
    buffer = 20
    startTime = time.perf_counter()
    now = time.perf_counter()
    while (now-startTime)<endTime:
        now = time.perf_counter()
        if round(time.perf_counter()-startTime,2)==timeBetween*n:
            n+=1
            if player.stamina-1/2<=0:
                player.energy=min(max(round(player.energy/2), player.maxEnergy), player.energy)
                player.stamina+=20
                print('Ran Out oF Stamina')
                print(player)
                break
            else:
                player.stamina-=1/2
            while 0>(startPos[0]+dx-width/buffer) or (startPos[0]+dx+width/buffer)>width or 0>(startPos[1]+dy-height/buffer) or (startPos[1]+dy+height/buffer)>height:
                #print('Hit Boundary', (dx,dy), rotation)
                if not sqrt(dx**2 + dy**2)>=tooLarge:
                    dx+=50*cos(rotation+pi)
                    dy+=50*sin(rotation+pi)
                else:
                    #time.sleep(0.5)
                    dx, dy = 7*dx/8, 3*dy/4
                rotation+=uniform(-pi/4,pi/4)
                location = (startPos[0]+dx,startPos[1]+dy)
                if rotation<0:
                    index=max(-5,min(round(5*(rotation+(pi/2))/pi),5))
                else:
                    index=max(-5,min(round(5*(rotation-(pi/2))/pi),5))
                while rotation>pi:
                    rotation-=pi/3
                while rotation<-pi:
                    rotation+=pi/3
                map.blit(mapArrows[index], (location[0]-(mapArrows[index].get_rect().centerx/2),location[1]-(mapArrows[index].get_rect().centery/2)))
                win.blit(map, (0,0))
                player = hud.update(player, mouse, keys)
                if round(now-startTime,1)==timeBetween*n:
                    n+=1
                    #particles.append(particleEffect(randint(5,10), 'circle', 3, [[128,0,0],[165,42,42],[160,82,45],[139,69,19]], ['sizeDown', -.01], [list(location)[0],list(location)[1]], [0,0], [0,0], [0,0], life=1000*timeBetween))
                for particle in particles:
                    particle.update(win)
                pg.event.pump()
                pg.display.update()
            dx+=spacer*cos(rotation+pi)
            dy+=spacer*sin(rotation+pi)
            rotation+=uniform(-pi/4,pi/4)
            location = (startPos[0]+dx,startPos[1]+dy)
            if rotation<0:
                index=max(-5,min(round(5*(rotation+(pi/2))/pi),5))
            else:
                index=max(-5,min(round(5*(rotation-(pi/2))/pi),5))
            while rotation>pi:
                rotation-=pi/3
            while rotation<-pi:
                rotation+=pi/3
            #print(index, rotation/pi)
            map.blit(mapArrows[index], (location[0]-(mapArrows[index].get_rect().centerx/2),location[1]-(mapArrows[index].get_rect().centery/2)))
            particles.append(particleEffect(randint(5,10), 'circle', 3, [[128,0,0],[165,42,42],[160,82,45],[139,69,19],[210,105,30]], -.005, [list(location)[0],list(location)[1]], [0,0], [0,0], [0,0], life=1000*timeBetween))
            player = hud.update(player, mouse, keys)
            win.blit(map, (0,0))
            for particle in particles:
                particle.update(win)
            #pg.draw.circle(win, (0,0,0), location, 3)
        win.blit(map, (0,0))
        player = hud.update(player, mouse, keys)
        for particle in particles:
            particle.update(win)
        pg.event.pump()
        pg.display.update()
    remIndexs = []
    for particle in particles:
        particle.update(win)
    dx+=spacer*cos(rotation+pi)
    dy+=spacer*sin(rotation+pi)
    location = (startPos[0]+dx,startPos[1]+dy)
    object = ch(choices, p=[.45,.10,.25,0,.20]) #['battle', 'cross', 'fire', 'tent', 'town']
    if player.stamina-1/2<0:
        object = 'tent'
    map.blit(mapLocations[choices.index(object)], (location[0]-mapLocations[choices.index(object)].get_rect().centerx,location[1]-mapLocations[choices.index(object)].get_rect().centery))
    startPos = location
    clickables[location] = [object, mapLocations[choices.index(object)].get_rect()]
    currentLocation = [location, object, mapLocations[choices.index(object)].get_rect()]
    if object == 'battle':
        player.screen = 2
    elif object == 'fire':
        player.stamina = min(player.maxStamina, player.stamina+5)
        player.energy = min(player.maxEnergy, player.energy+10)
    elif object == 'cross':
        bonus = randint(0,2)
        print(f'Bonus: {bonus}')
        if bonus == 0:
            player.deck.pullFromPack(1)
        if bonus == 1:
            player.stamina = player.maxStamina
            player.energy = player.maxEnergy
        if bonus == 2:
            player.expense([randint(-1,0),randint(-100,0),randint(-10,0)])
    elif object == 'town':
        player.skip = False
    return clickables, rotation, currentLocation, player, particles

def mapScreen(player, mouse, currentLocation, clickables, mapArrows, mapLocations, rotation):
    mousePos = mouse.get_pos()
    
    for key in clickables:
        if abs(mousePos[0]-key[0])<35 and abs(mousePos[1]-key[1])<35:
            if key == currentLocation[0]:
                #print(f'Current Location: {currentLocation[1]}')
                if mouse.get_pressed()[0] and not (currentLocation[1] == 'fire' or currentLocation[1] == 'tent'):
                    player.screen = player.locationDict[f'{currentLocation[1]}']
                    break
            else:
                #print(f'Previous Location: {clickables[key][0]}')
                pass

    return player, clickables, mapArrows, mapLocations, currentLocation, rotation

def battleScreen(win, width, height, mouse, clock, player, enemyDeck, keys, region=None):
    #Need to pick deck from region, right now it just defaults to this region
    enemyDeck.renderSprites(win, width, height)
    enemyDeck.lostCheck()
    if not (player.attacking or player.defending or not player.initiated):
        player.calc = True
    player.update(win, mouse)
    if player.calc:
        print('Attacking!')
        damadges = player.calcAttack(len(enemyDeck.cards)-1)
        enemyDeck.calcDamadges(win, damadges, keys)
        player.defending = True
        player.calc = False
        clock.tick(2.5)
    if player.defending:
        damadges, player.lost = enemyDeck.calcAttack(list(player.activeCards))
        player.calcDamadges(win, damadges, keys)
        player.attacking = True
        player.defending = False
        player.drew = False
        clock.tick(2.5)
    #if mouse.get_pressed()[2]:
    #    player.deck.pullFromPack(1)
    #    time.sleep(0.1)
    #    player.draw()
    if player.lost and player.skip and not len(player.handPile)+len(player.drawPile) == 0:
        print('Stopped Lost', player.attacking, player.defending, player.calc)
        player.skip = False
        player.lost = False
        player.attacking = True
        player.defending = False
        player.calc = False
        player.drew = True
    return player, enemyDeck.lost, player.lost