#include <stdio.h>
#include <stdlib.h>

void binsh() {
    system("/bin/sh");
}

// Simple Echo Program
int main(void) {
    char dump[101];
    while(1) {
        fgets(dump, 100, stdin);
        printf(dump); // vuln
        fflush(stdout);
    }
    return 0;
}
