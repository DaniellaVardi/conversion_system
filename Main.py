
from CSVParser import *

class Main:

    inputPath = '/conversion_system/Inputs/MyShop/file1.csv'


    convertedOrders, reasonCodes, MerchantName = getDataFromCSV('..'+ inputPath, "reason_codes.csv" )
    orders_dict, orders_dict_duplicate = formatDataToJson_CODE(convertedOrders, reasonCodes)
    outputPath = inputPath.replace('Inputs', 'Outputs').replace('.csv', '')

    createOutput(orders_dict, '..' + outputPath +'.json')
    createOutput(orders_dict_duplicate, '..' + outputPath+'_Duplicate.json')

