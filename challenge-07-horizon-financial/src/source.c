#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>
#include <string.h>

void win() {
        printf("\nHow did you get here !?\n");
        system("/bin/cat flag.txt");
}


void banner() {
        printf("-----=[ Horizon Financial ]=-----\n\n");
        printf("~Innovation in Every Transaction.\n");
        printf("                     since 2001~\n");

}

// --------------------------------------------------- SETUP

void buffering() {
        setvbuf(stdout, NULL, _IONBF, 0);
        setvbuf(stdin, NULL, _IONBF, 0);
        setvbuf(stderr, NULL, _IONBF, 0);
}

void kill_on_timeout(int sig) {
        if (sig == SIGALRM) {
                exit(0);
        }
}

void alarm_signal() {
        signal(SIGALRM, kill_on_timeout);
        alarm(60);
}


int main(void) {

        int ammount = 0;
        int sum = 0;
        int max = 1000;
        char comment[32];
        char choice[2];

        buffering();
        alarm_signal();

        banner();

        while(1) {
                printf("\nMax value: %d\n\n", max);
                printf("\n[+] Total ammount: %d$", ammount);
                printf("\n\nEnter the ammount > ");
                fflush(stdout);
                scanf("%d", &ammount);   
                getchar();
                printf("\nPlease take some time, and leave us a small comment > ");
                read(0,comment,41);
                if (ammount < max ) {
                        printf("\nTransaction completed successfully.\n");
                        sum += ammount;
                }
                else if (ammount >= 1000) {
                        printf("\nTranscaction failed. Insert ammounts lower than 1000$\n");
                }
                else if(ammount > max){
                                win();
                }
                printf("\n[+] Total ammount: %d$", sum);
                printf("\nDo you want to continue ? [y/n]: ");
                scanf("%1s", choice);
                if(strcmp(choice,"y") == 0){
                        getchar();
                        continue;
                }
                else{
                        printf("\nThank you for using our system.");
                        break;
                }

                }
        return 0;

}
