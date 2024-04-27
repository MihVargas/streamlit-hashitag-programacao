import streamlit as st
import pandas as pd
import locale

st.title("Análise de Vendas")
locale.setlocale(locale.LC_TIME, 'Portuguese_Brazil')

#@st.cache_data
def carrega_dataset():
    # Definindo os tipos de dados durante a leitura do CSV para eficiência
    dtypes = {
        "Postal_Code": 'float',  # Se Postal_Code não precisar de precisão inteira
        "Region": 'category',
        "Category": 'category',
        "State": 'category'
    }
    df = pd.read_csv(r"Data\Sales_Store_overview.csv", dtype=dtypes, encoding='utf-8')

    date_cols = ['Order_Date', 'Ship_Date']
    for col in date_cols:
        df[col] = pd.to_datetime(df[col])

    df["Postal_Code"] = pd.to_numeric(df["Postal_Code"], errors='coerce').astype('Int64')
    df['name_month'] = df['Order_Date'].dt.strftime('%B')
    df['num_month'] = df['Order_Date'].dt.month
    df['year'] = df['Order_Date'].dt.to_period('Y')
    df["mes_rotulo"] = df['num_month'].astype(str).apply(lambda x: x.zfill(2)) + ' - ' + df['name_month']
    
    return df

def df_novo(df, list_coluns):
    # Selecionando as colunas desejadas para o novo DataFrame
    colunas = list_coluns
    novo_df = df[colunas].copy()
    
    return novo_df


with st.container():
    # Carrega os dados
    dados = carrega_dataset()

    #Cria um df agrupado que só tem algumas colunas
    df_agrupado = (
        df_novo(dados, ['name_month', 'Category', 'Sales', 'year', 'num_month', "mes_rotulo"])
        )

    # Cria um df com todos os anos
    df_anos = df_novo(dados, ['year'])

    # Cria um df com todos os meses e adiciona o mes 0 que seria TODOS
    df_mes = df_novo(dados, ['name_month', 'num_month'])

    # Para criar um linha nova, precisei criar um novo df com essa linhas e depois concatenar
    # os valores
    novo_dado = pd.DataFrame([{'name_month': 'Todos', 'num_month': 0}])
    df_mes = pd.concat([df_mes, novo_dado], ignore_index=True).sort_values(by='num_month')
    

    # Crio os filtros 
    #ano_selecionado = st.selectbox("Selecione o Ano", df_anos["year"].unique())
    ano_selecionado = st.radio("Selecione o Ano", df_anos["year"].unique())
    mes_selecionado = st.radio("Selecione o Mes", df_mes["name_month"].unique(), horizontal=True)

    # Regras para os filtro
    if mes_selecionado == "Todos":
        df_agrupado = (
            df_agrupado[(df_agrupado["year"] == ano_selecionado)]
            )
    else:
        df_agrupado = (
            df_agrupado[(df_agrupado["year"] == ano_selecionado)
            & (df_agrupado["name_month"] == mes_selecionado)]
            )

    aggregated_data = (
        df_agrupado
        .groupby(['mes_rotulo', 'Category'])['Sales'].sum().reset_index()
        )

    st.write("---")

    # Criação do gráfico de barras
    st.bar_chart(aggregated_data, x="mes_rotulo", y="Sales", color="Category")