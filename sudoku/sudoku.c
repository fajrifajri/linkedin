#include <stdio.h> // printf
#include <stdbool.h> // bool

#define true 1 
#define false 0
#define NOLL 0 // empty cell
#define SIZE 9 // size of sudoku

bool check_null(int sud[SIZE][SIZE], int x, int y); // find block with zero value
bool check_answer(int sud[SIZE][SIZE], int num, int x, int y); // check if the solution is valid


void print_sudoku(int sud[9][9]) {
    for(int y = 0; y<9; y++) {
        if(y%3==0) {
            printf("\n============");
        }
        for(int x = 0; x<9; x++) {
            if(x==0) {
                printf("\n");
            }
            if(x%3==0) {
                printf("|");
            }
            printf("%d",sud[y][x]);
        }
    }
    printf("\n============\n");
}

bool solve(int sud[9][9]) {
    int x = 0;
    int y = 0;
    if(!check_null(sud, x, y)) {
        return(true); // answer is correct
    }
    for(int num=1; num<=9; num++) {
    // check if answer is correct
        if(check_answer(sud, x, y, num)) {
            sud[y][x] = num;
            if(solve(sud)) {
                return(true);
            }
            sud[y][x] = NOLL;
        }
    }
    return(false); // backtracking

}

bool check_null(int sud[9][9], int x, int y) {
    for(int y = 0; y <9;y++) {
        for(int x = 0; x<9; x++) {
            if(sud[y][x]==NOLL) {
                return(true);
            }
        }
    }
    return false;
}

bool check_x(int sud[9][9], int x, int num) {
    for(int y = 0; y<9; y++) {
        if(sud[y][x] == num) {
            return(true);
        }
    }
    return(false);
}

bool check_y(int sud[9][9], int y, int num) {
    for(int x=0; x<9; x++) {
        if(sud[y][x] == num) {
            return(true);
        }
    }
    return(false);
}

bool check_box(int sud[9][9], int x, int y, int num) {
    x = x - x%3;
    y = y - y%3;
    for(int row = 0; row < 3; row++) {
        for(int col=0; col < 3; col++) {
            if(sud[row+y][col+x] == num) {
                return(true);
            }
        }
    }
    return(false);
}

bool check_answer(int sud[9][9], int x, int y, int num) {
    return(
        !check_x(sud, x, num) && 
        !check_y(sud, y, num) && 
        !check_box(sud, x, y,num) &&
        sud[y][y] == NOLL);
}
   

int main() {
    int problem[9][9] = {
        {0,0,0,5,0,0,0,9,0}, // row 1
        {0,3,0,0,0,0,0,0,5}, // row 2
        {0,0,0,8,2,7,0,0,0}, // row 3
        {1,0,0,4,0,6,0,0,0}, // row 4
        {0,9,0,0,0,0,0,7,0}, // row 5
        {2,8,0,0,5,0,0,0,0}, // row 6
        {4,0,5,0,0,0,0,0,0}, // row 7
        {7,0,0,0,0,0,9,0,2}, // row 8
        {0,0,0,0,0,0,1,5,6} // row 9
    };
    print_sudoku(problem);
    if(solve(problem) == true) {
        print_sudoku(problem);
    }
    return(false);
    
}