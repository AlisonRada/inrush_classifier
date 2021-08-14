import io
import time

import streamlit as st
import plotly.express as px
import pandas as pd
from comtrade import Comtrade

from cleaner import read_comtrade, clean_entry

ICON_URL = 'energy.png'
title = 'Detección de Inrush'
results = {
    'error': '🔴',
    'normal': '🟢'
}

st.set_page_config(
    page_title=title, page_icon=ICON_URL,
)

# Display header.
#st.markdown(f"<h1>{title}</h1>", unsafe_allow_html=True)
f"""
# {title}
### **Nota**: Los archivos deben tener encoding UTF-8 para que el clasificador pueda dar resultados.
"""

with st.sidebar.subheader('Subir archivos'):
    uploaded_files = st.sidebar.file_uploader("Por favor, subir los archivos COMTRADE: cfg, dat", \
    type=["cfg", "dat"], accept_multiple_files=True)
st.sidebar.subheader("Señales de interés")
first_signal = st.sidebar.number_input('Señal A', min_value=1, value=1, step=1)
#print(f"{signal_a}, {signal_b}, {signal_c}")
st.sidebar.subheader("")
st.sidebar.write("&nbsp[![See source](https://img.shields.io/badge/Buy_Me_A_Coffee-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://github.com/AlisonRada/inrush_classifier)")
st.sidebar.subheader("")
if st.sidebar.button("Clear Cache"):
    st.caching.clear_cache()
    st.sidebar.success("Cache is cleared!")


if len(uploaded_files) == 2:
    # if ['.cfg' in a or '.CFG' in a for a in uploaded_files] == [] or \
    # ['.dat' in a or '.DAT' in a for a in uploaded_files] == []:
    comtrade_reader = Comtrade()
    cfg_file = [file for file in uploaded_files if '.CFG' in file.name or '.cfg' in file.name][0]
    dat_file = [file for file in uploaded_files if '.DAT' in file.name or '.dat' in file.name][0]

    cfg_content = io.TextIOWrapper(cfg_file)
    dat_content = io.TextIOWrapper(dat_file)
    
    comtrade_reader.read(cfg_content, dat_content)

    df = clean_entry(comtrade_reader, first_signal, 'FILE_1')
            
    result = results['normal']
    st.markdown(f"<h3>Clasificación: {result}</h3>", unsafe_allow_html=True)

    fig = px.line(df, x='Time', y='Value', color='Channel')
    fig.update_layout(template='simple_white',
                      legend_title='Señales',
                      xaxis_title='Tiempo (m/s)',
                      yaxis_title='Voltaje (A)',
                      title='Señales',
                      hovermode="x"
                      )
    st.plotly_chart(fig)

    st.markdown("<h3>Estadísticos</h3>", unsafe_allow_html=True)

    st.write(df.groupby('Channel').Value.describe())
else:
    fig = px.line({})
    st.plotly_chart(fig)

progress_bar = st.sidebar.progress(0)
status_text = st.sidebar.empty()

for i in range(1, 101):
    status_text.text("%i%% Complete" % i)
    progress_bar.progress(i)
    time.sleep(0.05)

progress_bar.empty()

# Streamlit widgets automatically run the script from top to bottom. Since
# this button is not connected to any other logic, it just causes a plain
# rerun.
st.button("Re-run")
