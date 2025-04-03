import tkinter as tk
from tkinter import ttk, messagebox
import json

# Global dictionary to store transactions
transactions = {}

# Function to load transactions from JSON file
def load_transactions():
    try:
        with open('transactions.json', 'r') as file:
            global transactions
            transactions = json.load(file)
            return transactions
    except FileNotFoundError:
        return {}
def show_transactions():
    print("\nTransactions:")
    for reason, trans_list in transactions.items():
        for transaction in trans_list:
            print(f"Reason: {reason}, Amount: {transaction['amount']}, Date: {transaction['date']}")
    print()


# Function to save transactions to a JSON file
def save_transactions():
    with open('transactions.json', 'w') as file:
        file.write("{\n")
        for reason, trans_list in transactions.items():
            file.write(f'  "{reason}": [\n')
            for transaction in trans_list:
                file.write(f'    {{"amount": {transaction["amount"]}, "date": "{transaction["date"]}"}}')
                if transaction != trans_list[-1]:
                    file.write(",")
                file.write("\n")
            file.write("  ]\n")
            if reason != list(transactions.keys())[-1]:
                file.write(",")
            file.write("\n")
        file.write("}\n")

# Function to add a transaction
def add_transaction():
    while True:
        try:
            amount = int(input("Enter the amount: "))
        except ValueError:
            print("Invalid amount. Please enter a valid integer amount.")
        else:
            break
    
    reason = input("Enter the reason: ")
    if not reason:
        print("Reason cannot be empty.")
        return

    while True:
        date = input("Enter the date (YYYY-MM-DD): ")
        if len(date) != 10 or date[4] != "-" or date[7] != "-" or not date[:4].isdigit() or not date[5:7].isdigit() or not date[8:].isdigit():
            print("Invalid date format. Please enter the date in YYYY-MM-DD format.")
        else:
            break

    if reason not in transactions:
        transactions[reason] = []

    transactions[reason].append({"amount": int(amount), "date": date})
    print("Transaction added successfully.")
    save_transactions()

# Function to update a transaction
def update_transaction():
    show_transactions()
    print("Enter Details:")

    reason = input("Reason: ")
    if not reason:
        print("Reason cannot be empty.")
        return
    while True:
        try:
            index = int(input("Index: "))
        except ValueError:
            print("Invalid index. Please enter a valid integer index.")
        else:
            break
    while True:
        try:
            amount = int(input("New Amount: "))
        except ValueError:
            print("Invalid index. Please enter a valid integer index.")
        else:
            break
    while True:
        date = input("New date (YYYY-MM-DD): ")
        if len(date) != 10 or date[4] != "-" or date[7] != "-" or not date[:4].isdigit() or not date[5:7].isdigit() or not date[8:].isdigit():
            print("Invalid date format. Please enter the date in YYYY-MM-DD format.")
        else:
            break

    if reason in transactions and 0 <= index < len(transactions[reason]):
        transactions[reason][index]["amount"] = amount
        transactions[reason][index]["date"] = date
        save_transactions()
        print("Transaction updated successfully.")
    else:
        print("Invalid reason or index.")



# Function to delete a transaction
def delete_transaction():
    show_transactions()
    reason = input("Enter the reason to delete from: ")
    if not reason:
        print("Reason cannot be empty.")
        return
    while True:
        try:
            index = int(input("Enter the index of the transaction to delete: "))
        except ValueError:
            print("Invalid index. Please enter a valid integer index.")
        else:
            break

    if reason in transactions and 0 <= index < len(transactions[reason]):
        deleted_transaction = transactions[reason].pop(index)
        print("Transaction deleted successfully.")
        print("Deleted transaction:", deleted_transaction)
        if not transactions[reason]:  
            del transactions[reason]
        save_transactions()
    else:
        print("Invalid reasonn or index.")
# Function to display a summary of transactions
def display_summary():
    total_expense = sum(transaction['amount'] for reason, trans_list in transactions.items() for transaction in trans_list)
    print("\nSummary:")
    print(f"Total Expense: {total_expense}")

