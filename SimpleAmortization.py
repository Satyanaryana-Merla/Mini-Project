import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Function to calculate monthly payment
def calculate_monthly_payment(loan_amount, annual_rate, term_months):
    monthly_rate = annual_rate / 12
    # Loan amortization formula for monthly payment
    if monthly_rate == 0:  # Handle case of zero interest rate
        return loan_amount / term_months
    else:
        return loan_amount * (monthly_rate * (1 + monthly_rate) ** term_months) / ((1 + monthly_rate) ** term_months - 1)

# Helper function to calculate SMM (Single Monthly Mortality)
def calculate_smm(cpr):
    return 1 - (1 - cpr) ** (1 / 12)

# Function to generate amortization schedule for each loan
def generate_amortization_schedule(loan):
    # Parameters
    loan_amount = loan['loan_amount']
    annual_rate = loan['annual_rate']
    start_date = datetime.strptime(loan['start_date'], "%d-%m-%Y")
    term_months = loan['term_months']
    monthly_payment = loan['payment']
    cpr = loan['cpr']
    
    # Monthly interest rate
    monthly_rate = annual_rate / 12
    smm = calculate_smm(cpr)
    
    # DataFrame to store the amortization schedule
    schedule = []
    
    # Initial values
    opening_balance = loan_amount
    period = 0
    
    # Generate schedule until the loan balance reaches 0
    while opening_balance > 0:
        period += 1
        
        # Calculate Interest
        interest = opening_balance * monthly_rate
        
        # Calculate Prepayment based on CPR
        prepayment = opening_balance * smm
        
        # Calculate Principal
        principal = monthly_payment + prepayment - interest
        
        # Calculate Closing Balance
        closing_balance = max(0, opening_balance - principal)
        
        # Add data for the current period to the schedule
        schedule.append({
            'period': period,
            'date': (start_date + timedelta(days=30 * (period - 1))).strftime('%d-%m-%Y'),  # No time, just date
            'opening_balance': round(opening_balance, 2),
            'payment': round(monthly_payment, 2),
            'prepayment': round(prepayment, 2),
            'interest_rate': f"{annual_rate * 100:.2f}%",  # Interest rate as percentage (e.g., 8%)
            'monthly_interest_rate': f"{monthly_rate * 100:.2f}%",  # Monthly rate as percentage (e.g., 0.67%)
            'interest': round(interest, 2),
            'principal': round(principal, 2),
            'closing_balance': round(closing_balance, 2)
        })
        
        # Update opening balance for the next period
        opening_balance = closing_balance
    
    return pd.DataFrame(schedule)

# Read the Excel file with the provided data (make sure the path to your Excel file is correct)
data = pd.read_excel("SimpleAmortizationTest.xlsx")  # Modify path as needed

# Predefined loan amounts and annual interest rate
loan_amounts = [35000, 40000, 40000, 40000, 40000, 40000, 40000, 40000, 40000, 40000]
annual_rate = 0.08  # Fixed annual interest rate of 8%

# Prepare the data for conversion
loan_data = []

for i, row in data.iterrows():
    loan_number = i + 1 # type: ignore
    start_date = row['start_date']
    term_months = row['term_months']
    
    # Convert start_date to the required format '%d-%m-%Y'
    start_date = pd.to_datetime(start_date).strftime('%d-%m-%Y')
    
    # Calculate the monthly payment using the loan parameters
    payment = calculate_monthly_payment(loan_amounts[i], annual_rate, term_months) # type: ignore
    
    # Handle CPR: check if it's already a float or percentage string
    cpr = row['cpr']
    if isinstance(cpr, str):  # If CPR is a string (e.g., '5%')
        cpr = cpr.strip('%')  # Remove '%' sign
        cpr = float(cpr) / 100  # Convert percentage to decimal
    else:  # If CPR is already a float (e.g., 5.0)
        cpr = cpr / 100  # Convert to decimal format
    
    loan_amount = loan_amounts[i]  # type: ignore # Assign loan amount based on the predefined list
    
    loan_data.append({
        "loan_number": loan_number,
        "loan_amount": loan_amount,
        "annual_rate": annual_rate,
        "start_date": start_date,
        "term_months": term_months,
        "payment": round(payment, 2),  # Round the payment to 2 decimal places
        "cpr": cpr
    })

# Convert the list to a DataFrame
loan_data_df = pd.DataFrame(loan_data)

# Save to CSV
loan_data_df.to_csv("converted_loan_data.csv", index=False)

print("CSV file has been saved successfully!")

# Generate amortization schedules for all loans
all_schedules = []
for _, loan in loan_data_df.iterrows():
    loan_schedule = generate_amortization_schedule(loan)
    loan_schedule['loan_number'] = loan['loan_number']  # Add loan number for identification
    all_schedules.append(loan_schedule)

# Concatenate all schedules into one DataFrame
consolidated_schedule = pd.concat(all_schedules)

# Sort by loan_number and then by date to ensure proper grouping
consolidated_schedule['date'] = pd.to_datetime(consolidated_schedule['date'], format='%d-%m-%Y')
consolidated_schedule = consolidated_schedule.sort_values(by=['loan_number', 'date'])

# Save consolidated schedule to CSV
consolidated_schedule.to_csv("consolidated_amortization_schedule.csv", index=False)

# Aggregating the amortization schedules by date and loan_number
aggregated_schedule = consolidated_schedule.groupby(['date', 'loan_number']).agg({
    'payment': 'sum',
    'prepayment': 'sum',
    'interest': 'sum',
    'principal': 'sum',
    'closing_balance': 'last'  # Use last closing balance for the given date
}).reset_index()

# Save the aggregated schedule to CSV
aggregated_schedule.to_csv("aggregated_amortization_schedule.csv", index=False)

# Save the consolidated schedule to an Excel file
consolidated_schedule.to_excel("consolidated_amortization_schedule.xlsx", index=False)

# Save the aggregated schedule to an Excel file
aggregated_schedule.to_excel("aggregated_amortization_schedule.xlsx", index=False)

# Display a message confirming the save operation
print("Amortization schedules have been saved to Excel and CSV files!")
