import pdfplumber
import pandas as pd
import re # regular expressions used for matching patterns in text

# step 1 load and read the PDF
pdf_path = 'bank_statement.pdf'

with pdfplumber.open(pdf_path) as pdf:
    full_text = "" # create empty string to hold text
    for page in pdf.pages:
        full_text += page.extract_text() # add each page into 'full_text'

# step 2 extract details using re 

transactions = []
# the following pattern looks for a date, followed by a description, an amount, and a balance
transaction_pattern = re.compile(r'(\d{2}-\d{2})\s+(.*?)\s+([\d,]+\.\d{2}-?)\s+([\d,]+\.\d{2})') # compile it in the following format and store it in a variable

lines = full_text.split('\n') # split the text into lines

for line in lines:
    match = transaction_pattern.match(line)
    if match:
        date = match.group(1) + "-2024"  # Adding year to date
        description = match.group(2)
        amount = float(match.group(3).replace(',', '').replace('-', '')) * (-1 if '-' in match.group(3) else 1)  # Handle negative amounts
        balance = match.group(4).replace(',', '')
        transactions.append([date, description, amount, balance])

# step 3 create a DataFrame to organize the data
df = pd.DataFrame(transactions, columns=["Date", "Description", "Amount", 'Balance'])



# Convert the Date column to a datetime format
df['Date'] = pd.to_datetime(df['Date'], format='%m-%d-%Y')

# Step 4: Calculate weekly spending
df['Week'] = df['Date'].dt.isocalendar().week  # Get the week number for each transaction
weekly_spending = df.groupby('Week')['Amount'].sum().reset_index(name='Weekly Spending')

# Step 5: Option 1 - Add Weekly Spending as a New Row in the DataFrame
weekly_totals = weekly_spending.set_index('Week').reindex(df['Week']).reset_index(drop=True)
df['Weekly Spending'] = weekly_totals['Weekly Spending']



# step 4 export the DF to an excel file
output_path = 'data.xlsx'
df.to_excel(output_path, index=False)

# Display a sucess message

print("Success")

