#include <stdio.h>
#include <string.h>
#include <stdlib.h>


//Not much to do here. Try to get the flag anyways
int main()
{
    printf("Hi from 0x%zx\n");
    char buffer[0256];
    fgets(buffer,256, stdin);
    printf("Bye");
}