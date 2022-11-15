"""
Developer: Ankit Tiwari
Date: 14 Nov 2022
File:"For Database Connection"
"""


'''Problem: If all the columns match, we will load the two json files, concatenate one to another and convert to a CSV file. '''
import pandas as pd
df1 = pd.read_json("File1.json")
df2 = pd.read_json("File2.json")
column1=[]
column2=[]
for col in df1.columns:
	column1.append(col)
for col in df2.columns:
	column2.append(col)
if column1 ==column2:
	result = pd.concat([df1, df2])
	result.to_csv('result.csv')  
	
