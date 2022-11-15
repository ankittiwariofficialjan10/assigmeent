"""
Developer: Ankit Tiwari
API version: 1.0
Date: 14 Nov 2022
File:"For Database Connection"
"""
import requests
import json
import logging
import sqlite3
import pandas as pd
import os
import fnmatch

#know folder where Files will be delivered. 
cwd = os.path.abspath('transaction_files')

#logging error in error.log file
logger = logging.getLogger(__name__)
logging.basicConfig(
     filename='error.log',
     level=logging.ERROR, 
     format= '[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
     datefmt='%H:%M:%S'
)

#api key (can also be stored inside env file)
headers= {
    "apikey": "iVMRLI0Vk6AyMz16DPOzlVHPbjvHzRTj"
    }

# Connecting to sqlite db named fx.db
try:
    connection_obj = sqlite3.connect('fx.db')
    # cursor object
    cursor_obj = connection_obj.cursor()
except sqlite3.InternalError as error:
    logging.error(error)    


def main():
    try:
        df = file_type(cwd)
        if df is not None :
            send_request(df)
        else:
            print("No transaction file found")
        return True
    except Exception as ex:
        logging.error(ex)
        return False 
    finally:
        connection_obj.close()


# check type of file recived from client's end
def file_type(cwd):
    os.chdir(cwd)
    for file in os.listdir(cwd):
        if fnmatch.fnmatch(file, '*.csv'):
            df=pd.read_csv('fx_input.csv')
        elif fnmatch.fnmatch(file, '*.json'):
            df=pd.read_json('fx_input.json')
        elif fnmatch.fnmatch(file, '*.xml'):
            df=pd.read_xml('fx_input.xml')
        return df


#this function sends request to api server for FX rates
def send_request(df):
    for ind in df.index:
        payload_to=df['SourceCurrency'][ind]
        payload_from=df['DestinationCurrency'][ind]
        payload_amount=df['SourceAmount'][ind]
        id=df['ID'][ind]
        payload={}
        url = "https://api.apilayer.com/fixer/convert?to="+str(payload_to)+"&from="+str(payload_from)+"&amount="+str(payload_amount)+""
        response = requests.request("GET", url, headers=headers, data = payload)
        check_response(response,id)
    if check_response:
        return True
    else:
        print("Sending request failed")


# this function checks the response recived from FX server
def check_response(response,id):
    if response.status_code == 200:
            json_data =  json.loads(response.text)
            connection(json_data,id) 
            if connection: 
                return True
            else:
                return False
    else:
        print("Error while sending request to API server for id " + id)
        return False


# this function stores the response into a SQLLite table named records
def connection(json_data,id):
    print(id)
    process_id = id
    FX_rate = json_data['info']['timestamp']
    date=json_data['date']
    result=json_data['result']
    payload_from=json_data['query']['from']
    payload_to=json_data['query']['to']
    payload_amount=json_data['query']['amount']
    try: 
        cursor_obj.execute("insert into records(process_id,SourceCurrency,DestinationCurrency,SourceAmount,TimeUpdated,FX_rate,ConvertedAmount) VALUES (?,?,?,?,?,?,?)", (process_id,payload_from,payload_to,payload_amount,date,FX_rate,result))
        connection_obj.commit()   
        return True 
    except sqlite3.InternalError as error:
        logging.error(error) 
        return False
    
if __name__ == '__main__':
    main()
   