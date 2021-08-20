import io

import streamlit as st
import plotly.express as px
from comtrade import Comtrade

import constants as C
from cleaner import clean_entry
from classify import inrush_classifier

st.set_page_config(
    page_title=C.TITLE,
    page_icon=C.ICON_URL,
)

# Display header.
f"""
# {C.TITLE}
### **Nota**: Los archivos deben tener encoding UTF-8 para que el clasificador pueda dar resultados.
"""

with st.sidebar.subheader("Subir archivos"):
    uploaded_files = st.sidebar.file_uploader(
        C.FILE_UPLOADER_TITLE,
        type=[C.CFG, C.DAT],
        accept_multiple_files=True,
    )

st.sidebar.subheader(C.SIGNALS_PICKER_HEADER)
first_signal = st.sidebar.number_input("Señal A", min_value=1, value=1, step=1)

if len(uploaded_files) == 2:
    comtrade_reader = Comtrade()
    input_errors = []
    try:
        cfg_file = next(
            file for file in uploaded_files if file.name.lower().endswith(f".{C.CFG}")
        )
    except StopIteration:
        input_errors.append(C.CFG_ERROR)
    try:
        dat_file = next(
            file for file in uploaded_files if file.name.lower().endswith(f".{C.DAT}")
        )
    except StopIteration:
        input_errors.append(C.DAT_ERROR)

    if not input_errors:
        cfg_content = io.TextIOWrapper(cfg_file)
        dat_content = io.TextIOWrapper(dat_file)

        comtrade_reader.read(cfg_content, dat_content)

        df = clean_entry(comtrade_reader, first_signal, "FILE_1")

        classification = inrush_classifier(df)
        result = C.RESULTS[classification]
        st.markdown(
            f"<h3>Clasificación: {result}</h3>", unsafe_allow_html=True
        )

        fig = px.line(df, x=C.TIME, y=C.VALUE, color=C.CHANNEL)
        fig.update_layout(
            template="simple_white",
            legend_title=C.PLOT_TITLE,
            xaxis_title=C.X_AXIS_TITLE,
            yaxis_title=C.Y_AXIS_TITLE,
            title=C.PLOT_TITLE,
            hovermode="x",
        )
        st.plotly_chart(fig)

        st.markdown(f"<h3>{C.TABLE_TITLE}</h3>", unsafe_allow_html=True)

        st.write(df.groupby(C.CHANNEL).Value.describe())
    else:
        st.error("\n".join(input_errors))
else:
    fig = px.line({})
    st.plotly_chart(fig)

# Streamlit widgets automatically run the script from top to bottom. Since
# this button is not connected to any other logic, it just causes a plain
# rerun.
st.button("Re-run")