# Function to bulk load transactions
def bulk_load_transactions(filename):
    try:
        with open(filename, 'r') as file:
            global transactions
            
            new_transactions = {}
            
            for line in file:
                parts = line.strip().split(', ')
                
                if len(parts) == 3:
                    reason, amount, date = parts
                    amount = int(amount)
                    
                    if reason not in new_transactions:
                        new_transactions[reason] = []
                    
                    new_transactions[reason].append({"amount": amount, "date": date})
            
            for reason, trans_list in new_transactions.items():
                if reason not in transactions:
                    transactions[reason] = []
                
                transactions[reason].extend(trans_list)
            
            save_transactions()  
            print("Transactions loaded successfully.")
    except FileNotFoundError:
        print(f"File '{filename}' not found.") 

# Function to open Tkinter app based on JSON data
def view_transaction():
    root = tk.Tk()
    transactions = load_transactions()  
    app = TransactionTrackerApp(root, transactions)
    root.mainloop()

class TransactionTrackerApp:
    def __init__(self, root, transactions):
        self.root = root
        self.root.title("Personal Finance Transactions ")
        
        self.transactions = transactions

        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        ttk.Label(self.main_frame, text="Search Transaction:").grid(row=0, column=0, sticky=tk.W)
        self.search_entry = ttk.Entry(self.main_frame)
        self.search_entry.grid(row=0, column=1, sticky=tk.W)
        ttk.Button(self.main_frame, text="Search", command=self.search_transaction).grid(row=0, column=2, pady=5)

        ttk.Button(self.main_frame, text="Sort by Reason", command=self.sort_by_reason).grid(row=1, column=0, pady=5)
        ttk.Button(self.main_frame, text="Sort by Amount", command=self.sort_by_amount).grid(row=1, column=1, pady=5)
        ttk.Button(self.main_frame, text="Sort by Date", command=self.sort_by_date).grid(row=1, column=2, pady=5)

        self.display_transactions()

    def search_transaction(self):
        transaction_reason = self.search_entry.get().strip()

        if transaction_reason:
            if transaction_reason in self.transactions:
                filtered_transactions = {transaction_reason: self.transactions[transaction_reason]}
                self.display_transactions(filtered_transactions)
                messagebox.showinfo("Search Result", f"Transactions found for '{transaction_reason}'.")
            else:
                messagebox.showinfo("Search Result", f"No transactions found for '{transaction_reason}'.")
        else:
            messagebox.showerror("Error", "Please enter the reason for the transaction.")

    def sort_by_reason(self):
        sorted_transactions = dict(sorted(self.transactions.items()))
        self.display_transactions(sorted_transactions)

   
    def sort_by_amount(self):
        sorted_transactions = {k: sorted(v, key=lambda x: x['amount']) for k, v in self.transactions.items()}
        self.display_transactions(sorted_transactions)
     

    def sort_by_date(self):
        sorted_transactions = {k: sorted(v, key=lambda x: x['date']) for k, v in self.transactions.items()}
        self.display_transactions(sorted_transactions)

    def display_transactions(self, transactions=None):
        if not transactions:
            transactions = self.transactions

        tree = ttk.Treeview(self.main_frame, columns=("Reason", "Amount", "Date"), show="headings")
        tree.heading("Reason", text="Reason")
        tree.heading("Amount", text="Amount")
        tree.heading("Date", text="Date")
        
        for reason, transactions_list in transactions.items():
            for transaction in transactions_list:
                tree.insert("", "end", values=(reason, transaction["amount"], transaction["date"]))
        
        tree.grid(row=2, column=0, columnspan=3, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))

# Main menu function
def main_menu():
    load_transactions()  
    while True:
        print("\nPersonal Finance Tracker")
        print("1. Add Expense")
        print("2. View Transaction")
        print("3. Update Transaction")
        print("4. Delete Transaction")
        print("5. Display Summary")
        print("6. Bulk Load Transactions")
        print("7. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            add_transaction()
        elif choice == '2':
            view_transaction()  #open tickinter app
        elif choice == '3':
            update_transaction()
        elif choice == '4':
            delete_transaction()
        elif choice == '5':
            display_summary()
        elif choice == '6':
            filename = input("Enter the filename to bulk load transactions from: ")
            bulk_load_transactions(filename)
        elif choice == '7':
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()
