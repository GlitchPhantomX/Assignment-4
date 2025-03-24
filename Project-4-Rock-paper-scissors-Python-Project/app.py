import random

def get_user_choice():
    """Get the user's choice and validate input."""
    while True:
        user_input = input("Enter rock, paper, or scissors (or 'quit' to exit): ").lower()
        if user_input in ["rock", "paper", "scissors"]:
            return user_input
        elif user_input == "quit":
            return None
        print("Invalid choice. Please enter rock, paper, or scissors.")

def get_computer_choice():
    """Generate a random choice for the computer."""
    return random.choice(["rock", "paper", "scissors"])

def determine_winner(user_choice, computer_choice):
    """Determine the winner based on game rules."""
    if user_choice == computer_choice:
        return "tie"
    elif (user_choice == "rock" and computer_choice == "scissors") or \
         (user_choice == "paper" and computer_choice == "rock") or \
         (user_choice == "scissors" and computer_choice == "paper"):
        return "user"
    else:
        return "computer"

def play_game():
    """Main function to play multiple rounds and track scores."""
    user_score = 0
    computer_score = 0
    ties = 0
    rounds_played = 0

    print("Welcome to Rock, Paper, Scissors!")
    
    while True:
        user_choice = get_user_choice()
        if user_choice is None:
            break
        
        computer_choice = get_computer_choice()

        print(f"\nYou chose: {user_choice}")
        print(f"Computer chose: {computer_choice}")

        result = determine_winner(user_choice, computer_choice)
        if result == "tie":
            print("It's a tie!")
            ties += 1
        elif result == "user":
            print("You win this round!")
            user_score += 1
        else:
            print("You lose this round!")
            computer_score += 1
        
        rounds_played += 1
        
        print(f"\nScore - You: {user_score} | Computer: {computer_score} | Ties: {ties}")
        
        play_again = input("\nDo you want to play again? (yes/no): ").lower()
        if play_again != "yes":
            break

    print("\nGame Over! Here are your final stats:")
    print(f"Total Rounds Played: {rounds_played}")
    print(f"Your Wins: {user_score}")
    print(f"Computer Wins: {computer_score}")
    print(f"Ties: {ties}")
    print("Thanks for playing!")

if __name__ == "__main__":
    play_game()
