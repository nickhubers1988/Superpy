# SuperPy

1. **Organized Code Sections for Simplicity:**
The code is split into smaller parts called functions, each doing a specific job like buying things, making reports, and dealing with dates. This method makes the code easier to understand and use again in the future. For example, the `buy_product` and `sell_product` functions handle buying and selling. This way, the code is easier to work with, making it less likely to make mistakes and helping everyone working on it to collaborate smoothly.

2. **Automatic Date Handling:**
The system can handle dates by itself using the `get_date` and `advance_time` functions. The `get_date` function checks a file to know what today's date is, even if you close and open the program. The `advance_time` function moves the date forward or backward by a certain number of days. This feature lets you see what might happen in the future and makes reports with the right dates. This makes it easy to check how things are going in different timeframes without needing to change things manually. You can find out how much money you've earned.

3. **Easy Commands with Clear Instructions:**
The system uses a tool called `argparse` to make it simple to use. It gives you a way to talk to the program without needing to know complicated knowledge. It's like talking to your computer in a special language. You can tell it what to do using words and it will understand. The different parts of the program (commands) have their own rules (arguments) that you can use. This way, you don't need to remember a lot of things. It's like having a helpful guide telling you what to do. In fact use the `--help` command to know what to do. This makes it easy to buy and sell things, get reports, and move time around. 
