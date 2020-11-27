#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char * argv[])
{
	puts("Hello from demo 1!");
	puts("Where am I?");
	size_t x = 0;
	scanf("%zx", &x);
	printf("%p\n", &main);
	if(x != (size_t)&main)
	{
		puts("Nope");
		exit(0);
	}
	puts("Correct!");
	
	int c = 0;
	printf("A random stack variable is at %p\n", &c);

	puts("Now, where was x again?");

	scanf("%zx", &x);
	if(x != (size_t) &x)
	{
		puts("Argh, almost got it");
		exit(0);
	}
	puts("Hey, nice");
	puts("Now let's see if the args are correct");
	if(strcmp(argv[0], "not_demo1"))
	{
		puts("Hm, no");
		exit(0);
	}
	puts("Good");
	puts("And now the environment");
	char *secret = getenv("SECRET");
	if(!strcmp(secret, "super-secret-password"))
	{
		puts("Well done, you solved this challenge");
		system("cat flag.txt");
		exit(1);
	}
}
