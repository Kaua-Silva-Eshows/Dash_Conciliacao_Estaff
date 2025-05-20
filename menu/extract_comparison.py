from datetime import date, datetime, timedelta
import streamlit as st
from data.querys_estaff import *
from data.querys_apis.asaas_api import *
from menu.page import Page
from utils.components import *
from utils.functions import *

def BuildExtractComparison(transactionsExtract, transactionsExtractEvents):

    row = st.columns(5)
    global day_Extract

    with row[2]:
        day_Extract = st.date_input('Selecione uma data:',value=date.today() - timedelta(days=1),format='DD/MM/YYYY',key='day_Extract')    

    asaasExtract_df = query_asaas_extract(day_Extract)
    transactionsExtract = transactions_extract(day_Extract)
    merged_extract_asaas = pd.merge(transactionsExtract, asaasExtract_df, how='outer', on=['ID Asaas', 'Data Compensação'])
    for col in merged_extract_asaas.columns:
        if col.endswith('_x'):
            base_col = col[:-2]  
            col_x = col
            col_y = f'{base_col}_y'
            
            if col_y in merged_extract_asaas.columns:
                merged_extract_asaas[base_col] = merged_extract_asaas[col_x].combine_first(merged_extract_asaas[col_y])
                merged_extract_asaas.drop(columns=[col_x, col_y], inplace=True)
    merged_extract_asaas = merged_extract_asaas[['Boleto ID EPM', 'Company ID EPM', 'Estabelecimento', 'Brigada Fixa', 'ID Asaas', 'Invoice Number Asaas', 'Data Compensação', 'Inicio Jobs', 'Data Vencimento','Valor Asaas','Valor Total','Valor Boleto', 'Status Pgto', 'Link', 'Data Repasse Freelas']]

    asaas_value = float(asaasExtract_df['Valor Asaas'].sum())
    bd_value = float(transactionsExtract['Valor Total'].sum())
    
    difference_asaas = abs(round(bd_value - asaas_value, 2))



    asaasExtractEvents_df = query_asaas_extract_events(day_Extract)
    transactionsExtractEvents = transactions_extract_events(day_Extract)
    merged_extract_asaas_events = pd.merge(transactionsExtractEvents, asaasExtractEvents_df, how='outer', on=['ID Asaas', 'Data Compensação'])
    for col in merged_extract_asaas_events.columns:
        if col.endswith('_x'):
            base_col = col[:-2]  
            col_x = col
            col_y = f'{base_col}_y'
            
            if col_y in merged_extract_asaas_events.columns:
                merged_extract_asaas_events[base_col] = merged_extract_asaas_events[col_x].combine_first(merged_extract_asaas_events[col_y])
                merged_extract_asaas_events.drop(columns=[col_x, col_y], inplace=True)
    merged_extract_asaas_events = merged_extract_asaas_events[['Boleto ID EPM', 'Company ID EPM', 'Estabelecimento','ID Asaas', 'Invoice Number Asaas', 'Data Compensação', 'Inicio Jobs', 'Data Vencimento','Valor Asaas','Valor Total','Valor Boleto', 'Status Pgto', 'Link', 'Data Repasse Freelas']]

    asaas_value_events = float(asaasExtractEvents_df['Valor Asaas'].sum())
    bd_value_events = float(transactionsExtractEvents['Valor Total'].sum())
    
    difference_asaas_events = abs(round(bd_value_events - asaas_value_events, 2))

    row1 = st.columns([1,2,2,1])

    with row1[1]:
        difference_asaas = function_format_number_columns(valor=difference_asaas)
        tile = row1[1].container(border=True)
        tile.write(f"""<p style='text-align: center; font-size: 12px;'>Diferença Boletos<br><span style='font-size: 17px;'>R$: {difference_asaas}</span></p>""",unsafe_allow_html=True)

    with row1[2]:
        difference_asaas_events = function_format_number_columns(valor=difference_asaas_events)
        tile = row1[2].container(border=True)
        tile.write(f"""<p style='text-align: center; font-size: 12px;'>Diferença Boletos Eventos<br><span style='font-size: 17px;'>R$: {difference_asaas_events}</span></p>""",unsafe_allow_html=True)

    st.markdown("""---""")

    tabs = st.tabs(["Asaas Boletos", "Asaas Boletos Eventos"])

    with tabs[0]:
        row2 = st.columns(1)

        with row2[0]:
            if difference_asaas == "0,00":
                if merged_extract_asaas.isna().all(axis=None):
                        st.warning('Nenhum extrato para essa data', icon="📄")
                else:
                    st.warning('Nenhuma diferença encontrada', icon="📄")
            
            else:
                merged_extract_asaas['Valor Total'] = pd.to_numeric(merged_extract_asaas['Valor Total'], errors='coerce')
                filtered = merged_extract_asaas[merged_extract_asaas['Valor Asaas'] != merged_extract_asaas['Valor Total']]

                filtered = function_total_line(filtered, ['Valor Asaas', 'Valor Total', 'Valor Boleto'], 'Estabelecimento')
                function_format_number_columns(filtered, ['Valor Asaas', 'Valor Total', 'Valor Boleto'])
                filtered_copy, count = component_plotDataframe(filtered, 'Diferença Assas X Boletos')
                function_copy_dataframe_as_tsv(filtered_copy)
                function_box_lenDf(len_df=count - 1, df=filtered_copy, y='-100', x='500', box_id='box1', item='Extratos') #count - 1 para não pegar a linha "Total"
        
                st.markdown("""---""")

                row3 = st.columns(1)

                with row3[0]:
                    transactionsExtract = function_total_line(transactionsExtract, ['Valor Total', 'Valor Boleto'], 'Estabelecimento')
                    function_format_number_columns(transactionsExtract, ['Valor Total', 'Valor Boleto'])
                    filtered_copy, count = component_plotDataframe(transactionsExtract, 'Boletos')
                    function_copy_dataframe_as_tsv(filtered_copy)
                    function_box_lenDf(len_df=count - 1, df=filtered_copy, y='-100', x='500', box_id='box1', item='Boletos') #count - 1 para não pegar a linha "Total"

                st.markdown("""---""")

                row4 = st.columns(1)

                with row4[0]:
                    asaasExtract_df = function_total_line(asaasExtract_df, ['Valor Asaas'], 'ID Asaas')
                    function_format_number_columns(asaasExtract_df, ['Valor Asaas'])
                    filtered_copy, count = component_plotDataframe(asaasExtract_df, 'Asaas Extratos')
                    function_copy_dataframe_as_tsv(filtered_copy)
                    function_box_lenDf(len_df=count - 1, df=filtered_copy, y='-100', x='500', box_id='box1', item='Extratos') #count - 1 para não pegar a linha "Total"

    with tabs[1]:
        row2 = st.columns(1)

        with row2[0]:

            if difference_asaas_events == "0,00":

                if merged_extract_asaas.isna().all(axis=None):
                        st.warning('Nenhum extrato para essa data', icon="📄")
                else:
                    st.warning('Nenhuma diferença encontrada', icon="📄")
            
            else:
                merged_extract_asaas_events['Valor Total'] = pd.to_numeric(merged_extract_asaas_events['Valor Total'], errors='coerce')
                filtered = merged_extract_asaas_events[merged_extract_asaas_events['Valor Asaas'] != merged_extract_asaas_events['Valor Total']]

                filtered = function_total_line(filtered, ['Valor Asaas', 'Valor Total', 'Valor Boleto'], 'Estabelecimento')
                function_format_number_columns(filtered, ['Valor Asaas', 'Valor Total', 'Valor Boleto'])
                filtered_copy, count = component_plotDataframe(filtered, 'Diferença Assas Eventos X Boletos')
                function_copy_dataframe_as_tsv(filtered_copy)
                function_box_lenDf(len_df=count - 1, df=filtered_copy, y='-100', x='500', box_id='box1', item='Extratos') #count - 1 para não pegar a linha "Total"
        
                st.markdown("""---""")

                row3 = st.columns(1)

                with row3[0]:
                    transactionsExtractEvents = function_total_line(transactionsExtractEvents, ['Valor Total', 'Valor Boleto'], 'Estabelecimento')
                    function_format_number_columns(transactionsExtractEvents, ['Valor Total', 'Valor Boleto'])
                    filtered_copy, count = component_plotDataframe(transactionsExtractEvents, 'Boletos Eventos')
                    function_copy_dataframe_as_tsv(filtered_copy)
                    function_box_lenDf(len_df=count - 1, df=filtered_copy, y='-100', x='500', box_id='box1', item='Boletos') #count - 1 para não pegar a linha "Total"

                st.markdown("""---""")

                row4 = st.columns(1)

                with row4[0]:
                    asaasExtractEvents_df = function_total_line(asaasExtractEvents_df, ['Valor Asaas'], 'ID Asaas')
                    function_format_number_columns(asaasExtractEvents_df, ['Valor Asaas'])
                    filtered_copy, count = component_plotDataframe(asaasExtractEvents_df, 'Asaas Eventos Extratos')
                    function_copy_dataframe_as_tsv(filtered_copy)
                    function_box_lenDf(len_df=count - 1, df=filtered_copy, y='-100', x='500', box_id='box1', item='Extratos') #count - 1 para não pegar a linha "Total"
        


class ExtractComparison(Page):
    def render(self):
        self.data = {}
        day_Extract = date.today() - timedelta(days=1)
        self.data['transactionsExtract'] = transactions_extract(day_Extract)
        self.data['transactionsExtractEvents'] = transactions_extract_events(day_Extract)

        BuildExtractComparison(self.data['transactionsExtract'],
                               self.data['transactionsExtractEvents'])