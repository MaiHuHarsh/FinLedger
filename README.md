
# 📋 Expense Tracker CLI

A Command Line Interface (CLI) tool to track and manage your daily expenses directly from your terminal.

With this tool, you can:

✅ Add new expenses
📋 List all or specific types of expenses
📝 Update expense details
🗑️ Delete expenses
💰 Set and track your monthly budget
📊 Generate detailed expense summaries
📈 View spending trends

## 📁 File Structure

```
.
├── expense_tracker.py    # Main Python script for the Expense Tracker CLI tool
└── expenses.json         # JSON file where all expenses and budget details are stored (created automatically)
```

## ⚙️ How to Use

▶️ Run the Script

```bash
python expense_tracker.py <command> [arguments]
```

Make sure you have Python installed and run the command from the same directory where `expense_tracker.py` is located.

## 🛠️ Available Commands

| Command            | Example Command                                         | Description                                                          |
| ------------------ | ------------------------------------------------------- | -------------------------------------------------------------------- |
| `add`              | `python expense_tracker.py add`                         | Add a new expense                                                    |
| `list`             | `python expense_tracker.py list`                        | List all expenses or filter by category                              |
| `delete`           | `python expense_tracker.py delete <id>`                 | Delete an expense by its ID                                          |
| `summary`          | `python expense_tracker.py summary`                     | View a summary of expenses (with optional filters by month/category) |
| `set-budget`       | `python expense_tracker.py set-budget <month> <amount>` | Set a budget for a specific month                                    |
| `category-report`  | `python expense_tracker.py category-report`             | View an expense report broken down by category                       |
| `spending-trend`   | `python expense_tracker.py spending-trend`              | View spending trends over months                                     |
| `detailed-summary` | `python expense_tracker.py detailed-summary`            | View a detailed summary of expenses, including budget comparisons    |
| `--help` or `-h`   | `python expense_tracker.py --help`                      | Show available commands                                              |

## 🗂️ Example Usage

### Add an Expense

```bash
python expense_tracker.py add "Lunch" 10.50 "Food"
```

### List All Expenses

```bash
python expense_tracker.py list
```

### List Expenses by Category

```bash
python expense_tracker.py list "Food"
```

### Delete an Expense

```bash
python expense_tracker.py delete 1
```

### Set a Budget for a Month

```bash
python expense_tracker.py set-budget 01 500
```

### View a Spending Trend

```bash
python expense_tracker.py spending-trend
```

### View Detailed Summary

```bash
python expense_tracker.py detailed-summary
```

## 🧠 How It Works

All expenses are stored in a file called `expenses.json`.
Each expense has:

* **id**: A unique identifier for the expense.
* **date**: The date of the expense (formatted as YYYY-MM-DD).
* **description**: A brief description of the expense.
* **amount**: The monetary value of the expense.
* **category**: The category of the expense (e.g., Food, Transport, Utilities).
* **month**: The 2-digit month number when the expense was added.

Budgets are also stored in `expenses.json` and can be set for each month.

## 📌 Requirements

* Python 3.x (No external libraries needed)

## 💡 Features You Can Add Later (Suggestions)

✅ Expense categorization with priority levels (e.g., High, Medium, Low)
⏰ Set due dates for expenses
🔁 Recurring expense options
🔍 Search/filter by description or amount
🌈 Enhanced terminal output with colors for better visibility

## 🙌 Author

**Lakshit Verma**
Beginner Python Developer 🌱
Made with ❤️ and curiosity

---
## Project URL
```
https://roadmap.sh/projects/expense-tracker
```
