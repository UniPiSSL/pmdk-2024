#!/usr/bin/env python
import os
import sys
import time
import random

def get_user_choice():
    print("Choose:")
    print("1. Rock")
    print("2. Paper")
    print("3. Scissors")
    try:
        choice = input('> ')
        choice = int(choice)
        return choice if 1 <= choice <= 3 else 0
    except Exception as e:
        print('Invalid input! Try again.')
        return 0

def get_server_choice():
    return random.randint(1, 3)

def determine_winner(user_choice, server_choice):
    choices = ["Rock", "Paper", "Scissors"]
    time.sleep(1)
    print("You chose: " + choices[user_choice - 1])
    time.sleep(1)
    print("Bot chose: " + choices[server_choice - 1])
    time.sleep(1)

    if user_choice == server_choice:
        print("It's a tie!")
        return 0
    elif (user_choice == 1 and server_choice == 3) or \
         (user_choice == 2 and server_choice == 1) or \
         (user_choice == 3 and server_choice == 2):
        print("You won the round!")
        return 1
    else:
        print("You lost the round!")
        return -1

def round(round_no):
    print('-= Round ' + str(round_no) + ' =-')
    time.sleep(1)
    server_choice = get_server_choice()
    while True:
        user_choice = get_user_choice()
        if user_choice:
            break

    return determine_winner(user_choice, server_choice)


def main():
    print('WELCOME TO ROCK-PAPER-SCISSORS GAME')
    print('RUNNING ON PYTHON ' + str(sys.version_info.major) + "." + str(sys.version_info.minor) + "." + str(sys.version_info.micro) + '!')
    time.sleep(1)
    print('THE FIRST ONE TO WIN 3 ROUND WINS!')
    print('')
    time.sleep(2)

    # New game stats
    round_no = 0
    bot_score = 0
    user_score = 0

    # For each round
    while True:
        # Run the round
        round_no += 1
        result = round(round_no)
        time.sleep(1)
        
        # Update score
        if result > 0:
            user_score += 1
        elif result < 0:
            bot_score += 1

        # Print score
        print('Score: Bot ' + str(bot_score) + ' - ' + str(user_score) + ' You')
        print('')
        time.sleep(2)

        # Check if someone won
        if user_score >= 3:
            print('YOU WON 3 ROUNDS!')
            print('YOU WON THE GAME!')
            break
        elif bot_score >= 3:
            print('BOT WON 3 ROUNDS!')
            print('GAME OVER!')
            break

    print('BYE!')


if __name__ == "__main__":
    main()
