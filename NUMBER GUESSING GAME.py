import random

logo = r'''
 .-._                           ___                  ,----.               
/==/ \  .-._ .--.-. .-.-..-._ .'=.'\    _..---.   ,-.--` , \  .-.,.---.   
|==|, \/ /, /==/ -|/=/  /==/ \|==|  | .' .'.-. \ |==|-  _.-` /==/  `   \  
|==|-  \|  ||==| ,||=| -|==|,|  / - |/==/- '=' / |==|   `.-.|==|-, .=., | 
|==| ,  | -||==|- | =/  |==|  \/  , ||==|-,   ' /==/_ ,    /|==|   '='  / 
|==| -   _ ||==|,  \/ - |==|- ,   _ ||==|  .=. \|==|    .-' |==|- ,   .'  
|==|  /\ , ||==|-   ,   /==| _ /\   |/==/- '=' ,|==|_  ,`-._|==|_  . ,'.  
/==/, | |- |/==/ , _  .'/==/  / / , /==|   -   //==/ ,     //==/  /\ ,  ) 
`--`./  `--``--`..---'  `--`./  `--``-._`.___,' `--`-----`` `--`-`--`--'

      _,---.                  ,----.    ,-,--.    ,-,--.   .=-.-..-._            _,---.   
  _.='.'-,  \ .--.-. .-.-. ,-.--` , \ ,-.'-  _\ ,-.'-  _\ /==/_ /==/ \  .-._ _.='.'-,  \  
 /==.'-     //==/ -|/=/  ||==|-  _.-`/==/_ ,_.'/==/_ ,_.'|==|, ||==|, \/ /, /==.'-     /  
/==/ -   .-' |==| ,||=| -||==|   `.-.\==\  \   \==\  \   |==|  ||==|-  \|  /==/ -   .-'   
|==|_   /_,-.|==|- | =/  /==/_ ,    / \==\ -\   \==\ -\  |==|- ||==| ,  | -|==|_   /_,-.  
|==|  , \_.' )==|,  \/ - |==|    .-'  _\==\ ,\  _\==\ ,\ |==| ,||==| -   _ |==|  , \_.' ) 
\==\-  ,    (|==|-   ,   /==|_  ,`-._/==/\/ _ |/==/\/ _ ||==|- ||==|  /\ , \==\-  ,    (  
 /==/ _  ,  //==/ , _  .'/==/ ,     /\==\ - , /\==\ - , //==/. //==/, | |- |/==/ _  ,  /  
 `--`------' `--`..---'  `--`-----``  `--`---'  `--`---' `--`-` `--`./  `--``--`------'   
'''

EASY_LEVEL_TURNS = 10
HARD_LEVEL_TURNS = 5


def check_answer(user_guess, actual_answer, turns):
    """Checks answer against guess and returns remaining turns."""

    if user_guess > actual_answer:
        print("📈 Too high.")
        return turns - 1

    elif user_guess < actual_answer:
        print("📉 Too low.")
        return turns - 1

    else:
        print(f"🎉 You got it! The answer was {actual_answer}.")
        return turns


def set_difficulty():
    """Returns number of turns based on difficulty."""

    while True:
        difficulty = input(
            "Choose a difficulty. Type 'easy' or 'hard': "
        ).lower()

        if difficulty == "easy":
            return EASY_LEVEL_TURNS

        elif difficulty == "hard":
            return HARD_LEVEL_TURNS

        else:
            print("❌ Invalid choice. Please type 'easy' or 'hard'.")


def play_game():

    print(logo)

    print("🎯 Welcome to the Number Guessing Game!")
    print("I'm thinking of a number between 1 and 100.")

    answer = random.randint(1, 100)

    turns = set_difficulty()

    guess = 0

    while guess != answer and turns > 0:

        print(f"\n💡 You have {turns} attempts remaining.")

        try:
            guess = int(input("Make a guess: "))
        except ValueError:
            print("❌ Please enter a valid number.")
            continue

        turns = check_answer(guess, answer, turns)

        if guess != answer:

            if turns == 0:
                print("\n💀 You've run out of guesses.")
                print(f"The number was {answer}.")
                return

            print("Guess again...")


while True:

    play_game()

    restart = input(
        "\n🔄 Do you want to play again? (y/n): "
    ).lower()

    if restart != "y":
        print("👋 Thanks for playing!")
        break
