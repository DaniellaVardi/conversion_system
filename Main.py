
from CSVParser import *

class Main:

    MAX_ATTEMPTS = 5
    attempt_count = 0

    while True:
        inputPath = input("Please enter the file path: ") # for example /conversion_system/Inputs/MyShop/file1.csv
        try:
            convertedOrders, reasonCodes, MerchantName = getDataFromCSV('..'+ inputPath, "reason_codes.csv" )
            orders_dict, orders_dict_duplicate = formatDataToJson_CODE(convertedOrders, reasonCodes)
            outputPath = inputPath.replace('Inputs', 'Outputs').replace('.csv', '')

            createOutput(orders_dict, '..' + outputPath +'.json')
            createOutput(orders_dict_duplicate, '..' + outputPath+'_Duplicate.json')

            print("The Converted Orders JSON file located at:")
            print(outputPath + '.json')
            print("\n")
            print("The Converted Duplicate Orders JSON file located at:")
            print(outputPath + '_Duplicate.json')
            break

        except FileNotFoundError:
            attempt_count += 1
            if attempt_count < MAX_ATTEMPTS:
                print("Error: The specified file was not found. Please try again.")
            else:
                print("Error: The specified file was not found. Maximum number of attempts reached.")
                break
        except Exception as e:
            print(f"Error: {e}")