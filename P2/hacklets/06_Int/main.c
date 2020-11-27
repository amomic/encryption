
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
typedef struct MyString_
{
    char *content;
    size_t string_length;
} String;


String *createStringArray(int amount)
{
    int overall_size = amount * sizeof(String);
    return malloc(overall_size);
}

int main()
{
    while(1)
    {
        puts("1: Create String array\n2: Fill string at position\n3: exit");
        int choice = 0;
        scanf("%d", &choice);
        switch (choice)
        {
        case 1:
            puts("For how many strings should i allocate?\n");
            int amount = 0;
            scanf("%d", &amount);
            if(amount < 0 || amount > round((float)__INT_MAX__ / sizeof(String)))
            {
                printf("Don't be ridiculous\n");
                continue;
            }
            void *x = createStringArray(amount);
            if(x == NULL)
            {
                goto panic;
            }
            break;
        
        case 2:
        {
            printf("Sorry, not implemented\n");
            continue;
        }
        case 3:
        {
            puts("Bye!\n");
            return 0;
        }

        default:
            break;
        }
    }
panic: 
    puts("This should not happen! Here, take the flag\n");
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