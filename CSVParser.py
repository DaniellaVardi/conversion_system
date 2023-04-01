import json
import pandas as pd
from datetime import datetime, timedelta

EUR_TO_USD = 2
AUD_TO_USD = 3
DIVIDE_IN_100 = 100

def getDataFromCSV(filenameToJson, filenameSearch):
    df_toJSON = pd.read_csv(filenameToJson)
    df_toSearch = pd.read_csv(filenameSearch)
    ## TODO explain
    df_toSearch = df_toSearch.replace(['AMERICAN_EXPRESS'], 'AMEX')
    MerchantName= df_toJSON['MerchantName'].head(1).values[0]
    return df_toJSON, df_toSearch, MerchantName

def formatDateType(processor, merchantName, dateOrder, addDays=0):
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

def formatDataToJson_CODE(df_toJSON, df_toSearch):
    orders_dict =[]
    orders_dict_duplicate =[]
    ordersId = []

    for index, row in df_toJSON.iterrows():

        processor = df_toSearch.loc[(df_toSearch['ReasonCode'] == row.ReasonCode) & (df_toSearch['Processor'] == row.ProcessorName)]['Reasoncategory'].values[0]

        existsID = False
        for id in ordersId:
            if id == row.OrderID:
                existsID = True
        if existsID == True:
            new_dict_duplicate = {
                'OrderID': row.OrderID,
                'ReasonCode':  row.ReasonCode,
                'Amount': int(row.Amount),
                'Currency': row.Currency,
                'ProcessorName': row.ProcessorName,
                'DeliveryDate': formatDateType(row.ProcessorName, row.MerchantName, row.DeliveryDate),
                'OrderDate': formatDateType(row.ProcessorName, row.MerchantName, row.OrderDate),
                'MerchantName': row.MerchantName,
                'Address': row.Address,
                'ReasonCatadory': processor,
                'AmountUSD': int(calculate_amount_usd(row.Amount, row.Currency, row.MerchantName, row.ProcessorName)),
                "ProcessingDate": formatDateType(row.ProcessorName, row.MerchantName, row.OrderDate, 3)
            }
            orders_dict_duplicate.append(new_dict_duplicate)
            continue

        ordersId.append(row.OrderID)

        new_dict = {
            'OrderID': row.OrderID,
            'ReasonCode':  row.ReasonCode,
            'Amount': int(row.Amount),
            'Currency': row.Currency,
            'ProcessorName': row.ProcessorName,
            'DeliveryDate': formatDateType(row.ProcessorName, row.MerchantName, row.DeliveryDate),
            'OrderDate': formatDateType(row.ProcessorName, row.MerchantName, row.OrderDate),
            'MerchantName': row.MerchantName,
            'Address': row.Address,
            'ReasonCatadory': processor,
            'AmountUSD': int(calculate_amount_usd(row.Amount, row.Currency, row.MerchantName, row.ProcessorName)),
            "ProcessingDate": formatDateType(row.ProcessorName, row.MerchantName, row.OrderDate, 3)
        }
        orders_dict.append(new_dict)
    orders_dict = json.dumps(orders_dict, indent = 4)
    orders_dict_duplicate = json.dumps(orders_dict_duplicate, indent = 4)

    return orders_dict, orders_dict_duplicate


def calculate_amount_usd(amount, currency, merchantName, processor):
    """
    Convert the given amount to USD based on the currency.

    Args:
        amount (float): A float representing the amount.
        currency (str): A string representing the currency.

    Returns:
        float: A float representing the converted amount in USD.
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
    outFile =  open(path, "w")
    outFile.write(orders_dict)