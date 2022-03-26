# === Import Libraries ===
from tabulate import tabulate

# === Global Lists ===
country_list = []
code_list = []
product_list = []
cost_list = []
quantity_list = []

shoe_objs_list = []
headings_list = []


# === Class Creation ===
class Shoe:
    """Shoe class consists of the read_data method which fetches inventory data
    from a text file."""

    def read_data(self):
        """ Method to read data from inventory1.txt."""

        try:
            with open("inventory1.txt", "r") as o_file:
                # reading the first line of the text file and putting that
                # info into a global list of headings for use view_table function
                first_line = o_file.readline()
                global headings_list
                headings_list = first_line.strip().split(",")

                # getting each line of the text file after the headings
                # into a long list
                line_list = o_file.readlines()

                # getting country, code, product, cost, quantity info of each
                # product and saving it to its own global list of that category
                # for use in creating objects with those attributes later
                for item in line_list:
                    temp_var = item.strip().split(",")

                    country = temp_var[0]
                    country_list.append(country)

                    code = temp_var[1]
                    code_list.append(code)

                    product = temp_var[2]
                    product_list.append(product)

                    cost = temp_var[3]
                    cost_list.append(
                        int(cost))  # casting to int for calculation purposes

                    quantity = temp_var[4]
                    quantity_list.append(
                        int(quantity))  # casting to int for calculation purposes

        except Exception:
            print("Something went wrong")


# NOTE: I am creating a separate class to instantiate objects as if I add the __init__ to
# the Shoe class, I would need to provide country, class...etc arguments to create
# an object, but I need to have an object available to first get that information.
# (the instructions say the Shoe class needs to contain a read_data() method).
class ShoeCreate:
    """The ShoeCreate class instantiates objects with country, code, product,
    cost, quantity and value attributes. The value attribute is not take as
    an argument but is calculated using the cost and quantity arguments."""

    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity
        # adding the value calculation
        self.value = self.cost * self.quantity

    def __str__(self):
        """Returns string information about each shoe object in the format:
        'country, code, product, cost, quantity, value'."""
        return f"{self.country}, {self.code}, {self.product}, {self.cost}, " \
               f"{self.quantity}, {self.value}"


# === Object Creation ===
# creating a Shoe object to use it's read_data() method to read from .txt
shoe0 = Shoe()
shoe0.read_data()

# creating 6 objects by passing arguments taken from the global lists
shoe_1 = ShoeCreate(country_list[0], code_list[0], product_list[0],
                    cost_list[0], quantity_list[0])
shoe_2 = ShoeCreate(country_list[1], code_list[1], product_list[1],
                    cost_list[1], quantity_list[1])
shoe_3 = ShoeCreate(country_list[2], code_list[2], product_list[2],
                    cost_list[2], quantity_list[2])
shoe_4 = ShoeCreate(country_list[3], code_list[3], product_list[3],
                    cost_list[3], quantity_list[3])
shoe_5 = ShoeCreate(country_list[4], code_list[4], product_list[4],
                    cost_list[4], quantity_list[4])
shoe_6 = ShoeCreate(country_list[5], code_list[5], product_list[5],
                    cost_list[5], quantity_list[5])

# appending the new objects to the global list of objects
shoe_objs_list.append(shoe_1)
shoe_objs_list.append(shoe_2)
shoe_objs_list.append(shoe_3)
shoe_objs_list.append(shoe_4)
shoe_objs_list.append(shoe_5)
shoe_objs_list.append(shoe_6)


# === Defining Menu Functions ===
def code_search(user_code):
    """Searches for the product code as given by the user and returns
    all attribute information for that product as a string."""

    for item in shoe_objs_list:
        # print the string info for an object that matches the user's input
        if user_code == item.code:
            return item.__str__()


def get_quantity():
    """Creates a list of quantity attributes for each object in the main
    shoe_objs_list list and return it. For use in restock_lowest() and
    sale_highest functions which use quantity information"""
    quantity_obj_list = [i.quantity for i in shoe_objs_list]
    return quantity_obj_list


