import random

def guess_the_number():
    print("🎯 Welcome to the Guess the Number Game! 🎯")
    
    while True:
        print("\nChoose Difficulty Level:")
        print("1. Easy (1-50, Unlimited attempts)")
        print("2. Medium (1-100, Max 10 attempts)")
        print("3. Hard (1-200, Max 7 attempts)")
        
        difficulty = input("Enter 1, 2, or 3: ").strip()
        
        if difficulty == "1":
            max_number = 50
            max_attempts = None
        elif difficulty == "2":
            max_number = 100
            max_attempts = 10
        elif difficulty == "3":
            max_number = 200
            max_attempts = 7
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
            continue

        number_to_guess = random.randint(1, max_number)
        attempts = 0
        guessed = False

        print(f"\nI have selected a number between 1 and {max_number}. Try to guess it!")

        while not guessed:
            user_guess = input("Enter your guess: ").strip()
            
            try:
                user_guess = int(user_guess)
                if user_guess < 1 or user_guess > max_number:
                    print(f"⚠ Please enter a number between 1 and {max_number}.")
                    continue
                
                attempts += 1

                if user_guess < number_to_guess:
                    print("📉 Too low! Try again.")
                elif user_guess > number_to_guess:
                    print("📈 Too high! Try again.")
                else:
                    guessed = True
                    print(f"🎉 Congratulations! You guessed the number {number_to_guess} in {attempts} attempts!")

                    if max_attempts:
                        if attempts <= max_attempts // 2:
                            print("🌟 Excellent job!")
                        elif attempts <= max_attempts:
                            print("👍 Good effort!")
                        else:
                            print("😅 You made it, but try to improve next time!")
                    break

                if attempts % 3 == 0 and not guessed:
                    hint_range = 5 if max_number <= 100 else 10
                    hint_min = max(1, number_to_guess - hint_range)
                    hint_max = min(max_number, number_to_guess + hint_range)
                    print(f"🔎 Hint: The number is between {hint_min} and {hint_max}.")

                if max_attempts and attempts >= max_attempts:
                    print(f"💀 Game Over! The number was {number_to_guess}. Better luck next time!")
                    break

            except ValueError:
                print("❌ Invalid input! Please enter a valid number.")

        play_again = input("\nDo you want to play again? (yes/no): ").strip().lower()
        if play_again != "yes":
            print("\nThanks for playing! Goodbye. 👋")
            break

if __name__ == "__main__":
    guess_the_number()
