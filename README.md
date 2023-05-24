# conversion_system
Conversion System @ Forter
Goal
The goal of this project is to implement a basic conversion system that converts files from one format to another. Specifically, the system will convert CSV files to JSON files and perform additional calculations on the data.

Background
The company requires a file conversion system that can convert CSV files containing rejected orders to JSON format. Each line in the CSV file represents a single rejected order, and the JSON file should contain an array of JSON objects, with each object representing an order.

The system should add calculated fields to each order during the conversion process. Additionally, duplicate orders with the same orderId should be filtered out and stored in a separate JSON file.

Instructions
Your task is to implement a basic conversion system with the following capabilities:

Convert order files from CSV to JSON format.
Enrich each order with additional calculated fields.
Save converted orders in a JSON file.
Filter out duplicate orders and store them in a separate JSON file.
Order Properties
Each order in the CSV file has the following properties (columns in the CSV):

OrderId: Order identifier
ReasonCode: Code representing the reason for order rejection
Amount: Order amount
Currency: Order currency
ProcessorName: Processor that charged the order
DeliveryDate: Date for the delivery of the ordered item
OrderDate: Date on which the order was placed
MerchantName: Name of the merchant that sold the item
Address: Customer's delivery address
Calculated Fields
For each order, the system should calculate the following fields:

ReasonCategory: Based on the reason code and processor of the order.
AmountUSD: Conversion of the order amount to USD based on the provided exchange rates.
ProcessingDate: Three days after the order date.
Output Fields
The resulting JSON output should contain the following fields for each order:

OrderId
ReasonCode
Amount
Currency
ProcessorName
DeliveryDate
OrderDate
MerchantName
Address
ReasonCategory (calculated field)
AmountUSD (calculated field)
ProcessingDate (calculated field)
Input and Output Files
The input CSV file should be located in the "Inputs/{merchant_name}" directory under the root project directory. The output JSON files should be stored in the "Outputs/{merchant_name}" directory.

Example file paths:

Input path: /conversion_system/Inputs/MyShop/file1.csv
Converted Orders JSON file path: /conversion_system/Outputs/MyShop/file1.json
Converted Duplicate Orders JSON file path: /conversion_system/Outputs/MyShop/file1_duplicates.json
Getting Started
To run the conversion system, follow these steps:

Set up the required programming environment (choose any language).
Clone the project repository from GitHub.
Open the project in your preferred Integrated Development Environment (IDE).
Ensure that the required external libraries or dependencies are installed.
Configure the input and output file paths in the project's configuration files.
Build and run the application.
Provide the file path for conversion as a command-line argument.
The application will convert the file, calculate the fields, and save the output JSON files.
The output file paths will be displayed in the console or terminal.
Notes
The scope of this assignment includes three merchants (MyShop, MyBook, MyFlight) and two processors (VISA, AMEX).
The formatting of input and output fields should follow the provided guidelines.
You may use any programming language and external libraries as long as you implement the conversion system functionality.
Remember to iterate and incrementally add functionality as you
