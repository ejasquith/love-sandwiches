import gspread
from google.oauth2.service_account import Credentials

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

    return [int(stock) - sales for sales, stock in zip(sales_row, stock_row)]


def update_worksheet(data, worksheet):
    """
    Update given worksheet with a single row of data.
    """
    print(f"Updating {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet.capitalize()} worksheet updated.")


def get_last_5_entries_sales():
    """
    Collects columns of data from salesworksheet, collecting
    the last 5 entries for each sandwich and returns the data
    as a list of lists
    """
    sales = SHEET.worksheet("sales")
    columns = []
    for ind in range(1, 7):
        columns.append(sales.col_values(ind)[-5:])
    return columns


def calculate_stock_data(data):
    """
    Calculate the recommended stock for each product type
    Recommendation is average of last 5 sales figures + 10%
    """
    print("Calculating recommended stock data...\n")
    new_stock_data = []
    for column in data:
        int_column = [int(data) for data in column]
        new_stock_data.append(
            round((sum(int_column) / len(int_column)) * 1.1, 0))
    print("Recommended stock data calculated.\n")
    return new_stock_data


def main():
    """
    Run main program functions
    """
    data = get_sales_data()
    update_worksheet(data, "sales")
    new_surplus_data = calculate_surplus_data(data)
    update_worksheet(new_surplus_data, "surplus")
    sales_columns = get_last_5_entries_sales()
    new_stock_data = calculate_stock_data(sales_columns)
    update_worksheet(new_stock_data, "stock")


print("Welcome to Love Sandwiches Data Automation\n")
main()
