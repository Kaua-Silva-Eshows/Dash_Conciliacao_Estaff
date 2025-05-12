from datetime import date, datetime, timedelta
import streamlit as st
from data.queys_estaff import *
from data.assas_api import *
from menu.page import Page
from utils.components import *
from utils.functions import *

def BuildExtractComparison(transactionsExtract):

    row = st.columns(5)
    global day_Extract

    with row[2]:
        day_Extract = st.date_input('Selecione uma data:',value=date.today() - timedelta(days=1),format='DD/MM/YYYY',key='day_Extract')    

    asaas_extract_df = asaas_extract(day_Extract)
    transactionsExtract = transactions_extract(day_Extract)
    
    merged_extract = pd.merge(transactionsExtract, asaas_extract_df, how='outer', on=['ID Asaas', 'Data Compensação'])
    
    for col in merged_extract.columns:
        if col.endswith('_x'):
            base_col = col[:-2]  
            col_x = col
            col_y = f'{base_col}_y'
            
            if col_y in merged_extract.columns:
                merged_extract[base_col] = merged_extract[col_x].combine_first(merged_extract[col_y])
                merged_extract.drop(columns=[col_x, col_y], inplace=True)

    merged_extract = merged_extract[['Boleto ID EPM', 'Company ID EPM', 'Estabelecimento','ID Asaas', 'Invoice Number Asaas', 'Data Compensação', 'Inicio Jobs', 'Data Vencimento','Valor Asaas','Valor Total','Valor Boleto', 'Status Pgto', 'Link', 'Data Repasse Freelas']]
    
    asaas_value = float(asaas_extract_df['Valor Asaas'].sum())
    bd_value = float(transactionsExtract['Valor Total'].sum())
    
    difference = abs(round(bd_value - asaas_value, 2))

    row1 = st.columns([5,3,5])

    with row1[1]:
            
        tile = row1[1].container(border=True)
        tile.write(f"""<p style='text-align: center; font-size: 12px;'>Diferença<br><span style='font-size: 17px;'>{difference:,.2f}</span></p>""",unsafe_allow_html=True)


    row2 = st.columns(1)

    with row2[0]:

        if difference == 0:

            if merged_extract.isnull().any().any():
                    st.warning('Nenhum extrato para essa data', icon="📄")
            else:
                st.warning('Nenhuma diferença encontrada', icon="📄")
        
        else:
            merged_extract['Valor Total'] = pd.to_numeric(merged_extract['Valor Total'], errors='coerce')
            filtered = merged_extract[merged_extract['Valor Asaas'] != merged_extract['Valor Total']]

            filtered = function_total_line(filtered, ['Valor Asaas', 'Valor Total', 'Valor Boleto'], 'Estabelecimento')
            function_format_numeric_columns(filtered, ['Valor Asaas', 'Valor Total', 'Valor Boleto'])
            filtered_copy, count = component_plotDataframe(filtered, 'Diferença Assas X Boletos')
            function_copy_dataframe_as_tsv(filtered_copy)
            function_box_lenDf(len_df=count, df=filtered_copy, y='-100', x='500', box_id='box1', item='Extratos')
    
    st.markdown("""---""")

    row3 = st.columns(1)

    with row3[0]:
        transactionsExtract = function_total_line(transactionsExtract, ['Valor Total', 'Valor Boleto'], 'Estabelecimento')
        function_format_numeric_columns(transactionsExtract, ['Valor Total', 'Valor Boleto'])
        filtered_copy, count = component_plotDataframe(transactionsExtract, 'Boletos')
        function_copy_dataframe_as_tsv(filtered_copy)
        function_box_lenDf(len_df=count, df=filtered_copy, y='-100', x='500', box_id='box1', item='Extratos')

    st.markdown("""---""")

    row4 = st.columns(1)

    with row4[0]:
        asaas_extract_df = function_total_line(asaas_extract_df, ['Valor Asaas'], 'ID Asaas')
        function_format_numeric_columns(asaas_extract_df, ['Valor Asaas'])
        filtered_copy, count = component_plotDataframe(asaas_extract_df, 'Asaas Extratos')
        function_copy_dataframe_as_tsv(filtered_copy)
        function_box_lenDf(len_df=count, df=filtered_copy, y='-100', x='500', box_id='box1', item='Extratos')

class ExtractComparison(Page):
    def render(self):
        self.data = {}
        day_Extract = date.today() - timedelta(days=1)
        self.data['transactionsExtract'] = transactions_extract(day_Extract)

        BuildExtractComparison(self.data['transactionsExtract'])