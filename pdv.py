import streamlit as st
import pandas as pd
import datetime
import plotly.express as px

# Configuración inicial
st.set_page_config(page_title="PDV Bazzar Poniente", layout="wide")

# Estado inicial de la aplicación
if "sales_data" not in st.session_state:
    st.session_state.sales_data = pd.DataFrame(columns=["Producto", "Precio", "Fecha"])

if "selected_date" not in st.session_state:
    st.session_state.selected_date = datetime.date.today()

if "quick_notes" not in st.session_state:
    st.session_state.quick_notes = []

# Función para agregar ventas
def add_sale(product, price):
    new_sale = {"Producto": product, "Precio": price, "Fecha": st.session_state.selected_date}
    st.session_state.sales_data = pd.concat(
        [st.session_state.sales_data, pd.DataFrame([new_sale])], ignore_index=True
    )

# Función para agregar una nota rápida
def add_note(note):
    if note:
        st.session_state.quick_notes.append(note)

# Sidebar para seleccionar el día de la semana
st.sidebar.title("Calendario Semanal")
week_days = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
selected_day = st.sidebar.radio("Selecciona el día", week_days)

# Actualizar la fecha seleccionada según el día
current_weekday = datetime.date.today().weekday()
selected_date = datetime.date.today() + datetime.timedelta(days=week_days.index(selected_day) - current_weekday)
st.session_state.selected_date = selected_date

# Título principal
st.title("PDV Bazaar Poniente")
st.write(f"**Día seleccionado:** {selected_day}, {st.session_state.selected_date}")

# Contenedor para el registro de ventas
with st.container():
    st.header("Registrar Venta")

    # Productos disponibles
    products = ["Falda", "Blusa", "Pantalón", "Vestido", "Camisa"]
    selected_product = st.selectbox("Selecciona un producto", products + ["Otro"])

    if selected_product == "Otro":
        selected_product = st.text_input("Ingresa el nombre del producto")

    # Precio de venta
    price = st.number_input("Precio de venta", min_value=0.0, step=0.5)

    # Botón para agregar venta
    if st.button("Agregar Venta"):
        if selected_product and price > 0:
            add_sale(selected_product, price)
            st.success(f"Venta registrada: {selected_product} por ${price:.2f}")
        else:
            st.error("El producto y el precio deben ser válidos.")

# Contenedor para mostrar ventas del día
with st.container():
    st.header("Ventas del Día")

    # Filtrar datos por la fecha seleccionada
    daily_sales = st.session_state.sales_data[
        st.session_state.sales_data["Fecha"] == st.session_state.selected_date
    ]

    # Mostrar tabla de ventas
    if not daily_sales.empty:
        st.subheader("Tabla de Ventas")
        st.dataframe(daily_sales)

        # Gráfico de barras
        st.subheader("Gráfico de Ventas")
        sales_summary = daily_sales.groupby("Producto")["Precio"].sum().reset_index()
        fig = px.bar(sales_summary, x="Producto", y="Precio", title="Ventas por Producto", text="Precio",
                     color="Producto", color_discrete_sequence=px.colors.qualitative.Pastel)
        fig.update_traces(texttemplate='$%{text:.2f}', textposition='outside')
        fig.update_layout(yaxis_title="Total Vendido", xaxis_title="Producto", template="plotly_white")
        st.plotly_chart(fig)
    else:
        st.info("No hay ventas registradas para este día.")

# Contenedor para la vista semanal
with st.sidebar.expander("Resumen Semanal"):
    st.header("Resumen de la Semana")
    weekly_sales = st.session_state.sales_data[
        st.session_state.sales_data["Fecha"].between(
            st.session_state.selected_date - datetime.timedelta(days=st.session_state.selected_date.weekday()),
            st.session_state.selected_date + datetime.timedelta(days=6 - st.session_state.selected_date.weekday()),
        )
    ]

    if not weekly_sales.empty:
        weekly_summary = weekly_sales.groupby("Producto")["Precio"].sum().reset_index()
        weekly_fig = px.bar(
            weekly_summary, x="Producto", y="Precio", title="Ventas Semanales", text="Precio",
            color="Producto", color_discrete_sequence=px.colors.qualitative.Vivid
        )
        weekly_fig.update_traces(texttemplate='$%{text:.2f}', textposition='outside')
        weekly_fig.update_layout(yaxis_title="Total Vendido", xaxis_title="Producto", template="plotly_white")
        st.plotly_chart(weekly_fig)
    else:
        st.info("No hay ventas registradas para esta semana.")

# Contenedor para notas rápidas
with st.container():
    st.header("Notas Rápidas")
    note = st.text_input("Escribe una nota rápida")
    if st.button("Agregar Nota"):
        add_note(note)
        st.success("Nota agregada.")

    if st.session_state.quick_notes:
        st.subheader("Notas Guardadas")
        for i, saved_note in enumerate(st.session_state.quick_notes):
            st.write(f"{i + 1}. {saved_note}")
