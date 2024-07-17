''' research and references
    https://iq.opengenus.org/python-min-lambda/#:~:text=in%20a%20list.-,Lambda%20in%20Min()%20built-in%20function,attribute%20of%20min()%20function.
    Found a methond of getting/excluding the first line in a file 
    https://www.tutorialspoint.com/How-to-read-only-the-first-line-of-a-file-with-Python
    using rich to try and improve UX
    https://www.youtube.com/watch?v=4zbehnz-8QU&t=18s
'''
from tabulate import tabulate
from rich.console import Console
import os

shoes_list = []
file_location = 'inventory.txt'
file_header = []
menu_option= ["c","v","r","s","i","h","e"]

class Shoe:

    def __init__(self, country, code, product, cost, quantity):
       self.country = country
       self.code = code
       self.product = product
       self.cost = cost
       self.quantity = quantity

        
    def get_cost(self):
        return self.cost

    def get_quantity(self):
        return self.quantity
    
    def __str__(self):
        # String representation of the class object
        return f"{self.country},{self.code},{self.product},{self.cost},{self.quantity}"


# The list will be used to store a list of objects of shoes.
shoes_list = []
# Used for quick reference of the shoe codes to ensure no duplicates captured
shoe_codes = []

def update_path_dir(file_path):
    '''Update the file path to include the current directory of the script file.'''

    # Get the directory of the current script
    current_directory = os.path.dirname(os.path.abspath(__file__))
    # Construct the path to the text file
    text_file_path = os.path.join(current_directory, file_path)
    return text_file_path 

file_location =update_path_dir(file_location)

def input_validation(input_string,validate_num,in_list,list_check):
    ''' Validate various scenarious for the user_input 
    base on the what is passed through the function.
        - no value entered.
        - if enabled if the user_input is a digit.
        - if in_list is true: 
            - checks if user input is found in the list passed into the function.
        - if in_line is false:
            - check if the user input is not found in the list passed into the function
    '''
    while True:
        try:
            user_input = input(input_string)
            if not user_input:
                raise ValueError("No Value entered.")
            if validate_num and not user_input.isdigit():
                raise ValueError("You have not entered a valid number")
            if list_check and in_list:
                if user_input in list_check:
                    raise ValueError("\nThe code you have entered already exist please try again.")
            elif list_check and in_list == False:
                if user_input not in list_check:
                    raise ValueError("\nYou have not entered a valid option please try again.")
            return user_input 
           
        except ValueError as ve:
            print(ve)

def read_shoes_data():
    ''' - Reads data from the inventory.txt file and creates a shoe obj stored in the shoes_list.
        - Create a list of shoe codes to be used for validation purposes.
    '''
    try:
        # Clear the shoe_list and shoe_codes so as to not duplicate values into the list
        shoes_list.clear()
        shoe_codes.clear()

        file_exist = os.path.exists(file_location)
        if file_exist == False:
             # Create file the missing file with the header
             with open(file_location,'w+') as file:
                 file.writelines("Country,Code,Product,Cost,Quantity")
             raise FileNotFoundError(f"The {file_location} could not be found.\nA blank file has been created with the first line being the header(Country,Code,Product,Cost,Quantity).")
        else:
            with open(file_location,'r') as file:
                # Storing the first line of the file and moving on to the next line
                file_header.append(next(file).strip().split(","))
                for line in file:
                    # Creating the shoe_list
                    line = line.strip().split(",")
                    shoe = Shoe(line[0],line[1],line[2],float(line[3]),float(line[4]))
                    shoes_list.append(shoe)
                    shoe_codes.append(line[1])

    except FileNotFoundError as file_not_found:
        console.print(file_not_found,style="bold red")
    except ValueError as ve:
        print(ve)

def capture_shoes():
    ''' Capture shoe details from a user and save to file.'''
    read_shoes_data()
    try:
        country = input_validation("Input the country:\n",False,False,[])
        code = input_validation("Input the shoe code (eg. SKU123):\n",False,True,shoe_codes).upper()
        product = input_validation("Input the product details:\n",False,False,[])
        cost = int(input_validation("What is the cost of the shoe:\n",True,False,[]))
        quantity = int(input_validation("What is the quantity:\n",True,False,[]))

        shoe_obj = Shoe(country,code,product,cost,quantity)
        shoes_list.append(shoe_obj)
        save_shoe_list()
        view_all()
    except ValueError as ve:
        print(ve)

