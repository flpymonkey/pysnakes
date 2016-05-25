import random, pygame, sys, matplotlib, pylab
from pygame.locals import *
#Colors   R    G   B
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
BLUE = (0, 0, 255)
AQUA = (0, 255, 255)#CYAN
BLACK = (0, 0, 0)
FUCHSIA = (255, 0, 255)
GRAY = (128, 128, 128)
LIME = (0, 255, 0)
MAROON = (128, 0, 0)
NAVYBLUE = (0, 0, 128)
OLIVE = (128, 128, 0)
PURPLE = (128, 0, 128)
RED = (255, 0, 0)
SILVER = (192, 192, 192)
TEAL = (0, 128, 128)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)
CYAN = (0, 255, 255) #AQUA
HOTPINK = (255, 105, 180)
'''
print ('help---------------------------------------')
'"s" key toggles game speed')
'mouse click or scroll creates new sprite at cursor')
'"space" key when held down kills sprites near cursor')
'"b" key toggles sprite babies')
'"c" key toggles color craziness')
'"t" key toggles sprite tails')
'"k" key toggles kill boudaries and no boundaries')
'"l" key toggles no boundaries and boundaries')
'"a" key kills all sprites')
'"e" key starts new simulation')
'"g" key creates graph of living sprites')
'"up" and "down" keys toggle stocks (invest mode)')
'"i" key buys or sells stocks (invest mode)')
('-------------------------------------------')
'''


pygame.init()

WINDOWWIDTH = 1000 #Size of windows width in pixels (invest mode default 1000)
WINDOWHEIGHT = 700 #Size of windows height in pixels (invest mode default 700)
BGCOLOR = WHITE #Back Ground Color
FPS = 60 #frames per second
graphing = True #data graphing when press G
investMode = False #Is invest mode on
FPSCLOCK = pygame.time.Clock()
DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
snakes = pygame.sprite.Group()
MENUHEIGHT = 50

class Snake(pygame.sprite.Sprite):
    def __init__(self,coords,color,num = random.randint(0,2)):
        self.movespeed = 5#sprite jump length
        self.babychance = 0.001#chance of baby being born, lower float less likely (invest mode default 0.0002)
        self.size = 5#size of each square sprite
        self.colorCrazSpeed = 1 #speed the colors change in color crazy mode
        self.bounds = 2 #0 exit screen, 1 no exit screen, 2 sprite dies if exit screen
        pygame.sprite.Sprite.__init__(self)
        self.x = coords[0]
        self.y = coords[1]
        self.color = color
        self.num = num

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getSize(self):
        return self.size

    def makeBabies(self, babybool):
        '''babybool: T or F bool value to make babies'''
        self.babies = babybool
    
    def update(self, babybool, colorbool, killBounds, screenBounds):
        self.render()
        self.move(killBounds, screenBounds)
        self.baby(babybool)
        self.colorcrazy(colorbool)#comment out for sanity

    def render(self):
        rectpos=Rect((self.x,self.y),(self.size,self.size))
        pygame.draw.rect(DISPLAYSURF, self.color, rectpos)

    def move(self, killBounds, screenBounds):
        move = random.randint(0,3)
        if killBounds == True:
            if move == 0:
                if self.x+self.movespeed > WINDOWWIDTH:
                    self.killBox()
                else:
                    self.x += self.movespeed
            if move == 1:
                if self.x-self.movespeed < 0:
                    self.killBox()
                else:
                    self.x -= self.movespeed
            if move == 2:
                if self.y+self.movespeed > WINDOWHEIGHT:
                    self.killBox()
                else:
                    self.y += self.movespeed
            if move == 3:
                if self.y-self.movespeed < MENUHEIGHT:   
                    self.killBox()
                else:
                   self.y -= self.movespeed 
        elif screenBounds == True:
            if move == 0 and self.x+self.movespeed <= WINDOWWIDTH:
                self.x += self.movespeed
            if move == 1 and self.x-self.movespeed >= 0:
                self.x -= self.movespeed
            if move == 2 and self.y+self.movespeed <= WINDOWHEIGHT:
                self.y += self.movespeed
            if move == 3 and self.y-self.movespeed >= MENUHEIGHT:
                self.y -= self.movespeed
        else:
            if move == 0:
                self.x += self.movespeed
            if move == 1:
                self.x -= self.movespeed
            if move == 2:
                self.y += self.movespeed
            if move == 3:
                self.y -= self.movespeed

    def colorcrazy(self,colorbool):
        if colorbool == True:
            if self.color[self.num] + self.colorCrazSpeed <= 255:
                self.color[self.num] += self.colorCrazSpeed
            else:
                self.color[self.num] = 0

    def baby(self, babybool):
        if babybool == True:
            global snakes
            babynum = random.random()
            if babynum < self.babychance:
                babysnake = Snake((self.x,self.y),self.color)
                snakes.add(babysnake)

    def killBox(self):
        rectpos=Rect((self.x,self.y),(self.size,self.size))
        pygame.draw.rect(DISPLAYSURF, BLACK, rectpos)
        pygame.draw.rect(DISPLAYSURF, RED, rectpos, 1)
        self.kill()
        
