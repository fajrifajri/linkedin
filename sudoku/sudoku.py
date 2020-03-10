from time import process_time 

problem = [
    [0,0,0,5,0,0,0,9,0],
    [0,3,0,0,0,0,0,0,5],
    [0,0,0,8,2,7,0,0,0],
    [1,0,0,4,0,6,0,0,0],
    [0,9,0,0,0,0,0,7,0],
    [2,8,0,0,5,0,0,0,0],
    [4,0,5,0,0,0,0,0,0],
    [7,0,0,0,0,0,9,0,2],
    [0,0,0,0,0,0,1,5,6]
]

def print_sudoku(s):
    for y in range(len(s)):
        if y%3 == 0:
            print("\n============", end="")
        for x in range(len(s)):
            if x == 0:
                print("")
            if x %3 == 0:
                print("|", end="")
            print(s[y][x], end="")

def location_zero(s):
    for y in range(len(s)):
        for x in range(len(s[y])):
            if s[y][x] == 0:
                return(x,y)
    return None

def check_solution(s, num, co_x, co_y):
    #check row
    for y in range(len(s[co_y])):
        if s[co_y][y]==num and co_x != y:
            return False
    
    #check column
    for x in range(len(s)):
        if s[x][co_x]==num  and co_y != x:
            return False
    
    # check box
    for y in range(3*int(co_y/3),3*int(co_y/3) +3):
        for x in range(3*int(co_x/3), 3*int(co_x/3) +3):
            if s[y][x] == num and (x,y) != (co_x,co_y):
                return False

    return True

def solve_sudoku(s):
    zero = location_zero(s)
    if not zero:
        return True
    else:
        x,y = zero
    for i in range(1,10):
        if check_solution(s,i,x,y):

            s[y][x] = i
            if solve_sudoku(s):
                return True
            s[y][x] = 0
    # triggering backtrack
    return False
    



#print_sudoku(problem)
print("\nSolution")
start_time = process_time() 
solve_sudoku(problem)
stop_time = process_time()
print_sudoku(problem)
print("\nprocessing time = " + str(stop_time - start_time) + " s")
