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
    validate_data(sales_data)


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
    except ValueError as e:
        print(f"Invalid data: {e}\nPlease try again.")


get_sales_data()
