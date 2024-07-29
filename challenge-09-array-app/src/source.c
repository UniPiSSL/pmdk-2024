#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

// gcc -o binary source.c -no-pie

void (*pfunc)() = (void (*)())0x00000000004011d6;
int array[16];

void message() {
    printf("Thank you for using our app!\n");
}

void win() {
	system("/bin/cat flag.txt");
}

void main(int argc, char* argv[]){
	
    int index, value;
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    
    printf("Let's play with arrays :)");

    printf("\nEnter the index: ");
    scanf("%d", &index);
    
    printf("Enter the value: ");
    scanf("%d", &value);
    
    array[index] = value;

    (*pfunc)();
    
    puts("Bye!");
}