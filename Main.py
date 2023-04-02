
from CSVParser import *

class Main:

    MAX_ATTEMPTS = 5
    attempt_count = 0

    while True:
        inputPath = input(f"Please enter the file path: ") # for example /conversion_system/Inputs/MyShop/file1.csv
        try:
            convertedOrders, reasonCodes, MerchantName = getDataFromCSV('..'+ inputPath, "reason_codes.csv" )
            orders_dict, orders_dict_duplicate = formatDataToJson_CODE(convertedOrders, reasonCodes)
            outputPath = inputPath.replace('Inputs', 'Outputs').replace('.csv', '')

            convert_orders_to_json(orders_dict, orders_dict_duplicate, outputPath)

            break

        except FileNotFoundError:
            attempt_count += 1
            if attempt_count < MAX_ATTEMPTS:
                print(f"Error: The specified file was not found. Please try again.")
            else:
                print(f"Error: The specified file was not found. Maximum number of attempts reached.")
                break
        except Exception as e:
            print(f"Error: {e}")