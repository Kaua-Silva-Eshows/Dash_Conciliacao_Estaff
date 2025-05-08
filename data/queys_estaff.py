from data.dbconnect import get_dataframe_from_query
import streamlit as st

@st.cache_data
def transactions_extract(day1):
    return get_dataframe_from_query(f""" 
SELECT
    B.ID AS 'Boleto ID EPM',
    C.ID AS 'Company ID EPM',
    C.NAME AS 'Estabelecimento',
    B.ID_ASAAS AS 'ID Asaas',
    B.INVOICE_NUMBER_ASAAS AS 'Invoice Number Asaas',
    DATE_FORMAT(B.DATA_CRIACAO, '%d/%m/%Y') AS 'Data Criação', 
    DATE_FORMAT(B.DATA_INICIO_JOBS, '%d/%m/%Y') AS 'Inicio Jobs', 
    DATE_FORMAT(B.DATA_FIM_JOBS, '%d/%m/%Y') AS 'Fim Jobs', 
    DATE_FORMAT(B.DATA_VENCIMENTO, '%d/%m/%Y') AS 'Data Vencimento', 
    B.VALOR AS 'Valor Boleto',
    B.VALOR + IF(B.JUROS_E_MULTA IS NULL, 0, B.JUROS_E_MULTA) AS 'Valor Total',
    B.STATUS_PAGAMENTO AS 'Status Pgto',
    DATE_FORMAT(B.DATA_COMPENSACAO, '%d/%m/%Y') AS 'Data Compensação', 
    B.LINK AS 'Link',
    DATE_FORMAT(DATE_ADD(B.DATA_FIM_JOBS, 
        INTERVAL (5 - WEEKDAY(B.DATA_FIM_JOBS) + 7) % 7 DAY),'%d/%m/%Y') AS 'Data Repasse Freelas'
FROM T_BOLETO B
INNER JOIN T_COMPANIES C ON (B.FK_COMPANY = C.ID)
WHERE B.CANCELADO = 0
AND B.DATA_COMPENSACAO <= '{day1}'
AND B.DATA_COMPENSACAO >= '{day1}'
""")