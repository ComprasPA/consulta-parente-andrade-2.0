import streamlit as st
import pandas as pd
import base64
import re
from datetime import datetime, timedelta
from io import BytesIO
import urllib.request

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="Portal Gestão de Compras | Parente Andrade",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. FUNÇÃO LOGO
@st.cache_data(ttl=86400)
def get_base64_logo(image_path="logo"):
    try:
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except: 
        return None

base64_logo = get_base64_logo()

# 3. CSS MODERNIZADO
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    div[data-testid="stElementToolbar"] { display: none !important; }
    .block-container { padding-top: 1rem !important; padding-bottom: 1rem !important; padding-left: 2rem !important; padding-right: 2rem !important; }
    .stApp { background-color: #f8fafc; font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; }
    .header-modern { background: #ffffff; padding: 16px 24px; border-radius: 12px; display: flex; align-items: center; justify-content: space-between; margin-top: 0px !important; margin-bottom: 16px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05), 0 2px 4px -1px rgba(0,0,0,0.03); }
    div[data-testid="column"] { display: flex; align-items: center; justify-content: center; }
    .center-title-container { width: 100%; text-align: center; display: flex; justify-content: center; align-items: center; }
    .portal-title { color: #1e293b !important; font-size: 38px !important; font-weight: 800 !important; margin: 0 auto !important; letter-spacing: -1px; line-height: 1; white-space: nowrap; }
    div[data-testid="stVerticalBlock"] > div:has(input), div[data-testid="stVerticalBlock"] > div:has(select), div[data-testid="stVerticalBlock"] > div:has(button) { background-color: #ffffff; padding: 2px 6px !important; border-radius: 8px; border: 1px solid #e2e8f0 !important; box-shadow: inset 0 2px 4px 0 rgba(0, 0, 0, 0.02); transition: border-color 0.2s; width: 100%; }
    div[data-testid="stVerticalBlock"] > div:has(input):focus-within, div[data-testid="stVerticalBlock"] > div:has(select):focus-within { border-color: #478c3b !important; }
    div[data-testid="stExpander"], div[data-testid="stExpander"] > div, div[data-testid="stExpander"][data-open="true"], div[data-testid="stExpander"][data-open="false"], .stElementContainer:has(div[data-testid="stExpander"]) { background-color: transparent !important; border: none !important; border-width: 0px !important; box-shadow: none !important; outline: none !important; }
    div[data-testid="stExpander"] summary, div[data-testid="stExpander"] [role="button"], .streamlit-expanderHeader { background-color: transparent !important; border: none !important; border-width: 0px !important; box-shadow: none !important; display: inline-flex !important; justify-content: flex-end !important; flex-direction: row !important; float: right !important; text-align: right !important; gap: 8px !important; width: auto !important; }
    div[data-testid="stExpander"] summary svg { transition: transform 0.2s ease-in-out !important; margin: 0 !important; padding: 0 !important; }
    div[data-testid="stExpander"] summary p, div[data-testid="stExpander"] [data-open="true"] summary p, .streamlit-expanderHeader p, .streamlit-expanderHeader:focus p { color: #1e293b !important; font-weight: 700 !important; font-size: 16px !important; margin: 0 !important; }
    div[data-testid="stExpander"] summary:hover p { color: #478c3b !important; }
    div[data-testid="stDateInput"] { width: 100%; }
    div[data-testid="stForm"] { border: none !important; padding: 0px !important; box-shadow: none !important; background-color: transparent !important; }
    .status-card { background: #ffffff; color: #1e293b; padding: 16px 24px; border-radius: 8px; font-weight: 600; font-size: 16px; border-left: 5px solid #478c3b; box-shadow: 0 1px 3px rgba(0,0,0,0.05); margin-bottom: 16px; width: 100%; }
    .custom-info-blue { background-color: #e0f2fe !important; color: #0369a1 !important; padding: 16px 24px; border-radius: 8px; font-weight: 600; font-size: 16px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); margin-bottom: 16px; width: 100%; border-left: 5px solid #0284c7; }
    .custom-error-red { background-color: #fee2e2 !important; color: #991b1b !important; padding: 16px 24px; border-radius: 8px; font-weight: 600; font-size: 16px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); margin-bottom: 16px; width: 100%; border-left: 5px solid #ef4444; }
    .custom-welcome-salutation { background-color: #ffffff; color: #1e293b; padding: 32px 24px; border-radius: 12px; font-weight: 600; font-size: 20px; text-align: center; border: 1px solid #e2e8f0; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02); margin-top: 20px; }
    div[data-testid="stDataFrame"] { background: #ffffff; padding: 16px; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); }
    div[data-testid="stDataFrame"] table th { white-space: nowrap !important; min-width: max-content !important; }
    .custom-footer-block { text-align: center !important; margin-top: 60px !important; border-top: 1px solid #e2e8f0 !important; padding-top: 24px !important; padding-bottom: 24px !important; position: static !important; clear: both !important; width: 100% !important; display: block !important; }
    .signature-fixed { position: fixed; bottom: 12px; left: 20px; color: #94a3b8; font-size: 11px; font-weight: 700; letter-spacing: 0.5px; z-index: 999999; pointer-events: none; }
    </style>
    """, unsafe_allow_html=True)

# 4. CARREGAMENTO COM ESTADO
def carregar_dados_seguros():
    file_id = "1e7pQ512ge5XMnXxsRODEO7V48KgWo6FpKeITFqBSg1o"
    URL_CSV = f"https://docs.google.com/spreadsheets/d/{file_id}/export?format=csv&gid=0"
    
    try:
        df = pd.read_csv(URL_CSV, dtype=str).fillna('')
        if "<html" in str(df.columns[0]).lower():
            raise ValueError("O Google retornou bloqueio HTML.")
        df.columns = [str(c).strip() for c in df.columns]
        return df
    except Exception as e_csv:
        try:
            URL_XLSX = f"https://docs.google.com/spreadsheets/d/{file_id}/export?format=xlsx"
            excel = pd.ExcelFile(URL_XLSX, engine='openpyxl')
            aba = "Pedidos_App" if "Pedidos_App" in excel.sheet_names else ("Pedidos" if "Pedidos" in excel.sheet_names else excel.sheet_names[0])
            df = pd.read_excel(excel, sheet_name=aba, dtype=str).fillna('')
            df.columns = [str(c).strip() for c in df.columns]
            return df
        except Exception as e_xlsx:
            st.session_state.erro_tecnico = f"CSV: {str(e_csv)} | XLSX: {str(e_xlsx)}"
            return pd.DataFrame()

if 'dados_globais' not in st.session_state:
    st.session_state.dados_globais = carregar_dados_seguros()

df_pc = st.session_state.dados_globais

# 5. CABEÇALHO INTEGRADO 
st.markdown('<div class="header-modern">', unsafe_allow_html=True)
c1, c2, c3 = st.columns([1.5, 6.5, 2.0])

with c1:
    if base64_logo: 
        st.markdown(f'<img src="data:image/png;base64,{base64_logo}" style="width:120px; display:block; margin:auto 0;">', unsafe_allow_html=True)
with c2:
    st.markdown('<div class="center-title-container"><p class="portal-title">Portal Gestão de Compras</p></div>', unsafe_allow_html=True)
with c3:
    busca = st.text_input("", placeholder="🔍 Rastrear SC, PC ou CC...", label_visibility="collapsed")
st.markdown('</div>', unsafe_allow_html=True)

# 6. FILTROS E LÓGICA DE GAVETA
if "filtro_status_val" not in st.session_state:
    st.session_state.filtro_status_val = "Todos"
if "filtro_data_val" not in st.session_state:
    st.session_state.filtro_data_val = ()
if "gaveta_aberta" not in st.session_state:
    st.session_state.gaveta_aberta = False

rotulo_seta = "Filtros Avançados ▲" if st.session_state.gaveta_aberta else "Filtros Avançados ▼"

with st.expander(rotulo_seta, expanded=st.session_state.gaveta_aberta):
    with st.form("form_filtros", clear_on_submit=False):
        f_col1, f_col2, f_col3, f_col4, f_col5 = st.columns([3.0, 3.0, 1.5, 1.5, 2.0])
        
        with f_col1:
            col_status_verificacao = next((c for c in df_pc.columns if "STATUS" in c.upper()), None) if not df_pc.empty else None
            if col_status_verificacao:
                lista_status = ["Todos"] + sorted([str(x).strip() for x in df_pc[col_status_verificacao].unique() if str(x).strip() != ""])
            else:
                lista_status = ["Todos"]
                
            idx_padrao = lista_status.index(st.session_state.filtro_status_val) if st.session_state.filtro_status_val in lista_status else 0
            filtro_status = st.selectbox("Filtrar por Status Operacional:", options=lista_status, index=idx_padrao)
            
        with f_col2:
            filtro_data = st.date_input("Filtrar por Período de Emissão:", value=st.session_state.filtro_data_val, format="DD/MM/YYYY")
            
        with f_col3:
            st.write("<div style='height: 28px;'></div>", unsafe_allow_html=True) 
            btn_pesquisar = st.form_submit_button("🔍 Pesquisar", use_container_width=True)
            
            if btn_pesquisar:
                st.session_state.filtro_status_val = filtro_status
                st.session_state.filtro_data_val = filtro_data
                st.session_state.gaveta_aberta = True  
                st.rerun()

        with f_col4:
            st.write("<div style='height: 28px;'></div>", unsafe_allow_html=True) 
            btn_limpar = st.form_submit_button("❌ Limpar", use_container_width=True)
            
            if btn_limpar:
                st.session_state.filtro_status_val = "Todos"
                st.session_state.filtro_data_val = ()
                st.session_state.gaveta_aberta = False  
                st.rerun()
                
        with f_col5:
            st.write("<div style='height: 28px;'></div>", unsafe_allow_html=True) 
            btn_atualizar = st.form_submit_button("🔄 Atualizar Banco", use_container_width=True)
            
            if btn_atualizar:
                st.session_state.dados_globais = carregar_dados_seguros()
                st.session_state.gaveta_aberta = True  
                st.rerun()

# 7. MAPEAMENTO DAS COLUNAS
DICIONARIO_COLUNAS_EXATAS = [
    {"planilha": "STATUS", "tela": "STATUS", "tipo": "texto"},
    {"planilha": "Centro de Custo", "tela": "Centro de Custo", "tipo": "texto"},
    {"planilha": "Solicitação", "tela": "Solicitação", "tipo": "texto"},
    {"planilha": "Pedido", "tela": "Pedidos", "tipo": "pedido"},   
    {"planilha": "Fornecedor", "tela": "Fornecedor", "tipo": "texto"},
    {"planilha": "Produto", "tela": "Produto", "tipo": "produto"},                 
    {"planilha": "Descricao", "tela": "Descrição", "tipo": "texto"},
    {"planilha": "Qtd", "tela": "Qtd", "tipo": "numero"},
    {"planilha": "Preço Unitário", "tela": "Preço Unitário", "tipo": "moeda"},
    {"planilha": "Valor Total", "tela": "Valor Total", "tipo": "moeda"}
]

def formatar_para_dd_mm_aaaa(valor):
    try: return pd.to_datetime(valor, errors='coerce', format='mixed').strftime('%d/%m/%Y')
    except: return valor

# 8. MOTOR DE BUSCA (Ajustado para E, H, L e exclusão de finalizados/pedidos)
if busca:
    termo = busca.lower()
    
    # Exclusão de Finalizados (coluna Status) e Pedidos preenchidos (Coluna G/índice 6)
    df_busca = df_pc.copy()
    col_status = next((c for c in df_busca.columns if "STATUS" in c.upper()), df_busca.columns[1])
    df_busca = df_busca[~df_busca[col_status].str.lower().str.contains("finalizado|concluido", na=False)]
    df_busca = df_busca[df_busca.iloc[:, 6].astype(str).str.strip() == ""]
    
    # Busca mesclada em E(4), H(7), L(11)
    indices_busca = [4, 7, 11]
    def filtrar_linhas(row):
        for idx in indices_busca:
            if idx < len(row) and termo in str(row.iloc[idx]).lower(): return True
        return False

    df_final = df_busca[df_busca.apply(filtrar_linhas, axis=1)].copy()

    if not df_final.empty:
        for col in df_final.columns:
            if any(x in col.upper() for x in ["DATA", "EMISSAO", "ENTREGA", "APROVACAO"]):
                df_final[col] = df_final[col].apply(formatar_para_dd_mm_aaaa)
        
        st.markdown(f'<div class="status-card">🔍 Pendentes encontrados: {len(df_final)}</div>', unsafe_allow_html=True)
        st.dataframe(df_final, use_container_width=True, hide_index=True)
    else:
        st.markdown('<div class="custom-error-red">⚠️ Nenhum item pendente (sem pedido) encontrado.</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="custom-welcome-salutation">👋 Olá! Seja bem-vindo ao Portal de Gestão de Compras.</div>', unsafe_allow_html=True)

# 9. RODAPÉ INSTITUCIONAL
st.markdown("<div class=\"custom-footer-block\"><p style='color:#64748b; font-size:13px; font-weight:600; margin:0;'>Parente Andrade | Coordenação de Suprimentos</p></div>", unsafe_allow_html=True)

# 10. MARCA D'ÁGUA FIXA
st.markdown('<div class="signature-fixed">Created by SS.</div>', unsafe_allow_html=True)
