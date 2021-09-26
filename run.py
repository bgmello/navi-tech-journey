import streamlit as st
from PIL import Image

import home
import prediction

PAGES = {
    "Custo de carbono da carteira": home,
    "Predição do custo de carbono de um ativo": prediction,
}

st.set_page_config(layout="wide")

img = Image.open("assets/logo.png")
st.sidebar.image(img)

selection = st.sidebar.radio("Ir para", list(PAGES.keys()))
page = PAGES[selection]
page.app()
