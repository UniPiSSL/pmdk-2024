#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>
#include <string.h>

// --------------------------------------------------- SETUP

void ignore_me_init_buffering() {
	setvbuf(stdout, NULL, _IONBF, 0);
	setvbuf(stdin, NULL, _IONBF, 0);
	setvbuf(stderr, NULL, _IONBF, 0);
}

void kill_on_timeout(int sig) {
  if (sig == SIGALRM) {
  	printf("[!] Anti DoS Signal. Patch me out for testing.");
    _exit(0);
  }
}

void ignore_me_init_signal() {
	signal(SIGALRM, kill_on_timeout);
	alarm(60);
}

// --------------------------------------------------- FUNCTIONS

void backdoor() {
    system("/bin/cat flag.txt");
}


char* operation(const char* input) {
    // Determine the length of the input string

    int length = strlen(input);

    // Allocate memory for the modified string
    char* modifiedString = (char*)malloc((length + 1) * sizeof(char));

    for (int i = 0; i < length; i++) {
        char currentChar = input[i];

        switch (currentChar) {
            case 'i':
            case 'I':
                modifiedString[i] = '1';
                break;
            case 'a':
            case 'A':
                modifiedString[i] = '4';
                break;
            case 'e':
            case 'E':
                modifiedString[i] = '3';
                break;
            case 'o':
            case 'O':
                modifiedString[i] = '0';
                break;
            case 's':
            case 'S':
                modifiedString[i] = '5';
                break;
            default:
                modifiedString[i] = currentChar;
                break;
        }
    }

    // Null-terminate the modified string
    modifiedString[length] = '\0';

    return modifiedString;
}


// --------------------------------------------------- MAIN

int main(int argc, char* argv[]) {
	
    ignore_me_init_buffering();
	ignore_me_init_signal();

    char text[128];
    printf("-=[ Hacktrox 01010 ]=-");
    printf("\n         - Version 1.0");
    printf("\n\n~ Because Text Should Feel Like a Hacker's Playground!");
    printf("\n\nInsert text > ");
    fgets(text, 180, stdin);
    // Replace specific letters in the string
    char* hacktrox_text = operation(text);

    // Print the results
    printf("\nOriginal text: %s\n", text);
    printf("Hacktrox result: %s\n", hacktrox_text);

    printf("Thank you for using our app x)\n");

    // Free the dynamically allocated memory
    free(hacktrox_text);
    hacktrox_text = NULL;

    return 0;
    
  
}