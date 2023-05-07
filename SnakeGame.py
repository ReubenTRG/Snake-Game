import pygame
import random
from pygame import mixer

pygame.init()
mixer.init()
try:  # If a problem has risen from the tests or an error it resets saved data
    with open('SavedData.txt') as f:  # This is the decryption part which takes the saved data from a txt file
        f = f.read().split('/')
        Test = lambda x: float(x) == int(x)
        Score = (int(f[0]) - 127) ** 0.5
        EquippedSkin = (int(f[1]) - 890) ** 0.25
        UnlockedSkin = []
        for i in f[2].split():
            if not Test(i):
                print('Unlocked Skin Error')
                raise IOError
            UnlockedSkin.append(bool((int(i) - 2837) ** 0.125))
        Difficulty = (int(f[3]) - 1890) ** 0.2
        if Test(Score) and Test(EquippedSkin) and UnlockedSkin == '' and Test(Difficulty):
            print('Test Error')
            raise IOError
        Score, EquippedSkin, Difficulty = int(Score), int(EquippedSkin), bool(Difficulty)

except:
    with open('SavedData.txt', 'w') as f:
        Score = 0
        EquippedSkin = 0
        UnlockedSkin = [False, False, False, False]
        Difficulty = True  # True for Easy and False for Hard
    print('Error\nSaves have been reset!')

print('Press esc to pause in game')

f = open('SavedData.txt', 'w')

DisplayHeight, DisplayWidth = 750, 1050
run, DelayTime = True, 1
count = 0

try:
    mixer.music.load('Bite.mp3')  # This opens a Bite mp file, if it can't it moves on
except:
    pass

CurrentDirection = 'Right'
Move = True
escON = False
mouse = (0, 0)
ButtonCounter = 0
DeathCount = 0
Start = True

CurrentSkin = [{'Name': 'Original', 'Cost': 0, 'Head': (0, 0, 0), 1: (0, 64, 0), 2: (0, 128, 0), 0: (0, 255, 0)},
               {'Name': 'Lime', 'Cost': 40, 'Head': (200, 255, 0), 1: (153, 255, 153), 0: (190, 255, 190)},
               {'Name': 'Purple', 'Cost': 15, 'Head': (95, 0, 160), 1: (235, 205, 255), 0: (186, 85, 255)},
               {'Name': 'Red', 'Cost': 10, 'Head': (255, 0, 0), 1: (64, 0, 0), 0: (128, 0, 0)},
               {'Name': 'Gold', 'Cost': 70, 'Head': (218, 165, 32), 0: (255, 231, 92), 1: (208, 188, 78),
                2: (150, 136, 60), 3: (94, 86, 38), 4: (84, 77, 33)}]
# Order is a bit broken but can adjust
CurrentDeath = ['None', 'TailTouch', 'WallLoss']
CurrentScreen = ['Home', 'Game', 'Achievement', 'Credit', 'Skins', 'Difficulty', 'Pause']
# the first element in the list is the current Screen

window = pygame.display.set_mode((DisplayWidth, DisplayHeight))
pygame.display.set_caption('Sneke Game')


class Snake:
    x = 50
    y = 0
    Width = 30
    Offset = 10
    TailParts = {'Num': 0, 'Head': False, 'Direction': 'Right', 'Colour': (0, 255, 0), 'x': 0, 'y': 0}
    Tail = [{'Num': 0, 'Head': True, 'Direction': 'Right', 'Colour': (0, 0, 0), 'x': 450, 'y': 0},
            # This is a dict that will put the snakes location
            {'Num': 1, 'Head': False, 'Direction': 'Right', 'Colour': (255, 255, 255), 'x': 400, 'y': 0},
            {'Num': 2, 'Head': False, 'Direction': 'Right', 'Colour': (255, 255, 255), 'x': 350, 'y': 0},
            {'Num': 3, 'Head': False, 'Direction': 'Right', 'Colour': (255, 255, 255), 'x': 0, 'y': 0}]


