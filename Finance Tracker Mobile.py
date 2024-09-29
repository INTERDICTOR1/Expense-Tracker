from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.storage.jsonstore import JsonStore
from kivy.uix.scrollview import ScrollView
from datetime import date
from kivy.uix.spinner import Spinner
import pyrebase
from kivy.uix.checkbox import CheckBox
from kivy.uix.gridlayout import GridLayout
import matplotlib.pyplot as plt
from kivy.garden.matplotlib import FigureCanvasKivyAgg
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure


# Firebase Configuration
config = {
    "apiKey": "your API key",
    "authDomain": "fintrack-d6c2e.firebaseapp.com",
    "databaseURL": "https://fintrack-d6c2e.firebaseio.com",
    "projectId": "fintrack-d6c2e",
    "storageBucket": "fintrack-d6c2e.appspot.com",
    "messagingSenderId": "577713094426",
    "appId": "1:577713094426:web:06750f5238558a3781f6a3",
    "measurementId": "G-2EHLWH9PZ9"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()


class WelcomeScreen(Screen):
    def __init__(self, **kwargs):
        super(WelcomeScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        new_user_button = Button(text="New User", on_press=self.go_to_registration)
        existing_user_button = Button(text="Existing User", on_press=self.go_to_login)
        layout.add_widget(new_user_button)
        layout.add_widget(existing_user_button)
        self.add_widget(layout)

    def go_to_registration(self, instance):
        self.manager.current = 'registration'

    def go_to_login(self, instance):
        self.manager.current = 'login'

class RegistrationScreen(Screen):
    def __init__(self, **kwargs):
        super(RegistrationScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.email_input = TextInput(hint_text="Email", size_hint_y=None, height=40)
        self.password_input = TextInput(hint_text="Password", password=True, size_hint_y=None, height=40)
        register_button = Button(text="Register", on_press=self.register_user, size_hint_y=None, height=40)
        self.message_label = Label(size_hint_y=None, height=40)

        # Add back button
        back_button = Button(text="Back", on_press=self.go_back, size_hint_y=None, height=40)

        # Add widgets to layout
        layout.add_widget(self.email_input)
        layout.add_widget(self.password_input)
        layout.add_widget(register_button)
        layout.add_widget(back_button)
        layout.add_widget(self.message_label)
        self.add_widget(layout)

    def register_user(self, instance):
        email = self.email_input.text
        password = self.password_input.text
        try:
            auth.create_user_with_email_and_password(email, password)
            self.manager.current = 'login'
        except Exception as e:
            self.message_label.text = f"Registration Failed! {str(e)}"

    def go_back(self, instance):
        self.manager.current = 'welcome'

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.email_input = TextInput(hint_text="Email", size_hint_y=None, height=40)
        self.password_input = TextInput(hint_text="Password", password=True, size_hint_y=None, height=40)
        login_button = Button(text="Login", on_press=self.login_user, size_hint_y=None, height=40)
        back_button = Button(text="Back", on_press=self.go_back, size_hint_y=None, height=40)
        self.message_label = Label(size_hint_y=None, height=40)

        # Adding widgets to the layout
        layout.add_widget(self.email_input)
        layout.add_widget(self.password_input)
        layout.add_widget(login_button)
        layout.add_widget(back_button)
        layout.add_widget(self.message_label)
        self.add_widget(layout)

    def login_user(self, instance):
        email = self.email_input.text
        password = self.password_input.text
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            self.manager.current = 'finance_tracker'
            self.manager.get_screen('finance_tracker').set_user(user['localId'])
        except Exception as e:
            self.message_label.text = f"Login Failed! {str(e)}"

    def go_back(self, instance):
        self.manager.current = 'welcome'

class FinanceTrackerScreen(Screen):
    def __init__(self, **kwargs):
        super(FinanceTrackerScreen, self).__init__(**kwargs)
        self.store = JsonStore('finance_data.json')
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.add_widget(self.layout)

    def set_user(self, user_id):
        self.user_id = user_id
        self.load_data()
        self.build_ui()

    def build_ui(self):
        # Clear previous widgets
        self.layout.clear_widgets()

        # Account Value
        self.layout.add_widget(Label(text="Account Value:"))
        self.account_value = TextInput(text=str(self.data['account_value']), multiline=False)
        self.layout.add_widget(self.account_value)

        # Monthly EMI
        self.layout.add_widget(Label(text="Monthly EMI:"))
        self.monthly_emi = TextInput(text=str(self.data['monthly_emi']), multiline=False)
        self.layout.add_widget(self.monthly_emi)

        # Savings
        self.layout.add_widget(Label(text="Savings:"))
        self.savings = TextInput(text=str(self.data['savings']), multiline=False)
        self.layout.add_widget(self.savings)

        # Investments
        self.layout.add_widget(Label(text="Investments:"))
        self.investments = TextInput(text=str(self.data['investments']), multiline=False)
        self.layout.add_widget(self.investments)

        # Expense Category
        self.layout.add_widget(Label(text="Expense Category:"))
        self.category_spinner = Spinner(
            text='Select Category',
            values=('Food', 'Transport', 'Entertainment', 'Utilities', 'Other'),
            size_hint_y=None,
            height=44
        )
        self.layout.add_widget(self.category_spinner)

        # Expense Amount
        self.layout.add_widget(Label(text="Expense Amount:"))
        self.expense_amount = TextInput(text='', multiline=False)
        self.layout.add_widget(self.expense_amount)

        # Add Expense Button
        add_expense_button = Button(text="Add Expense", on_press=self.add_expense)
        self.layout.add_widget(add_expense_button)

        # Update Button
        update_button = Button(text="Update", on_press=self.update_values)
        self.layout.add_widget(update_button)

        # Results
        self.results_label = Label(size_hint_y=None, height=100)
        results_scroll = ScrollView(size_hint=(1, None), height=100)
        results_scroll.add_widget(self.results_label)
        self.layout.add_widget(results_scroll)

        self.calculate_and_display()

    def load_data(self):
        # Load user-specific data
        if self.store.exists(f'data_{self.user_id}'):
            self.data = self.store.get(f'data_{self.user_id}')
        else:
            self.data = {
                'account_value': 0,
                'monthly_emi': 0,
                'savings': 0,
                'investments': 0,
                'expenses': [],
                'last_update': str(date.today())
            }
        # Ensure 'expenses' key exists
        if 'expenses' not in self.data:
            self.data['expenses'] = []

    def save_data(self):
        self.store.put(f'data_{self.user_id}', **self.data)

    def add_expense(self, instance):
        try:
            category = self.category_spinner.text
            amount = float(self.expense_amount.text)
            if category != 'Select Category' and amount > 0:
                self.data['expenses'].append({'category': category, 'amount': amount})
                self.save_data()
                self.calculate_and_display()
            else:
                self.results_label.text = "Please select a category and enter a valid amount."
        except ValueError:
            self.results_label.text = "Please enter a valid expense amount."

    def update_values(self, instance):
        try:
            self.data['account_value'] = float(self.account_value.text)
            self.data['monthly_emi'] = float(self.monthly_emi.text)
            self.data['savings'] = float(self.savings.text)
            self.data['investments'] = float(self.investments.text)
            self.data['last_update'] = str(date.today())
            self.save_data()
            self.calculate_and_display()
        except ValueError:
            self.results_label.text = "Please enter valid numbers."

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

        # Plot Expenses
        if self.data['expenses']:
            categories = [e['category'] for e in self.data['expenses']]
            amounts = [e['amount'] for e in self.data['expenses']]
            fig, ax = plt.subplots()
            ax.pie(amounts, labels=categories, autopct='%1.1f%%')
            ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

            # Display the plot in Kivy
            if hasattr(self, 'figure_canvas'):
                self.layout.remove_widget(self.figure_canvas)
            self.figure_canvas = FigureCanvasKivyAgg(fig)
            self.results_label.text += "\n\nExpense Distribution:"
            self.layout.add_widget(self.figure_canvas)

        self.results_label.text += "\n\n" + result

class FinanceApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(WelcomeScreen(name='welcome'))
        sm.add_widget(RegistrationScreen(name='registration'))
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(FinanceTrackerScreen(name='finance_tracker'))
        return sm

if __name__ == '__main__':
    FinanceApp().run()
