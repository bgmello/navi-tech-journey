import streamlit as st

from home import HomePage

# Instancia classe da pagina home
home_page = HomePage()

# Inicializa variaveis da sessao
home_page.initialize_session_variables()

# Mostra logo da navi
home_page.show_logo()

# Pega informacoes de posicao da carteira a partir do form
company, date, number_of_shares, posicao_submit_button = home_page.get_position_form()

# Adiciona posicao na carteira
home_page.add_purchase(posicao_submit_button, company, date, number_of_shares)

# Mostra a carteira
home_page.show_wallet()

# Cria botao para calcular metricas
metrics_button = st.button(label="Calcule métricas de carbono")

# Mostra as metricas calculadas
home_page.show_metrics(metrics_button)
