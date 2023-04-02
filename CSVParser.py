import json
import pandas as pd
from datetime import datetime, timedelta

EUR_TO_USD = 2
AUD_TO_USD = 3

def getDataFromCSV(filenameToJson, filenameSearch):
    """
    Reads two CSV files and returns the dataframes for converting orders to JSON and for searching reason codes.

    Args:
        filenameToJson (str): A string that represents the file path to the CSV file containing the order data for conversion.
        filenameSearch (str): A string that represents the file path to the CSV file containing the reason code data for searching.

    Returns:
        df_toJSON (pandas.DataFrame): A pandas dataframe that contains the order data for conversion to JSON format.
        df_toSearch (pandas.DataFrame): A pandas dataframe that contains the reason code data for searching.
        MerchantName (str): A string that represents the name of the merchant for the order data.

    Raises:
        FileNotFoundError: If the specified file path does not exist.
    """
    df_toJSON = pd.read_csv(filenameToJson)
    df_toSearch = pd.read_csv(filenameSearch)

    # This line replaces the string 'AMERICAN_EXPRESS' with 'AMEX' in the DataFrame df_toSearch.
    # This is done to match the appropriate processor name with the template defined in the file file1.
    df_toSearch = df_toSearch.replace(['AMERICAN_EXPRESS'], 'AMEX')

    MerchantName= df_toJSON['MerchantName'].head(1).values[0]
    return df_toJSON, df_toSearch, MerchantName

def formatDateType(processor, merchantName, dateOrder, addDays=0):
    """
   Formats the dateOrder string based on the specified processor and merchantName.

   Args:
       processor (str): The payment processor used for the order.
       merchantName (str): The name of the merchant that processed the order.
       dateOrder (str): The original date of the order.
       addDays (int, optional): The number of days to add to the date. Defaults to 0.

   Returns:
       str: The formatted date string.

   Raises:
       None
   """
    if(processor == 'VISA'):
        if merchantName in ['MyBook', 'MyShop']:
            dateOrder_N = datetime.strptime(dateOrder, '%Y-%m-%d')
        elif merchantName in ['MyFlight']:
            dateOrder_N = datetime.strptime(dateOrder, '%Y/%m/%d')
        else:
            return ""
    elif(processor == 'AMEX'):
        if merchantName in ['MyBook', 'MyFlight']:
            dateOrder_N = datetime.strptime(dateOrder, '%d-%m-%Y')
        elif merchantName in ['MyShop']:
            dateOrder_N = datetime.strptime(dateOrder, '%d/%m/%Y')
        else:
            return ""
    else:
        dateOrder_N = dateOrder.isoformat()

    dateOrder_N = dateOrder_N + timedelta(days=addDays)
    dateOrder_N = dateOrder_N.strftime('%Y-%m-%d')

    return dateOrder_N

def getReasonCategory(df_toSearch, reasonCode, processorName):
    """
    Returns the reason category associated with the given reason code and processor name, by searching in the
    provided DataFrame df_toSearch.

    Parameters:
    - df_toSearch (pandas.DataFrame): A DataFrame containing the reason codes and categories to be searched.
    - reasonCode (str): The reason code to be searched for.
    - processorName (str): The name of the processor to be searched for.

    Returns:
    - str: The reason category associated with the given reason code and processor name, as a string.

    Raises:
    - IndexError: If no match is found in the DataFrame, i.e., no row has both the given reason code and processor name.
    """
    return df_toSearch.loc[(df_toSearch['ReasonCode'] == reasonCode) & (df_toSearch['Processor'] == processorName)]['Reasoncategory'].values[0]

def createOrder(row, ordersId, df_toSearch):
    """
    Create a new order dictionary based on the input row and add its order ID to the ordersId list.

    Args:
    - row: a pandas Series object representing a single row in the input data
    - ordersId: a list of order IDs to which the new order ID will be added
    - df_toSearch: a pandas DataFrame containing information for mapping ReasonCodes to ReasonCategories

    Returns:
    - new_order: a dictionary representing the new order
    """
    processor = getReasonCategory(df_toSearch, row.ReasonCode, row.ProcessorName)
    new_order = {
        'OrderID': row.OrderID,
        'ReasonCode':  isInt(row.ReasonCode),
        'Amount': int(row.Amount),
        'Currency': row.Currency,
        'ProcessorName': row.ProcessorName,
        'DeliveryDate': formatDateType(row.ProcessorName, row.MerchantName, row.DeliveryDate),
        'OrderDate': formatDateType(row.ProcessorName, row.MerchantName, row.OrderDate),
        'MerchantName': row.MerchantName,
        'Address': row.Address,
        'ReasonCategory': processor,
        'AmountUSD': int(calculate_amount_usd(row.Amount, row.Currency, row.MerchantName, row.ProcessorName)),
        "ProcessingDate": formatDateType(row.ProcessorName, row.MerchantName, row.OrderDate, 3)
    }
    ordersId.append(row.OrderID)
    return new_order

