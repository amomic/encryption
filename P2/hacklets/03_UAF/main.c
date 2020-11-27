#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <sys/stat.h>


char *create_with_size(size_t bytes)
{
	char *c = malloc(sizeof(char) * bytes);
	if(c == NULL)
	{
		exit(0);
	}
	return c;
}

int read_integer()
{
	int temp = 0;
	scanf("%d", &temp);
	while(getchar() != '\n');
	return temp;
}

int main()
{
	//Array that will hold our strings
   char *pointer_array[10] = {0,0,0,0,0,0,0,0,0,0};
   size_t string_sizes[10] = {0,0,0,0,0,0,0,0,0,0};
   int secret = 0;
   int decision = 0;
   while(decision != 6)
   {
   	puts("0: Create new regular string");
   	puts("1: Create super secret string");
   	puts("2: Fill regular string");
   	puts("3: Fill secret string");
   	puts("4: Delete Entry");
   	puts("5: Print Content");
   	puts("6: Stop");
    decision = read_integer();
   	switch(decision)
   	{
   		case 6:
   			exit(0);
   		case 1:
   		case 0:
   		{
   			printf("At which index?\n");
   			size_t index = read_integer();
   			if(index >= 10)
   			{
   				puts("No!");
   				continue;
   			}
   			printf("How many characters?\n");
   			int size = read_integer();
   			pointer_array[index] = create_with_size(size);
   			printf("Done, got new string at %p\n", pointer_array[index]);
   			secret |= ((1&decision)<<index);
   			string_sizes[index] = size; 
   			continue;
   		}

   		case 2:
   		{
   			printf("At which index?\n");
   			size_t index = read_integer();
   			if(index >= 10 || (secret & (1<<index)) != 0)
   			{
   				puts("No!");
   				continue;
   			}
   			printf("Work in progress\n");
   			continue;
   		}
   		case 3:
   		{
   			printf("At which index?\n");
   			size_t index = read_integer();
   			if(index >= 10 || (secret & (1<<index)) == 0 || pointer_array[index] == NULL)
   			{
   				puts("No!");
				continue;
   			}
   			printf("Give me a file name\n");
   			char fbuf[128];
   			fgets(fbuf, 127, stdin);
   			for(char *p = fbuf; p < fbuf+127; p++)
   			{
   				if(*p == ' ' || *p == '\n')
   				{
   					*p = '\0';
   					break;
   				}
   			}
   			printf("Reading %s for you\n", fbuf);
   			FILE *f = fopen(fbuf, "r");
   			if(f == NULL)
   			{
   				puts("Could not open file");
   				continue;
   			}
   			fgets(pointer_array[index], string_sizes[index]-1, f);
   			fclose(f);
   			//Debug functionality
   			//printf("%s\n", pointer_array[index]);
   			break;
   		}
   		case 4:
   		{
   			puts("Which entry do you want to delete?");
   			size_t index = read_integer();
   			if(index >= 10)
   			{
   				puts("No!");
   				continue;
   			}
   			free(pointer_array[index]);
   			secret &= ~((1) << index);
   			continue;
   		}
   		case 5:
   		{
   			puts("Which string do you want to print?");
   			size_t index = read_integer();
   			if(index >= 10 || pointer_array[index] == NULL)
   			{
   				puts("NO!");
   				continue;
   			}
   			if(secret & (1 << index))
   			{
   				puts("No, this information is secret!");
   				continue;
   			}
   			printf("%s\n", pointer_array[index]);
   			continue;
   		}
   		
   	}
   }
}