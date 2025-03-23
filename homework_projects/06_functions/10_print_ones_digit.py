def print_ones_digit(num):
    ones_digit = num % 10
    print("The ones digit is", ones_digit)

def main():
    user_input = int(input("Enter a number: "))
    print_ones_digit(user_input)

if __name__ == "__main__":
    main()