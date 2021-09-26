import streamlit as st
import utils

utils.initialize_session_variables()

utils.show_logo()

company, date, number_of_shares, posicao_submit_button = utils.get_position_form()

utils.add_purchase(posicao_submit_button, company, date, number_of_shares)

utils.show_wallet()

carbon_credit_button = st.button(label="Calcule métricas de carbono")

utils.calculate_carbon_credit(carbon_credit_button)
