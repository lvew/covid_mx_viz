import markdown
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from plotly import express as px
from plotly.subplots import make_subplots
from datetime import date

today = date.today()

st.set_page_config(
    layout="wide",
)

st.title("COVID-19 en México")

# Dataframes
death1 = pd.read_csv("dat/death1.csv")
contagios = pd.read_csv("dat/contagios.csv")
contagios_estatal = pd.read_csv("dat/contagios_estatal.csv")
muertes_estatal = pd.read_csv("dat/defunciones_estatal.csv")
contagsemanal = contagios.groupby("semana")["Casos diarios"].sum().reset_index()
semana_entidad = contagios_estatal.groupby("semana").sum().reset_index()
death2 = death1.groupby("semana")["Casos diarios"].sum().reset_index()
muerte_semana_entidad = muertes_estatal.groupby("semana").sum().reset_index()


@st.experimental_memo
# Función para los datos Nacionales
def graph_nac(base, tiempo: str):
    fig = px.bar(
        base,
        x=f"{tiempo}",
        y="Casos diarios",
        text="Casos diarios",
        title="Nacional",
        labels={"Casos diarios": "", f"{tiempo}": ""},
        width=1200,
        height=600,
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(10,10,10,0)",
    )
    if (base is death1) or (base is death2):
        fig.update_traces(marker_color="gray")
    return fig


# Función para graficar todos los estados
def graph_tot(base, tiempo: str):
    # Esta función grafica en plotly los casos a nivel estado
    # plotly setup
    plot_rows = 8
    plot_cols = 4

    fig = make_subplots(
        rows=plot_rows,
        cols=plot_cols,
        subplot_titles=base.columns[1:],
    )

    # add traces
    x = 1
    for i in range(1, plot_rows + 1):
        for j in range(1, plot_cols + 1):
            # print(str(i)+ ', ' + str(j))
            fig.add_trace(
                go.Bar(
                    x=base[f"{tiempo}"],
                    y=base[base.columns[x]].values,
                ),
                row=i,
                col=j,
            )

            x = x + 1

    # Format and show fig
    fig.update_layout(
        showlegend=False,
        height=1200,
        width=1200,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(10,10,10,0)",
    )
    if tiempo == "semana":
        fig.update_xaxes(tickangle=45, tickfont=dict(size=5))

    return fig


# Función para graficar entidad por entidad
def graph_estatal(base, tiempo: str, entidad: str):
    fig = px.bar(
        base,
        x=f"{tiempo}",
        y=f"{entidad}",
        text=f"{entidad}",
        title=f"{entidad}",
        labels={f"{tiempo}": ""},
        width=1000,
        height=400,
    )
    if (base is muertes_estatal) or (base is muerte_semana_entidad):
        fig.update_traces(marker_color="gray")
    return fig


# Barra lateral.
st.sidebar.title("Menú")
selection = st.sidebar.radio(
    "",
    [
        "Positivos diarios",
        "Positivos semanales",
        "Defunciones diarias",
        "Defunciones semanales",
    ],
)
with st.sidebar.expander("Click para conocer más de estas gráficas"):
    st.markdown(
        f"""
    Desarrollé esta app para tener una vista rápida de las tendencias de COVID-19 en México. 
    Algunos aspectos a considerar:
    - La fuente de los datos es la 
    [Secretaría de Salud Federal.](https://www.gob.mx/salud/documentos/datos-abiertos-bases-historicas-direccion-general-de-epidemiologia?idiom=es)
    
    - Están graficadas las **frecuencias totales** Por eso, cada gráfica tiene su propio eje. 
    Para realizar comparaciones, se podría usar otras métricas, por ejemplo la tasa de positivos/defunciones 
    por cien mil habitantes.

    - En el caso de los casos positivos, estoy graficando respecto **al día que se presentaron síntomas**.

    - Otros sitios muy útiles son los generados por el [Conacyt](https://salud.conacyt.mx/coronavirus/), 
    [SINAVE](https://covid19.sinave.gob.mx/) o el [tablero de Conacyt](https://datos.covid-19.conacyt.mx/)
     que se ubica en el micro sitio de COVID-19 de de la propia Secretaría de Salud.
    Para CDMX, el sitio del [Gobierno local](https://covid19.cdmx.gob.mx/) es imprescindible.

    - Debido al tamaño de la base de datos, aquí solo se usan subconjuntos de la base principoal

    📪 **[@l_venegas](https://twitter.com/l_venegas)**

    *Última actualización: {str(today)}.*  
    """
    )

if selection == "Positivos diarios":
    # Casos positivos diarios, por fecha de síntomas
    st.subheader("Casos positivos diarios, por fecha de síntoma")

    # Nacional
    st.plotly_chart(graph_nac(contagios, "Fecha"))

    # Cada entidad
    st.subheader("Casos positivos diarios, por entidad")
    entidades = contagios_estatal.columns[1:33]
    entidad = st.selectbox("Selecciona una entidad:", entidades)
    if entidad == (f"{entidad}"):
        st.plotly_chart(graph_estatal(contagios_estatal, "Fecha", f"{entidad}"))

    # Todas entidades.
    st.subheader("Casos positivos diarios, todas las entidades")

    st.plotly_chart(graph_tot(contagios_estatal, "Fecha"))

elif selection == "Positivos semanales":
    # Casos positivos semanal, por fecha de síntomas
    st.subheader("Casos positivos semanales, por fecha de síntoma")

    # Nacional
    st.plotly_chart(
        graph_nac(
            contagsemanal,
            "semana",
        )
    )

    # Cada entidad
    st.subheader("Casos positivos semanales, por entidad")
    entidades = contagios_estatal.columns[1:33]
    entidad = st.selectbox("Selecciona una entidad:", entidades)
    if entidad == (f"{entidad}"):
        st.plotly_chart(graph_estatal(semana_entidad, "semana", f"{entidad}"))

    # Por entidad.
    st.subheader("Casos positivos semanales, todas las entidades")
    st.plotly_chart(graph_tot(semana_entidad, "semana"))

elif selection == "Defunciones diarias":
    # Defunciones nacionales diarias
    st.subheader("Defunciones diarias")

    # Nacional
    st.plotly_chart(graph_nac(death1, "Fecha"))

    # Cada entidad
    st.subheader("Defunciones diarias, por entidad")
    entidades = contagios_estatal.columns[1:33]
    entidad = st.selectbox("Selecciona una entidad:", entidades)
    if entidad == (f"{entidad}"):
        st.plotly_chart(graph_estatal(muertes_estatal, "Fecha", f"{entidad}"))

    # Por entidad
    st.subheader("Defunciones diarias, por entidad")
    st.plotly_chart(graph_tot(muertes_estatal, "Fecha"))

elif selection == "Defunciones semanales":
    # Defunciones nacionales semanales
    st.subheader("Defunciones semanales")

    # Nacional
    st.plotly_chart(graph_nac(death2, "semana"))

    # Cada entidad
    st.subheader("Defunciones semanales, por entidad")
    entidades = contagios_estatal.columns[1:33]
    entidad = st.selectbox("Selecciona una entidad:", entidades)
    if entidad == (f"{entidad}"):
        st.plotly_chart(graph_estatal(muerte_semana_entidad, "semana", f"{entidad}"))

    # Por entidad
    st.subheader("Defunciones semanales, todas las entidades")
    st.plotly_chart(graph_tot(muerte_semana_entidad, "semana"))
