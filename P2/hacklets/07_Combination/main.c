#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/mman.h>
#include <malloc.h>
#include <stdint.h>
void memprotect_wrapper(void *addr, int prot, size_t len)
{
	if(prot & PROT_EXEC)
	{
		puts("Stage 1 solved!\n");
		puts("Read flag 2 for a bonus point which can be exchanged for a cookie at the end of the semester!");
		printf("Well done, here is your file: ");
        FILE *f = fopen("flag.txt", "r");
        if (f == NULL)
        {
			return;
        }
        char buf[128];
        memset(buf, 0, sizeof(buf));
        fread(&buf, 1, sizeof(buf) - 1, f);
        printf("%s", buf);
        fflush(stdout);
	}
	printf("mprotect 0x%zx\n", (size_t)addr);
	int x = mprotect(addr, len, prot);
	printf("returned %d\n", x);
}


void *get_aligned_memory(size_t size, size_t count)
{
	if(size >= SIZE_MAX/count)
	{
		return NULL;
	}
	void *res;
	int x =  posix_memalign(&res, 4096, size*count);
	return res;
}

void read_to_buffer()
{
	puts("Where is the buffer located?");
	char *buf;
	size_t ptr;
	scanf("%zx", &ptr);
	//To drop the \n
	getchar();
	buf = (char*) ptr;
	printf("Buffer at %zx\n", (size_t)buf);
	puts("Input 32 bytes please!");
	for(int i = 0; i < 32; i++)
	{
		buf[i] = getchar();
	}
	return;
}

void print_string()
{
	puts("Give string size pls");
	unsigned int x;
	scanf("%ud", &x);
	if(x == 0 || x > 128)
	{
		return;
	}
	char *p = malloc(sizeof(char) * x);
	if(p == NULL)
	{
		return;
	}
	puts("Give string pls");
	while(getchar() != '\n');
	fgets(p, x-1, stdin);
	//NO!
	if(strstr(p, "n"))
	{
		return;
	}
	printf(p);
	printf("\n");
	free(p);
}

int main()
{
    printf("Hi from main at 0x%zx\n", (size_t)&main);
    void *mem = get_aligned_memory(sizeof(char), 128);
    printf("Mem at 0x%zx points to 0x%zx\n",(size_t)&mem, (size_t)mem);
	//Now the memory is only readable and writeable, but not executable
	memprotect_wrapper(mem, PROT_READ | PROT_WRITE, 128);
	int running = 1;
	while(running)
	{
		puts("What do you want to do?");
		puts("1: read stuff to buffer");
		puts("2: print arbitrary string");
		puts("3: done");
		int choice;
		scanf("%d", &choice);
		switch (choice)
		{
		case 1:
			/* code */
			read_to_buffer();
			break;
		
		case 2:
			print_string();
			break;

		case 3:
			running = 0;
			break;

		default:
			break;
		}
	}
}