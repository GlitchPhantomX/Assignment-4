import random
import string
import pyperclip 

def generate_password(length=12, use_special_chars=True, avoid_ambiguous=False):
    letters = string.ascii_letters
    digits = string.digits
    special_chars = string.punctuation
    ambiguous_chars = "lI0O"

    characters = letters + digits
    if use_special_chars:
        characters += special_chars
    if avoid_ambiguous:
        characters = ''.join(c for c in characters if c not in ambiguous_chars)

    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def save_password_to_file(password):
    with open("passwords.txt", "a") as file:
        file.write(password + "\n")
    print("Password saved to passwords.txt ✅")

if __name__ == "__main__":
    print("🔐 Password Generator with Advanced Features 🔐\n")

    print("Choose Password Strength:\n1️⃣ Weak (6 characters)\n2️⃣ Medium (12 characters)\n3️⃣ Strong (16 characters)")
    strength_choice = input("Enter choice (1/2/3): ").strip()

    strength_levels = {"1": 6, "2": 12, "3": 16}
    password_length = strength_levels.get(strength_choice, 12)  

    include_special_chars = input("Include special characters? (yes/no): ").strip().lower() == 'yes'
    avoid_ambiguous_chars = input("Avoid ambiguous characters (e.g., l, I, 0, O)? (yes/no): ").strip().lower() == 'yes'

    while True:
        num_passwords_input = input("How many passwords do you want to generate? (default: 1): ").strip()
        if num_passwords_input.isdigit():
            num_passwords = int(num_passwords_input)
            break
        elif num_passwords_input == "": 
            num_passwords = 1
            break
        else:
            print("❌ Invalid input! Please enter a number.")

    print("\nGenerated Passwords:\n" + "=" * 30)
    for _ in range(num_passwords):
        generated_password = generate_password(password_length, include_special_chars, avoid_ambiguous_chars)
        print(generated_password)
        
        if num_passwords == 1:
            pyperclip.copy(generated_password)
            print("✅ Password copied to clipboard!")

        save_password_to_file(generated_password)

    print("=" * 30 + "\n🎉 Password Generation Complete!")
