def print_multiple(message, repeats):
    for _ in range(repeats):  
        print(message, end=" ")  
    print()  

def main():
    message = input("Please type a message: ")
    repeats = int(input("Enter a number of times to repeat your message: "))
    print_multiple(message, repeats)

if __name__ == "__main__":
    main()