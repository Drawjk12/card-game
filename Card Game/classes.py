from random import randint, choice, choices, uniform
import pygame as pg
import pygame.gfxdraw
import inspect
import time
from math import floor
import sys, os
import logging

class Cards():
    def __init__(self, sprites, attributeList):
        self.sprites = sprites
        self.blank = pg.image.load(r'assets\sprites\blank.png')
        self.blankXY = (self.blank.get_rect().centerx,self.blank.get_rect().centery)
        self.bigBlank = pg.image.load(r'assets\sprites\bigBlank.png')
        self.bigBlankXY = (self.bigBlank.get_rect().centerx,self.bigBlank.get_rect().centery)
        self.cardSurfs = {}
        self.smallFont = pg.font.SysFont("gillsans", 15)
        self.font = pg.font.SysFont("gillsans", 20)
        for n, sprite in enumerate(sprites):
            gold = attributeList[n].split(';')[1]
            health = attributeList[n].split(';')[2]
            energy = attributeList[n].split(';')[3]
            shield = attributeList[n].split(';')[4]
            attack = attributeList[n].split(';')[5]
            surf = pg.Surface((self.blank.get_rect().w,self.blank.get_rect().h)).convert_alpha()
            surf.blit(self.blank, (0,0))
            surf.blit(sprites[sprite][0], (self.blankXY[0]-sprites[sprite][0].get_rect().centerx, self.blankXY[1]-sprites[sprite][0].get_rect().centery))
            healthS = self.smallFont.render(f'HP:{health}', 1, (255,255,255))
            energyS = self.smallFont.render(f'E:{energy}', 1, (255,255,255))
            attackS = self.smallFont.render(f'A:{attack}', 1, (255,255,255))
            shieldS = self.smallFont.render(f'S:{shield}', 1, (255,255,255))
            xSpacer = 20
            ySpacer = 15
            surf.blit(energyS, (xSpacer,ySpacer))
            surf.blit(healthS, (surf.get_rect().w-xSpacer-healthS.get_rect().w,ySpacer))
            surf.blit(attackS, (xSpacer,surf.get_rect().h-ySpacer-shieldS.get_rect().h))
            surf.blit(shieldS, (surf.get_rect().w-xSpacer-shieldS.get_rect().w,surf.get_rect().h-ySpacer-shieldS.get_rect().h))
            self.cardSurfs[sprite] = [surf, gold, health, energy, shield]
        self.bigCardSurfs = {}
        for n, sprite in enumerate(sprites):
            gold = attributeList[n].split(';')[1]
            health = attributeList[n].split(';')[2]
            energy = attributeList[n].split(';')[3]
            shield = attributeList[n].split(';')[4]
            attack = attributeList[n].split(';')[5]
            surf = pg.Surface((self.bigBlank.get_rect().w,self.bigBlank.get_rect().h)).convert_alpha()
            surf.blit(self.bigBlank, (0,0))
            surf.blit(sprites[sprite][0], (self.bigBlankXY[0]-sprites[sprite][0].get_rect().centerx, self.bigBlankXY[1]-sprites[sprite][0].get_rect().centery))
            healthS = self.font.render(f'HP:{health}', 1, (255,255,255))
            energyS = self.font.render(f'E:{energy}', 1, (255,255,255))
            attackS = self.font.render(f'A:{attack}', 1, (255,255,255))
            shieldS = self.font.render(f'S:{shield}', 1, (255,255,255))
            xSpacer = 25
            ySpacer = 15
            surf.blit(energyS, (xSpacer,ySpacer))
            surf.blit(healthS, (surf.get_rect().w-xSpacer-healthS.get_rect().w,ySpacer))
            surf.blit(attackS, (xSpacer,surf.get_rect().h-ySpacer-shieldS.get_rect().h))
            surf.blit(shieldS, (surf.get_rect().w-xSpacer-shieldS.get_rect().w,surf.get_rect().h-ySpacer-shieldS.get_rect().h))
            self.bigCardSurfs[sprite] = [surf, gold, health, energy, shield]

    def getSurfs(self, cards):
        Surfs = [self.cardSurfs[card] for card in cards]
        return Surfs
    
    def getBigSurfs(self, cards):
        Surfs = [self.bigCardSurfs[card] for card in cards]
        return Surfs

