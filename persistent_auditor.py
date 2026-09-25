import os

failed_attempts = 0
history = []
products = []  # Stores list of dicts: [{'id': 1, 'name': 'Widget', 'inventory': 50}, ...]


def load_inventory():
    global products
    products = []

    if os.path.exists("inventory.txt"):
        file = open("inventory.txt", "r")
        lines = file.readlines()
        file.close()

        for line in lines:
            line = line.strip()
            if line:
                parts = [item.strip() for item in line.split(",")]
                products.append({
                    "id": int(parts[0]),
                    "name": parts[1],
                    "inventory": int(parts[2])
                })


def save_inventory():
    file = open("inventory.txt", "w")
    for prod in products:
        file.write(f"{prod['id']}, {prod['name']}, {prod['inventory']}\n")
    file.close()


def get_valid_input():
    global failed_attempts, products

    # 1. Ask for product name FIRST
    while True:
        name_input = input("\nEnter product name (or 'quit' to finish): ").strip()
        if name_input.lower() == "quit":
            return "quit", None
        if name_input:
            break
        print("Product Name cannot be empty.")

    # Check if product already exists or create new entry with auto-increment ID
    current_product = None
    for prod in products:
        if prod["name"].lower() == name_input.lower():
            current_product = prod
            break

    if current_product is None:
        next_id = max([p["id"] for p in products], default=0) + 1
        current_product = {"id": next_id, "name": name_input, "inventory": 0}
        products.append(current_product)

    # 2. Ask for stock quantity SECOND
    while True:
        stock = input(f"Enter stock quantity for '{current_product['name']}' (or 'quit' to finish): ").strip()

        if stock.lower() == "quit":
            return "quit", None

        while not stock.isdigit() or int(stock) < 0:
            failed_attempts += 1
            stock = input("Invalid input. Please enter a whole number: ").strip()

            if stock.lower() == "quit":
                return "quit", None

        return current_product, int(stock)


def process_delivery(product, new_value):
    product["inventory"] += new_value
    return product["inventory"]


def calculate_tax(amount):
    tax = (amount / 100) * 10
    return tax


def generate_report():
    print("\n--- Final Inventory Report ---")
    for prod in products:
        print(f"ID: {prod['id']} | Product: {prod['name']} | Total Units: {prod['inventory']}")
    print("Number of Failed/Rejected Entries:", failed_attempts)


# Main Execution
load_inventory()
total_deliveries_processed = 0

while True:
    current_product, result = get_valid_input()

    if result == "quit" or current_product == "quit":
        save_inventory()
        generate_report()
        break

    new_total = process_delivery(current_product, result)
    history.append(result)

    total_deliveries_processed += 1
    tax = calculate_tax(result)