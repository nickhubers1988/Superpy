#Use of modules
import sys
import argparse
import csv
from texttable import Texttable
from datetime import timedelta, datetime
import datetime as dt
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, Paragraph

# Function to export data to a PDF
def export_to_pdf(bought_table, bought_price, sold_table, sold_price, profit_price, file_name):
    doc = SimpleDocTemplate(file_name, pagesize=letter)
    
    # Define column widths for the bought table
    col_width_bought = [15, 100, 100 , 100, 100]
    
    # Create tables with specified column widths
    bought_table = Table(bought_table, colWidths=col_width_bought)
    bought_price = Table(bought_price)
    sold_table = Table(sold_table, colWidths=[138])
    sold_price = Table(sold_price)
    profit_price = Table(profit_price, style=[('FONT', (0, 0), (-1, 0), 'Helvetica-Bold')])
    
    # Set styles for the tables
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])
    bought_table.setStyle(style)
    sold_table.setStyle(style)

    # Add elements to the PDF
    elements = [bought_table, Spacer(1, 12), bought_price, Spacer(1, 12), sold_table, Spacer(1, 12), sold_price, Spacer(1, 12), profit_price, Spacer(1, 12)]
    
    doc.build(elements)
# Function to create a CSV file for bought items if it doesn't exist
def create_inventory_file():
    if not os.path.exists('bought.csv'):
        with open('bought.csv', mode='w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)            
            csv_writer.writerow(['id', 'product_name', 'buy_date', 'price', 'expiration_date'])

# Function to retrieve inventory data from the CSV file    
def get_inventory():
    create_inventory_file()
    
    with open('bought.csv', mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        all_rows = []
        for row in csv_reader:
            all_rows.append(row)
    return all_rows

# Function to validate a date
def validate_date(date_string):
   try:
      datetime.strptime(date_string, '%Y-%m-%d')
      return True
   except ValueError:
      sys.stdout.write("Invalid expiration date. It must be formatted like YYYY-MM-DD")
      return False

# Function to get the current date from a text file
def get_date():
    try:
        with open("current_date.txt", "r") as file:
            file_contents = file.read()
    except FileNotFoundError:
        current_date = dt.datetime.now().strftime("%Y-%m-%d")
        with open("current_date.txt", "w") as file:
            file.write(current_date)
        file_contents = current_date
    
    return file_contents

# Function to record a purchased product in the inventory CSV file
def buy_product(id, product_name, price, expiry, buy_date):
   create_inventory_file()
   with open('bought.csv', mode='a', newline='') as file:
       formatted_product_price = "€{:.2f}".format(float(price))
       writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
       writer.writerow([id, product_name, buy_date, float(price), expiry])
   sys.stdout.write(f"You've bought {product_name} for {formatted_product_price}")

# Function to record a sold product in the sold CSV file
def sell_product(id, product_name, product_price, inventory, current_date):
   product = None
   for item in inventory:
      if item[1] == product_name:
         product = item

   if product == None:
      sys.stdout.write("ERROR: Product not in stock")
   else:
      if not os.path.exists('sold.csv'):
         with open('sold.csv', mode='w', newline='') as file:
            writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(['id', 'bought_id', 'sell_date', 'sell_price'])
      
      # Record the sale information in the sold CSV file
      # Use of external text files (CSV) to read and write data 
      with open('sold.csv', mode='a', newline='') as file:
       formatted_product_price = "€{:.2f}".format(float(product_price))
       writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
       writer.writerow([id, product[0], current_date, float(product_price)])
       sys.stdout.write(f"You've sold {product[1]} for {formatted_product_price}")


# Function to generate an inventory report for a specific date
def report_inventory(current_date, inventory, day):
    inventory_to_display = []
    
    if day == "--yesterday":
        dt = datetime.strptime(current_date, '%Y-%m-%d')
        yesterday = dt - timedelta(days=1)
        current_date = yesterday.strftime('%Y-%m-%d')
    elif day != current_date:  
        current_date = day
        
    for item in inventory:        
        if item[2] == current_date:
         product_price = "€{:.2f}".format(float(item[3]))
         inventory_to_display.append([item[0], item[1], item[2], product_price, item[4]])
    
    if len(inventory_to_display) == 0:
        sys.stdout.write("Product not found in the inventory for the specified date.")
    else:
        t = Texttable()
        formatted_data = [['id', 'Product', 'Date purchased', 'Buy Price', 'Expiration date']] + inventory_to_display
        
        t.add_rows(formatted_data)
        sys.stdout.write(t.draw())

# Function to advance the current date by a specified number of days 
def advance_time(days_to_increase):
   current_date = get_date()
   dt = datetime.strptime(current_date, '%Y-%m-%d')
   yesterday = dt + timedelta(days = days_to_increase)
   current_date = yesterday.strftime('%Y-%m-%d')
   
   file = open("current_date.txt", "w")
   file.write(current_date)
   file.close()
   sys.stdout.write(f"Date is now set to: {current_date}")

# Function to generate a revenue and profit report
def report_revenue_profit(report_date, current_date):
    revenue = 0
    bought = 0
    profit = 0
    is_period = None
    inventory_report = []
    sold_report =[]
    sold_report_table = []
    bought_total_report = []
    sold_total_report = []
    inventory_report_pdf =[]
    profit_total_report = []
    
    # Determine the reporting period based on the given report_date
    if report_date == "yesterday":
        current_date = get_date()
        dt = datetime.strptime(current_date, '%Y-%m-%d')
        days_to_increase = 1 
        yesterday = dt - timedelta(days=days_to_increase)
        current_date = yesterday.strftime('%Y-%m-%d')
        
    elif report_date == "today":
        report_date = current_date

    # Calculate revenue from sold products     
    with open('sold.csv', mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            sold_report.append(row)
            if row[2] >= report_date[0] and row[2] <= report_date[1]:
                revenue += float(row[-1])
                is_period = True
            elif row[2] == current_date:
               revenue += float(row[-1])
               is_period = False
    
    # Calculate profit based on bought products   
    with open('bought.csv', mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            #print(row[2])
            if row[2] >= report_date[0] and row[2] <= report_date[1]:                
                bought += float(row[-2])
                is_period = True
            elif row[2] == current_date:               
               row[2] == current_date
               bought += float(row[-2])               
               is_period = False

        profit = revenue - bought

    bought = "€ {:.2f}".format(float(bought))
    formatted_revenue = "€ {:.2f}".format(revenue) 
    formatted_profit = "€ {:.2f}".format(profit) 

     # Generate and display revenue and profit reports
    if is_period:
        sys.stdout.write(f"Revenue for {report_date[0]} to {report_date[1]}: {formatted_revenue}\n" 
        f"Profit for {report_date[0]} to {report_date[1]}: {formatted_profit}")
    else:        
        sys.stdout.write(f"Revenue for {current_date}: {formatted_revenue}\n"
                         f"Profit for {current_date}: {formatted_profit}" )    
    
    # Create revenue and profit report within the specified date range
    if isinstance(report_date, list):
      inventory_report = get_inventory()
      
      for item in inventory_report:
         
         if item[2] >= report_date[0] and item[2] <= report_date[1]:
            
            product_price = "€ {:.2f}".format(float(item[3]))
            inventory_report_pdf.append([item[0], item[1], item[2], product_price, item[4]])

      # Generate sold report table  
      for item in sold_report:
         
         if item[2] >= report_date[0] and item[2] <= report_date[1]:
            
            product_price = "€ {:.2f}".format(float(item[3]))
            sold_report_table.append([item[1], item[2], product_price])      
      
      # Prepare formatted tables for the revenue and profit report
      formatted_report_bought_table = [['id', 'Product', 'Date of purchase', 'Price', 'Expiration date']] + inventory_report_pdf
      formatted_report_sold_table = [['Product ID', 'Sold date', 'Price']] + sold_report_table
      
      # Append total buy, sold, and profit data
      bought_total_report.append(['Total buy price', bought])
      sold_total_report.append(['Total sold price', formatted_revenue])
      profit_total_report.append(['Total profit', formatted_profit])

      # Generate the report filename and PDF Report    
      file_name = f"Revenue and profit report {report_date[0]} to {report_date[1]}.pdf"
      export_to_pdf(formatted_report_bought_table,bought_total_report, formatted_report_sold_table, sold_total_report, profit_total_report, file_name)      
      print(f'\nRevenue and profit report created, named as {file_name}')
    
    # Create revenue and profit report for today or yesterday
    else:
        inventory_report = get_inventory()
        inventory_report_pdf =[]        
        for item in inventory_report:
            
            if item[2] == current_date:
                
                product_price = "€ {:.2f}".format(float(item[3]))
                inventory_report_pdf.append([item[0], item[1], item[2], product_price, item[4]])
        
        for item in sold_report:
         
         if item[2] == current_date:
            
            product_price = "€ {:.2f}".format(float(item[3]))
            sold_report_table.append([item[1], item[2], product_price])

        formatted_report_bought_table = [['id', 'Product', 'Date of purchase', 'Price', 'Expiration date']] + inventory_report_pdf
        formatted_report_sold_table = [['Product ID', 'Sold date', 'Price']] + sold_report_table
        
        bought_total_report.append(['Total buy price', bought])
        sold_total_report.append(['Total sold price', formatted_revenue])
        profit_total_report.append(['Total profit', formatted_profit])
        file_name = f"Revenue and profit report {current_date}.pdf"
        export_to_pdf(formatted_report_bought_table,bought_total_report, formatted_report_sold_table, sold_total_report, profit_total_report, file_name)
      
        print(f'\nRevenue and profit report created, named as {file_name}')

def main():
    # Setting and advancing the date that the application perceives as 'today'
    
    current_date = get_date()
    inventory = get_inventory()
    try:
        last_item_id = int(inventory[-1][0])
    except ValueError:
        last_item_id = 1

    # A well-structured and user-friendly command-line interface with clear descriptions of each argument in the --help section.  
    parser = argparse.ArgumentParser(description="Manage inventory and generate reports.")
    subparsers = parser.add_subparsers(dest="command", title="Available commands")

    # Buy command
    buy_parser = subparsers.add_parser("buy", help="Add a new item to the inventory.")
    buy_parser.add_argument("product_name", type=str, help="Name of the product.")
    buy_parser.add_argument("price", type=float, help="Price of the product.")
    buy_parser.add_argument("expiry_date", type=str, help="Expiry date of the product. Formatted as yyyy-mm-dd")
    
    # Report command
    report_parser = subparsers.add_parser("report", help="Generate reports from the inventory.")
    report_subparsers = report_parser.add_subparsers(dest="report_type", title="Report types")
    
    # Inventory report
    # inventory python main.py report inventory <date: specific date>
    # e.g. Today's inventory python main.py report inventory
    # e.g. Specific date inventory python main.py report inventory --date 2023-08-06
    inventory_parser = report_subparsers.add_parser("inventory", help="Generate inventory report.")
    inventory_parser.add_argument("--date", type=str, nargs="?", default=current_date, help="Date for the inventory report. Formatted as yyyy-mm-dd (default: current date)")
    
    # Revenue report
    # main.py report revenue --date <date: start date range date: eind date range>
    # e.g. Data range main.py report revenue --date 2023-08-01 2023-08-07
    revenue_parser = report_subparsers.add_parser("revenue", help="Generate revenue report.")
    revenue_parser.add_argument("--date", nargs=2, metavar=("start_date", "end_date"), help="Date range for the revenue profit report. Formatted as yyyy-mm-dd")
    # e.g. Today's report python main.py report revenue today
    # e.g. Yesterday's report python main.py report revenue yesterday
    revenue_parser.add_argument("today", type=str, nargs="?", help="Today's report")

    # Sell command
    # python main.py sell <str: product name> <int: sell price>
    # e.g. Sell main.py sell "Product A" 3.45
    sell_parser = subparsers.add_parser("sell", help="Sell an item from the inventory.")
    sell_parser.add_argument("product_name", type=str, help="Name of the product to sell.")
    sell_parser.add_argument("product_price", type=float, help="Price at which the product is sold.")
    
    # Advance time command
    # python main.py --advance-time <int: days>
    # e.g. One week in the future python main.py --advance-time 7
    # e.g. One week in the past python main.py --advance-time -7
    advance_time_parser = subparsers.add_parser("advance-time", help="Advance the current date by a specified number of days.")
    advance_time_parser.add_argument("days", type=int, help="Number of days to advance the current date. Minus is past and Plus is future")
    
    args = parser.parse_args()
    
    # Recording the buying and selling of products on certain dates
    if args.command == "buy":
        product_name = args.product_name
        price = args.price
        expiry = args.expiry_date
        buy_date = current_date
        if validate_date(expiry):
            buy_product(last_item_id + 1, product_name, price, expiry, buy_date)

    # Reporting inventory on specific day
    elif args.command == "report":
        if args.report_type == "inventory":
            day = args.date            
            report_inventory(current_date, inventory, day)
        
        # Reporting revenue and profit over specified time periods;
        elif args.report_type == "revenue":
            
            if args.date:                
                start_date, end_date = args.date                
                report_revenue_profit([start_date, end_date], current_date)
            elif args.today:
                report_revenue_profit(args.today, current_date)
            
    # Recording the buying and selling of products on certain dates
    elif args.command == "sell":
        product_name = args.product_name
        product_price = args.product_price
        sell_product(last_item_id, product_name, product_price, inventory, current_date)
    # Change the systemdate by days
    elif args.command == "advance-time":
        advance_time(int(args.days))

if __name__ == "__main__":
    
    main()