class Deck():
    def __init__(self, size=0, enemy=True):
        self.cards = {}
        self.renderInit = False
        self.blank = pg.image.load(r'assets\sprites\blank.png')
        self.blankXY = (self.blank.get_rect().centerx,self.blank.get_rect().centery)
        self.bigBlank = pg.image.load(r'assets\sprites\bigBlank.png')
        self.bigBlankXY = (self.bigBlank.get_rect().centerx,self.bigBlank.get_rect().centery)
        self.lost = False
        self.cardSurfs = {}
        self.smallFont = pg.font.SysFont("gillsans", 15)
        self.font = pg.font.SysFont("gillsans", 20)
        self.initRender = False
        with open(r'assets\sprites\cards\attributes.txt', 'r') as f:
            attributeList = f.readlines()
            f.close()
        self.attributeList = attributeList
        names = [name.split(';')[0] for name in attributeList]
        for _ in range(size):
            name = choices(names, weights=[.25,.40,.15,.05,.10,0.5])[0]
            options = [type for type in self.attributeList if type.split(';')[0]==name]
            info = choice(options)
            attributes = {}
            attributes['cost'] = info.split(';')[1]
            attributes['health'] = info.split(';')[2]
            attributes['energy'] = info.split(';')[3]
            attributes['shield'] = info.split(';')[4]
            attributes['attack'] = info.split(';')[5]
            specials = {}
            for n, item in enumerate(info.split(';')):
                if item=='h' or item=='e' or item=='p' or item=='g':
                    specials[item]=info.split(';')[n-1]
            attributes['specials'] = specials
            location = (-100,-100)
            card = [name, attributes, pg.image.load(r'assets\sprites\cards'+f'\\{name}.png'), location]
            self.cards[randint(0,2**32)]=card
        self.deck = self.cards.copy()

    def getStandardofName(self, name):
        index = randint(1,len(self.attributeList))-1
        options = [type for type in self.attributeList if type.split(';')[0]==name]
        info = choice(options)
        attributes = {}
        attributes['cost'] = info.split(';')[1]
        attributes['health'] = info.split(';')[2]
        attributes['energy'] = info.split(';')[3]
        attributes['shield'] = info.split(';')[4]
        attributes['attack'] = info.split(';')[5]
        specials = {}
        for n, item in enumerate(info.split(';')):
            if item=='h' or item=='e' or item=='p' or item=='g':
                specials[item]=info.split(';')[n-1]
        attributes['specials'] = specials
        location = (-100,-100)
        card = [name, attributes, pg.image.load(r'assets\sprites\cards'+f'\\{name}.png'), location]
        return card

    def pullFromPack(self, amount=1):
        for _ in range(amount):
            index = randint(1,len(self.attributeList))-1
            name = self.attributeList[index].split(';')[0]
            options = [type for type in self.attributeList if type.split(';')[0]==name]
            info = choice(options)
            attributes = {}
            attributes['cost'] = info.split(';')[1]
            attributes['health'] = info.split(';')[2]
            attributes['energy'] = info.split(';')[3]
            attributes['shield'] = info.split(';')[4]
            attributes['attack'] = info.split(';')[5]
            specials = {}
            for n, item in enumerate(info.split(';')):
                if item=='h' or item=='e' or item=='p' or item=='g':
                    specials[item]=info.split(';')[n-1]
            attributes['specials'] = specials
            location = (-100,-100)
            card = [name, attributes, pg.image.load(r'assets\sprites\cards'+f'\\{name}.png'), location]
            self.cards[randint(0,2**32)]=card

    def addToDeck(self, name):
        for n, check in enumerate(self.attributeList):
            if name == check.split(';')[0]:
                index = n
        name = self.attributeList[index].split(';')[0]
        options = [type for type in self.attributeList if type.split(';')[0]==name]
        info = choice(options)
        attributes = {}
        attributes['cost'] = info.split(';')[1]
        attributes['health'] = info.split(';')[2]
        attributes['energy'] = info.split(';')[3]
        attributes['shield'] = info.split(';')[4]
        attributes['attack'] = info.split(';')[5]
        specials = {}
        for n, item in enumerate(info.split(';')):
            if item=='h' or item=='e' or item=='p' or item=='g':
                specials[item]=info.split(';')[n-1]
        attributes['specials'] = specials
        location = (-100,-100)
        card = [name, attributes, pg.image.load(r'assets\sprites\cards'+f'\\{name}.png'), location]
        self.cards[randint(0,2**32)]=card

    def renderSprites(self, win, width, height):
        for n, card in enumerate(self.cards):
            if not self.renderInit:
                self.cards[card][3] = (randint(int(width/2 + width/12), width-width/12),randint(int(2*height/3 - height/12),int(2*height/3 + height/12)))
            info = self.cards[card]
            if int(info[1]['health'])>0:
                try:
                    enemy = pg.transform.flip(info[2], True, False)
                    win.blit(enemy, info[3])
                except:
                    print('Problem with Rendering Enemy')
                try:
                    pg.draw.rect(win, (min(max(int(info[1]['health'])-510,0),255),min(int(info[1]['health']),255),min(max(int(info[1]['health'])-255,0),255)), (info[3][0]+5,info[3][1]-15, 2*info[2].get_rect().centerx*int(info[1]['health'])/255, 5))
                except:
                    try:
                        pg.draw.rect(win, (100,255,255), (self.activeCards[card][1][0]+5,self.activeCards[card][1][1]-15, 2*info[2].get_rect().centerx*int(info[1]['health'])/255, 5))
                    except:
                        print('Problem Rendering Player HealthBar')
        self.renderInit = True

    def calcDamadges(self, win, damadges, keys):
        removals = {}
        for n, card in enumerate(self.cards):
            for damadge in damadges:
                if damadge[1]==n:
                    info = self.cards[card]
                    power = damadge[0]-int(info[1]['shield'])
                    if power>0:
                        info[1]['health']=str(int(info[1]['health'])-power)
                        particles = particleEffect(randint(8,15), 'circle', 7, [[139,0,0],[255,0,0],[128,0,0],[178,34,34]], -.05, [info[3][0]+randint(10,45),info[3][1]+randint(10,45)], [0,0], [0,0], [0,0], life=5000)
                        damadgeText = self.font.render(f'{-power}', 1, (200+randint(-55,50),200+randint(-55,50),200+randint(-55,50)))
                        surf = win.copy()
                        effectLoc = [info[3][0]+randint(0,15),info[3][1]+randint(-10,5)]
                        surf = win.copy()
                        while len(particles.particles)>0:
                            if keys[pg.K_LEFT]:
                                self.skip = False
                                particles.killParticles()
                                time.sleep(0.1)
                                break
                            win.blit(surf, (0,0))
                            particles.update(win)
                            win.blit(damadgeText, [effectLoc[0]+randint(-3,3),effectLoc[1]+randint(-3,3)])
                            pg.display.update()
                            win.blit(surf, (0,0))
                            win.blit(damadgeText, [effectLoc[0]+randint(-15,30),effectLoc[1]-30])
                    self.cards[card] = info
                    if int(info[1]['health'])<=0:
                        removals[n] = card
        for card in removals:
            try:
                self.cards.pop(removals[card])
            except:
                print(removals[card], self.cards, 'Failed pop')

    def calcAttack(self, targets):
        won = False
        damadges=[]
        for key in self.cards:
            damadge = 0
            info = self.cards[key]
            damadge=int(info[1]['attack'])
            print(f'Enemy Attack: {damadge}')
            try:
                target = choice(targets)
                damadges.append([damadge, target])
            except:
                try:
                    print('Enemy Attack Failed, attempting to assign different target', damadge, target)
                    damadges.append([damadge, target])
                except:
                    print('Enemy Attack failed due to TARGET', damadge)
                    won = True
            try:
                if len(info[1]['specials']['h'])>0:
                    print(f'Healing: {info[1]["specials"]["h"]}')
                    info[1]['health']=str(int(info[1]['health'])+int(info[1]['specials']['h']))
                    self.cards[key][0] = info
            except:
                pass
            pg.event.pump()
        return damadges, won
    
    def lostCheck(self):
        if len(self.cards)==0:
            self.lost = True

    def deadCheck(self):
        removals = []
        for key in self.cards:
            if int(self.cards[key][1]['health'])<=0:
                removals.append(key)
        for key in removals:
            self.cards.pop(key)

    def renderDeck(self, win):
        if not self.initRender:
            self.cardSurfs = {}
            for n, (key, info) in enumerate(self.cards.items()):
                gold = info[1]['cost']
                health = info[1]['health']
                energy = info[1]['energy']
                shield = info[1]['shield']
                attack = info[1]['attack']
                surf = pg.Surface((self.blank.get_rect().w,self.blank.get_rect().h)).convert_alpha()
                surf.blit(self.blank, (0,0))
                surf.blit(info[2], (self.blankXY[0]-info[2].get_rect().centerx, self.blankXY[1]-info[2].get_rect().centery))
                healthS = self.smallFont.render(f'HP:{health}', 1, (255,255,255))
                energyS = self.smallFont.render(f'E:{energy}', 1, (255,255,255))
                attackS = self.smallFont.render(f'A:{attack}', 1, (255,255,255))
                shieldS = self.smallFont.render(f'S:{shield}', 1, (255,255,255))
                xSpacer = 20
                ySpacer = 15
                surf.blit(energyS, (xSpacer,ySpacer))
                surf.blit(healthS, (surf.get_rect().w-xSpacer-healthS.get_rect().w,ySpacer))
                surf.blit(attackS, (xSpacer,surf.get_rect().h-ySpacer-shieldS.get_rect().h))
                surf.blit(shieldS, (surf.get_rect().w-xSpacer-shieldS.get_rect().w,surf.get_rect().h-ySpacer-shieldS.get_rect().h))
                surf.set_colorkey([0,0,0])
                self.cardSurfs[key] = [surf, gold, health, energy, shield]
            self.initRender = True
        for n, info in enumerate(self.cardSurfs.values()):
            if n<=10:
                win.blit(info[0], ((n+1)*info[0].get_rect().w,info[0].get_rect().h))
            else:
                win.blit(info[0], ((n+1-10)*info[0].get_rect().w,2*info[0].get_rect().h))
        

    def getRewards(self, player):
        reward = [0,0,0]
        for key in self.deck:
            reward[0]-=floor(int(eval(self.deck[key][1]['cost'])[0])/4)
            reward[1]-=floor(int(eval(self.deck[key][1]['cost'])[1])/3)
            reward[2]-=floor(int(eval(self.deck[key][1]['cost'])[2])/2)
        player.expense(reward)
        return player

