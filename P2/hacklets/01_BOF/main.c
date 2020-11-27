#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

//Read data to buffer until "\0" is found
void readToBuffer(char *buffer)
{
	char c = 0;
	int index = 0;
	do
	{
		c = getchar();
		buffer[index++] = c;
	} while (c != '\0');
}

//You should try to get here!
void target()
{
	printf("Welcome! \n");
	FILE *f = fopen("flag.txt", "r");
	if (f == NULL)
		return;
	char buf[128];
	memset(buf, 0, sizeof(buf));
	fread(&buf, 1, sizeof(buf) - 1, f);
	printf("%s", buf);
	fflush(stdout);
}

int main()
{
	char buffer[20];
	printf("Hi from main at 0x%zx, say something!\n", (size_t)&main);
	fflush(stdout);
	readToBuffer(buffer);
	printf("Done here!\n");
	return 0;
}