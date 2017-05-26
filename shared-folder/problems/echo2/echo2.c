#include <stdio.h>
#include <stdlib.h>

void shell() {
    puts("Can you see me?");
    system("/bin/sh");
}

int main(void) {
    char name[100];
    printf("**Greeting service**\nWhat's your name: ");
    fflush(stdout);
    gets(name);
    printf("Hello, %s\n", name);
    fflush(stdout);
    return 0;
}