class Player():
    def __init__(self, deck, spriteDict, width, height, path):
        #Stats
        self.energy = 100
        self.stamina = 20
        self.maxStamina = 50
        self.maxEnergy = 100
        self.balance = [1, randint(0,100), randint(0,10)]
        self.blankCards = 0
        #Dicts
        self.drawPile = {}
        self.handPile = {}
        self.activeCards = {}
        self.locationDict = {'map':0, 'town':1, 'battle':2, 'cross':3}
        self.deck = deck
        self.spriteDict = spriteDict
        #Bools
        self.walking = False
        self.initiated = False
        self.inBattle = False
        self.drew = False
        self.attacking = True
        self.calc = False
        self.defending = False
        self.lost = False
        self.rested = False
        self.lock = False
        self.quit = False
        self.skip = False
        #GUI
        self.screen = 1
        self.width = width
        self.height = height
        #Rendering
        self.hoverSprite = pg.image.load(r'assets\sprites\effects\hoverSprite.png')
        self.font = pg.font.SysFont("gillsans", 20)
        #OTHER
        self.path = path

    def __str__(self):
        log = str([i for i in inspect.getmembers(self) if not i[0].startswith('_') and (isinstance(i[1], int) or isinstance(i[1], bool) or isinstance(i[1], list) or isinstance(i[1], dict))])
        with open(self.path+r'\error.log', 'a') as f:
            f.writelines(f'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}\t'+log+'\n')
            print('wrote lines')
        return f'Balance: {self.balance}, Stamina: {self.stamina}/{self.maxStamina}, Energy: {self.energy}/{self.maxEnergy}'
    
    def expense(self, amount):
        if 1000*(self.balance[0]-amount[0]) + 10*(self.balance[1]-amount[1]) + self.balance[2]-amount[2]>0:
            self.balance[0]-=amount[0]
            self.balance[1]-=amount[1]
            self.balance[2]-=amount[2]
            if self.balance[2]<0:
                self.balance[1]-=1
                self.balance[2]+=10
            if self.balance[1]<0:
                self.balance[0]-=1
                self.balance[1]+=100
            if self.balance[1]>=100:
                self.balance[0]+=1
                self.balance[1]-=100
            if self.balance[2]>=10:
                self.balance[1]+=1
                self.balance[2]-=10
            return True
        else:
            return False
    
    def update(self, win, mouse, render=True):
        if self.inBattle and len(self.activeCards)==0 and self.drew and self.initiated and not self.attacking:
            self.lost = True
            print('You Died')
        if self.screen == 2:
            self.hand(win, mouse)
        if len(self.activeCards)>0:
            for card in self.activeCards:
                info = self.activeCards[card]
                if render:
                    win.blit(info[2], self.activeCards[card][3])
                    try:
                        pg.draw.rect(win, (min(max(int(info[1]['health'])-510,0),255),min(int(info[1]['health']),255),min(max(int(info[1]['health'])-255,0),255)), (self.activeCards[card][3][0]+5,self.activeCards[card][3][1]-15, 2*info[2].get_rect().centerx*int(info[1]['health'])/255, 5))
                    except:
                        try:
                            print('Problem Rendering Player Healthbar 1')
                            pg.draw.rect(win, (100,255,255), (self.activeCards[card][3][0]+5,self.activeCards[card][3][1]-15, 2*info[2].get_rect().centerx*int(info[1]['health'])/255, 5))
                        except:
                            print('Problem Rendering Player HealthBar 2')
                    if self.activeCards[card][3][0]<mouse.get_pos()[0]<self.activeCards[card][3][0]+self.activeCards[card][2].get_rect().w and self.activeCards[card][3][1]<mouse.get_pos()[1]<self.activeCards[card][3][1]+self.activeCards[card][2].get_rect().h:
                        win.blit(self.hoverSprite, (self.activeCards[card][3][0]+self.activeCards[card][2].get_rect().centerx-self.hoverSprite.get_rect().centerx,self.activeCards[card][3][1]+self.activeCards[card][2].get_rect().h+10))

    def resetHand(self):
        self.lost = False
        self.inBattle = False
        self.initiated = False
        print()
        temp = {}
        for key in self.activeCards:
            temp[key] = self.activeCards[key]
        
        self.deck.cards = self.handPile | self.drawPile | temp
        self.handPile = {}
        self.drawPile = {}
        self.activeCards = {}

    def draw(self):
        if len(self.drawPile)>0 and len(self.handPile)<7:
            seed = choice(list(self.drawPile))
            self.handPile[seed] = self.drawPile[seed]
            self.drawPile.pop(seed)

    def hand(self, win, mouse):
        mousePos = mouse.get_pos()
        bigIndex = None
        pressed = False
        if self.attacking:
            if not self.initiated:
                self.handPile = {}
                self.drawPile = self.deck.cards.copy()
                startNumber = min(len(self.deck.cards),5)
                for _ in range(startNumber):
                    seed = choice(list(self.drawPile))
                    self.handPile[seed] = self.drawPile[seed]
                    self.drawPile.pop(seed)
                self.initiated = True
                self.drew = True
            if not self.drew:
                self.draw()
                self.drew = True
        for n, card in enumerate(self.handPile):
            numOfCardsInHand = len(self.handPile)
            info = self.handPile[card]
            Cardcorner=(self.width/2 - (numOfCardsInHand-1)*self.deck.blankXY[0]  + (2*n)*self.deck.blankXY[0]-self.deck.blankXY[0],self.height-2*self.deck.blankXY[1])
            if not (abs(mousePos[0]-Cardcorner[0]-self.deck.blankXY[0])<70 and abs(mousePos[1]-Cardcorner[1]-self.deck.blankXY[1])<90):
                win.blit(self.deck.blank, Cardcorner)
                win.blit(info[2], (self.width/2 - info[2].get_rect().centerx - (numOfCardsInHand-1)*self.deck.blankXY[0]  + (2*n)*self.deck.blankXY[0], self.height-self.deck.blankXY[1]- info[2].get_rect().centery))
            else:
                bigIndex=n
                bigSeed=card
                if mouse.get_pressed()[0] and self.energy-int(info[1]['energy'])>=0 and self.attacking:
                    print(f'Used {info[0]}: {info[1]}\nEnergy: {self.energy}')
                    self.energy-=int(info[1]['energy'])
                    seed = card
                    pressed = True
                    time.sleep(0.15)
                    break
        if not bigIndex is None:
            info = self.handPile[bigSeed]
            win.blit(self.deck.bigBlank, (self.width/2 - (numOfCardsInHand-1)*self.deck.blankXY[0]  + (2*bigIndex)*self.deck.blankXY[0]-self.deck.bigBlankXY[0],self.height-2*self.deck.bigBlankXY[1]))
            win.blit(info[2], (self.width/2 - info[2].get_rect().centerx - (numOfCardsInHand-1)*self.deck.blankXY[0]  + (2*bigIndex)*self.deck.blankXY[0], self.height-self.deck.bigBlankXY[1]- info[2].get_rect().centery))
        if pressed:
            self.blankCards+=1
            self.handPile[seed][3] = (randint(0,int(self.width/2 - self.width/12)),randint(int(2*self.height/3 - self.height/12),int(2*self.height/3 + self.height/12)))
            self.activeCards[seed] = self.handPile[seed]
            self.handPile.pop(seed)
            bigIndex = None
            pressed = False

    def calcAttack(self, targets):
        damadges=[]
        for key in self.activeCards:
            damadge = 0
            info = self.activeCards[key]
            damadge=int(info[1]['attack'])
            print(f'Damadge Done: {damadge}')
            try:
                damadges.append([damadge, randint(0, targets)])
            except:
                damadges.append([damadge, randint(0, 0)])
                print('Problem with randint targets', targets)
                return []
            try:
                if len(info[1]['specials']['h'])>0:
                    print(f'Healing: {info[1]["specials"]["h"]}')
                    info[1]['health']=str(int(info[1]['health'])+int(info[1]['specials']['h']))
                    self.activeCards[key][0] = info
            except:
                pass
            try:
                if len(info[1]['specials']['e'])>0:
                    print(f'Energy: +{info[1]["specials"]["e"]}')
                    self.energy=min(int(info[1]['specials']['e'])+self.energy,self.maxEnergy)
            except:
                pass
            try:
                if len(info[1]['specials']['g'])>0:
                    initchance = randint(0,1)
                    if initchance:
                        chance = randint(0,6)+randint(0,6)
                        if chance == 12:
                            growthType = randint(0,len(info[1]["specials"]["g"].split(','))-1)
                            evolve = info[1]["specials"]["g"].split(',')[growthType]
                            info = self.deck.getStandardofName(evolve)
                            self.activeCards[key][0] = info
                            print('Growth:',info[0])
            except:
                pass
        return damadges
    
    def calcDamadges(self, win, damadges, keys):
        removals = []
        for card in self.activeCards:
            for damadge in damadges:
                if damadge[1]==card:
                    info = self.activeCards[card]
                    power = damadge[0]-int(info[1]['shield'])
                    if power>0:
                        info[1]['health']=str(int(info[1]['health'])-power)
                        try:
                            if not self.skip:
                                lifeTime = 5000
                                alphaChange = -.05
                            else:
                                lifeTime = 1000
                                alphaChange = -.1
                            particles = particleEffect(randint(8,15), 'circle', 7, [[139,0,0],[255,0,0],[128,0,0],[178,34,34]], alphaChange, [info[3][0]+randint(0,30),info[3][1]+randint(0,30)], [0,0], [0,0], [0,0], life=lifeTime)
                            damadgeText = self.font.render(f'{-power}', 1, (200+randint(-55,50),200+randint(-55,50),200+randint(-55,50)))
                            surf = win.copy().convert_alpha()
                            effectLoc = [info[3][0]+randint(0,15),info[3][1]+randint(-10,5)]
                            while len(particles.particles)>0:
                                if keys[pg.K_LEFT]:
                                    self.skip = False
                                    particles.killParticles()
                                    time.sleep(0.1)
                                    break
                                win.blit(surf, (0,0))
                                particles.update(win)
                                win.blit(damadgeText, [effectLoc[0]+randint(-3,3),effectLoc[1]+randint(-3,3)])
                                pg.display.update()
                                pg.event.pump()
                            win.blit(surf, (0,0))
                            win.blit(damadgeText, [effectLoc[0]+randint(-15,30),effectLoc[1]-randint(30,45)])
                        except:
                            print("Problem with particle system")
                    self.activeCards[card] = info
                    if int(info[1]['health'])<=0:
                        if self.skip and len(self.handPile)+len(self.drawPile)>0:
                            self.skip = False
                        removals.append(card)
        for card in removals:
            print(self.activeCards)
            try:
                self.activeCards.pop(card)
            except:
                return True

