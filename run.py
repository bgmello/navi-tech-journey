import streamlit as st
from PIL import Image

import home
import prediction

PAGES = {
    "Custo de carbono da carteira": home,
    "Predição do custo de carbono de um ativo": prediction,
}

# Configura a pagina para layout grande
st.set_page_config(layout="wide")

# Pega logo da navi
img = Image.open("assets/logo.png")
st.sidebar.image(img)

# Selecao de qual aba do sistema o usuario ira usar
selection = st.sidebar.radio("Ir para", list(PAGES.keys()))
page = PAGES[selection]
page.app()