menuFont = pygame.font.Font(None, 30)
selectedFont = pygame.font.Font(None, 30)
selectedFont.set_underline(True)
def blitMenu(createText, speedText, livingText, babyText, colorText, tailText, boundsText, frameText,helpText):
    menupos=Rect((0,0),(WINDOWWIDTH,MENUHEIGHT))
    pygame.draw.rect(DISPLAYSURF, GRAY, menupos)
    createRect = createText.get_rect()
    speedRect = speedText.get_rect()
    livingRect = livingText.get_rect()
    babyRect = babyText.get_rect()
    colorRect = colorText.get_rect()
    tailRect = tailText.get_rect()
    boundsRect = boundsText.get_rect()
    frameRect = frameText.get_rect()
    helpRect = helpText.get_rect()
    DISPLAYSURF.blit(createText, (5,5))
    livingRect.x = 78
    DISPLAYSURF.blit(livingText, (livingRect.x,5))
    frameRect.x = livingRect.right+5
    DISPLAYSURF.blit(frameText, (frameRect.x,5))

    helpRect.x = WINDOWWIDTH - (helpRect.width)
    DISPLAYSURF.blit(helpText, (helpRect.x,5))
    
    DISPLAYSURF.blit(speedText, (5,27))
    babyRect.x = 78
    DISPLAYSURF.blit(babyText, (babyRect.x,27))
    colorRect.x = babyRect.right+5
    DISPLAYSURF.blit(colorText, (colorRect.x,27))
    tailRect.x = colorRect.right+5
    DISPLAYSURF.blit(tailText, (tailRect.x,27))
    boundsRect.x = tailRect.right+5
    DISPLAYSURF.blit(boundsText, (boundsRect.x ,27))

