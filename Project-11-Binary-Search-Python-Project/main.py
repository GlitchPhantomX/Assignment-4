import time

def binary_search(arr, target):
    """Performs binary search on a sorted array."""
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = left + (right - left) // 2 
        
        if arr[mid] == target:
            return mid 
        elif arr[mid] < target:
            left = mid + 1  
        else:
            right = mid - 1  
            
    return -1

def get_sorted_list():
    """Allows user to enter a sorted list or use the default."""
    choice = input("Do you want to enter your own sorted list? (yes/no): ").strip().lower()
    
    if choice == "yes":
        while True:
            try:
                user_input = input("Enter a sorted list of numbers separated by spaces: ")
                sorted_list = list(map(int, user_input.split()))
                
                if sorted_list != sorted(sorted_list):  
                    print("⚠️ Please enter a sorted list.")
                    continue
                
                return sorted_list
            except ValueError:
                print("⚠️ Invalid input! Please enter only numbers.")
    else:
        return [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  

if __name__ == "__main__":
    sorted_array = get_sorted_list()
    
    if not sorted_array:
        print("⚠️ The list is empty. Exiting program.")
    else:
        try:
            target_value = int(input("Enter the number to search for: "))
            start_time = time.time()  
            
            result = binary_search(sorted_array, target_value)
            
            end_time = time.time()  
            execution_time = (end_time - start_time) * 1000  
            
            if result != -1:
                print(f"✅ Element {target_value} found at index {result}!")
            else:
                print(f"❌ Element {target_value} not found in the array.")
            
            print(f"⏳ Execution Time: {execution_time:.4f} ms")
        
        except ValueError:
            print("⚠️ Invalid input! Please enter a valid number.")
