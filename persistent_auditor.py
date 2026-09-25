import os

failed_attempts = 0
history = []
products = []  # Stores list of dicts: [{'id': 1, 'name': 'Widget', 'inventory': 50}, ...]


def load_inventory():
    global products, history

    products = []
    history = []

    if os.path.exists("inventory.txt"):
        file = open("inventory.txt", "r")
        lines = file.readlines()
        file.close()

        reading_history = False

        for line in lines:
            line = line.strip()

            if not line:
                continue

            if line == "HISTORY":
                reading_history = True
                continue

            parts = [item.strip() for item in line.split(",")]

            if reading_history:
                history.append({
                    "id": int(parts[0]),
                    "name": parts[1],
                    "added": int(parts[2]),
                    "total": int(parts[3])
                })

            else:
                products.append({
                    "id": int(parts[0]),
                    "name": parts[1],
                    "inventory": int(parts[2])
                })


def save_inventory():
    file = open("inventory.txt", "w")

    # Save current inventory
    for prod in products:
        file.write(
            f"{prod['id']}, {prod['name']}, {prod['inventory']}\n"
        )

    # Separate inventory and history
    file.write("\n")
    file.write("HISTORY\n")

    # Save stock addition history
    for entry in history:
        file.write(
            f"{entry['id']}, {entry['name']}, "
            f"{entry['added']}, {entry['total']}\n"
        )

    file.close()


def get_valid_input():
    global failed_attempts, products

    # Ask for product name FIRST
    while True:
        name_input = input(
            "\nEnter product name (or 'quit' to finish): "
        ).strip()

        if name_input.lower() == "quit":
            return "quit", None

        if name_input:
            break

        failed_attempts += 1
        print("Product Name cannot be empty.")

    # Check if product already exists
    current_product = None

    for prod in products:
        if prod["name"].lower() == name_input.lower():
            current_product = prod
            break

    # Create a new product if it does not exist
    if current_product is None:
        next_id = max(
            [p["id"] for p in products],
            default=0
        ) + 1

        current_product = {
            "id": next_id,
            "name": name_input,
            "inventory": 0
        }

        products.append(current_product)

    # Ask for stock quantity SECOND
    while True:
        stock = input(
            f"Enter stock quantity for '{current_product['name']}' "
            "(or 'quit' to finish): "
        ).strip()

        if stock.lower() == "quit":
            return "quit", None

        while not stock.isdigit() or int(stock) < 0:
            failed_attempts += 1

            stock = input(
                "Invalid input. Please enter a whole number: "
            ).strip()

            if stock.lower() == "quit":
                return "quit", None

        return current_product, int(stock)


def process_delivery(product, new_value):
    # Add the new stock to the current inventory
    product["inventory"] += new_value

    # Record this individual stock addition
    history.append({
        "id": product["id"],
        "name": product["name"],
        "added": new_value,
        "total": product["inventory"]
    })

    return product["inventory"]


def calculate_tax(amount):
    tax = (amount / 100) * 10
    return tax


def generate_report():
    print("\n--- Final Inventory Report ---")

    for prod in products:
        print(
            f"ID: {prod['id']} | "
            f"Product: {prod['name']} | "
            f"Total Units: {prod['inventory']}"
        )

    print("\n--- Stock Addition History ---")

    for entry in history:
        print(
            f"ID: {entry['id']} | "
            f"Product: {entry['name']} | "
            f"Added: {entry['added']} | "
            f"Total After Addition: {entry['total']}"
        )

    print(
        "\nNumber of Failed/Rejected Entries:",
        failed_attempts
    )


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

    total_deliveries_processed += 1

    tax = calculate_tax(result)

