# Importar paquetes/modulos/bibliotecas
#################################################################################
import pandas as pd
import plotly.express as px
import streamlit as st

# Funciones
#################################################################################


def get_coutn_values(car_data: pd.DataFrame, idx: list, vals: list):
    pivot_cars = car_data.pivot_table(index=idx,
                                      values=vals,
                                      aggfunc=['count', 'sum']).reset_index()
    return pivot_cars


def get_brand(car_data: pd.DataFrame) -> list:
    res = []
    aux = []
    for model in car_data['model']:
        aux = model.split(' ', 1)
        res.append(aux[0])
        aux = []
    return res


def get_brand_s(car_data: pd.DataFrame) -> list:
    res = []
    aux = []
    for model in car_data:
        aux = model.split(' ', 1)
        res.append(aux[0])
        aux = []
    return res


def hist_Create(car_data: pd.DataFrame, brand1: str, brand2: str, column: str) -> pd.DataFrame:
    df_1 = car_data[car_data['brand'] == brand1][column]
    df_2 = car_data[car_data['brand'] == brand2][column]

    show_df = pd.concat([df_1, df_2])

    return show_df


def hist_Create_df(car_data: pd.DataFrame, brand1: str, brand2: str) -> pd.DataFrame:
    df_1 = car_data[car_data['brand'] == brand1]
    df_2 = car_data[car_data['brand'] == brand2]

    show_df = pd.concat([df_1, df_2])
    # show_df.reset_index(drop=True)

    return show_df


# Global variables
#################################################################################
l_hist = False
hist = False
disperssion = False

# ck_hist_1 = 'bmw'
# ck_hist_2 = 'bmw'

# Data management
#################################################################################


# leer los datos
car_data = pd.read_csv('vehicles_us.csv')

# Creamos la columna para almacenar la marca del vehículo
car_data['brand'] = get_brand(car_data)

# Creamos un dataframe para agrupar la cantidad de carros vendidos por marca
# y tipo
brand_type_grp = get_coutn_values(car_data, ['brand', 'type'], ['price'])
brand_type_grp.columns = ['brand', 'type', 'count', 'sales']

# Creamos un dataframe para agrupar los precios por modelo
model_type_grp = get_coutn_values(car_data, ['model', 'type'], ['price'])
model_type_grp.columns = ['model', 'type', 'count', 'sales']
model_type_grp['brand'] = get_brand(model_type_grp)

# Guardamos en una lista las marcas existentes
brands = car_data['brand'].unique()

# Streamlit objects
#################################################################################

#       Builder
# ----------------------------------
st.header('DATA VIEWER',
          divider='rainbow')
# Mostrar el dataframe como una tabla
st.dataframe(car_data)
# st.dataframe(model_type_grp)
# st.dataframe(hist_df)

# st.dataframe(pivot_cars)

st.header('Informative charts',
          divider='rainbow')
# crear una casilla de verificación
build_long_hist = st.checkbox('Deploy bar charts with Long Format Data')

# crear un botón
# hist_button = st.button('Construir histograma')

# crear un botón
# disp_button = st.button('Construir diagrama de dispersión')

#       Graphs
# ----------------------------------
if build_long_hist:  # si la casilla de verificación está seleccionada
    # crear un histograma
    st.write('Creación de una gráfica de carros vendidos por marca y modelo')
    fig_l = px.histogram(brand_type_grp, x="brand", y="count", color="type")

    fig_l.update_layout(
        title_text='Sold cars per model and brand',  # title of plot
        xaxis_title_text='Cars model-brand',  # xaxis label
        yaxis_title_text='Count',  # yaxis label
    )

    # mostrar un gráfico Plotly interactivo
    st.plotly_chart(fig_l, use_container_width=True)
    st.write('Note: Building a bar chart with Long Format Data')

#       Builder
# ----------------------------------
st.header(' ', divider='rainbow')

st.write("Select a chart to deploy:")
option = st.selectbox(
    "Which graph do you want to display?",
    # ("- Select a chart -", "Sold cars per brand", "Histogram", "Dispesion chart"))
    ("- Select a chart -", "Histogram", "Dispesion chart"))

# st.write("You selected:", option)

match option:

    case "Histogram":
        hist = True

    case "Dispesion chart":
        disperssion = True

    case _:
        st.write("No chart selected.")


#       Graphs
# ----------------------------------

if hist:  # al hacer clic en el botón
    # escribir un mensaje
    st.write(
        'Creación de un histograma para el conjunto de datos de anuncios de venta de coches')
    # crear un histograma
    fig_o = px.histogram(car_data, x="odometer")

    fig_o.update_layout(
        title_text='Odometer histogram',  # title of plot
        xaxis_title_text='Odometer',  # xaxis label
        yaxis_title_text='Count',  # yaxis label
    )

    # mostrar un gráfico Plotly interactivo
    st.plotly_chart(fig_o, use_container_width=True)
    # st.plotly_chart(fig2, use_container_width=True)

if disperssion:  # al hacer clic en el botón
    # escribir un mensaje
    st.write('Creación de un diagrama de dispersión para el conjunto de datos de anuncios de venta de coches')

    # crear un gráfico de dispersión
    fig_d = px.scatter(car_data, x="odometer", y="price")

    fig_d.update_layout(
        title_text='Price vs Odometer chart',  # title of plot
        yaxis_title_text='Price in thousands of dollars',  # xaxis label
        xaxis_title_text='Odometer',  # yaxis label
    )

    # mostrar un gráfico Plotly interactivo
    st.plotly_chart(fig_d, use_container_width=True)

#       Builder
# ----------------------------------
st.header(' ', divider='rainbow')

st.write("Select a chart to deploy:")
ck_hist_1 = st.selectbox(
    "Select the firt brand to compare:",
    (brands))

st.write("Select a chart to deploy:")
ck_hist_2 = st.selectbox(
    "Select the second brand to compare:",
    (brands))

#       Graphs
# ----------------------------------
st.write('Creación de un histograma para el conjunto de datos de anuncios de venta de coches')

# Data management
#################################################################################
hist_df = hist_Create_df(car_data, ck_hist_1, ck_hist_2)
hist_df.reset_index(inplace=True)

# Streamlit objects
#################################################################################
# crear un histograma
fig_h = px.histogram(hist_df, x='price', color='brand')

fig_h.update_layout(
    title_text='Prices histogram ' + ck_hist_1 + ' and ' +
    ck_hist_2 + ' comparison',  # title of plot
    xaxis_title_text='Price in thousands of dollars',  # xaxis label
    yaxis_title_text='Frequency',  # yaxis label
)

st.plotly_chart(fig_h, use_container_width=True)
