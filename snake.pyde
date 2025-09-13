## Variabler
# Vindues størrelse (Kan ændres på)
windowSize = 1000

# Altså roden af Arealet, så arealet er 5^2 = 25 felter i alt (Kan ændes på)
count = 10

# Hvor tit vi opdater skærmbilledet. Slanges hastighed er påvirket (Kan ændres på)
framesPerSecond = 6

# Den aktuelle størrelse på hver felt
fieldSize = windowSize / count

# En liste af koordinater med slanges position. Head first, tail last
snakePositions = []

# Slanges længde
snakeLength = 3

# En default value for direction
uninitialized = -1

# Hvad retning som slanges vil bevæger sig
direction = uninitialized

# Den sidste retning som slangen bevægede sig
previousDirection = uninitialized

# Hvis vi har ramt væggen
collision = False

# 
appleCoordinate = (uninitialized, uninitialized)
appleCollision = False

## Funktioner
# Metoden bliver kaldt ved hvert tastatur tryk
def keyPressed():
    global direction
    global collision
    global appleCoordinate
    global snakeLength
    
    # Her tjekker vi om det var et specielt tegn 
    # https://py.processing.org/reference/key
    if key == CODED:
        # Vi tjekker om det var en pil-tast, og at den ikke går modsat den tidligere ryk
        # https://py.processing.org/reference/keycode
        if keyCode == UP and previousDirection != DOWN:
            direction = UP
        elif keyCode == DOWN and previousDirection != UP:
            direction = DOWN
        elif keyCode == RIGHT and previousDirection != LEFT:
            direction = RIGHT
        elif keyCode == LEFT and previousDirection != RIGHT:
            direction = LEFT
    elif key == ENTER and collision == True:
        while len(snakePositions) > 0:
            deleteTail()
        
        drawField(appleCoordinate[0], appleCoordinate[1])
        
        # Resetter variabler til 
        snakeLength = 3
        setupSnake()
        drawSnake()
        spawnApple()
        direction = uninitialized
        collision = False
        
            

# Her tegner vi slangen for første gang
def setupSnake():
    global snakePositions
    global previousDirection

    # Starter med at rydde listen fra f.eks. tidligere spil
    snakePositions = []

    # Starter  med at finde et helt tilfældigt felt indenfor spillepladen    
    headCoordinate = generateRandomCoordinate()
    snakePositions.append(headCoordinate)
    
    # Hvis hele slangen kan være til højre for hovedt så gør vi det. headCoordinate[0] == x koordinat OG headCoordinate[1] == y koordinat
    if headCoordinate[0] < count - snakeLength:
        # Gå til højre
        snakePositions.append((headCoordinate[0] + 1, headCoordinate[1]))
        snakePositions.append((headCoordinate[0] + 2, headCoordinate[1]))
        previousDirection = LEFT
    else:
        # Gå til venstre
        snakePositions.append((headCoordinate[0] - 1, headCoordinate[1]))
        snakePositions.append((headCoordinate[0] - 2, headCoordinate[1]))
        previousDirection = RIGHT



def setup():
    size(windowSize, windowSize)
    frameRate(framesPerSecond)

    setupSnake()
    drawBoard()
    drawSnake()
    spawnApple()


# Vores "main" loop
def draw():
    # Hvis spillet venter på input eller man er kollideret med væggen, så slutter vi tidligt
    if direction == uninitialized or collision:
        return

    # Hvis spillet stadig er igang, så rykker vi på slangen
    moveSnake()

# Til at tegne et æble
def drawApple(x, y):
    fill(255, 0, 0)
    square(x * fieldSize, y * fieldSize, fieldSize)
    
# Til at tegne slanges hoved
def drawSnakeHead(x, y):
    fill(150, 255, 0)
    square(x * fieldSize, y * fieldSize, fieldSize)
    
# Til at tegne det enkelte kropsdel af slangen
def drawSnakeBody(x, y):
    fill(0, 255, 0)
    square(x * fieldSize, y * fieldSize, fieldSize)
    
# Til at tegne slangen når spillet startes 
def drawSnake():
    drawSnakeHead(snakePositions[0][0], snakePositions[0][1])
    for i in range(1, snakeLength): # 1, 2
        drawSnakeBody(snakePositions[i][0], snakePositions[i][1])

