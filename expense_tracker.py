# expense_tracker.py
# Personal Expense Tracker (simple, file-persistent JSON storage)

import json
from datetime import datetime
from collections import defaultdict
import os

DATA_FILE = "expenses.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_data(expenses):
    with open(DATA_FILE, "w") as f:
        json.dump(expenses, f, indent=2)

def add_expense(expenses):
    print("\n--- Add Expense ---")
    try:
        amount = float(input("Amount (e.g. 50.0): ").strip())
    except ValueError:
        print("Invalid amount. Try again.")
        return
    category = input("Category (Food, Transport, Entertainment, etc.): ").strip() or "Other"
    date_str = input("Date (YYYY-MM-DD) [leave blank for today]: ").strip()
    if not date_str:
        date = datetime.today().strftime("%Y-%m-%d")
    else:
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            date = date_str
        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD.")
            return
    note = input("Note (optional): ").strip()

    record = {
        "amount": amount,
        "category": category,
        "date": date,
        "note": note
    }
    expenses.append(record)
    save_data(expenses)
    print("Expense saved.")

def view_summary(expenses):
    if not expenses:
        print("\nNo expenses recorded yet.")
        return
    print("\n--- Summaries ---")
    # Total overall
    total = sum(e["amount"] for e in expenses)
    print(f"Total overall spending: {total:.2f}")

    # By category
    by_cat = defaultdict(float)
    for e in expenses:
        by_cat[e["category"]] += e["amount"]
    print("\nSpending by category:")
    for cat, amt in sorted(by_cat.items(), key=lambda x: -x[1]):
        print(f"  {cat}: {amt:.2f}")

    # Spending over time: group by month (YYYY-MM)
    by_month = defaultdict(float)
    for e in expenses:
        month = e["date"][:7]  # YYYY-MM
        by_month[month] += e["amount"]
    print("\nSpending by month:")
    for m, amt in sorted(by_month.items()):
        print(f"  {m}: {amt:.2f}")

    # Show last 10 records
    print("\nLast 10 records:")
    for r in expenses[-10:]:
        print(f"  {r['date']} | {r['category']} | {r['amount']:.2f} | {r.get('note','')}")

def delete_or_edit(expenses):
    if not expenses:
        print("\nNo records to edit/delete.")
        return
    print("\n--- Edit / Delete ---")
    for i, e in enumerate(expenses, 1):
        print(f"{i}. {e['date']} | {e['category']} | {e['amount']:.2f} | {e.get('note','')}")
    choice = input("Enter record number to edit/delete (or blank to cancel): ").strip()
    if not choice:
        return
    try:
        idx = int(choice) - 1
        if idx < 0 or idx >= len(expenses):
            print("Invalid number.")
            return
    except ValueError:
        print("Invalid input.")
        return

    rec = expenses[idx]
    action = input("Type 'd' to delete or 'e' to edit: ").strip().lower()
    if action == 'd':
        expenses.pop(idx)
        save_data(expenses)
        print("Record deleted.")
    elif action == 'e':
        print("Leave blank to keep current value.")
        new_amount = input(f"Amount [{rec['amount']}]: ").strip()
        if new_amount:
            try:
                rec['amount'] = float(new_amount)
            except ValueError:
                print("Invalid amount; keeping old value.")
        new_cat = input(f"Category [{rec['category']}]: ").strip()
        if new_cat:
            rec['category'] = new_cat
        new_date = input(f"Date [{rec['date']}]: ").strip()
        if new_date:
            try:
                datetime.strptime(new_date, "%Y-%m-%d")
                rec['date'] = new_date
            except ValueError:
                print("Invalid date; keeping old.")
        new_note = input(f"Note [{rec.get('note','')}]: ").strip()
        if new_note:
            rec['note'] = new_note
        save_data(expenses)
        print("Record updated.")
    else:
        print("Cancelled.")

def main_menu():
    expenses = load_data()
    while True:
        print("\n=== Personal Expense Tracker ===")
        print("1. Add an expense")
        print("2. View summaries")
        print("3. Edit / Delete record")
        print("4. Exit")
        choice = input("Choose (1-4): ").strip()
        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            view_summary(expenses)
        elif choice == "3":
            delete_or_edit(expenses)
        elif choice == "4":
            print("Goodbye.")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main_menu()
