from datetime import date, datetime, timedelta
import streamlit as st
from data.querys_apis.transfeera_api import *
from data.querys_estaff import *
from data.querys_apis.asaas_api import *
from menu.page import Page
from utils.components import *
from utils.functions import *

def BuildPaymentsComparison(transaction_Payments):

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


    row1 = st.columns([5,3,5])

    with row1[1]:
        difference = float(transaction_Payments_group['Valor Freela'].sum()) - float(transfeera_Payments_group['Valor Transfeera'].sum())
        difference = function_format_number_columns(valor=difference)
        tile = row1[1].container(border=True)
        tile.write(f"""<p style='text-align: center; font-size: 12px;'>Diferença Total<br><span style='font-size: 17px;'>R$: {difference}</span></p>""",unsafe_allow_html=True)


    row2 = st.columns([1,3,1])
    with row2[1]:
        merged_payments = pd.merge(transaction_Payments_group, transfeera_Payments_group, how='outer', on=['Data Pgto'])
        merged_payments["Diferença"] = merged_payments["Valor Freela"].astype(float) - merged_payments["Valor Transfeera"].astype(float)
        merged_payments["Diferença"] = merged_payments["Diferença"].abs()
        merged_payments = function_total_line(merged_payments, ['Valor Freela', 'Valor Transfeera', 'Diferença'], 'Data Pgto')        
        function_format_number_columns(merged_payments, ['Valor Freela', 'Valor Transfeera', 'Diferença'])
        filtered_copy, count = component_plotDataframe(merged_payments, 'Comparação Transfeera X Propostas')
        function_copy_dataframe_as_tsv(filtered_copy)
    
    st.markdown("""---""")

    row3 = st.columns(1)
    with row3[0]:
        transaction_Payments = function_total_line(transaction_Payments, ['Valor Freela'], 'Estabelecimento')
        function_format_number_columns(transaction_Payments, ['Valor Freela'])
        filtered_copy, count = component_plotDataframe(transaction_Payments, 'Pagamento Propostas')
        function_copy_dataframe_as_tsv(filtered_copy)
        function_box_lenDf(len_df=count, df=filtered_copy, y='-100', x='500', box_id='box1', item='Propostas')

    st.markdown("""---""")

    row4 = st.columns(1)
    with row4[0]:
        transfeera_Payments = function_total_line(transfeera_Payments, ['Valor Transfeera'], 'Crédito / Débito')
        function_format_number_columns(transfeera_Payments, ['Valor Transfeera'])
        filtered_copy, count = component_plotDataframe(transfeera_Payments, 'Pagamento Transfeera')
        function_copy_dataframe_as_tsv(filtered_copy)
        function_box_lenDf(len_df=count, df=filtered_copy, y='-100', x='500', box_id='box1', item='Pagamentos')
    

class PaymentsComparison(Page):
    def render(self):
        self.data = {}
        day_Payments = date.today() - timedelta(days=1)
        day_Payments2 = date.today() - timedelta(days=1)
        self.data['transactionPayments'] = transactions_payments(day_Payments, day_Payments2)
        BuildPaymentsComparison(self.data['transactionPayments'])