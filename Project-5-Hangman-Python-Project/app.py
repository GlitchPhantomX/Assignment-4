import random

word_categories = {
    "Animals": {
        "words": ["elephant", "giraffe", "kangaroo", "dolphin", "penguin"],
        "hints": ["Large mammal with a trunk", "Tallest land animal", "Hops on two legs", "Smart ocean creature", "A bird that cannot fly"]
    },
    "Technology": {
        "words": ["computer", "internet", "keyboard", "smartphone", "software"],
        "hints": ["Used for coding and browsing", "Connects the world", "Typing device", "Portable communication device", "Programs that run on devices"]
    },
    "Sports": {
        "words": ["soccer", "basketball", "tennis", "cricket", "baseball"],
        "hints": ["Played with a round ball and goals", "Hoop and dribbling", "Played with a racket", "Bat and ball sport", "American favorite with a bat"]
    }
}

def choose_category():
    """Allows the player to select a category."""
    print("\nChoose a category:")
    categories = list(word_categories.keys())
    for i, category in enumerate(categories, 1):
        print(f"{i}. {category}")
    
    while True:
        choice = input("Enter the number of your chosen category: ")
        if choice.isdigit() and 1 <= int(choice) <= len(categories):
            return categories[int(choice) - 1]
        print("Invalid choice. Please enter a valid number.")

def choose_word(category):
    """Selects a random word and hint from the chosen category."""
    index = random.randint(0, len(word_categories[category]["words"]) - 1)
    return word_categories[category]["words"][index], word_categories[category]["hints"][index]

def choose_difficulty():
    """Allows the player to select difficulty, affecting the number of tries."""
    difficulties = {"easy": 8, "medium": 6, "hard": 4}
    while True:
        difficulty = input("\nChoose a difficulty (Easy, Medium, Hard): ").lower()
        if difficulty in difficulties:
            return difficulties[difficulty]
        print("Invalid choice. Please enter Easy, Medium, or Hard.")

def display_hangman(tries):
    """Returns the hangman drawing based on remaining tries, preventing out-of-range errors."""
    stages = [
        """
           ------
           |    |
           |    O
           |   /|\\
           |   / \\
           |
        """,
        """
           ------
           |    |
           |    O
           |   /|\\
           |   / 
           |
        """,
        """
           ------
           |    |
           |    O
           |   /|\\
           |    
           |
        """,
        """
           ------
           |    |
           |    O
           |   /|
           |    
           |
        """,
        """
           ------
           |    |
           |    O
           |    |
           |    
           |
        """,
        """
           ------
           |    |
           |    O
           |    
           |    
           |
        """,
        """
           ------
           |    |
           |    
           |    
           |    
           |
        """,
        """
           ------
           |    
           |    
           |    
           |    
           |
        """
    ]
    
    if tries < 0:
        tries = 0
    elif tries >= len(stages): 
        tries = len(stages) - 1
    
    return stages[tries]

def play_hangman():
    """Main function to play the game with improved features."""
    wins = 0
    losses = 0

    while True:
        print("\nWelcome to Hangman!")
        category = choose_category()
        word, hint = choose_word(category)
        tries = choose_difficulty()
        word_completion = "_" * len(word)
        guessed = False
        guessed_letters = []
        guessed_words = []
        hint_used = False

        print(f"\nCategory: {category}")
        print(display_hangman(tries))
        print(word_completion)
        print("\n")

        while not guessed and tries > 0:
            guess = input("Guess a letter or the full word (or type 'hint' for a clue): ").lower()

            if guess == "hint":
                if not hint_used:
                    print(f"Hint: {hint}")
                    hint_used = True
                else:
                    print("You have already used your hint!")
                continue

            if len(guess) == 1 and guess.isalpha():
                if guess in guessed_letters:
                    print("You already guessed that letter.")
                elif guess not in word:
                    print(f"{guess} is not in the word.")
                    tries -= 1
                    guessed_letters.append(guess)
                else:
                    print(f"Good job! {guess} is in the word.")
                    guessed_letters.append(guess)
                    word_completion = "".join([letter if letter in guessed_letters else "_" for letter in word])
                    if "_" not in word_completion:
                        guessed = True
            elif len(guess) == len(word) and guess.isalpha():
                if guess in guessed_words:
                    print("You already guessed that word.")
                elif guess != word:
                    print(f"{guess} is not the word.")
                    tries -= 1
                    guessed_words.append(guess)
                else:
                    guessed = True
                    word_completion = word
            else:
                print("Invalid input. Please try again.")

            print(display_hangman(tries))
            print(word_completion)
            print("\n")

        if guessed:
            print("🎉 Congratulations! You've guessed the word!")
            wins += 1
        else:
            print(f"😢 Sorry, you ran out of tries. The word was '{word}'.")
            losses += 1

        print(f"\n🏆 Wins: {wins} | ❌ Losses: {losses}")

        play_again = input("\nDo you want to play again? (yes/no): ").lower()
        if play_again != "yes":
            print("\nThanks for playing Hangman! Goodbye! 😊")
            break

if __name__ == "__main__":
    play_hangman()
