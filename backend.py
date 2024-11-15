import random
import symbols
class Backend:
    
    def __init__(self):
        self.rows = 7 
        self.columns = 7
        self.grid = [[] for _ in range(self.rows)]
        self.pop = []
        self.payoutTable = {
                1 : 0.05,
                2 : 0.1,
                3 : 0.1,
                4 : 0.15,
                5 : 0.2,
                6 : 0.25,
                7 : 0.35,
                8 : 0.5
            }
        self.winnings = 0
        self.multi = 0 


    def fillGrid(self):
        self.winnings = 0
        self.grid = [[] for _ in range(self.rows)]
        for i in range(self.rows):
            for j in range(self.columns):
                randomNum = random.randint(1,489011)
                self.grid[i].append(randomNum)
        for i in range(self.rows):
            for j in range(self.columns):
                self.grid[i][j]=self.convert(self.grid[i][j])

    def convert(self, num):
        if 1 <= num <= 113500:
            return 1
        elif 113501 <= num <= 206500:
            return 2
        elif 206501 <= num <= 279000:
            return 4
        elif 279001 <= num <= 351500:
            return 5
        elif 351501 <= num <= 403500:
            return 6
        elif 403501 <= num <= 455500:
            return 7
        elif 455501 <= num <= 487500:
            return 8
        elif 487501 <= num <= 488000:
            return 9
        elif 488001 <= num <= 488500:
            return 10
        elif 488501 <= num <= 488800:
            return 11
        elif 488801 <= num <= 488950:
            return 12
        elif 488951 <= num <= 489000:
            return 13
        elif 489001 <= num <= 489010:
            return 14
        elif num == 489011:
            return 15
        

    def createGrids(self, baseline):
        self.fillGrid()
        print (self.grid)
        symbolGrid = [[None for _ in range(self.columns)] for _ in range(self.rows)]
        for i in range(len(symbolGrid)-1,-1,-1):
            for j in range(self.columns):
                if (i == len(symbolGrid)-1):
                    symbolGrid[i][j] = symbols.Symbols(self.grid[i][j], j + 1, baseline)
                else:
                    symbolGrid[i][j] = symbols.Symbols(self.grid[i][j], j + 1, symbolGrid[i+1][j].rect)
        return symbolGrid
     

    def checkGrid(self):
        global scatterCount, multiCount
        global pop
        pop = []
        scatterCount = 0 
        self.multi = 0
        seen = set()
        
        for i in range(self.rows):
            for j in range(self.columns):
                if (i,j) in seen:
                    continue
                elif self.grid[i][j] == 9:
                    seen.add((i,j))
                    scatterCount += 1 
                elif self.grid[i][j] in range (10,16):
                    seen.add((i,j))
                    self.multi += self.getMulti(self.grid[i][j])
                else:
                    currentIsland = []
                    target = self.grid[i][j]
                    self.check(i,j,seen, currentIsland, target)
                    if len(currentIsland) >= 5:
                        pop.append(currentIsland)
        if len(pop) == 0:
            return False 
        else:
            return True
   
    def check(self, i, j, seen, currentIsland, target):
        if i < 0 or i >=self.rows or j < 0 or j >= self.columns:
            return
        if (i,j) in seen or self.grid[i][j] != target :
            return
        seen.add((i,j))
        currentIsland.append((i,j))
        self.check(i+1,j,seen, currentIsland,target)
        self.check(i-1,j,seen, currentIsland,target)
        self.check(i,j+1,seen, currentIsland,target)
        self.check(i,j-1,seen, currentIsland,target)

    def getMulti(self, num):
        if num == 10:
            return 2
        if num == 11:
            return 3
        if num == 12:
            return 4
        if num == 13:
            return 5
        if num == 14:
            return 10 
        if num == 15:
            return 100
    
    def popIslands(self, symbolGrid, timer1, timer2):
        if not timer2.active:
            if timer1.active:
                for islands in pop:
                    for i in islands:
                        if self.grid[i[0]][i[1]] != 0:
                            self.winnings += self.payoutTable[self.grid[i[0]][i[1]]]
                        self.grid[i[0]][i[1]] = 0
                        symbolGrid[i[0]][i[1]].swapColors()
            else: 
                for islands in pop:
                    for i in islands:
                        symbolGrid[i[0]][i[1]] = None
                return True
            return False
                
               
    def tumble(self, symbolGrid, baseline): 
        for j in range(self.columns):
            nonZeros = []
            nonNones = []
            zeros = []
            for i in range(self.rows):
                if self.grid[i][j] != 0:
                    nonZeros.append(self.grid[i][j])
                    nonNones.append(symbolGrid[i][j])
                else:
                    zeros.append(i)
            for i in range(self.rows-1, -1, -1):
                if nonZeros:
                    placeHolder = nonZeros.pop()
                    self.grid[i][j] = placeHolder
                    placeHolder = nonNones.pop()
                    symbolGrid[i][j] = placeHolder
                else: 
                    self.grid[i][j] = 0 
                    symbolGrid[i][j] = None
        
        self.reinitalizeStoppingPoint(symbolGrid, baseline)

    
    def reinitalizeStoppingPoint(self, symbolGrid, baseline):
        for i in range(self.rows):
            for j in range(self.columns):
                if symbolGrid[i][j] == None:
                    continue
                if (i == len(symbolGrid)-1):
                    symbolGrid[i][j].stoppingPoint =  baseline
                else:
                    symbolGrid[i][j].stoppingPoint =  symbolGrid[i+1][j].rect          
        
    
    def refillGrid(self, symbolGrid, baseline):  
        for i in range(len(symbolGrid)-1,-1,-1):
            for j in range(self.columns):
                if self.grid[i][j] == 0:
                    randomNum = random.randint(1,489011)
                    self.grid[i][j] = self.convert(randomNum)
                    if (i == len(symbolGrid)-1):
                        symbolGrid[i][j] = symbols.Symbols(self.grid[i][j], j + 1, baseline)
                    else:
                        symbolGrid[i][j] = symbols.Symbols(self.grid[i][j], j + 1, symbolGrid[i+1][j].rect)

    