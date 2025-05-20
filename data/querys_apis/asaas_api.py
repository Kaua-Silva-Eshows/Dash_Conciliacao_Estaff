from itertools import count
import numpy as np
import streamlit as st
import requests
import pandas as pd

@st.cache_data
def query_asaas_extract(day):
    offset = 0
    access_token = st.secrets["asaas_api"]["access_token"]
    
    headers = {
        'Content-Type': 'application/json',
        'access_token': access_token
    }

    df = pd.DataFrame()
    item_count = 0

    while True:
        url = f"https://api.asaas.com/v3/financialTransactions?startDate={day}&finishDate={day}&limit=100&offset={offset}"
        response = requests.get(url, headers=headers)
        data = response.json()
        if len(data['data']) == 0:
            df = pd.DataFrame({'ID Asaas': [np.nan],'Valor Asaas': [np.nan],'Status Pgto': [np.nan],'Data Compensação': [np.nan], 'Estabelecimento': [np.nan] }).astype('object')
            break
        else:
            selected_fields = [
            {
                'paymentId': item['paymentId'],
                'value': item['value'],
                'type': item['type'],
                'date': item['date'],
                'description': item['description']
            }
            for item in data['data']
        ]
            item_count = len(data['data'])
            if item_count == 100:
                offset += 100
                df = pd.concat([df, pd.DataFrame(selected_fields)])
            else:
                df = pd.concat([df, pd.DataFrame(selected_fields)])
                break
                
    df = df.rename(columns={'paymentId': 'ID Asaas', 'value': 'Valor Asaas', 'type': 'Status Pgto', 'date': 'Data Compensação', 'description': 'Estabelecimento'})
    df = df[~df["Status Pgto"].isin(["PAYMENT_FEE", "TRANSFER"])]
    df['Data Compensação'] = pd.to_datetime(df['Data Compensação'], errors='coerce').dt.strftime('%d/%m/%Y')        

    return df

@st.cache_data
def query_asaas_extract_events(day):
    offset = 0
    access_token = st.secrets["asaas_api_events"]["access_token"]
    
    headers = {
        'Content-Type': 'application/json',
        'access_token': access_token
    }

    df = pd.DataFrame()
    item_count = 0

    while True:
        url = f"https://api.asaas.com/v3/financialTransactions?startDate={day}&finishDate={day}&limit=100&offset={offset}"
        response = requests.get(url, headers=headers)
        data = response.json()
        if len(data['data']) == 0:
            df = pd.DataFrame({'ID Asaas': [np.nan],'Valor Asaas': [np.nan],'Status Pgto': [np.nan],'Data Compensação': [np.nan], 'Estabelecimento': [np.nan] }).astype('object')
            break
        else:
            selected_fields = [
            {
                'paymentId': item['paymentId'],
                'value': item['value'],
                'type': item['type'],
                'date': item['date'],
                'description': item['description']
            }
            for item in data['data']
        ]
            item_count = len(data['data'])
            if item_count == 100:
                offset += 100
                df = pd.concat([df, pd.DataFrame(selected_fields)])
            else:
                df = pd.concat([df, pd.DataFrame(selected_fields)])
                break

    df = df.rename(columns={'paymentId': 'ID Asaas', 'value': 'Valor Asaas', 'type': 'Status Pgto', 'date': 'Data Compensação', 'description': 'Estabelecimento'})
    df = df[~df["Status Pgto"].isin(["PAYMENT_FEE", "TRANSFER_FEE", "TRANSFER"])]
    df['Data Compensação'] = pd.to_datetime(df['Data Compensação'], errors='coerce').dt.strftime('%d/%m/%Y')        

    return df