# Til at tegne det enkelte felt 
def drawField(x, y):
    fill(55, 125, 200)
    square(x * fieldSize, y * fieldSize, fieldSize)

# Til at tegne hele brættet
def drawBoard():
    # For hver kolonne 
    for x in range(count): # 0, 1, 2, 3, 4
        # for hver række i den enkelte kolonne
        for y in range(count): # 0, 1, 2, 3, 4
            drawField(x, y)
            
            
# Fjern halen først, så ryk hovedt i direction
def moveSnake():
    # fjern halen
    deleteTail()
    # Ryk hovedt
    moveHead()
    # Tjek om vi kollidere med en væg, æble, sig selv, eller man har udfyldt hele banen
    collisionDetector()
            
def deleteTail():
    global appleCollision
    global snakeLength
    
    if appleCollision:
        appleCollision = False
        snakeLength = snakeLength + 1
    else:
        tailPosition = snakePositions.pop()
        drawField(tailPosition[0], tailPosition[1])

def moveHead():
    global direction
    global previousDirection
    
    
    previousDirection = direction
    newDirection = ''
    # Her finder vi det nye koordinat ud fra hovedts nyværende position og piltastetryk.
    # UP så trække vi en fra y værdien
    if direction == UP:
        newDirection = (snakePositions[0][0], snakePositions[0][1] - 1)
    # DOWN så tilføjer vi en til y værdien
    elif direction == DOWN:
        newDirection = (snakePositions[0][0], snakePositions[0][1] + 1)
    # LEFT så trække vi en fra x værdien
    elif direction == LEFT:
        newDirection = (snakePositions[0][0] - 1, snakePositions[0][1])
    # RIGHT så tilføjer vi en til x bærdien
    elif direction == RIGHT:
        newDirection = (snakePositions[0][0] + 1, snakePositions[0][1])
    # Hvis det ikke er en fra overstående, så returnere vi tidligt
    else: 
        return
    
    # Her tegner vi det gamle hovedt om til krop
    drawSnakeBody(snakePositions[0][0], snakePositions[0][1])
    # Tilføjer hovedt nye position til starten af listen af slanges koordinater
    snakePositions.insert(0, newDirection)
    # Her tegner vi det nye slangehoved
    drawSnakeHead(newDirection[0], newDirection[1])

# Vi tjekker om et koordinat-værdi i x og y vil være udenfor banen (0 til count -1)
def collisionDetector():
    global collision
    global appleCollision
    
    head = snakePositions[0]
    
    # Tjekker for højre og venstre væg
    if head[0] < 0 or head[0] >= count:
        collision = True
    # Tjekker for oppe og neder væg
    elif head[1] < 0 or head[1] >= count:
        collision = True
        

    # Tjekker om man ramte sig selv
    for i in range(1, len(snakePositions)):
        if snakePositions[i][0] == head[0] and snakePositions[i][1] == head[1]:
            collision = True
            break

    if collision:
        return
        
    if head[0] == appleCoordinate[0] and head[1] == appleCoordinate[1]:
        appleCollision = True
        spawnApple()
        
    if snakeLength == count ** 2:
        collision = True

# Til at generere et æble
def spawnApple():
    global appleCoordinate
    
    # en variable til at holde alle tomme felter
    fields = []
    # For hver række
    for x in range(count):
        # I hver kolonne
        for y in range(count):
            # kontrol variable om feltet ikke er tomt
            found = False
            # For hver koordinat af slanges
            for coordinate in snakePositions:
                if coordinate[0] == x and coordinate[1] == y:
                    found = True
                    break
            
            # Hvis vi fandt den blandt slanges koordinater, så hopper vi videre til den næste kolonne
            if found:
                continue
            
            # Hvis ikke, så tilføjer vi den til listen
            fields.append((x, y))
    
    # Antal tomme felter
    c = len(fields)
    # Et tilfædigt int fra 0 til (og ikke med) c
    index = int(random(c))
    # Det tilfældige koordinat
    appleCoordinate = fields[index]
    # Vi tegner æblet på det koordinant
    drawApple(appleCoordinate[0], appleCoordinate[1])
    
                    

# Generere et tilfældet koordinate
def generateRandomCoordinate():
    # random(count) vil finde et tilfædet float værdi fra 0,0 til hvad count værdi er. int() konverter den float til en integer
    x = int(random(count))
    y = int(random(count))
    return (x, y)