def Draw_Snake():  # Displays each part one by one
    for t in Snake.Tail:
        Left, Right, UP, Down = 0, 0, 0, 0
        if t['Head']:  # The head is a square while the body is a rectangle which follows direction
            pygame.draw.rect(window, t['Colour'],
                             ((t['x'] + Snake.Offset), (t['y'] + Snake.Offset), Snake.Width, Snake.Width))
        elif not t['Head']:
            if t['Direction'] == 'Right':
                Right = 20
            elif t['Direction'] == 'Left':
                Left, Right = 20, 20
            elif t['Direction'] == 'UP':
                UP, Down = 20, 20
            elif t['Direction'] == 'Down':
                Down = 20
            pygame.draw.rect(window, t['Colour'], (
                (t['x'] + Snake.Offset - Left), (t['y'] + Snake.Offset - UP), (Snake.Width + Right),
                (Snake.Width + Down)))


def UpdateTail():  # Updates the location and colour of tail parts when moving
    TailLocList = []
    num = 0
    for t in Snake.Tail:
        TailLocList.append([t['Direction'], t['x'], t['y']])

    TailLocList.insert(0, [CurrentDirection, Snake.x, Snake.y])
    TailLocList[1][0] = CurrentDirection

    for t in Snake.Tail:  # Shifts the location of tail parts
        t['Direction'], t['x'], t['y'] = TailLocList[num][0], TailLocList[num][1], TailLocList[num][2]
        num += 1

    for t in Snake.Tail:  # Updates the colour of tail parts
        for n in range(len(CurrentSkin[0]) - 3):
            if t['Num'] == 0:
                t['Colour'] = CurrentSkin[0]['Head']
            elif t['Num'] % (len(CurrentSkin[0]) - 3) == n:
                t['Colour'] = CurrentSkin[0][n]
                break


def TouchTail():  # If any of the tail parts and head are found together then dead
    global Move
    for t in Snake.Tail:
        X = t['x'] + Snake.Offset - 20
        Y = t['y'] + Snake.Offset - 20
        if not t['Head'] and (
                X <= Snake.x <= X + Snake.Width + 20 and Y <= Snake.y <= Y + Snake.Width + 20):
            Change('TailTouch', CurrentDeath)
            Move = False


def WallLoss():  # If Snake found outside the wall then dead
    global Move
    if not (0 <= Snake.x <= DisplayWidth) or not (0 <= Snake.y <= DisplayHeight):
        Change('WallLoss', CurrentDeath)
        Move = False


def OppositeWall():  # If found outside a wall change location to be opposite wall
    if Snake.x < 0:
        Snake.x = DisplayWidth + Snake.Offset
    elif Snake.x > DisplayWidth:
        Snake.x = 0 - Snake.Offset

    if Snake.y < 0:
        Snake.y = DisplayHeight + Snake.Offset
    elif Snake.y > DisplayHeight:
        Snake.y = 0 - Snake.Offset


def TailLengthen():  # Adds a new tail part to the end
    Snake.Tail.append(Snake.TailParts)
    Snake.Tail[-1]['Num'] = len(Snake.Tail) + Apple.NumApples - 1


