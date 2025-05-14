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

@st.cache_data
def transactions_payments(day1, day2):
    return get_dataframe_from_query(f""" 
SELECT
    P.ID AS 'ID Proposta',
    C.NAME AS 'Estabelecimento',
    DATE_FORMAT(O.START_AT, '%d/%m/%Y') AS 'Data job', 
    DATE_FORMAT(P.DATA_PAGAMENTO, '%d/%m/%Y') AS 'Data Pgto', 
    P.VALOR_FREELA AS 'Valor Freela'
    FROM T_PROPOSALS P 
    INNER JOIN T_PROPOSAL_STATUS PS ON (P.FK_PROPOSAL_STATUS = PS.ID)
    INNER JOIN T_FREELA F ON (P.FK_FREELA = F.ID)
    INNER JOIN ADMIN_USERS AU ON (F.FK_ADMIN_USERS = AU.ID)
    INNER JOIN T_OPPORTUNITIES O ON (P.FK_OPPORTUNITIE = O.ID)
    INNER JOIN T_COMPANIES C ON (O.FK_COMPANIE = C.ID)
    INNER JOIN T_PROPOSAL_TYPE PT ON (O.FK_PROPOSAL_TYPE = PT.ID)
    LEFT JOIN T_STATUS_PAGAMENTO SP ON (P.FK_STATUS_PAGAMENTO = SP.ID)
    LEFT JOIN T_COMPANY_GROUP CG ON (C.FK_GROUP = CG.ID)
    WHERE P.FK_PROPOSAL_STATUS IN (102, 103, 106, 115)
    AND P.FK_STATUS_PAGAMENTO = 101
    AND DATE(P.DATA_PAGAMENTO) >= '{day1}'
    AND DATE(P.DATA_PAGAMENTO) <= '{day2}'
    ORDER BY C.NAME ASC, O.START_AT ASC
    """)