class World():
    def __init__(self, clickables, win):
        #Map
        self.clickables = clickables
        self.win = win
        self.initiated = False
        self.time = 0

class HUD():
    def __init__(self, win, width, height, icons):
        #Side Menu
        self.win = win
        self.width = width
        self.height = height
        self.sideMenuSurf = pg.Surface((width/7, height)).convert()
        self.sideMenuSurf.set_alpha(100)
        self.sideMenuSurf.fill((0,0,0))
        self.marketSurf = pg.Surface((8*width/10, 8*height/10)).convert()
        self.marketSurf.set_alpha(150)
        self.marketSurf.fill((0,0,0))
        self.cornerPos = (6*self.width/7, self.height)
        self.townText = ['Inn & Tavern', 'Market', 'Portal']
        self.innText = ['Sleep', 'Eat', 'Leave']
        self.portalText = ['1', '2', '3']
        self.font = pg.font.SysFont("gillsans", 40)
        self.smallFont = pg.font.SysFont("gillsans", 20)

        #Icons
        self.icons = icons
        self.moneySurf = pg.Surface(self.smallFont.size('Gold: __, Silver: __, Copper: __'), pg.SRCALPHA)
        self.moneySurf.fill((0,0,0,125))
        self.staminaSurf = pg.Surface(self.smallFont.size('Energy: __ Stamina: __'), pg.SRCALPHA)
        self.staminaSurf.fill((0,0,0,125))

        #Windows
        self.marketSurf = pg.Surface((8*width/10, 8*height/10),  pg.SRCALPHA).convert_alpha()
        self.marketSurf.fill((0,0,0,100))
        self.popUpSurf = pg.Surface((7*width/10, 5*height/10),  pg.SRCALPHA).convert_alpha()
        self.popUpSurf.fill((225,225,225,225))
        self.popUpsEnabled = True

    
    def update(self, player, mouse, keys, sprites = None):
        pressed = self.updateSideMenu(player, mouse, sprites)
        player = self.updateIcons(player, mouse, keys)
        player = self.buttonLogic(player, pressed) #Needs fixed
        if keys[pg.K_ESCAPE]:
            player.screen = 100
        if keys[pg.K_RIGHT]:
            player.skip = True
            time.sleep(0.1)
        elif keys[pg.K_LEFT]:
            player.skip = False
            time.sleep(0.1)
        return player

    def updateIcons(self, player, mouse, keys):
        mousePos = mouse.get_pos()
        for icon in self.icons:
            if 'mapIcon.png' in icon[1].split('\\'):
                center = icon[0].get_rect().center
                if self.width - (2*center[0])<mousePos[0]<self.width and self.height - (2*center[1])<mousePos[1]<self.height:
                    if mouse.get_pressed()[0]:
                        player.screen = 0
                self.win.blit(icon[0], (self.width - (2*center[0]), self.height - (2*center[1])))
            elif 'playIcon.png' in icon[1].split('\\') and (player.screen == 0 or player.screen == 2):
                center = icon[0].get_rect().center
                if (0<mousePos[0]<(2*center[0]) and 0<mousePos[1]<(2*center[1])) or keys[pg.K_SPACE] or player.skip:
                    if mouse.get_pressed()[0] or keys[pg.K_SPACE] or player.skip:
                        if player.screen == 0 and player.stamina-1/2>0 and not player.lock:
                            player.walking = True
                        elif player.screen == 2 and not player.skip:
                            if player.attacking:
                                player.attacking = False
                        elif player.screen ==2 and player.skip and player.initiated:
                            if player.attacking:
                                player.attacking = False
                        if not player.skip:
                            time.sleep(0.15)
                self.win.blit(icon[0], (0, 0))
            elif 'deckIcon.png' in icon[1].split('\\'):
                center = icon[0].get_rect().center
                if 0<mousePos[0]<(2*center[0]) and self.height - (2*center[1])<mousePos[1]<self.height:
                    if mouse.get_pressed()[0]:
                        player.deck.renderDeck(self.win)
                        player.deck.initRender = False
                        time.sleep(0.1)
                self.win.blit(icon[0], (0, self.height - (2*center[1])))  
            elif 'backIcon.png' in icon[1].split('\\') and (player.screen == 4 or player.screen == 6):
                center = icon[0].get_rect().center
                if (0<mousePos[0]<(2*center[0]) and 0<mousePos[1]<(2*center[1])) or keys[pg.K_BACKSPACE]:
                    if mouse.get_pressed()[0] or keys[pg.K_BACKSPACE]:
                        player.screen = 1
                self.win.blit(icon[0], (0, 0))
            elif 'moneyIcon.png' in icon[1].split('\\'):
                center = icon[0].get_rect().center
                if (0<mousePos[0]<(2*center[0]) and icon[0].get_rect().w<mousePos[1]<icon[0].get_rect().h+(2*center[1])) or player.screen == 4 or player.screen == 1 or keys[pg.K_UP]:
                    moneyText = self.smallFont.render(f'Gold: {player.balance[0]}, Silver: {player.balance[1]}, Copper: {player.balance[2]}', 1, (255,255,255))
                    moneySurf = pg.transform.scale(self.moneySurf.copy(), (5*moneyText.get_width()/4, moneyText.get_height()))
                    moneySurf.blit(moneyText, (moneyText.get_width()/8, 0))
                    self.win.blit(moneySurf, (icon[0].get_rect().w,3*icon[0].get_rect().h/2 - moneySurf.get_rect().centery))
                self.win.blit(icon[0], (0,icon[0].get_rect().h))
            elif 'energyIcon.png' in icon[1].split('\\'):
                center = icon[0].get_rect().center
                if (0<mousePos[0]<(2*center[0]) and 2*icon[0].get_rect().w<mousePos[1]<2*icon[0].get_rect().h+(2*center[1])) or player.screen == 2 or player.screen == 3 or player.screen == 1 or keys[pg.K_UP]:
                    staminaText = self.smallFont.render(f'Energy: {player.energy} Stamina: {player.stamina}', 1, (255,255,255))
                    staminaSurf = pg.transform.scale(self.staminaSurf.copy(), (5*staminaText.get_width()/4, staminaText.get_height()))
                    staminaSurf.blit(staminaText, (staminaText.get_width()/8, 0))
                    self.win.blit(staminaSurf, (icon[0].get_rect().w,5*icon[0].get_rect().h/2 - staminaSurf.get_rect().centery))
                self.win.blit(icon[0], (0,2*icon[0].get_rect().h))

            pg.event.pump()
        return player

    def updateSideMenu(self, player, mouse, sprites = None):
        mousePos = mouse.get_pos()
        pressed = None
        textList = []
        spacer = self.font.size(' ')[0]
        if player.screen == 1:
            self.win.blit(self.sideMenuSurf, (self.cornerPos[0],0))
            textList = self.townText
        elif player.screen == 3:
            self.win.blit(self.sideMenuSurf, (self.cornerPos[0],0))
            textList = self.innText
        elif player.screen == 4:
            spacer = (self.width/16, self.height/8)
            self.win.blit(self.marketSurf, spacer)
            if not sprites is None:
                for n, sprite in enumerate(sprites.cardSurfs):
                    if n<12:
                        if spacer[0] + (n*sprites.cardSurfs[sprite][0].get_rect().w)<mousePos[0]<((n+1)*sprites.cardSurfs[sprite][0].get_rect().w)+spacer[0] and spacer[1]<mousePos[1]<sprites.cardSurfs[sprite][0].get_rect().h+spacer[1]:
                            sprites.bigCardSurfs[sprite][0].set_colorkey([0,0,0])
                            self.win.blit(sprites.bigCardSurfs[sprite][0], (spacer[0] + (n*sprites.cardSurfs[sprite][0].get_rect().w)+(sprites.cardSurfs[sprite][0].get_rect().w-sprites.bigCardSurfs[sprite][0].get_rect().w)/2,spacer[1]))
                            costText = self.smallFont.render(f'{eval(sprites.cardSurfs[sprite][1])[0]}G, {eval(sprites.cardSurfs[sprite][1])[1]}S, {eval(sprites.cardSurfs[sprite][1])[2]}C', 1, (255,255,255))
                            self.win.blit(costText, (spacer[0] + (n*sprites.cardSurfs[sprite][0].get_rect().w)+sprites.cardSurfs[sprite][0].get_rect().centerx-costText.get_rect().centerx,spacer[1]+sprites.bigCardSurfs[sprite][0].get_rect().h))
                            if mouse.get_pressed()[0]:
                                if player.expense(eval(sprites.cardSurfs[sprite][1])):
                                    print(f'Bought: {sprite}')
                                    player.deck.addToDeck(sprite)
                                else:
                                    print('Too Poor')
                                print(player)
                                time.sleep(0.1)
                            elif mouse.get_pressed()[2]:
                                print('Special Info will be Found Here')
                        else:
                            sprites.cardSurfs[sprite][0].set_colorkey([0,0,0])
                            self.win.blit(sprites.cardSurfs[sprite][0], (spacer[0] + (n*sprites.cardSurfs[sprite][0].get_rect().w),spacer[1]))
                            costText = self.smallFont.render(f'{eval(sprites.cardSurfs[sprite][1])[0]}G, {eval(sprites.cardSurfs[sprite][1])[1]}S, {eval(sprites.cardSurfs[sprite][1])[2]}C', 1, (255,255,255))
                            self.win.blit(costText, (spacer[0] + (n*sprites.cardSurfs[sprite][0].get_rect().w)+sprites.cardSurfs[sprite][0].get_rect().centerx-costText.get_rect().centerx,spacer[1]+sprites.cardSurfs[sprite][0].get_rect().h))
                    elif n<24:
                        self.win.blit(sprites.cardSurfs[sprite][0], (spacer[0] + ((n-12)*sprites.cardSurfs[sprite][0].get_rect().w),spacer[1]+n*sprites.cardSurfs[sprite][0].get_rect().h))
        elif player.screen == 6:
            self.win.blit(self.sideMenuSurf, (self.cornerPos[0],0))
            textList = self.portalText
        for n, text in enumerate(textList):
            buttonText = self.font.render(f'{text}', 1, (255,255,255))
            if self.cornerPos[0]+spacer<mousePos[0]<self.cornerPos[0]+buttonText.get_width()+spacer and self.height/28+(n*(self.height/28+buttonText.get_height()))<mousePos[1]<buttonText.get_height()+self.height/28+(n*(self.height/28+buttonText.get_height())):
                buttonText = self.font.render(f'{text}', 1, (0,0,0))
                self.win.blit(buttonText, (self.cornerPos[0]+spacer,self.height/28+(n*(self.height/28+buttonText.get_height()))))
                if mouse.get_pressed()[0]:
                    pressed = n
            else:
                self.win.blit(buttonText, (self.cornerPos[0]+spacer,self.height/28+(n*(self.height/28+buttonText.get_height()))))
        return pressed
    
    def buttonLogic(self, player, pressed):
        screen = player.screen
        if screen == 1:
            if not pressed is None:
                if pressed == 0:
                    player.screen = 3
                elif pressed == 1:
                    player.screen = 4
                elif pressed == 2:
                    player.screen = 6
                elif pressed == 5:
                    player.screen = 1
                time.sleep(0.1)
        elif screen == 3:
            if not pressed is None:
                if pressed == 0:
                    allowed=player.expense([0,20,0])
                    if allowed:
                        player.stamina=min(player.maxStamina, player.stamina+25)
                        player.energy=min(player.maxEnergy, player.energy+75)
                    print(player)
                elif pressed == 1:
                    allowed=player.expense([0,8,5])
                    if allowed:
                        player.stamina=min(player.maxStamina, player.stamina+5)
                        player.energy=min(player.maxEnergy, player.energy+25)
                    print(player)
                elif pressed == 2:
                    player.screen = 1
                time.sleep(0.1)
        elif screen == 6:
            if not pressed == None:
                if pressed == 0:
                    player.screen = 1
                elif pressed == 1:
                    if player.expense([5,0,0]):
                        player.screen = 1
                        print('Teleporting to Region 2')
                        print('YOU WIN RN')
                    else:
                        print('Not Enough Money')
                time.sleep(0.1)
        return player
    
    def popUp(self, text=['Something','Something Else','Yo!','HEEEEEEEEEELLP!!'], delay=3):
        if self.popUpsEnabled:
            print(self.popUpsEnabled)
            popUpSurf = self.popUpSurf.copy()
            for n, line in enumerate(text):
                popUpText = self.font.render(line, 1, (0,0,0))
                popUpSurf.blit(popUpText, (popUpSurf.get_rect().w/2 - popUpText.get_rect().w/2,2*(n+1)*popUpText.get_rect().h))
            self.win.blit(popUpSurf, (self.width/2 - popUpSurf.get_rect().w/2,self.height/2 - popUpSurf.get_rect().h/2))
            pg.display.update()
            time.sleep(delay)
        else:
            print('Skipped PopUp')