def restock_lowest():
    """Finds the product with the lowest quantity from the shoe_objs_list and
    increases it by a user defined amount."""

    for item in shoe_objs_list:
        if item.quantity == min(get_quantity()):
            print("The product with the lowest stock is: ")
            print("Product details:", item.__str__())
            print("Original Quantity:", item.quantity)

            # restock the item
            try:
                item.quantity += int(
                    input("Please enter number to increase stock by: "))
            except ValueError:
                print("Invalid input. Please try again.")
            else:
                print("Updated details:", item.__str__())
                print("New Quantity:", item.quantity)


def sale_highest():
    """Finds the product with the highest quantity in the shoe_objs_list and
    discounts the cost of that product by a user-entered percentage."""

    for item in shoe_objs_list:
        # find the object with the attribute equal to the highest quantity from the quantity list
        if item.quantity == max(get_quantity()):

            # printing out all of that product's information
            print("The product with the most stock is:")
            print("Product details:", item.__str__())

            # isolating and printing the quantity and cost attributes for that ite,
            print("Original Quantity:", item.quantity)
            print("Original Cost: R", item.cost)

            # mark product on sale by user given percentage
            # try/except block to handle user input that cannot be cast as an int
            try:
                percentage = int(input("Please enter the percentage to discount (e.g. 20): "))
                # calculating the discounted price
                # checking that the input is a value percentage i.e. between 1 - 100
                if percentage in range(1, 100):
                    # calculate the new cost after the discount % is deducted
                    item.cost = item.cost - (item.cost * (percentage / 100))
                    # printing the updated info
                    print("Updated details:", item.__str__())
                    print("New Cost: R", item.cost)
                else:
                    print("Please enter a number between 1 and 100.")
            # exception if input cannot be cast into an int
            except ValueError:
                print("Invalid input. Please try again.")


def view_table():
    """Uses the Tabulate module to present the information about each product
    in the shoe_objs_list in a table."""

    # appending the new "Value" column heading to the global headings list
    headings_list.append("Value")

    # creating a list of strings describing the objects in the shoe_objs_list
    obj_as_str_list = [i.__str__() for i in shoe_objs_list]

    # creating a list of lists as required by the tabulate method
    new_listing = []
    for i in obj_as_str_list:
        temp_split = i.split(", ")
        new_listing.append(temp_split)

    # displaying the contents of the list of lists under the headings in a table
    print(tabulate(new_listing, headings_list, tablefmt="github"))


# === Main Menu Loop ===
menu_option = ""
# print a welcome message
print("Welcome to the Shoe Inventory Manager! ")

# program exits when the user enters "e"
while menu_option != "e":
    print("\nMenu Options: \n"
          "s - search product code\n"
          "r - restock items\n"
          "m - mark items for sale\n"
          "v - view data\n"
          "e - exit\n")
    menu_option = input("Please select an option: ").lower()

    if menu_option == "s":
        # prompting the user to enter a product code
        user_prod_code = input("Please enter product code: ")

        # if the code_search function returns something then there was a match
        if code_search(user_prod_code) is not None:
            print("\nMatch found: ")
            print(code_search(user_prod_code))
        # if there was no match, print error message
        else:
            print(f"Sorry, no products with code {user_prod_code} found.")

    elif menu_option == "r":
        # get a list of object quantities and call restock_lowest function
        get_quantity()
        restock_lowest()

    elif menu_option == "m":
        # get a list of object quantities and call sale_highest function
        get_quantity()
        sale_highest()

    elif menu_option == "v":
        # printing an empty line before the table to make it easier to read
        print()
        view_table()

    elif menu_option == "e":
        # printing a goodbye message and exiting the program
        print("Thank you for using the inventory manager :)")
        exit()

    else:
        print("Please try again.")

# --- END --