class Apple:
    NumApples = 3
    LocationList = []
    NumAte = 0

    def Location(self):  # Assigns a random location for the apples
        while 1:
            AppleLoc = (random.randint(0, int(DisplayWidth / 50) - 1), random.randint(0, int(DisplayHeight / 50) - 1))
            LocSuc = True
            for t in Snake.Tail:
                if t['x'] == AppleLoc[0] and t['y'] == AppleLoc[1] and AppleLoc not in self.LocationList:
                    LocSuc = False
            if LocSuc:
                break
        return AppleLoc

    def NumApple(self, Number=1):  # Using the Apple.Location func to assign location for n number of them
        for L in range(Number):
            L1 = self.Location()
            self.LocationList.append((L1[0] * 50, L1[1] * 50))

    def Draw(self):  # Displays the apple
        for L in self.LocationList:
            pygame.draw.rect(window, (255, 0, 0),
                             (L[0] + Snake.Offset, L[1] + Snake.Offset, 30, 30))
            pygame.draw.rect(window, (0, 0, 0),
                             (L[0] + Snake.Offset + 12, L[1] + 2, 6, 20))

    def Eat(self):  # When the snake head is found on an apple it eats and makes a sound
        for L in self.LocationList:
            if L[0] - 10 <= Snake.x <= L[0] + 30 and L[1] - 10 <= Snake.y <= L[1] + 30:
                self.LocationList.pop(self.LocationList.index(L))
                Apple.NumAte += 1
                TailLengthen()
                mixer.music.set_volume(0.05)
                try:
                    mixer.music.play()
                except:
                    pass

    def EatCountDisplay(self):  # Displays the number of apple ate and an apple
        x = 1 if Difficulty else 2
        TextRECT(str(Apple.NumAte * x), (255, 255, 255), (), DisplayWidth - 75, 25, 50)
        pygame.draw.rect(window, (255, 0, 0), (DisplayWidth - 50, Snake.Offset, 30, 30))
        pygame.draw.rect(window, (0, 0, 0), (DisplayWidth - 50 + 12, 2, 6, 20))


def BackGround():  # Makes the chess green background
    for i in range(int(DisplayWidth / 50)):
        for j in range(int(DisplayHeight / 50)):
            if (i + j) % 2 == 0:
                pygame.draw.rect(window, (0, 100, 0), (i * 50, j * 50, 50, 50))


def GameScreen():  # This is the func that works with the game
    window.fill((0, 128, 128))
    BackGround()

    if Difficulty:  # if easy number of apples that can spawn at a time are 3 but for hard 1
        Apple.NumApples = 3
    else:
        Apple.NumApples = 1

    if len(Apple.LocationList) < Apple.NumApples:
        Apple().NumApple(Apple.NumApples - len(Apple.LocationList))

    Apple().Eat()
    Apple().Draw()
    Apple().EatCountDisplay()

    if Move:
        if Difficulty:  # if easy runs opposite wall func but if hard runs wall loss func
            OppositeWall()
        else:
            WallLoss()
        UpdateTail()
        TouchTail()
    Draw_Snake()

    Snake.TailParts = {'Head': False, 'Direction': 'Right', 'Colour': (0, 255, 0), 'x': 0, 'y': 0}


def TextRECT(text, colour, backgroundcolour, midX, midY, height, width=0, Button=False, Display=True):
    # This func was used to make displaying text or button easy
    if Display:
        if backgroundcolour != ():
            text1 = pygame.font.Font('freesansbold.ttf', height).render(text, True, colour, backgroundcolour)
        else:
            text1 = pygame.font.Font('freesansbold.ttf', height).render(text, True, colour)
        textR = text1.get_rect()
        textR.center = (midX, midY)
        window.blit(text1, textR)

        Y = midY - height // 2
        X = midX - width // 2
        if Button:
            if X <= mouse[0] <= X + width and Y <= mouse[1] <= Y + height:
                return True