class particleEffect():
    def __init__(self, number, shape, size, colors, change, pos, vel, acc=[0,0], drag=[0,0], life=4, alphaChange=0.4):
        self.shape = shape
        self.particles = []
        self.alpha = 255
        self.alphaChange = alphaChange
        for _ in range(number):
            color = choices(colors)[0]
            newChange = change+uniform(-0.005,0.005)
            newPos = [pos[0]+randint(-8,8),pos[1]+randint(-8,8)]
            newVel = [vel[0]+uniform(-.125,.125),vel[1]+uniform(-.125,.125)]
            newAcc = [acc[0]+uniform(-.00015,.00015),acc[1]+uniform(-.00015,.00015)]
            newDrag = [drag[0]+uniform(-.00000015,.00000015),drag[1]+uniform(-.00000015,.00000015)]
            self.particles.append([size+randint(0,7), newChange, newPos, newVel, newAcc, newDrag, life, color])

    def update(self, win):
        self.alphaChange=self.alphaChange*101/100
        self.alpha-=self.alphaChange
        particles = []
        removals = []
        for n, particle in enumerate(self.particles):
            particle[0]+=particle[1]
            particle[4][0]+=particle[5][0]
            particle[4][1]+=particle[5][1]
            particle[3][0]+=particle[4][0]
            particle[3][1]+=particle[4][1]
            particle[2][0]+=particle[3][0]
            particle[2][1]+=particle[3][1]
            if particle[6]<=0 or particle[0]<=0 or self.alpha<=0 or 255<=self.alpha:
                removals.append(n)
            else:
                particle[6]-=1
                particles.append(particle)
                pg.gfxdraw.filled_circle(win,int(particle[2][0]),int(particle[2][1]),int(particle[0]),(particle[7][0],particle[7][1],particle[7][2],int(self.alpha)))
        for i in removals[::-1]:
            self.particles.pop(i)
        self.particles = particles

    def killParticles(self):
        self.particles = []