def invblitMenu(createText,speedText,livingText,babyText,colorText,tailText,boundsText,frameText,helpText,moneyText,Stockinf1,Stockinf2):
    menupos=Rect((0,0),(WINDOWWIDTH,MENUHEIGHT))
    pygame.draw.rect(DISPLAYSURF, GRAY, menupos)
    createRect = createText.get_rect()
    speedRect = speedText.get_rect()
    livingRect = livingText.get_rect()
    babyRect = babyText.get_rect()
    colorRect = colorText.get_rect()
    tailRect = tailText.get_rect()
    boundsRect = boundsText.get_rect()
    frameRect = frameText.get_rect()
    moneyRect = moneyText.get_rect()
    Stock1Rect = Stockinf1.get_rect()
    Stock2Rect = Stockinf2.get_rect()
    helpRect = helpText.get_rect()
    
    DISPLAYSURF.blit(createText, (5,5))
    moneyRect.x = 78
    DISPLAYSURF.blit(moneyText, (moneyRect.x,5))
    Stock1Rect.x = moneyRect.right+5
    DISPLAYSURF.blit(Stockinf1, (Stock1Rect.x,5))
    Stock2Rect.x = Stock1Rect.right+5
    DISPLAYSURF.blit(Stockinf2, (Stock2Rect.x,5))

    helpRect.x = WINDOWWIDTH - (helpRect.width)
    DISPLAYSURF.blit(helpText, (helpRect.x,5))
    
    DISPLAYSURF.blit(speedText, (5,27))
    babyRect.x = 78
    DISPLAYSURF.blit(babyText, (babyRect.x,27))
    colorRect.x = babyRect.right+5
    DISPLAYSURF.blit(colorText, (colorRect.x,27))
    tailRect.x = colorRect.right+5
    DISPLAYSURF.blit(tailText, (tailRect.x,27))
    boundsRect.x = tailRect.right+5
    DISPLAYSURF.blit(boundsText, (boundsRect.x ,27))
    livingRect.x = 510
    DISPLAYSURF.blit(livingText, (livingRect.x,27))
    frameRect.x = livingRect.right+5
    DISPLAYSURF.blit(frameText, (frameRect.x,27))
    
    
    
