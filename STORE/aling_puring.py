import os
import json

DATA_FILE = "store_data.json"

def load_data():
    """Loads the database state from a JSON file."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                pass
    # Default initial data structures kapag wala pang file
    return {
        "branches": {
            "main_branch": {
                "name": "Main Branch",
                "location": "Quezon City",
                "inventory": {
                    "Coke Original": {"price": 20.0, "stock": 50, "restock_level": 5},
                    "Pancit Canton": {"price": 15.0, "stock": 4, "restock_level": 5}
                }
            }
        },
        "transactions": []
    }

def save_data(data):
    """Saves the current database state to a JSON file."""
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)
        
def manage_branches(data):
    while True:
        print("\n  === BRANCH MANAGEMENT ===")
        print("  [1] Add New Branch")
        print("  [2] View All Branches")
        print("  [3] Remove Branch")
        print("  [0] Back")
        choice = input("  Choose: ").strip()

        if choice == "1":
            name = get_nonempty_input("  Branch Name: ").title()
            location = get_nonempty_input("  Location/Barangay: ").title()
            b_id = name.lower().replace(" ", "_")
            if b_id in data["branches"]:
                print("  Branch already exists.")
            else:
                # Gumagawa ng bagong branch na may hiwalay at walang lamang inventory {}
                data["branches"][b_id] = {"name": name, "location": location, "inventory": {}}
                save_data(data)
                print(f"  Branch '{name}' added successfully.")
        elif choice == "2":
            print("\n  === REGISTERED BRANCHES ===")
            for b_info in data["branches"].values():
                print(f"  - {b_info['name']} in {b_info['location']}")
        elif choice == "3":
            b_id = select_branch(data)
            if b_id:
                confirm = input(f"  Delete this branch and its files? (y/n): ").lower()
                if confirm in ['y', 'yes']:
                    del data["branches"][b_id]
                    save_data(data)
                    print("  Branch removed from system.")
        elif choice == "0":
            break
        
def record_sale(data):
    b_id = select_branch(data)
    if not b_id: return

    branch = data["branches"][b_id]
    if not branch["inventory"]:
        print("  No stock available in this branch.")
        return

    display_inventory(data, b_id)
    items_list = list(branch["inventory"].keys())
    order_items = []

    print("\n  Enter Item No. to sell (Type 0 to complete checkout):")
    while True:
        choice = get_int_input("  Item No: ", 0)
        if choice == 0: break
        if choice > len(items_list):
            print("  Invalid selection.")
            continue
        
        p_name = items_list[choice - 1]
        p_info = branch["inventory"][p_name]
        qty = get_int_input(f"  Quantity for {p_name}: ", 1)

        # Validation kung sapat ba ang stock
        if qty > p_info["stock"]:
            print(f"  Insufficient stock. Available: {p_info['stock']}")
            continue

        subtotal = p_info["price"] * qty
        order_items.append({"name": p_name, "qty": qty, "price": p_info["price"], "subtotal": subtotal})
        print(f"  Added: {qty}x {p_name} = P{subtotal:.2f}")

    if not order_items: return

    confirm = input("\n  Confirm payment receipt? (y/n): ").lower()
    if confirm in ['y', 'yes']:
        
        # --- REQUIREMENT #3: AUTOMATICALLY UPDATE STOCK LEVELS ---
        for item in order_items:
            branch["inventory"][item["name"]]["stock"] -= item["qty"]

        # --- REQUIREMENT #2: RECORD TRANSACTION ---
        txn_id = len(data["transactions"]) + 1
        total_amount = sum(i["subtotal"] for i in order_items)
        
        data["transactions"].append({
            "txn_id": txn_id,
            "branch_id": b_id,
            "branch_name": branch["name"],
            "items": order_items,
            "total": total_amount
        })
        save_data(data)

        # Print out ng resibo para sa transaksyon
        print("\n  ========================================")
        print("               SALES RECEIPT")
        print(f"  Branch: {branch['name']}")
        print(f"  TXN ID: #{txn_id}")
        print("  ----------------------------------------")
        for i in order_items:
            print(f"  {i['name']:<18} {i['qty']:>3}x   P{i['subtotal']:>8.2f}")
        print("  ----------------------------------------")
        print(f"  TOTAL AMOUNT DUE:         P{total_amount:>8.2f}")
        print("  ========================================")
        
def view_reports(data):
    print("\n  === SALES REPORTS ===")
    print("  [1] Branch Sales Report")
    print("  [2] Overall Sales Report (All Branches)")
    choice = input("  Choose: ").strip()

    if choice == "1":
        # Report para sa isang partikular na branch lamang
        b_id = select_branch(data)
        if not b_id: return
        print(f"\n  === REPORT FOR {data['branches'][b_id]['name'].upper()} ===")
        branch_txns = [t for t in data["transactions"] if t["branch_id"] == b_id]
        total_rev = sum(t["total"] for t in branch_txns)
        print(f"  Total Transactions: {len(branch_txns)}")
        print(f"  Total Gross Revenue: P{total_rev:.2f}")
        
    elif choice == "2":
        # Overall report para sa kabuuang kita ng buong negosyo
        print("\n  === OVERALL GLOBAL REPORT ===")
        grand_total = sum(t["total"] for t in data["transactions"])
        print(f"  Total Orders Processed: {len(data['transactions'])}")
        print(f"  Grand Total Revenue (All Branches): P{grand_total:.2f}")
        
def manage_inventory(data):
    while True:
        print("\n  === INVENTORY MANAGEMENT ===")
        print("  [1] View Branch Inventory")
        print("  [2] Add Product to Branch")
        print("  [3] Update Product Details")
        print("  [4] Remove Product")
        print("  [0] Back")
        choice = input("  Choose: ").strip()

        if choice in ["1", "2", "3", "4"]:
            b_id = select_branch(data)
            if not b_id: continue

            if choice == "1":
                display_inventory(data, b_id)
            elif choice == "2":
                name = get_nonempty_input("  Product Name: ").title()
                price = get_float_input("  Selling Price (P): ")
                stock = get_int_input("  Initial Stock: ", 0)
                restock = get_int_input("  Restock Alert Level: ", 1)
                data["branches"][b_id]["inventory"][name] = {"price": price, "stock": stock, "restock_level": restock}
                save_data(data)
                print(f"  '{name}' saved to inventory file.")
            elif choice == "3":
                display_inventory(data, b_id)
                p_name = get_nonempty_input("  Product Name to Update: ").title()
                if p_name in data["branches"][b_id]["inventory"]:
                    price = get_float_input("  New Price (P): ")
                    stock = get_int_input("  New Stock Qty: ", 0)
                    data["branches"][b_id]["inventory"][p_name]["price"] = price
                    data["branches"][b_id]["inventory"][p_name]["stock"] = stock
                    save_data(data)
                    print("  Product file updated.")
                else:
                    print("  Product not found.")
            elif choice == "4":
                display_inventory(data, b_id)
                p_name = get_nonempty_input("  Product Name to Remove: ").title()
                if p_name in data["branches"][b_id]["inventory"]:
                    del data["branches"][b_id]["inventory"][p_name]
                    save_data(data)
                    print("  Product deleted.")
        elif choice == "0":
            break


def get_nonempty_input(prompt):
    """Keeps asking until the user types something that isn't blank."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("  Input cannot be empty. Please try again.")

