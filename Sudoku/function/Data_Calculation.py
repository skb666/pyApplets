import copy

class Sudoku:
    def __init__(self,sudoku):
        self._sudoku=sudoku
        self._solve_sudoku=copy.deepcopy(sudoku)
        self.__Solve()

    def solved(self):
            t=('+'+'-'*7)*3+'+\n'
            for i in range(9):
                t+='|'
                for j in range(9):
                    t+=' '+str(self._solve_sudoku[i][j])
                    if (j+1)%3==0:t+=' |'
                t+='\n'
                if (i+1)%3==0 and i!=8:t+=('+'+'-'*7)*3+'+\n'
            t+=('+'+'-'*7)*3+'+'
            return t

    def __str__(self):
        t=('+'+'-'*7)*3+'+\n'
        for i in range(9):
            t+='|'
            for j in range(9):
                t+=' '+(str(self._sudoku[i][j])if self._sudoku[i][j]!=0 else '.')
                if (j+1)%3==0:t+=' |'
            t+='\n'
            if (i+1)%3==0 and i!=8:t+=('+'+'-'*7)*3+'+\n'
        t+=('+'+'-'*7)*3+'+'
        return t

    def __findNextCellToFill(self,i,j):
        for x in range(i,9):
            for y in range(j,9):
                if self._solve_sudoku[x][y]==0:
                    return x,y
        for x in range(0,9):
            for y in range(0,9):
                if self._solve_sudoku[x][y]==0:
                    return x,y
        return -1,-1

    def __isValid(self,i,j,e):
        rowOk=all([e!=self._solve_sudoku[i][x] for x in range(9)])
        if rowOk:
            columnOk=all([e!=self._solve_sudoku[x][j] for x in range(9)])
            if columnOk:
                secTopX,secTopY=3*(i//3),3*(j//3) 
                for x in range(secTopX,secTopX+3):
                    for y in range(secTopY,secTopY+3):
                        if self._solve_sudoku[x][y]==e:
                            return False
                return True
        return False

    def __Solve(self,i=0,j=0):
        i,j=self.__findNextCellToFill(i,j)
        if i==-1:return True
        for e in range(1,10):
            if self.__isValid(i,j,e):
                self._solve_sudoku[i][j]=e
                if self.__Solve(i,j):
                    return True
                self._solve_sudoku[i][j]=0
        return False

