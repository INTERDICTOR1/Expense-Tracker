import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import json
from datetime import date

class FinanceTracker:
    def __init__(self, master):
        self.master = master
        master.title("Finance Tracker")
        master.configure(bg="#2E4053")

        self.style = ttk.Style()
        self.style.configure("TLabel", background="#2E4053", foreground="white", font=("Helvetica", 10))
        self.style.configure("TButton", background="#1ABC9C", font=("Helvetica", 10, "bold"))

        self.load_data()

        # Account Value
        ttk.Label(master, text="Account Value:").grid(row=0, column=0, sticky="e", padx=10, pady=5)
        self.account_value = ttk.Entry(master)
        self.account_value.grid(row=0, column=1, padx=10, pady=5)
        self.account_value.insert(0, str(self.data['account_value']))

        # Monthly EMI
        ttk.Label(master, text="Monthly EMI:").grid(row=1, column=0, sticky="e", padx=10, pady=5)
        self.monthly_emi = ttk.Entry(master)
        self.monthly_emi.grid(row=1, column=1, padx=10, pady=5)
        self.monthly_emi.insert(0, str(self.data['monthly_emi']))

        # Savings
        ttk.Label(master, text="Savings:").grid(row=2, column=0, sticky="e", padx=10, pady=5)
        self.savings = ttk.Entry(master)
        self.savings.grid(row=2, column=1, padx=10, pady=5)
        self.savings.insert(0, str(self.data['savings']))

        # Investments
        ttk.Label(master, text="Investments:").grid(row=3, column=0, sticky="e", padx=10, pady=5)
        self.investments = ttk.Entry(master)
        self.investments.grid(row=3, column=1, padx=10, pady=5)
        self.investments.insert(0, str(self.data['investments']))

        # Update Button
        self.update_button = ttk.Button(master, text="Update", command=self.update_values)
        self.update_button.grid(row=4, column=0, columnspan=2, pady=10)

        # Results
        self.results_text = tk.Text(master, height=5, width=40, bg="#34495E", fg="white", font=("Helvetica", 10))
        self.results_text.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

        self.calculate_and_display()

    def load_data(self):
        try:
            with open('finance_data.json', 'r') as f:
                self.data = json.load(f)
        except FileNotFoundError:
            self.data = {
                'account_value': 0,
                'monthly_emi': 0,
                'savings': 0,
                'investments': 0,
                'last_update': str(date.today())
            }

    def save_data(self):
        with open('finance_data.json', 'w') as f:
            json.dump(self.data, f)

    def update_values(self):
        try:
            self.data['account_value'] = float(self.account_value.get())
            self.data['monthly_emi'] = float(self.monthly_emi.get())
            self.data['savings'] = float(self.savings.get())
            self.data['investments'] = float(self.investments.get())
            self.data['last_update'] = str(date.today())
            self.save_data()
            self.calculate_and_display()
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers.")

    def calculate_and_display(self):
        account_value = self.data['account_value']
        monthly_emi = self.data['monthly_emi']
        savings = self.data['savings']
        investments = self.data['investments']

        remaining_money = account_value - monthly_emi - savings - investments
        daily_burn_rate = remaining_money / 30  # Assuming 30 days in a month

        result = f"Remaining Money: ₹{remaining_money:.2f}\n"
        result += f"Daily Burn Rate: ₹{daily_burn_rate:.2f}\n"
        result += f"Last Updated: {self.data['last_update']}"

        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, result)

root = tk.Tk()
finance_tracker = FinanceTracker(root)
root.mainloop()
