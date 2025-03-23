def main():
    first_number = input("Enter your first number: ")
    convert_into_integer = int(first_number)
    print(convert_into_integer)

    second_number = input("Enter your second number: ")
    convert_into_integer2 = int(second_number)
    print(convert_into_integer2)

    sum_of_numbers = convert_into_integer + convert_into_integer2
    print(f"The sum of the two numbers is: {sum_of_numbers}")

main()