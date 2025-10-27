"""
Lab 5: Inventory system static analysis.
"""
import json
# Removed unused 'logging' import
from datetime import datetime

# Global variable
stock_data = {}


def add_item(item="default", qty=0, logs=None):
    """Adds an item to the stock inventory."""
    # FIX: Use 'is None' for mutable default arg
    if logs is None:
        logs = []
    if not item:
        return
    try:
        # Add basic type validation
        valid_qty = int(qty)
    except ValueError:
        print(f"Error: Quantity '{qty}' for item '{item}' is not a valid number.")
        return

    stock_data[item] = stock_data.get(item, 0) + valid_qty
    # FIX: Converted to an f-string
    logs.append(f"{datetime.now()}: Added {valid_qty} of {item}")


def remove_item(item, qty):
    """Removes a specified quantity of an item from stock."""
    try:
        stock_data[item] -= qty
        if stock_data[item] <= 0:
            del stock_data[item]
    # FIX: Changed bare 'except:' to 'except KeyError:'
    except KeyError:
        # This just means the item wasn't in the stock, which is fine.
        pass
    except TypeError:
        print(f"Error: Could not remove item '{item}'. Invalid quantity.")


def get_qty(item):
    """Gets the current quantity of a specific item."""
    return stock_data.get(item, 0) # Use .get() for safety


def load_data(file="inventory.json"):
    """Loads the inventory data from a JSON file."""
    global stock_data # pylint: disable=global-statement
    try:
        # FIX: Use 'with open()' and specify encoding
        with open(file, "r", encoding="utf-8") as f:
            stock_data = json.load(f)
    except FileNotFoundError:
        stock_data = {}  # Start fresh if no file exists
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {file}.")
        stock_data = {}


def save_data(file="inventory.json"):
    """Saves the current inventory data to a JSON file."""
    # FIX: Use 'with open()' and specify encoding
    with open(file, "w", encoding="utf-8") as f:
        # Use indent=4 for readable JSON
        json.dump(stock_data, f, indent=4)


def print_data():
    """Prints a report of all items and their quantities."""
    print("--- Items Report ---")
    for item, quantity in stock_data.items():
        print(f"{item} -> {quantity}")
    print("--------------------")


def check_low_items(threshold=5):
    """Returns a list of items below the specified threshold."""
    result = []
    for item, quantity in stock_data.items():
        if quantity < threshold:
            result.append(item)
    return result


def main():
    """Main function to run the inventory system."""
    load_data()  # Start by loading existing data
    logs = []
    add_item("apple", 10, logs)
    add_item("banana", 5, logs)
    add_item(123, "ten", logs)  # This will now be handled gracefully by the try/except in add_item
    remove_item("apple", 3)
    remove_item("orange", 1)  # This will fail gracefully (KeyError)
    print(f"Apple stock: {get_qty('apple')}")
    print(f"Low items: {check_low_items()}")
    save_data()
    print_data()
    # FIX: Removed the dangerous 'eval()' line
    print("\nLog of operations:")
    for log_entry in logs:
        print(log_entry)


if __name__ == "__main__":
    main()
