import pandas as pd
"""
The Data is quite clean. Th only steps taken in data cleaning are are converting the csv file
to an excel file which is easier to work with and reformatting the date column.
"""
df = pd.read_csv('Nike.csv')


# reformat date column
df['Invoice Date'] = pd.to_datetime(df['Invoice Date'], format='%d-%m-%Y', errors='coerce')
df['Invoice Date'] = df['Invoice Date'].dt.strftime('%#d-%#m-%Y')


df.to_excel(r'Nike.xlsx', index=False, header=True)