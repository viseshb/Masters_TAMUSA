// cfg.c
#include <stdio.h>

void check(int x) {
    if (x > 0) {
        if (x > 0) { // redundant
            printf("Positive\n");
        }
    } else {
        printf("Non-positive\n");
    }

    // Redundant branch
    if (x > 0) {
        printf("Definitely Positive\n");
    }
}

int main() {
    check(5);
    return 0;
}
