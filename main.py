#importação de bibliotecas
import streamlit as st
import pandas as pd
from datetime import datetime

def calc_general_stats(df:pd.DataFrame):
    df_data = df.groupby(by = "Data")[["Valor"]].sum() 
    df_data["lag_1"] = df_data["Valor"].shift(1)
    df_data["Diferença Mensal Abs."] = df_data["Valor"]- df_data["lag_1"]

    df_data["Média 6M Diferença Mensal Abs."] = df_data["Diferença Mensal Abs."].rolling(6).mean()
    df_data["Média 12M Diferença Mensal Abs."] = df_data["Diferença Mensal Abs."].rolling(12).mean()
    df_data["Média 24M Diferença Mensal Abs."] = df_data["Diferença Mensal Abs."].rolling(24).mean()

    df_data["Diferença Mensal Relativa."] = df_data["Valor"] / df_data["lag_1"] - 1

    df_data["Evolução 6M Total"] = df_data["Valor"].rolling(6).apply(lambda x: x[-1] - [0])
    df_data["Evolução 12M Total."] = df_data["Valor"].rolling(12).apply(lambda x: x[-1] - [0])
    df_data["Evolução 24M Total"] = df_data["Valor"].rolling(24).apply(lambda x: x[-1] - [0])
    
    df_data = df_data.drop("lag_1", axis = 1)

    return df_data



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

    exp3 = st.expander("Estatísticas Gerais")

    df_stats = calc_general_stats(df)
    columns_config = {
    "Diferença Mensal Abs.":st.column_config.NumberColumn("Diferença Mensal Abs.", format= "R$ %.2f"),  
    "Média 6M Diferença Mensal Abs.":st.column_config.NumberColumn("Média 6M Diferença Mensal Abs.", format= "R$ %.2f" ), 
    "Média 12M Diferença Mensal Abs.":st.column_config.NumberColumn("Média 12M Diferença Mensal Abs.", format= "R$ %.2f" ),  
    "Média 24M Diferença Mensal Abs.":st.column_config.NumberColumn("Média 24M Diferença Mensal Abs.", format= "R$ %.2f" ),   
    "Diferença Mensal Relativa.": st.column_config.NumberColumn("Diferença Mensal Relativa.", format= "percent" ),
    "Evolução 6M Total": st.column_config.NumberColumn("Evolução 6M Total", format= "R$ %.2f" ),
    "Evolução 12M Total.":st.column_config.NumberColumn("Evolução 12M Total", format= "R$ %.2f" ),
    "Evolução 24M Total": st.column_config.NumberColumn("Evolução 24M Total", format= "R$ %.2f" )
    }

    tab_stats, tab_abs, tab_rel = exp3.tabs(tabs = ["Dados", "Histórico de Evolução", "Crescimento Relativo" ])

    with tab_stats:
        st.dataframe(df_stats, column_config = columns_config) 

    with tab_abs:
        abs_cols = [       
            "Diferença Mensal Abs.",
            "Média 6M Diferença Mensal Abs.",
            "Média 12M Diferença Mensal Abs.",
            "Média 24M Diferença Mensal Abs."
        ]   
        st.line_chart(df_stats[abs_cols])

    with tab_rel:
        rel_cols = [
            "Diferença Mensal Relativa.",
            "Evolução 6M Total",
            "Evolução 12M Total.",
            "Evolução 24M Total"
        ]
        st.line_chart(df_stats[rel_cols])  
          
        
    with st.expander("Metas"):

        col1, col2 = st.columns(2)

        data_inicio_meta = col1.date_input("Início da Meta", max_value = df_stats.index.max())
        data_filtrada = df_stats.index [df_stats.index <= data_inicio_meta] [-1]

        Custos_fixos = col1.number_input("Custos Fixos", min_value = 0., format = "%.2f")
        

        Sálario_Bruto = col2.number_input("Sálario Bruto", min_value = 0., format = "%.2f")
        Sálario_Líquido = col2.number_input("Sálario Líquido", min_value = 0., format = "%.2f")
        
        valor_inicio = df_stats.loc[data_filtrada]["Valor"]
        col1.markdown(f"**Patrimônio no Início da Meta**: R$ {valor_inicio: .2f}")


        col1_pot, col2_pot = st.columns(2)
        mensal = Sálario_Líquido - Custos_fixos
        anual = mensal * 12

        
        with col1_pot.container(border = True):
            st.markdown(f"**Potencial Arrecadação Mês**: R$ {mensal: .2f}")

        with col2_pot.container(border = True):  
            st.markdown(f"**Potencial Arrecadação Anual**: R$ {anual: .2f}")
        
        

        with st.container(border = True):
            col1_meta, col2_meta = st.columns(2)
            with col1_meta:
                meta_estipulada = st.number_input("Meta Estipulada", min_value = -99999999., format = "%.2f", value = anual)

            with col2_meta:
                patrimonio_final = meta_estipulada + valor_inicio
                st.markdown(f" Patrimônio Estimado pós meta: \n\n R$ {patrimonio_final:.2f}")

 

