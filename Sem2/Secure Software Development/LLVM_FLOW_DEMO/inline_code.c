#include <stdio.h>

int double_sum(int a, int b) {
    int sum = a + b;
    return sum * 2;
}

int main() {
    int x = 5;
    int y = 10;
    int result = double_sum(x, y) + double_sum(x, y);
    printf("Final Result: %d\n", result);  // (5 + 10) * 2 + (5 + 10) * 2 = 60
    return 0;
}