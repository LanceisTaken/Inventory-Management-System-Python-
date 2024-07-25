import sqlite3

def create_table():
    conn = sqlite3.connect('inventory')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS inventory
                (id INTEGER PRIMARY KEY,
                name TEXT,
                price REAL,
                quantity INTEGER)''')
    conn.commit()
    conn.close()

def add_item():
    name = input("Enter name of item: ")
    while True:
        try:
            price = float(input("Enter price of item: "))
            break
        except ValueError:
            print("Invalid input. Please enter a number.")
    while True:
        try:
            quantity = int(input("Enter quantity of item: "))
            break
        except ValueError:
            print("Invalid input. Please enter a whole number.")
    conn = sqlite3.connect('inventory')
    c = conn.cursor()
    c.execute("INSERT INTO inventory (name, price, quantity) VALUES (?,?,?)", (name, price, quantity))
    conn.commit()
    print("Item added successfully")

def remove_item():
    item_id = input("Enter the ID of the item to remove: ")
    conn = sqlite3.connect('inventory')
    c = conn.cursor()
    c.execute("SELECT * FROM inventory WHERE id=?", (item_id,))
    item = c.fetchone()
    if item is None:
        print("Item not found in inventory")
        return remove_item()  # reprompt user input if there is an error
    print("Item details:")
    print(item)
    confirm = input("Are you sure you want to remove this item? (y/n): ")
    if confirm.lower() == "y":
        c.execute("DELETE FROM inventory WHERE id=?", (item_id,))
        conn.commit()
        print("Item removed successfully")
    else:
        print("Item removal cancelled")
    

def view_items():
    conn = sqlite3.connect('inventory')
    c = conn.cursor()
    c.execute("SELECT * FROM inventory")
    items = c.fetchall()
    for item in items:
        print(item)
    conn.close()

def search_item():
    search_query = input("Enter the name of the item to search for: ")
    conn = sqlite3.connect('inventory')
    c = conn.cursor()
    c.execute("SELECT * FROM inventory WHERE name=?", (search_query,))
    items = c.fetchall()
    if not items:
        print("No items found in inventory matching that name.")
        reprompt = input("Would you like to search again? (Y/N): ").strip().lower()
        if reprompt == "y":
            search_item()
        else:
            return
    else:
        print("Items found in inventory:")
        for item in items:
            print(item)

def update_item():
    item_id = input("Enter the ID of the item to update: ")
    conn = sqlite3.connect('inventory')
    c = conn.cursor()
    c.execute("SELECT * FROM inventory WHERE id=?", (item_id,))
    item = c.fetchone()
    if item is None:
        print("Item not found in inventory")
        return
    print("Current item details:")
    print(item)

    while True:
        new_price = input("Enter new price (leave empty to keep current price): ")
        if new_price == "":
            new_price = item[2]  # keep current price
            break
        try:
            new_price = float(new_price)
            if new_price < 0:
                raise ValueError("Price must be a positive number")
            break
        except ValueError as e:
            print("Invalid input. " + str(e))

    while True:
        new_quantity = input("Enter new quantity (leave empty to keep current quantity): ")
        if new_quantity == "":
            new_quantity = item[3]  # keep current quantity
            break
        try:
            new_quantity = int(new_quantity)
            if new_quantity < 0:
                raise ValueError("Quantity must be a positive integer")
            break
        except ValueError as e:
            print("Invalid input. " + str(e))

    c.execute("UPDATE inventory SET price=?, quantity=? WHERE id=?", (new_price, new_quantity, item_id))
    conn.commit()
    print("Item updated successfully")

def main():
    create_table()
    while True:
        print("\nWelcome to Inventory Management System\n")
        print("1. Add item")
        print("2. Remove item")
        print("3. View items")
        print("4. Search item")
        print("5. Update item")
        print("6. Exit")
        choice = int(input("\nEnter your choice: "))
        if choice == 1:
            add_item()
        elif choice == 2:
            remove_item()
        elif choice == 3:
            view_items()
        elif choice == 4:
            search_item()
        elif choice == 5:
            update_item()
        elif choice == 6:
            print("Thank you for using the Inventory Management System.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()