import os

failed_attempts = 0
history = []

def load_inventory():

    if os.path.exists("inventory.txt"):
        file = open("inventory.txt", "r")
        line = file.readline().strip()
        file.close()

        if line:

            for item in line.split(","):

                parts = item.strip

            product_id = int(parts[0])
            product_name = parts[1]
            inventory = int(parts[2])
            
            return product_id, product_name, inventory

    product_id = 1
    product_name = get_valid_input("product_name")
    return product_id, product_name, 0



def get_valid_input ():

    while True:

        global failed_attempts
        stock = input("Enter stock quantity of type 'quit' to finish: ")

        if stock == "quit":
            return "quit" 
       
        while stock.isdigit() == False or int(stock) < 0:
            failed_attempts += 1
            
            stock = input("Invalid input. Please enter a whole number: ")

            if stock == "quit":
                return "quit" 
            

        return int(stock)

def process_delivery(current_total, new_value):

    current_total += new_value

    return current_total

def calculate_tax(amount):
    tax = (amount / 100) * 10

    return tax

def generate_report(total_units, failed_attempts):

    print("\n--- Inventory Report ---")
    print("Total Units Processed:", total_units)
    print("Number of Failed/Rejected Entries:", failed_attempts)


inventory = 0
total_deliveries_processed = 0

while True:

    result = get_valid_input()

    if result == 'quit':
        generate_report(inventory, failed_attempts)
        break


    inventory = process_delivery(inventory, result)
    total_deliveries_processed += 1

    tax = calculate_tax(result)

