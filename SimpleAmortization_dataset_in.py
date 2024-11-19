import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Helper function to calculate SMM (Single Monthly Mortality)
def calculate_smm(cpr):
    return 1 - (1 - cpr) ** (1 / 12)

# Function to calculate amortization schedule for a single loan
def generate_amortization_schedule(loan_number, loan_amount, annual_rate, start_date, term_months, payment, cpr):
    schedule = []
    opening_balance = loan_amount
    smm = calculate_smm(cpr)
    monthly_rate = annual_rate / 12
    start_date = datetime.strptime(start_date, "%d-%m-%Y")
    
    for period in range(1, term_months + 1):
        interest = opening_balance * monthly_rate
        prepayment = opening_balance * smm
        principal = payment - interest
        total_principal = principal + prepayment
        closing_balance = max(0, opening_balance - total_principal)
        
        # Append data to the schedule
        schedule.append({
            "loan_number": loan_number,
            "period": period,
            "date": (start_date + timedelta(days=30 * period)).strftime("%d-%m-%Y"),
            "opening_balance": round(opening_balance, 2),
            "payment": round(payment, 2),
            "prepayment": round(prepayment, 2),
            "annual_rate": round(annual_rate, 4),
            "monthly_rate": round(monthly_rate, 4),
            "interest": round(interest, 2),
            "principal": round(principal, 2),
            "closing_balance": round(closing_balance, 2)
        })
        
        # Update balance for the next period
        opening_balance = closing_balance
        if closing_balance == 0:
            break  # Stop if the loan is fully paid off
    
    return schedule

# Main function to read loan data, generate schedules, and consolidate
def main():
    # Loan data input
    loan_data = [
        {"loan_number": 1, "loan_amount": 35000, "annual_rate": 0.08, "start_date": "01-09-2023", "term_months": 36, "payment": 1096.77, "cpr": 0.05},
        {"loan_number": 2, "loan_amount": 40000, "annual_rate": 0.08, "start_date": "01-10-2023", "term_months": 12, "payment": 3479.54, "cpr": 0.05},
        {"loan_number": 3, "loan_amount": 40000, "annual_rate": 0.08, "start_date": "01-11-2023", "term_months": 48, "payment": 976.52, "cpr": 0.05},
        {"loan_number": 4, "loan_amount": 40000, "annual_rate": 0.08, "start_date": "01-12-2023", "term_months": 60, "payment": 811.06, "cpr": 0.05},
        {"loan_number": 5, "loan_amount": 40000, "annual_rate": 0.08, "start_date": "01-01-2024", "term_months": 72, "payment": 701.33, "cpr": 0.05},
        {"loan_number": 6, "loan_amount": 40000, "annual_rate": 0.08, "start_date": "01-02-2024", "term_months": 60, "payment": 811.06, "cpr": 0.05},
        {"loan_number": 7, "loan_amount": 40000, "annual_rate": 0.08, "start_date": "01-03-2024", "term_months": 72, "payment": 701.33, "cpr": 0.05},
        {"loan_number": 8, "loan_amount": 40000, "annual_rate": 0.08, "start_date": "01-04-2024", "term_months": 60, "payment": 811.06, "cpr": 0.05},
        {"loan_number": 9, "loan_amount": 40000, "annual_rate": 0.08, "start_date": "01-05-2024", "term_months": 72, "payment": 701.33, "cpr": 0.05},
        {"loan_number": 10, "loan_amount": 40000, "annual_rate": 0.08, "start_date": "01-06-2024", "term_months": 60, "payment": 811.06, "cpr": 0.05},
    ]

    # Generate amortization schedules
    all_schedules = []
    for loan in loan_data:
        schedule = generate_amortization_schedule(
            loan["loan_number"], loan["loan_amount"], loan["annual_rate"], 
            loan["start_date"], loan["term_months"], loan["payment"], loan["cpr"]
        )
        all_schedules.extend(schedule)

    # Convert to DataFrame
    all_schedules_df = pd.DataFrame(all_schedules)

    # Save individual schedules to an Excel file
    individual_excel_file = "individual_amortization_schedules.xlsx"
    with pd.ExcelWriter(individual_excel_file, engine="openpyxl") as writer:
        all_schedules_df.to_excel(writer, sheet_name="Amortization Schedule", index=False)

    # Save individual schedules to a CSV file
    individual_csv_file = "individual_amortization_schedules.csv"
    all_schedules_df.to_csv(individual_csv_file, index=False)
    print(all_schedules_df.head(20))

    # Consolidate schedules by date
    consolidated_schedule = all_schedules_df.groupby("date").agg({
        "payment": "sum",
        "prepayment": "sum",
        "interest": "sum",
        "principal": "sum",
        "closing_balance": "sum"
    }).reset_index()

    # Save consolidated schedule to an Excel file
    consolidated_excel_file = "consolidated_amortization_schedule.xlsx"
    with pd.ExcelWriter(consolidated_excel_file, engine="openpyxl") as writer:
        consolidated_schedule.to_excel(writer, sheet_name="Consolidated Schedule", index=False)

    # Save consolidated schedule to a CSV file
    consolidated_csv_file = "consolidated_amortization_schedule.csv"
    consolidated_schedule.to_csv(consolidated_csv_file, index=False)
    print(consolidated_schedule.head(20))

    print(f"Amortization schedules have been saved to Excel and CSV files:\n- {individual_excel_file}\n- {individual_csv_file}\n- {consolidated_excel_file}\n- {consolidated_csv_file}")

# Run the main function
if __name__ == "__main__":
    main()
