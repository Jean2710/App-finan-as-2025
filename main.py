#importação de bibliotecas
import streamlit as st
import pandas as pd
from datetime import datetime
#Configuração da página
st.set_page_config(page_title="Finanças", page_icon= '💰')

st.markdown('''
     # BOAS VINDAS!
            
     ## NOSSO APP FINANCEIRO

     Espero que você possa ter uma excelente experiência de solução financeira 💫
            
''')

#widget de Upload de dados do usuário
file_upload=st.file_uploader(label="Faça upload dos dados aqui", type=['csv'])

#verifica se algum upload foi feito
if file_upload: 
    
    #leitura dos dados
    df = pd.read_csv(file_upload)
    df["Data"] = pd.to_datetime(df["Data"], format="mixed", dayfirst=True).dt.date
    #exibição dos dados no app
    exp1 = st.expander("Dados Brutos")
    columns_format = {"Valor": st.column_config.NumberColumn("Valor", format= "R$ %f" )}
    exp1.dataframe(df, hide_index=True, column_config=columns_format)

#Visão intituição, forma pivotada
    exp2 = st.expander("Visão Instituição")
    df_instituição = df.pivot_table(index="Data",columns="Instituição", values = "Valor")
    tab_data,tab_history, tab_share = exp2.tabs(["Dados", "Histórico", "Distribuição"])

#Criação de abas para a visão instituição
#Exibe dataframe    
    with tab_data:
        st.dataframe(df_instituição)

#Exibe gráfico de linha da visão instituição
    with tab_history:
        st.line_chart(df_instituição)

#Exibe distribuição dos dados da visão instituição
    with tab_share:
# Exibe um seletor de data       
        date = st.selectbox("Filtro Data", options=df_instituição.index)

#Exibe o gráfico de barras para a data selecionada
        st.bar_chart(df_instituição.loc[date])
        

        
             
        



 

