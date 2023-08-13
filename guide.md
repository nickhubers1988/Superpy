**Inventory Management and Reporting System Usage Guide**
Welcome to the Inventory Management and Reporting System! This guide will help you understand how to use the system's features effectively. The system allows you to manage your product inventory, generate reports, and simulate different scenarios using a simple command-line interface.

### Buying Products
To add new items to your inventory, use the `buy` command followed by the product name, price, and expiry date in the format `YYYY-MM-DD`.
Example:
```bash
python main.py buy "Product A" 10.99 2023-08-31
```
### Selling Products
Record the sale of items from your inventory using the `sell` command. Provide the product name and the selling price.
Example:
```bash
python main.py sell "Product A" 15.49
```
### Generating Inventory Reports
Generate an inventory report for a specific date using the `report inventory` command. Use the `--date` option to specify the desired date in the format `YYYY-MM-DD`.
Example:
```bash
python main.py report inventory --date 2023-08-12
```
### Generating Revenue and Profit Reports
Generate revenue and profit reports using the `report revenue` command. You can specify a date range or use `today` or `yesterday` for specific days.
Example (Date Range):
```bash
python main.py report revenue --date 2023-08-01 2023-08-10
```
Example (Today's Report):
```bash
python main.py report revenue today
```
Example (Yesterday's Report):
```bash
python main.py report revenue yesterday
```
### Advancing Time
Simulate scenarios by changing the system date using the `advance-time` command. Provide the number of days to advance (or go back in time) as an argument.
Example (Advance Time by 7 days):
```bash
python main.py advance-time 7
```
Example (Go Back in Time by 3 days):
```bash
python main.py advance-time -3
```
Remember to follow the specified date format (YYYY-MM-DD) for inputting dates.

### Trouble shooting
For detailed information about each command and its options, you can use the `--help` option with any command.
Example:
```bash
python main.py buy --help
python main.py report --help
python main.py sell --help
python main.py advance-time --help
```

Feel free to experiment with the system and discover its full potential in managing your inventory and generating reports!