import json
import os

from abc import ABC, abstractmethod

file_name = "Week 6/inventory.json"

class Product(ABC):
    """Represents a single product in the inventory."""

    @abstractmethod
    def get_fulfilment_info(self):
        pass
    
    def __init__(self, product_id, name, price, quantity):
        """Constructor - initialize a product with its attributes."""
        self.__product_id = str(product_id)
        self.__name = name
        self.__price = price
        self.__quantity = quantity
    
    def update_stock(self, new_quantity):
        """Update the stock quantity for this product."""
        self.__quantity = new_quantity
    
    def display_information(self):
        """Display product in multi-line format (for search)."""
        print(f"ID: P{self.__product_id}")
        print(f"Name: {self.__name}")
        print(f"Price: ${self.__price:.2f}")
        print(f"Stock: {self.__quantity}")

    def display_single_line(self):
        """Display product in single-line format (for inventory list)."""
        print(f"ID: P{self.__product_id} | Name: {self.__name} | Price: ${self.__price:.2f} | Stock: {self.__quantity}")
    
    # Getters (to read private attributes from outside the class)
    def get_id(self):
        return self.__product_id
    
    def get_name(self):
        return self.__name
    
    def get_price(self):
        return self.__price
    
    def get_quantity(self):
        return self.__quantity

class DigitalProduct(Product):
    """A product delivered as a download."""

    def __init__(self, product_id, name, price, quantity, download_size):
        super().__init__(product_id, name, price, quantity)
        self.__download_size = download_size

    def get_download_size(self):
        return self.__download_size

    def get_fulfilment_info(self):
        return "Delivered digitally. Download size: " + str(self.__download_size) + " MB"

class PhysicalProduct(Product):
    """A product that is shipped to the customer."""

    def __init__(self, product_id, name, price, quantity, weight):
        super().__init__(product_id, name, price, quantity)
        self.__weight = weight

    def get_weight(self):
        return self.__weight

    def get_fulfilment_info(self):
        return "Ships to the customer's address."

    def display_information(self):
        super().display_information()
        print(f"Weight: {self.__weight} kg")

class Inventory:
    """Manages a collection of products in the inventory."""
    
    def __init__(self):
        """Constructor - initialize an empty product list."""
        self.__products = []

    def get_total_stock(self):
        """Return total quantity of all products in inventory."""
        return sum(product.get_quantity() for product in self.__products)
    
    def add_product(self, product):
        """Add a product object (Physical or Digital) to the inventory."""
        self.__products.append(product)

    def search_product_by_term(self, search_term):
        """Search for products by ID or name. Returns list of matching products."""
        found_items = []
        clean_term = search_term.lstrip("Pp").strip()
        
        for product in self.__products:
            # Match by ID or name (case-insensitive)
            if str(product.get_id()) == clean_term or clean_term.lower() in product.get_name().lower():
                found_items.append(product)
        
        return found_items

    def update_product_stock(self, search_term, new_quantity):
        """Update stock for a product by ID or name. Returns True if successful."""
        clean_term = search_term.lstrip("Pp").strip()
        
        for product in self.__products:
            # Match by ID or name (case-insensitive)
            if str(product.get_id()) == clean_term or clean_term.lower() in product.get_name().lower():
                product.update_stock(new_quantity)
                return True
        
        return False
    
    def display_all(self):
        """Display all products in single-line format."""
        if not self.__products:
            print("Inventory is empty.")
        else:
            for product in self.__products:
                product.display_single_line()
    
    def get_products(self):
        """Return the list of all products."""
        return self.__products

