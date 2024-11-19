README File for Setting Up and Running the Project

Project Overview

This project involves calculating loan amortization schedules, including monthly payments, interest, prepayments based on a specified Conditional Prepayment Rate (CPR), and generating consolidated and aggregated reports. The outputs are saved in both CSV and Excel formats for further analysis.

---

  Prerequisites

To run this project, you'll need to set up a Python virtual environment and install the required dependencies. Follow the steps below for setup and execution. 

Setting Up the Virtual Environment

1. Navigate to the project directory: where the project files are located (e.g., `C:\Users\hp\Desktop\Mini Project`).

2. Create a Virtual Environment:
   Run the following command in the command prompt or terminal to create a virtual environment named `venv`:

   bash   python -m venv venv
   

3. Activate the Virtual Environment:
   To activate the virtual environment, use the following command:

   - On Windows:
     bash:   venv\Scripts\activate
     
   
   After activation, the command prompt will show `(venv)` before the path.

4. Install Required Dependencies:
   With the virtual environment activated, install the required libraries using the following command:

   bash   pip install -r requirements.txt
   

   This will install all the dependencies listed in the `requirements.txt` file, which may include libraries like `pandas`, `numpy`, and other packages necessary for the project to run.

Run the python scripts: 

ModifiedAmortization.py-------------- copy and past in the cmd
SimpleAmortization.py----------------copy and past in the cmd 
SimpleAmortization_dataset_in.py------copy and past in the cmd


  Project Structure

-  `venv/` : The virtual environment folder containing necessary dependencies.
-  `requirements.txt` : A file that lists all the Python dependencies required for the project.
-  `SimpleAmortizationTest.xlsx` : The Excel file containing the loan data, including start dates, terms, and CPR values for each loan.
-  `convert.py` : Python script to calculate monthly payments, generate amortization schedules, and save the results in CSV and Excel formats.
-  `converted_loan_data.csv` : Output CSV file containing loan details.
-  `consolidated_amortization_schedule.csv` : Output CSV file with the complete amortization schedule for all loans.
-  `aggregated_amortization_schedule.csv` : Output CSV file with aggregated loan schedule data.
-  `consolidated_amortization_schedule.xlsx` : Output Excel file with consolidated amortization schedule.
-  `aggregated_amortization_schedule.xlsx` : Output Excel file with aggregated amortization schedule. 

  Running the Project

After setting up the virtual environment and installing the dependencies, follow these steps to run the project:

1.  Place your input data :
   - Ensure the Excel file (`SimpleAmortizationTest.xlsx`) with your loan data is located in the project folder. The data should include columns like `start_date`, `term_months`, and `cpr`.

2.  Run the Python Script :
   Execute the Python script `convert.py` to generate the amortization schedules and output files. You can run the script using:

   bash
   python convert.py
   

3.  Output Files :
   After running the script, the following files will be generated:
   -  `converted_loan_data.csv` : Loan details after calculation.
   -  `consolidated_amortization_schedule.csv` : Full amortization schedule for all loans.
   -  `aggregated_amortization_schedule.csv` : Summarized amortization schedule data.
   -  `consolidated_amortization_schedule.xlsx` : Full amortization schedule in Excel format.
   -  `aggregated_amortization_schedule.xlsx` : Summarized amortization schedule in Excel format. 

  Dependencies

The project requires the following Python packages, which are specified in the `requirements.txt` file:

- (Additional libraries as per your project)

To install these dependencies, make sure you're in the virtual environment and run:

bash : pip install -r requirements.txt


  Troubleshooting

- If you encounter any issues with missing modules or dependencies, ensure that you've activated the virtual environment and installed all the packages from `requirements.txt`.
- If the Excel or CSV files are not generated correctly, check the format of the input data in the `SimpleAmortizationTest.xlsx` file. 

  Conclusion

This project allows you to calculate loan amortization schedules, including the effects of prepayments, and generates comprehensive reports in both CSV and Excel formats. It can be useful for financial analysts or loan servicers who need detailed insights into loan repayments and forecasts.
