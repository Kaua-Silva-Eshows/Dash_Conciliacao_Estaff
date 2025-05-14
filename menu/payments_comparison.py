from datetime import date, datetime, timedelta
import streamlit as st
from data.querys_apis.transfeera_api import *
from data.queys_estaff import *
from data.querys_apis.assas_api import *
from menu.page import Page
from utils.components import *
from utils.functions import *

def BuildPaymentsComparison(transactionPayments):

    row = st.columns(6)
    global day_Payments, day_Payments2

    with row[2]:
        day_Payments = st.date_input('Data Inicio:',value=date.today() - timedelta(days=1),format='DD/MM/YYYY',key='day_Payments')
    
    with row[3]:
        day_Payments2 = st.date_input('Data Fim:',value=date.today() - timedelta(days=1),format='DD/MM/YYYY',key='day_Payments2')
    
    transaction_Payments = transactions_payments(day_Payments, day_Payments2)
    transfeera_Payments = query_transfeera_payments(day_Payments, day_Payments2)

    transaction_Payments_group = transaction_Payments.groupby(['Data Pgto'])['Valor Freela'].sum().reset_index()
    transfeera_Payments_group = transfeera_Payments.groupby(['Data Pgto'])['Valor Transfeera'].sum().reset_index()


    row1 = st.columns([1,3,1])
    with row1[1]:
        merged_payments = pd.merge(transaction_Payments_group, transfeera_Payments_group, how='outer', on=['Data Pgto'])
        function_format_numeric_columns(merged_payments, ['Valor Freela', 'Valor Transfeera'])
        filtered_copy, count = component_plotDataframe(merged_payments, 'Comparação Transfeera X Propostas')
    
    st.markdown("""---""")

    row2 = st.columns(1)
    with row2[0]:
        function_format_numeric_columns(transaction_Payments, ['Valor Freela'])
        filtered_copy, count = component_plotDataframe(transaction_Payments, 'Pagamento Propostas')

    st.markdown("""---""")

    row3 = st.columns(1)
    with row3[0]:
        function_format_numeric_columns(transfeera_Payments, ['Valor Transfeera'])
        filtered_copy, count = component_plotDataframe(transfeera_Payments, 'Pagamento Transfeera')
    

class PaymentsComparison(Page):
    def render(self):
        self.data = {}
        day_Payments = date.today() - timedelta(days=1)
        day_Payments2 = date.today() - timedelta(days=1)
        self.data['transactionPayments'] = transactions_payments(day_Payments, day_Payments2)
        BuildPaymentsComparison(self.data['transactionPayments'])