def PauseScreen():  # Displays a pause screen
    global escON, run
    s = pygame.Surface((DisplayWidth - 60, DisplayHeight - 60))  # the size of your rect
    s.set_alpha(128)  # alpha level
    s.fill((255, 255, 255))  # this fills the entire surface
    window.blit(s, (30, 30))  # Placement of the translucent screen

    TextRECT('Pause Menu', (0, 0, 128), (), DisplayWidth // 2, DisplayHeight // 2 - 250, 50)

    TextRECT('U giving up already?', (128, 0, 0), (), DisplayWidth // 2, DisplayHeight // 2 - 150, 50)

    if TextRECT('Resume', (0, 0, 0), (), DisplayWidth // 2, DisplayHeight // 2 - 50, 50, width=200, Button=True):
        Change('Game')

    if TextRECT('Restart', (0, 0, 0), (), DisplayWidth // 2, DisplayHeight // 2 + 50, 50, width=200, Button=True):
        Restart()
        Change('Game')

    if TextRECT('Home', (0, 0, 0), (), DisplayWidth // 2, DisplayHeight // 2 + 150, 50, width=150, Button=True):
        Change('Home')

    if TextRECT('Exit', (0, 0, 0), (), DisplayWidth // 2, DisplayHeight // 2 + 250, 50, width=110, Button=True):
        run = False
        Restart()


def HomeScreen():  # Displays home screen
    global run
    Change('Home')
    Restart()
    window.fill((255, 255, 255))
    TextRECT('Sneke Game', (0, 128, 0), (), DisplayWidth // 2, DisplayHeight // 2 - 300, 100)

    if TextRECT('Start', (0, 128, 32), (), DisplayWidth // 2, DisplayHeight // 2 - 150, 50, 150, True):
        Restart()
        Change('Game')

    if TextRECT('Difficulty', (0, 128, 64), (), DisplayWidth // 2, DisplayHeight // 2 - 50, 50, 150, True):
        Change('Difficulty')

    if TextRECT('Skins', (0, 128, 128), (), DisplayWidth // 2, DisplayHeight // 2 + 50, 50, 150, True):
        Change('Skins')

    if TextRECT('Achievement', (0, 128, 172), (), DisplayWidth // 2, DisplayHeight // 2 + 150, 50, 150, True):
        Change('Achievement')

    if TextRECT('Credit', (0, 128, 255), (), DisplayWidth // 2, DisplayHeight // 2 + 250, 50, 150, True):
        Change('Credit')

    if TextRECT('Quit', (112, 224, 151), (), DisplayWidth // 2, DisplayHeight // 2 + 350, 50, 150, True):
        run = False

    TextRECT('By TRG', (0, 0, 0), (), DisplayWidth // 2 + 325, DisplayHeight // 2 + 365, 20)


def Restart():  # This func resets all the values/variables
    global CurrentDirection, Move, escON, Score
    SkinScreen(Button=False)
    CurrentDirection = 'Right'
    Move = True
    escON = False
    Snake.x = 50
    Snake.y = 0
    Snake.Tail = [{'Num': 0, 'Head': True, 'Direction': 'Right', 'Colour': (0, 0, 0), 'x': 450, 'y': 0},
                  {'Num': 1, 'Head': False, 'Direction': 'Right', 'Colour': (255, 255, 255), 'x': 400, 'y': 0},
                  {'Num': 2, 'Head': False, 'Direction': 'Right', 'Colour': (255, 255, 255), 'x': 350, 'y': 0},
                  {'Num': 3, 'Head': False, 'Direction': 'Right', 'Colour': (255, 255, 255), 'x': 0, 'y': 0}]
    Apple.LocationList = []
    if Difficulty:  # if hard multiplies apple ate by 2
        Score += Apple.NumAte
    else:
        Score += Apple.NumAte * 2
    Apple.NumAte = 0


def Change(Screen, List=CurrentScreen):  # Small func to make a specific element 1st
    try:
        List.insert(0, List.pop(List.index(Screen)))
    except:
        raise LookupError


def Death():  # Displays different death text of different deaths
    global DeathCount
    if CurrentDeath[0] == 'TailTouch' and DeathCount == 10:
        DeathCount = 0
        Change('None', CurrentDeath)
        Change('Home')
    elif CurrentDeath[0] == 'TailTouch':
        TextRECT('O_O ???', (0, 0, 0), (), DisplayWidth // 2, DisplayHeight // 2, 50)
        DeathCount += 1

    if CurrentDeath[0] == 'WallLoss' and DeathCount == 10:
        DeathCount = 0
        Change('None', CurrentDeath)
        Change('Home')
    elif CurrentDeath[0] == 'WallLoss':
        TextRECT('Wall = Bad!!!', (0, 0, 0), (), DisplayWidth // 2, DisplayHeight // 2, 50)
        DeathCount += 1


def DifficultyScreen():  # Displays the difficulty screen
    global Difficulty
    pygame.draw.rect(window, (121, 201, 195),
                     (DisplayWidth * 0.15, DisplayHeight * 0.35, DisplayWidth * 0.7, DisplayHeight * 0.3))
    if TextRECT('Easy', (0, 0, 255), (), DisplayWidth * 0.3, DisplayHeight * 0.5, 70, 150, True):
        Difficulty = True
        Change('Home')
    elif TextRECT('Hard', (255, 0, 0), (), DisplayWidth * 0.7, DisplayHeight * 0.5, 70, 150, True):
        Difficulty = False
        Change('Home')


def SkinScreen(Button=True):  # Displays the skin screen
    global EquippedSkin, Start, Score
    if Button:
        window.fill((121, 201, 195))

    if TextRECT('Back', (255, 255, 255), (0, 0, 0), DisplayWidth // 2 - 305, DisplayHeight // 2 - 345, 50, 150, True,
                Button) and Button:
        Change('Home')

    def SkinShop(SkinNo, Name, Location):  # Func to make the buying of the skins easy
        global EquippedSkin, Start, Score, SkinIndex
        for S in CurrentSkin:
            if S['Name'] == Name:
                SkinIndex = CurrentSkin.index(S)
                break
        if (TextRECT('$' + str(CurrentSkin[SkinIndex]['Cost']), (255, 128, 0), (), Location[0], Location[1], 50, 100,
                     True, Button and not UnlockedSkin[SkinNo - 1]) and Score >= CurrentSkin[SkinIndex]['Cost']) or \
                UnlockedSkin[SkinNo - 1]:
            if not UnlockedSkin[SkinNo - 1]:
                Score -= CurrentSkin[SkinIndex]['Cost']
            UnlockedSkin[SkinNo - 1] = True
            if TextRECT(Name, (0, 128, 0), (), Location[0], Location[1], 50, 100, True,
                        Button) or EquippedSkin == SkinNo:
                if Start:
                    Start = False
                    for S in CurrentSkin:
                        if S['Name'] == Name:
                            Change(S, CurrentSkin)
                EquippedSkin = SkinNo

    if TextRECT('Original', (0, 128, 0), (), DisplayWidth * 0.25, DisplayHeight * 0.5, 50, 100, True,
                Button) or EquippedSkin == 0:
        if Start:
            Start = False
            for S in CurrentSkin:
                if S['Name'] == 'Original':
                    Change(S, CurrentSkin)
        EquippedSkin = 0

    SkinShop(1, 'Red', (DisplayWidth * 0.5, DisplayHeight * 0.5))
    SkinShop(2, 'Purple', (DisplayWidth * 0.75, DisplayHeight * 0.5))
    SkinShop(3, 'Lime', (DisplayWidth * 0.33, DisplayHeight * 0.75))
    SkinShop(4, 'Gold', (DisplayWidth * 0.66, DisplayHeight * 0.75))

    if Button:  # Shows the skin preview
        Start = True
        for t in CurrentSkin[0]:
            for n in range(len(CurrentSkin[0])):
                if t == 'Name':
                    break
                elif t == 'Head':
                    pygame.draw.rect(window, CurrentSkin[0]['Head'], (560, 60, 30, 30))
                    break
                elif t == 'Cost':
                    pass
                elif t % (len(CurrentSkin[0]) - 3) == n:
                    pygame.draw.rect(window, CurrentSkin[0][n], (560 - 50 * (n + 1), 60, 50, 30))
                    break


def CreditScreen():  # Displays credit skin
    window.fill((121, 201, 195))
    if TextRECT('Back', (255, 255, 255), (0, 0, 0), DisplayWidth // 2 - 305, DisplayHeight // 2 - 345, 50, 150, True):
        Change('Home')
    TextRECT('Made by TRG', (0, 0, 0), (), DisplayWidth // 2, DisplayHeight // 2, 100)


def AchievementScreen():  # Displays your achievement
    window.fill((121, 201, 195))

    if TextRECT('Back', (255, 255, 255), (0, 0, 0), DisplayWidth // 2 - 305, DisplayHeight // 2 - 345, 50, 150, True):
        Change('Home')

    TextRECT('Achievement', (255, 255, 255), (), DisplayWidth * 0.5, DisplayHeight * 0.2, 100)
    TextRECT('Number of Apples Ate: ' + str(Score), (255, 255, 255), (), DisplayWidth * 0.5, DisplayHeight * 0.4, 50)
    if UnlockedSkin[-1]:
        TextRECT('Knight in Shining Armor', (218, 165, 32), (255, 195, 100), DisplayWidth * 0.5, DisplayHeight * 0.6,
                 50)
    else:
        TextRECT('Get Golden Skin', (255, 255, 255), (), DisplayWidth * 0.5, DisplayHeight * 0.6, 50)
    if len([x for x in UnlockedSkin if x]) == 4:
        TextRECT('All Skins Collected', (192, 192, 192), (128, 128, 128), DisplayWidth * 0.5, DisplayHeight * 0.8, 50)
    else:
        TextRECT('Get All the Skins', (0, 0, 0), (), DisplayWidth * 0.5, DisplayHeight * 0.8, 50)


def UpdateWindow():  # The main func which displays the different screens and updates the frames
    if CurrentDeath[0] == 'None':
        if CurrentScreen[0] == 'Home':  # According to which screen is first in list, that screen is displayed
            HomeScreen()
        elif CurrentScreen[0] == 'Game':
            GameScreen()
        elif CurrentScreen[0] == 'Pause':
            PauseScreen()
        elif CurrentScreen[0] == 'Difficulty':
            DifficultyScreen()
        elif CurrentScreen[0] == 'Skins':
            SkinScreen()
        elif CurrentScreen[0] == 'Credit':
            CreditScreen()
        elif CurrentScreen[0] == 'Achievement':
            AchievementScreen()

    Death()

    pygame.display.update()


while run:  # The main loop
    pygame.time.delay(DelayTime)

    for event in pygame.event.get():  # If you close the window it quits
        if event.type == pygame.QUIT:
            run = False

    if pygame.mouse.get_pressed()[0]:  # Takes the location of the mouse
        mouse = pygame.mouse.get_pos()
    else:
        mouse = (0, 0)

    key = pygame.key.get_pressed()  # Stores the key that are pressed

    if (key[pygame.K_d] or key[
        pygame.K_RIGHT]) and CurrentDirection != 'Left':  # This part decides how the snake moves and cannot accept opposite movement
        CurrentDirection = 'Right'
    if (key[pygame.K_w] or key[pygame.K_UP]) and CurrentDirection != 'Down':
        CurrentDirection = 'UP'
    if (key[pygame.K_a] or key[pygame.K_LEFT]) and CurrentDirection != 'Right':
        CurrentDirection = 'Left'
    if (key[pygame.K_s] or key[pygame.K_DOWN]) and CurrentDirection != 'UP':
        CurrentDirection = 'Down'
    if key[pygame.K_ESCAPE] and ButtonCounter == 0 and (CurrentScreen[0] == 'Game' or CurrentScreen[0] == 'Pause'):
        ButtonCounter = 1
        if escON:
            escON = False
            Change('Game')
        else:
            escON = True
            Change('Pause')
    elif ButtonCounter == 200:
        ButtonCounter = 0
    elif ButtonCounter > 0:
        ButtonCounter += 1

    if count % 100 == 0 and Move and CurrentScreen[0] == 'Game':
        if CurrentDirection == 'Right':
            Snake.x += 50
            CurrentDirection = 'Right'

        if CurrentDirection == 'UP':
            Snake.y -= 50
            CurrentDirection = 'UP'

        if CurrentDirection == 'Left':
            Snake.x -= 50
            CurrentDirection = 'Left'

        if CurrentDirection == 'Down':
            Snake.y += 50
            CurrentDirection = 'Down'
    if count % 100 == 0:
        UpdateWindow()

    count += 1

A = str(int(Score ** 2 + 127))
B = str(int(EquippedSkin ** 4 + 890))
C = ''
for i in UnlockedSkin:
    C += str(int(int(i) ** 8 + 2837)) + ' '
D = str(int(Difficulty ** 5 + 1890))
f.write(A + '/' + B + '/' + C + '/' + D)  # This is the encryption that saves the data in a txt file

f.close()
