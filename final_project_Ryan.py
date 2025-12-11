
"""
Final Project: Expense Tracker
Student Name: Kyle Ryan

A simple expense tracker that lets a user:
- Add expenses
- View all expenses
- Compute total and average expenses
- Save/load expenses to/from a CSV file

Uses:
- variables, conditionals, loops, functions
- a list to store expenses and a simple Expense class
- file I/O for saving/loading 
- error handling with try/except
"""

import csv
from datetime import datetime


class Expense:
    def __init__(self, date, category, description, amount):
        self.date = date
        self.category = category
        self.description = description
        self.amount = amount

    def to_list(self):
        return [self.date, self.category, self.description, f"{self.amount:.2f}"]

    def __str__(self):
        return f"{self.date} | {self.category:12} | ${self.amount:8.2f} | {self.description}"


expenses = []

def add_expense():
    while True:
        try:
            date_in = input("Enter date (YYYY-MM-DD) or press Enter for today: ").strip()
            if date_in == "":
                date_in = datetime.today().strftime("%Y-%m-%d")
            else:
                datetime.strptime(date_in, "%Y-%m-%d")
            category = input("Enter category (e.g., Food, Transport, Bills): ").strip()
            if category == "":
                category = "Uncategorized"
            description = input("Enter a short description: ").strip()
            amount_str = input("Enter amount (e.g., 7.25): ").strip()
            amount = float(amount_str)
            if amount < 0:
                print("Amount cannot be negative. Try again.")
                continue
            exp = Expense(date_in, category, description, amount)
            expenses.append(exp)
            print("Expense added.")
            break
        except ValueError:
            print("Invalid input (date or amount). Please try again.")


def show_expenses():
    if not expenses:
        print("No expenses recorded.")
        return
    print("Date       | Category      |    Amount | Description")
    print("-" * 60)
    for e in expenses:
        print(e)
    print("-" * 60)
    print(f"Total expenses recorded: {len(expenses)}")

def compute_summary():
    if not expenses:
        print("No expenses to summarize.")
        return
    total = 0.0
    by_category = {}
    for e in expenses:
        total += e.amount
        by_category.setdefault(e.category, []).append(e.amount)
    average = total / len(expenses)
    print(f"Overall total: ${total:.2f}")
    print(f"Overall average (per entry): ${average:.2f}")
    print("\nBy category:")
    for cat, amounts in by_category.items():
        cat_total = sum(amounts)
        cat_avg = cat_total / len(amounts)
        print(f" - {cat:12}: total ${cat_total:8.2f} | avg ${cat_avg:8.2f} ({len(amounts)} items)")

def save_to_file(filename="expenses.csv"):
    try:
        with open(filename, "w", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["date", "category", "description", "amount"])
            for e in expenses:
                writer.writerow(e.to_list())
        print(f"Saved {len(expenses)} expenses to {filename}.")
    except Exception as ex:
        print(f"Error saving to file: {ex}")

def load_from_file(filename="expenses.csv"):
    try:
        with open(filename, "r", newline='', encoding="utf-8") as f:
            reader = csv.DictReader(f)
            loaded = 0
            for row in reader:
                try:
                    amount = float(row["amount"])
                    date_in = row.get("date", "").strip() or datetime.today().strftime("%Y-%m-%d")
                    category = row.get("category", "Uncategorized").strip()
                    description = row.get("description", "").strip()
                    expenses.append(Expense(date_in, category, description, amount))
                    loaded += 1
                except (ValueError, KeyError):
                   continue
        print(f"Loaded {loaded} expenses from {filename}.")
    except FileNotFoundError:
        print(f"No file named {filename} found.")
    except Exception as ex:
        print(f"Error loading from file: {ex}")

def main_menu():
    print("Welcome to the Expense Tracker!")
    print("Options:")
    while True:
        print("\nMenu:")
        print(" 1 - Add expense")
        print(" 2 - Show all expenses")
        print(" 3 - Compute totals/averages")
        print(" 4 - Save expenses to file")
        print(" 5 - Load expenses from file (append)")
        print(" 6 - Clear all expenses")
        print(" 0 - Quit")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            add_expense()
        elif choice == "2":
            show_expenses()
        elif choice == "3":
            compute_summary()
        elif choice == "4":
            fname = input("Enter filename to save (or press Enter for expenses.csv): ").strip() or "expenses.csv"
            save_to_file(fname)
        elif choice == "5":
            fname = input("Enter filename to load (or press Enter for expenses.csv): ").strip() or "expenses.csv"
            load_from_file(fname)
        elif choice == "6":
            confirm = input("Are you sure you want to clear all expenses? (yes/no): ").strip().lower()
            if confirm in ("yes", "y"):
                expenses.clear()
                print("All expenses cleared.")
            else:
                print("Clear canceled.")
        elif choice == "0":
            print("Goodbye! Remember to save your data if you want to keep it.")
            break
        else:
            print("Invalid option. Please enter a number from the menu.")

if __name__ == "__main__":
    main_menu()