def view_all():
    ''' displays all the shoes from the shoes_list. '''
    
    if shoes_list:
        shoes_table  = []
        for shoe in shoes_list:
            shoes_table.append((shoe.__str__()).split(','))
        print(tabulate(shoes_table,headers=["Country","Code","Product","Cost","Quantity"],tablefmt="fancy_grid"))
    else:
        console.print("No invertory found in the inventory.txt file", style="bold red")
 
def view_single_shoe(shoe_obj):
    ''' Displays the a single shoe object in a table. '''
    single_table = []
    single_table.append((shoe_obj.__str__()).split(','))
    print(tabulate(single_table,headers=["Country","Code","Product","Cost","Quantity"],tablefmt="fancy_grid"))

def re_stock():
    '''- Finds the shoe with the lowest quantity. 
       - Ask the user if they would like to restock the shoe.
       - Display the results of the quantity update
'''
    if shoes_list:
        # Finds the object with the min quantity attribute
        smallest_value = min(shoes_list, key=lambda x: x.quantity)
        console.print("Shoe with the lowest quantity:",style="bold")
        view_single_shoe(smallest_value)

        update_item = input_validation("Would you like to restock this shoe:(answer y/n)\n",False,False,["y","n"]).lower()
        if update_item == 'y':
            new_qty = input_validation("What is the new stock quantity:\n",True,False,[])
            for shoe in shoes_list:
                if shoe.code == smallest_value.code:
                    shoe.quantity = int(new_qty)
                    console.print("Restock was successful",style="bold")
                    view_single_shoe(shoe)
    else:
        console.print("No invertory found in the inventory.txt file", style="bold red")

def seach_shoe():
    '''
     This function will search for a shoe from the list
     using the shoe code and return this object so that it will be printed.
    '''
    shoe_code = input_validation("What is the code of the shoe you would like to search for(eg. SKU123):\n",False,False,[]).upper()
    shoe_found = False
    for shoe in shoes_list:
        if shoe.code == shoe_code:
            view_single_shoe(shoe)
            shoe_found= True
    if shoe_found is False:
        console.print("Sorry we where unable to find the shoe you where looking for.",style="bold red")

def value_per_item():
    '''
    This function will calculate the total value for each item.
    Please keep the formula for value in mind: value = cost * quantity.
    Print this information on the console for all the shoes.
    '''
    
    value_table = []
    if shoes_list:
        console.print("Value per item:",style="bold green")
        for shoe in shoes_list:
            value = shoe.cost * shoe.quantity
            value_table.append([shoe.product,value])
            
    else:
        console.print("No shoes available.",style="bold green")
    print(tabulate(value_table,headers=["shoe","value"],tablefmt="fancy_grid"))


def highest_qty():
    ''' Print the shoe with highest quantity. '''
    # Finds the object with the max quantity attribute
    if shoes_list and len(shoes_list) >0:
        console.print("\nHighest quantity product",style="bold underline green")
        max_quantity_shoe = max(shoes_list, key=lambda x: x.quantity)
        print(f"The product with the highest quantity for sale is: {max_quantity_shoe.product}")
    else:
        console.print("\nThe inventory.txt file contains no data to compare.",style="bold red")
   
def save_shoe_list():
    ''''''
    try:
        with open(file_location,'w+') as file:
            file.writelines(f"{file_header[0][0]},{file_header[0][1]},{file_header[0][2]},{file_header[0][3]},{file_header[0][4]}\n")
            for line in shoes_list:
                file.writelines(f"{line.__str__()}\n")
    except FileNotFoundError as file_not_found:
        print(file_not_found)
    except ValueError as ve:
        print(ve)
        
console = Console()
read_shoes_data()

while True:
        try:
            menu_selection = input_validation('''\nShoe inventory controller menu:
c - capture shoe 
v - view invertory
r - restock a product 
s - search for a product
i - individual product costing
h - highest quantity product                                 
e - exit
Enter your choice:''',False,False,menu_option).lower()
            match menu_selection:
                    case 'c':
                        console.print("\nCapture stock",style="bold underline green")
                        capture_shoes()
                    case 'v':
                         console.print("\nAll shoes",style="bold underline green")
                         view_all()
                    case 'r':
                         console.print("\nRestock shoes",style="bold underline green")
                         re_stock()
                         save_shoe_list()
                    case 's':
                         console.print("\nSearch shoes",style="bold underline green")
                         seach_shoe()
                    case 'i':
                         console.print("\nIndividual product costing",style="bold underline green")
                         value_per_item()
                    case 'h':
                         
                         highest_qty()
                    case 'e':
                        #the program will now exit
                        console.print("The application will now exit",style="bold red")
                        break
           
        except ValueError as ve:
            print(ve)   