#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

struct user
{
  char name[31];
  char is_admin;
};


int main(int argc, char** argv)
{
    printf("Welcome to the Login service.\n");
    struct user user_;

    user_.is_admin = 0;
    gets(user_.name);

    int compare_value = 0x61; //char c = 'a';
    if (user_.is_admin == compare_value)
    {
        printf("Hello admin\n");
        char flag_buffer[32];
        FILE* f = fopen("flag.txt", "r");
        size_t len = fread(flag_buffer, 1, sizeof(flag_buffer), f);
        printf("%s\n",flag_buffer);
    }
    else
    {
        printf("You are no admin sry\n");
    }
}
