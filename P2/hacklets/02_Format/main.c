#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main()
{
    printf("Hi, this is the format string challenge! Try to overwrite the value\n");
    fflush(stdout);
    int decision = 0;
    size_t address = 0;
    int x = 1;
    char buffer[128];
    do
    {
        printf("First you will need to give me an address\n");
        fgets(buffer, 128, stdin);
        address = atol(buffer);
        printf("0x%zx\n", address);
        //Clear buffer
        memset(buffer, 0, sizeof(char) * 128);
        printf("Ok, give me a string\n");
        fflush(stdout);
        //No gets here
        fgets(buffer, 128, stdin);
        printf(buffer);

    } while (x != 0x1337);
    printf("Well done, here is your flag: ");
    FILE *f = fopen("flag.txt", "r");
    if (f == NULL)
        return -1;
    char buf[128];
    memset(buf, 0, sizeof(buf));
    fread(&buf, 1, sizeof(buf) - 1, f);
    printf("%s", buf);
    fflush(stdout);
    return 0;
}