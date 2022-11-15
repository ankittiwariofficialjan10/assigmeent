"""
Developer: Ankit Tiwari
API version: 1.0
Date: 14 Nov 2022
File:"For Database Connection"
"""

''' Merge multiple CSV files in a unique dataset making it into 5 million rows using python.
Problem: You have been given a folder that contains 5 CSV files having 1 million sales records each. Using pandas and python merge all the csv files in the given folder into one CSV file having 5 million records. You may choose to reset the index. (You may write the code assuming you have a folder named sales_records in your project directory which would contain the 5 csv files)'''


import os
import pandas as pd
cwd = os.path.abspath('sales_records')
file_list = os.listdir(cwd)
os.chdir(cwd)
csv_list = []
#append all files together and add a column to store the name of file from which the given data comes from
for file in sorted(file_list):
    csv_list.append(pd.read_csv(file).assign(File_Name = os.path.basename(file)))

# merges single pandas DFs into a single DF, index is refreshed 
csv_merged = pd.concat(csv_list)

# Single DF is saved to the path in CSV format, without index column
csv_merged.to_csv(cwd + '.csv', index=False)
