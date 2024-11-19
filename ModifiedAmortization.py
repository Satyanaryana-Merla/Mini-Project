"""
This script processes amortization schedules and generates both daily and monthly schedules 
from periodic loan data. It consolidates the schedules by date for both daily and monthly 
frequencies. The steps include creating daily and monthly amortization schedules from provided 
loan data and aggregating them by date.

### Functions and Steps:
1. **Creating Daily Amortization Schedules:**
   - For each period in the provided data, a daily schedule is created. 
   - Payments, interest, principal, prepayment, and closing balance are carried forward for 
     every day in the month (assuming 30 days for simplicity). 
   - The dummy daily schedules can later be expanded with more accurate logic for dividing payments.

2. **Creating Monthly Amortization Schedules:**
   - A monthly schedule is created for each period using the start date of each month.
   - This aggregates all the payments, interest, principal, prepayment, and closing balances 
     for that month.

3. **Consolidating Schedules:**
   - The daily and monthly schedules are aggregated by date. For the daily schedule, the 
     sum of all payments, interest, principal, prepayment, and closing balances are calculated 
     for each day.
   - The same aggregation process is applied to the monthly schedule.

### Output:
- `df`: The original DataFrame representing the sample periodic loan data.
- `daily_df`: The daily amortization schedule, with one entry for each day of the month.
- `monthly_df`: The monthly amortization schedule, with one entry for each month.
- `consolidated_daily_df`: A consolidated daily schedule, grouped by date.
- `consolidated_monthly_df`: A consolidated monthly schedule, grouped by date.

### Dependencies:
- `pandas`: Used for reading, manipulating, and aggregating the data.

"""
import pandas as pd

# Sample Data (This would be replaced with your actual input data for periodic amortization)
data = {
    'period': [0, 1, 2, 3, 4],
    'date': ['13-01-2024', '13-02-2024', '13-03-2024', '13-04-2024', '13-05-2024'],
    'opening_balance': [10000.00, 9899.87, 9800.17, 9700.87, 9601.99],
    'payment': [58.46, 58.46, 58.46, 58.46, 58.46],
    'interest': [41.67, 41.25, 40.83, 40.42, 40.01],
    'principal': [16.79, 17.21, 17.62, 18.04, 18.45],
    'prepayment': [83.33, 82.50, 81.67, 80.84, 80.02],
    'new_origination': [0, 0, 0, 0, 0],
    'maturity': [0, 0, 0, 0, 0],
    'closing_balance': [9899.87, 9800.17, 9700.87, 9601.99, 9503.53]
}

# Create a DataFrame from the sample data
df = pd.DataFrame(data)

# Step 1: Develop the Daily Amortization Schedule
daily_schedule = []
for _, row in df.iterrows():
    # For each row, create daily schedules. Here, we generate dummy daily schedules for illustration purposes.
    # In a real-world scenario, the logic for splitting payments over each day should be more detailed.
    date = pd.to_datetime(row['date'])
    for day in range(30):  # Assume 30 days in each month for simplicity
        daily_schedule.append({
            'period': row['period'],
            'date': date + pd.Timedelta(days=day),
            'opening_balance': row['opening_balance'],
            'payment': row['payment'],
            'interest': row['interest'],
            'principal': row['principal'],
            'prepayment': row['prepayment'],
            'new_origination': row['new_origination'],
            'maturity': row['maturity'],
            'closing_balance': row['closing_balance'],
        })

# Convert daily_schedule to DataFrame
daily_df = pd.DataFrame(daily_schedule)

# Step 2: Develop the Monthly Amortization Schedule
monthly_schedule = []
for _, row in df.iterrows():
    # Group by monthly payments based on the start date of the period.
    month_start = pd.to_datetime(row['date']).replace(day=1)
    monthly_schedule.append({
        'period': row['period'],
        'date': month_start,
        'opening_balance': row['opening_balance'],
        'payment': row['payment'],
        'interest': row['interest'],
        'principal': row['principal'],
        'prepayment': row['prepayment'],
        'new_origination': row['new_origination'],
        'maturity': row['maturity'],
        'closing_balance': row['closing_balance'],
    })

# Convert monthly_schedule to DataFrame
monthly_df = pd.DataFrame(monthly_schedule)

# Step 3: Consolidate Daily and Monthly Schedules

# Consolidating the Daily Schedules (group by date)
consolidated_daily_df = daily_df.groupby('date').agg({
    'payment': 'sum',
    'interest': 'sum',
    'principal': 'sum',
    'prepayment': 'sum',
    'new_origination': 'sum',
    'maturity': 'sum',
    'closing_balance': 'sum',
}).reset_index()

# Consolidating the Monthly Schedules (group by date)
consolidated_monthly_df = monthly_df.groupby('date').agg({
    'payment': 'sum',
    'interest': 'sum',
    'principal': 'sum',
    'prepayment': 'sum',
    'new_origination': 'sum',
    'maturity': 'sum',
    'closing_balance': 'sum',
}).reset_index()

# Displaying the outputs
print("Sample Periodic Amortization Schedule (for one loan):")
print(df)

print("\nSample Daily Amortization Schedule (for one loan):")
print(daily_df)

print("\nSample Monthly Amortization Schedule (for one loan):")
print(monthly_df)

print("\nConsolidated Daily Amortization Schedule (all loans):")
print(consolidated_daily_df)

print("\nConsolidated Monthly Amortization Schedule (all loans):")
print(consolidated_monthly_df)
