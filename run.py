import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("love_sandwiches")


def get_sales_data():
    """
    Get sales figure inputs from the user
    """

    print("Please enter sales data from the last market.")
    print("Data should be 6 numbers, separatd by commas.")
    print("Example: 10,20,30,40,50,60\n")

    data_str = input(">")
    sales_data = [data.strip() for data in data_str.split(",")]
    while not validate_data(sales_data):
        data_str = input(">")
        sales_data = [data.strip() for data in data_str.split(",")]

    return [int(data) for data in sales_data]


def validate_data(values):
    """
    Attempts to covert data into integers
    Raises ValueError if strings cannot be converted to int,
    or if there are not 6 values
    """
    try:
        if len(values) != 6:
            raise ValueError(
                f"6 values expected, {len(values)} provided"
            )
        values = [int(data) for data in values]
    except ValueError as exception:
        print(f"Invalid data: {exception}\nPlease try again.")
        return False
    else:
        return True


def update_sales_data(data):
    """
    Update sales worksheet, add new row with list data provided
    """
    print("Updating sales worksheet...\n")
    sales_worksheet = SHEET.worksheet("sales")
    sales_worksheet.append_row(data)
    print("Sales worksheet updated.\n")


def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate the surplus for each item type.

    Surplus is defined as sales figure subtracted from stock.
    - Positive surplus indicates waste
    - Negative surplus indicates sandwiches made when stock runs out
    """
    print("Calculating surplus data...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]
    print(stock_row)


def main():
    """
    Run main program functions
    """
    data = get_sales_data()
    update_sales_data(data)
    calculate_surplus_data(data)


print("Welcome to Love Sandwiches Data Automation\n")
main()