def main():
    DISPLAYSURF.fill(BGCOLOR)
    pygame.display.set_caption('Snakes')
    mousex = 0 
    mousey = 0
    mouseClicked = False
    frameNum = 0
    frameNumList = [0]
    spriteNum = 0
    spriteNumList = [0]
    xInterval = 10 #interval by which spriteNum is recorded and plotted
    killRange = 100#width and height of kill square when click
    killSnakes = False #kill snakes near mouse
    fpsSpeed = True #Max speed or fps speed
    babyBool = True #Do sprites make babies
    colorBool = True #color crazy mode
    tailBool = True #do sprites leave tails
    killBounds = False #Do screen boundries kill
    screenBounds = True #Do screen boundaries contain sprites
    #investMode------
    sMoney = 500 #starting amount of money
    sinvestMoney = 0 #invested amount
    sinitialSnakes = 0
    sStockToInvest = 1 #amount of money will be invested
    sinvested = False#is invested in snakes
    sStockInvested = 0                
    sinvestable = True
    sbankRupt = False
    
    Money = sMoney
    investMoney = sinvestMoney
    initialSnakes = sinitialSnakes
    StockToInvest = sStockToInvest 
    invested = sinvested
    StockInvested = sStockInvested               
    investable = sinvestable
    bankRupt = sbankRupt
    #----------------
    empty = False
    speedText = menuFont.render('%s FPS' % (FPS), True, YELLOW)
    if babyBool == True: babyText = selectedFont.render('Babies', True, ORANGE)
    else: babyText = menuFont.render('Babies', True, ORANGE)
    if colorBool == True: colorText = selectedFont.render('Color Crazy', True, HOTPINK)
    else: colorText = menuFont.render('Color Crazy', True, WHITE)
    if tailBool == True: tailText = selectedFont.render('Tails', True, MAROON)
    else: tailText = menuFont.render('Tails', True, MAROON)
    if killBounds == True: boundsText = menuFont.render('KILL BOUNDRIES', True, RED)
    elif screenBounds == True: boundsText = menuFont.render('Boundries', True, YELLOW)
    else: boundsText = menuFont.render('No Boundries', True, (0, 160, 0))
    while True:
        investMoney = StockToInvest*spriteNum
        outputInvest = StockInvested*spriteNum
        investable = StockToInvest*spriteNum <= Money
        if invested == True: costPerClick = StockInvested + 1 + int(StockInvested*random.uniform(0.005,0.35))
        else: costPerClick = 20 #cost per click when not invested
        injectable = Money >= costPerClick
        if Money <= costPerClick and spriteNum == 0:
            bankRupt = True
        if tailBool == False: DISPLAYSURF.fill(BGCOLOR)
        if empty == True:
            tailBool = True
            empty = False
        for event in pygame.event.get(): 
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClickedPos = (mousex, mousey)
                mouseClicked = True
            elif event.type == KEYDOWN:
                if event.key == pygame.K_s:
                    if fpsSpeed == True:
                        fpsSpeed = False
                        speedText = menuFont.render('FAST', True, YELLOW)
                    else:
                        fpsSpeed = True
                        speedText = menuFont.render('%s FPS' % (FPS), True, YELLOW)
                elif event.key == pygame.K_b:
                    if babyBool == False:
                        babyBool = True
                        babyText = selectedFont.render('Babies', True, ORANGE)
                    else:
                        babyBool = False
                        babyText = menuFont.render('Babies', True, ORANGE)
                elif event.key == pygame.K_c:
                    if colorBool == False:
                        colorBool = True
                        colorText = selectedFont.render('Color Crazy', True, HOTPINK)
                    else:
                        colorBool = False
                        colorText = menuFont.render('Color Crazy', True, HOTPINK)
                elif event.key == pygame.K_t:
                    if tailBool == False:
                        tailBool = True
                        tailText = selectedFont.render('Tails', True, MAROON)
                    else:
                        tailBool = False
                        tailText = menuFont.render('Tails', True, MAROON)
                elif event.key == pygame.K_k:
                    if killBounds == False:
                        killBounds = True
                        boundsText = menuFont.render('KILL BOUNDRIES', True, RED)
                    else:
                        killBounds = False
                        screenBounds = False
                        boundsText = menuFont.render('No Boundries', True, (0, 160, 0))
                elif event.key == pygame.K_l:
                    if screenBounds == False:
                        screenBounds = True
                        killBounds = False
                        boundsText = menuFont.render('Boundries', True, YELLOW)
                    else:
                        screenBounds = False
                        killBounds = False
                        boundsText = menuFont.render('No Boundries', True, (0, 160, 0))
                elif event.key == pygame.K_a:
                    snakes.empty()
                elif event.key == pygame.K_e:
                    snakes.empty()
                    tailBool = False
                    mouseClicked = False
                    frameNum = 0
                    frameNumList = [0]
                    spriteNum = 0
                    spriteNumList = [0]
                    empty = True
                    if investMode:
                        Money = sMoney
                        investMoney = sinvestMoney
                        initialSnakes = sinitialSnakes
                        StockToInvest = sStockToInvest 
                        invested = sinvested
                        StockInvested = sStockInvested               
                        investable = sinvestable
                        bankRupt = sbankRupt
                elif event.key == pygame.K_g and graphing == True:
                    pylab.plot(frameNumList,spriteNumList)
                    pylab.xlabel('Frame Number')
                    pylab.ylabel('Living Sprites')
                    pylab.title('Number of Living Sprites Graph')
                    pylab.show()
                elif event.key == pygame.K_q:
                    print ('help---------------------------------------')
                    print ('"s" key toggles game speed')
                    print ('mouse click or scroll creates new sprite at cursor')
                    print ('"space" key when held down kills sprites near cursor')
                    print ('"b" key toggles sprite babies')
                    print ('"c" key toggles color craziness')
                    print ('"t" key toggles sprite tails')
                    print ('"k" key toggles kill boudaries and no boundaries')
                    print ('"l" key toggles no boundaries and boundaries')
                    print ('"a" key kills all sprites')
                    print ('"e" key starts new simulation')
                    print ('"g" key creates graph of living sprites')
                    print ('"up" and "down" keys toggle stocks (invest mode)')
                    print ('"i" key buys or sells stocks (invest mode)')
                    print ('-------------------------------------------')
                    
                elif event.key == pygame.K_SPACE:
                    killSnakes = True
                elif event.key == pygame.K_i and investMode == True:
                    if invested == False and spriteNum > 0:
                        if investable:
                            Money -= investMoney
                            StockInvested = StockToInvest
                            initialInvest = investMoney
                            invested = True
                    else:
                        Money += outputInvest
                        investMoney = 0
                        initialInvest = 0
                        StockInvested = 0
                        invested = False
                elif event.key == pygame.K_UP:
                    StockToInvest += 1
                elif event.key == pygame.K_DOWN and StockToInvest > 1:
                    StockToInvest -= 1           
            elif event.type == KEYUP:
                if event.key == pygame.K_SPACE: killSnakes = False

        if mouseClicked == True:
            if mouseClickedPos[1] > MENUHEIGHT:
                if investMode == True and injectable:
                    Money -= costPerClick
                    snake = Snake(mouseClickedPos,[random.randint(0,255),random.randint(0,255),random.randint(0,255)])
                    snakes.add(snake)
                    mouseClicked = False
                elif investMode == False:
                    snake = Snake(mouseClickedPos,[random.randint(0,255),random.randint(0,255),random.randint(0,255)])
                    snakes.add(snake)
                    mouseClicked = False
        if killSnakes == True:
            createText = menuFont.render('KILL', True, RED)
            for sprite in snakes:
                if sprite.getX() >= mousex and sprite.getX() < mousex+killRange and sprite.getY() >= mousey and sprite.getY() < mousey+killRange: 
                    sprite.killBox()
        else:
            createText = menuFont.render('Create', True, (0, 160, 0))

        spriteNum = len(snakes.sprites())
        livingText = menuFont.render('Snakes: %s' % (spriteNum), True, CYAN)
                        
        snakes.update(babyBool, colorBool, killBounds, screenBounds)
           
        frameNum += 1
        frameText = menuFont.render('Frame: %s' % (frameNum), True, NAVYBLUE)
        helpText = menuFont.render('"Q" key for help', True, WHITE)
        if graphing == True and frameNum%xInterval == 0:
            frameNumList.append(frameNum)
            spriteNumList.append(spriteNum)
        if investMode == True:
            moneyText = menuFont.render('Money: %s' % (Money), True, GREEN)
            if invested == True:
                if investMoney >= initialInvest:
                    investText = menuFont.render('Invested: %s' % (initialInvest), True, LIME)
                    ReturnText = menuFont.render('Invested Return: %s' % (outputInvest), True, LIME)
                else:
                    investText = menuFont.render('Invested: %s' % (initialInvest), True, RED)
                    ReturnText = menuFont.render('Invested Return: %s' % (outputInvest), True, RED)
                invblitMenu(createText, speedText, livingText, babyText, colorText, tailText, boundsText, frameText,helpText,moneyText,investText,ReturnText)
            elif bankRupt == False and invested == False:
                if investable == True:
                    stockText = menuFont.render('Stock to Invest: %s' % (StockToInvest), True, LIME)
                    priceTest = menuFont.render('Price to Invest: %s' % (investMoney), True, LIME)
                else:
                    stockText = menuFont.render('Stock to Invest: %s' % (StockToInvest), True, RED)
                    priceTest = menuFont.render('Price to Invest: %s' % (investMoney), True, RED)
                invblitMenu(createText, speedText, livingText, babyText, colorText, tailText, boundsText, frameText,helpText,moneyText,stockText,priceTest)
            else:
                moneyText = menuFont.render('Money: %s' % (Money), True, RED)
                stockText = menuFont.render('X', True, RED)
                priceTest = menuFont.render('X', True, RED)
                invblitMenu(createText, speedText, livingText, babyText, colorText, tailText, boundsText, frameText,helpText,moneyText,stockText,priceTest)
                
        else:
            blitMenu(createText, speedText, livingText, babyText, colorText, tailText, boundsText, frameText,helpText)
        if fpsSpeed == True: FPSCLOCK.tick(FPS) 
        pygame.display.update()

#def startMenu():

        
main()





                
