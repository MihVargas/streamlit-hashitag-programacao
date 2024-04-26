import streamlit as st

st.set_page_config(page_title="Meu Site Streamlit")

# Separação site é por containers e usa o with para isso
with st.container():
    st.subheader("Meu primeiro site com o streamlit")
    st.title("Dashboard de contratos")
    st.write("Informações sobre os contratos fechados pela Hash&Co ao longo de Maio")
    st.write("Quere aprender Python? [Clique aqui](https://www.hashtagtreinamentos.com/curso-python)")

with st.container():
    st.write("---")

with st.container():
    st.write("Um teste de texto para ver atualização da pagina")
    st.title("vou escrever um titulo e ver como ele fica aqui")
    