def createDuplicateOrder(row, df_toSearch):
    """
    Creates a new order dictionary from a given row of data, with the same data as the original order
    but with a new order ID.

    Args:
        row (pandas.Series): A pandas Series object representing a row of order data.
        df_toSearch (pandas.DataFrame): A pandas DataFrame object representing a lookup table of processor
            and merchant name combinations and their respective date formats.

    Returns:
        dict: A dictionary representing the new order with a duplicate of the original data but with a new order ID.
    """
    processor = getReasonCategory(df_toSearch, row.ReasonCode, row.ProcessorName)
    new_order = {
        'OrderID': row.OrderID,
        'ReasonCode':  isInt(row.ReasonCode),
        'Amount': int(row.Amount),
        'Currency': row.Currency,
        'ProcessorName': row.ProcessorName,
        'DeliveryDate': formatDateType(row.ProcessorName, row.MerchantName, row.DeliveryDate),
        'OrderDate': formatDateType(row.ProcessorName, row.MerchantName, row.OrderDate),
        'MerchantName': row.MerchantName,
        'Address': row.Address,
        'ReasonCategory': processor,
        'AmountUSD': int(calculate_amount_usd(row.Amount, row.Currency, row.MerchantName, row.ProcessorName)),
        "ProcessingDate": formatDateType(row.ProcessorName, row.MerchantName, row.OrderDate, 3)
    }
    return new_order

def formatDataToJson_CODE(df_toJSON, df_toSearch):
    """
    Convert a pandas DataFrame `df_toJSON` to JSON, checking for duplicate orders.

    Parameters:
    -----------
    df_toJSON : pandas.DataFrame
        The DataFrame to be converted to JSON.
    df_toSearch : pandas.DataFrame
        The DataFrame to search for duplicate orders.

    Returns:
    --------
    tuple : Two JSON-formatted strings:
        - Unique orders converted from `df_toJSON`.
        - Duplicate orders converted from `df_toJSON`.
    """
    orders_dict =[]
    orders_dict_duplicate =[]
    ordersId = []

    for index, row in df_toJSON.iterrows():

        existsID = row.OrderID in ordersId
        if existsID:
            new_dict_duplicate = createDuplicateOrder(row, df_toSearch)
            orders_dict_duplicate.append(new_dict_duplicate)
            continue

        new_dict = createOrder(row, ordersId, df_toSearch)
        orders_dict.append(new_dict)

    orders_dict = json.dumps(orders_dict, indent=4)
    orders_dict_duplicate = json.dumps(orders_dict_duplicate, indent=4)

    return orders_dict, orders_dict_duplicate

def calculate_amount_usd(amount, currency, merchantName, processor):

    """
    Converts `amount` from `currency` to USD, adjusting for merchant and processor rules.

    Parameters:
    amount : float
        The amount of money to be converted.
    currency : str
        The currency of the original `amount`.
    merchantName : str
        The name of the merchant for which the `amount` was charged.
    processor : str
        The name of the processor that handled the transaction.

    Returns:
    float : The equivalent `amount` in USD, after any conversions or adjustments.
    """
    if currency == 'EUR':
        return amount / EUR_TO_USD
    elif currency == 'AUD':
        return amount / AUD_TO_USD
    else:
        amountUSD = amount

    if(processor == 'VISA'):
        if merchantName in ['MyBook', 'MyFlight']:
            amountUSD = amountUSD / 100
        elif merchantName in ['MyShop']:
            amountUSD = amountUSD / 1000

    return amountUSD

def createOutput(orders_dict, path):
    """
    Write the JSON-formatted `orders_dict` to the specified `path`.

    Parameters:
    -----------
    orders_dict : str
        A JSON-formatted string to be written to the output file.
    path : str
        The file path where the output should be written.
    """
    outFile =  open(path, "w")
    outFile.write(orders_dict)

def isInt(reasonCode):
    if reasonCode % 1 != 0:
        return reasonCode
    return int(reasonCode)

def convert_orders_to_json(orders_dict, orders_dict_duplicate, outputPath):
    """
    Converts two dictionaries of orders to JSON files and prints the location of the output files.

    Args:
        orders_dict (dict): A dictionary containing orders.
        orders_dict_duplicate (dict): A dictionary containing duplicate orders.
        outputPath (str): The desired path for the output files.

    Returns:
        None
    """
    createOutput(orders_dict, '..' + outputPath +'.json')
    createOutput(orders_dict_duplicate, '..' + outputPath+'_Duplicate.json')

    print(f"The Converted Orders JSON file located at:")
    print(f"{outputPath}.json")
    print(f"\n")
    print(f"The Converted Duplicate Orders JSON file located at:")
    print(f"{outputPath}_Duplicate.json")