def get_int_input(prompt, min_value=0):
    """Keeps asking until the user enters a valid integer >= min_value."""
    while True:
        try:
            value = int(input(prompt).strip())
            if value >= min_value:
                return value
            print(f"  Please enter a number of at least {min_value}.")
        except ValueError:
            print("  Invalid input. Please enter a whole number.")

def get_float_input(prompt, min_value=0.0):
    """Keeps asking until the user enters a valid positive decimal number."""
    while True:
        try:
            value = float(input(prompt).strip())
            if value >= min_value:
                return value
            print(f"  Please enter a value of at least {min_value}.")
        except ValueError:
            print("  Invalid input. Please enter a number (e.g. 25.50).")




def select_branch(data):
    """Shows a numbered list of branches and returns the chosen branch ID."""
    branches = list(data["branches"].items())
    if not branches:
        print("  No branches registered yet.")
        return None

    print("\n  === SELECT BRANCH ===")
    for i, (b_id, b_info) in enumerate(branches, 1):
        print(f"  [{i}] {b_info['name']} — {b_info['location']}")
    print("  [0] Cancel")

    choice = get_int_input("  Choose branch: ", 0)
    if choice == 0 or choice > len(branches):
        return None

    return branches[choice - 1][0]   

def display_inventory(data, b_id):
    """Prints a formatted inventory table for a given branch."""
    branch = data["branches"][b_id]
    inventory = branch["inventory"]

    print(f"\n  === INVENTORY: {branch['name'].upper()} ===")
    if not inventory:
        print("  No products found.")
        return

    print(f"  {'No.':<5} {'Product':<22} {'Price':>8} {'Stock':>7} {'Restock':>8}")
    print("  " + "-" * 55)

    for i, (name, info) in enumerate(inventory.items(), 1):
        # Highlight items that are at or below the restock alert level
        alert = " !" if info["stock"] <= info["restock_level"] else ""
        print(
            f"  {i:<5} {name:<22} "
            f"P{info['price']:>7.2f} "
            f"{info['stock']:>7} "
            f"{info['restock_level']:>8}"
            f"{alert}"
        )
    print()




def sari_sari():
    data = load_data()

    while True:
        print("\n" + "=" * 45)
        print("       SARI-SARI STORE MANAGEMENT SYSTEM")
        print("=" * 45)
        print("  [1] Manage Branches")
        print("  [2] Manage Inventory")
        print("  [3] Record a Sale")
        print("  [4] View Reports")
        print("  [0] Exit")
        print("-" * 45)

        choice = input("  Choose an option: ").strip()

        if choice == "1":
            manage_branches(data)
        elif choice == "2":
            manage_inventory(data)
        elif choice == "3":
            record_sale(data)
        elif choice == "4":
            view_reports(data)
        elif choice == "0":
            print("\n  Goodbye! Data saved.\n")
            break
        else:
            print("  Invalid choice. Please try again.")


if __name__ == "__main__":
    sari_sari()
