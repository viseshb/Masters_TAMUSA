// dead.c
#include <stdio.h>

int main() {
    int a = 10;
    int b = 20;  // unused variable
    int c = a + 5;
    
    printf("Value of c: %d\n", c);

    return 0;

    // Dead code: this part will never be executed
    printf("This is dead code\n");
    int d = 100;
}