class MainProgram:
    """Displays the menu, gets user input, calls the appropriate Inventory methods."""

    def __init__(self, file_name):
        self.file_name = file_name
        self.inventory = Inventory()
        self.file_handler = FileHandling()
        self.file_handler.load_inventory(file_name, self.inventory)

    def display_welcome(self):
        print("\n========================================")
        print("\nINVENTORY MANAGER SYSTEM")
        print("\n========================================")

        if self.inventory.get_products():
            print("\ninventory.json found.")
            print("Inventory loaded successfully.\n")
        else:
            print("\ninventory.json not found.")
            print("Starting with an empty inventory.\n")

    def display_menu(self):
        print("\n----------- MENU -----------")
        print("1. Display All Products")
        print("2. Add Product")
        print("3. Update Stock")
        print("4. Search Product")
        print("5. Save Inventory")
        print("6. Exit")

    def handle_display_all(self):
        print("\nCurrent Inventory")
        print("------------------------------------------------")
        self.inventory.display_all()
        print("------------------------------------------------")

    def handle_add_product(self):
        print("\nAdd New Product")

        # INPUT 1: Get and validate Product ID - must be numbers only
        while True:
            try:
                raw_id = input("Product ID: ").strip()
                product_id = raw_id.lstrip("Pp")

                if not product_id:
                    print("Invalid ID. Please enter a valid product ID.")
                    continue

                if not product_id.isdigit():
                    print("Invalid ID. ID must contain only numbers (0-9)")
                    continue

                # CHECK IF ID ALREADY EXISTS
                existing_products = self.inventory.search_product_by_term(product_id)
                if existing_products:
                    product = existing_products[0]
                    print(f"\nP{product_id} already added to cart.")
                    print(f"Name: {product.get_name()} | Price: ${product.get_price():.2f} | Current Stock: {product.get_quantity()}")

                    # VALIDATE YES/NO ONLY
                    while True:
                        response = input("Do you want to continue adding more? (yes/no): ").strip().lower()
                        if response in ["yes", "no"]:
                            break
                        print("Invalid input. Please enter 'yes' or 'no'.")

                    if response == "no":
                        print("Cancelled.")
                        return

                break
            except:
                print("Invalid input. Please enter a valid product ID.")

        # INPUT 2: Get Product Name
        product_name = input("Product Name: ").strip()

        # INPUT 3: Get and validate Price - must be a number, not negative
        while True:
            try:
                price = float(input("Price: ").strip())
                if price < 0:
                    print("Price cannot be negative. Please enter a valid price.")
                    continue
                break
            except ValueError:
                print("Invalid input. Please enter a valid price (e.g., 9.99)")

        # INPUT 4: Choose product type
        while True:
            print("\nProduct type:")
            print("1. Physical")
            print("2. Digital")
            product_type = input("Choose type (1 or 2): ").strip()
            if product_type in ["1", "2"]:
                break
            print("Invalid choice. Enter 1 or 2.")

        # INPUT 5: Extra field depends on type
        if product_type == "1":
            while True:
                try:
                    weight = float(input("Weight (kg): ").strip())
                    if weight <= 0:
                        print("Weight must be greater than 0.")
                        continue
                    break
                except ValueError:
                    print("Invalid input. Please enter a number.")
        else:
            while True:
                try:
                    download_size = float(input("Download size (MB): ").strip())
                    if download_size <= 0:
                        print("Download size must be greater than 0.")
                        continue
                    break
                except ValueError:
                    print("Invalid input. Please enter a number.")

        # INPUT 6: Get and validate Stock Quantity - must be number, check 500 limit
        while True:
            qty_input = input("Stock Quantity: ").strip()

            if qty_input.lower() == "quit":
                print("Cancelled.")
                return

            if not qty_input.isdigit():
                print("Invalid input. Quantity must be a positive number.")
                continue

            valid_quantity = int(qty_input)

            if valid_quantity <= 0:
                print("Quantity must be greater than 0.")
                continue

            if valid_quantity > 500:
                print(f"Quantity cannot exceed 500. You entered: {valid_quantity}")
                continue

            current_total = self.inventory.get_total_stock()
            new_total = current_total + valid_quantity

            if new_total > 500:
                print(f"Cannot add {valid_quantity} units.")
                print(f"Current stock: {current_total} | Max allowed: 500 | Available space: {500 - current_total}")
                continue

            # Create the matching subclass object and pass it to Inventory
            if product_type == "1":
                product = PhysicalProduct(product_id, product_name, price, valid_quantity, weight)
            else:
                product = DigitalProduct(product_id, product_name, price, valid_quantity, download_size)
            self.inventory.add_product(product)
            print(f"Product P{product_id} added successfully.")
            break

    def handle_update_stock(self):
        print("\nUpdate Stock")
        search_term = input("Enter Product ID or Name: ").strip()

        found_items = self.inventory.search_product_by_term(search_term)

        if found_items:
            product = found_items[0]
            print("\nProduct Found:")
            product.display_information()

            while True:
                raw_qty = input("\nNew Stock Quantity: ").strip()

                if raw_qty.lower() == "quit":
                    print("Cancelled.")
                    break

                if not raw_qty.isdigit():
                    print("Invalid input. Please enter a positive number.")
                    continue

                valid_quantity = int(raw_qty)

                if valid_quantity <= 0:
                    print("Quantity must be greater than 0.")
                    continue

                current_total = self.inventory.get_total_stock()
                old_quantity = product.get_quantity()
                new_total = current_total - old_quantity + valid_quantity

                if new_total <= 500:
                    self.inventory.update_product_stock(search_term, valid_quantity)
                    print("Stock updated successfully!")
                    break
                else:
                    print(f"Current stock (excl. this product): {current_total - old_quantity} | New quantity: {valid_quantity} | Total would be: {new_total} | Limit: 500")

        else:
            print("\nProduct not found.")

    def handle_search_product(self):
        search_term = input("Search Product ID: ").strip()
        found_items = self.inventory.search_product_by_term(search_term)

        if found_items:
            print("\nProduct Found")
            print("\n------------------------------------------------")
            for product in found_items:
                product.display_information()
            print("------------------------------------------------\n")
        else:
            print("Product not found.\n")

    def handle_save_inventory(self):
        self.file_handler.save_inventory(self.file_name, self.inventory)
        print("Saving inventory...")
        print(f"Inventory saved successfully to {self.file_name}\n")

    def run(self):
        self.display_welcome()

        while True:
            self.display_menu()
            choice = input("\nEnter option: ").strip()

            if choice == "1":
                self.handle_display_all()
            elif choice == "2":
                self.handle_add_product()
            elif choice == "3":
                self.handle_update_stock()
            elif choice == "4":
                self.handle_search_product()
            elif choice == "5":
                self.handle_save_inventory()
            elif choice == "6":
                self.handle_save_inventory()
                print("Thank you for using Inventory Management System.")
                print("Program terminated.")
                break
            else:
                print("Invalid choice. Please select from 1 to 6.")

class FileHandling:
    """Loads inventory data from JSON and saves inventory data to JSON."""

    def load_inventory(self, file_name, inventory_obj):
        """Load products from JSON file into Inventory object as Product instances."""
        try:
            with open(file_name, "r") as f:
                data = json.load(f)
                for item in data:
                    inventory_obj.add_product(item["id"], item["name"], item["price"], item["quantity"])
        except FileNotFoundError:
            pass
        except json.JSONDecodeError:
            pass

    def save_inventory(self, file_name, inventory_obj):
        """Convert Product objects to dictionaries and save to JSON."""
        try:
            products_data = []
            for product in inventory_obj.get_products():
                products_data.append({
                    "id": product.get_id(),
                    "name": product.get_name(),
                    "price": product.get_price(),
                    "quantity": product.get_quantity()
                })
            with open(file_name, "w") as f:
                json.dump(products_data, f, indent=4)
        except Exception as e:
            print(f"Error saving file: {e}\n")


#---- THE MENU SHIT -----
if __name__ == "__main__":
    program = MainProgram(file_name)
    program.run()

#Eugene Repo URL: https://github.com/Eugene2603188/Lab7

