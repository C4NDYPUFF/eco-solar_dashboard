import streamlit as st 
import pandas as pd 
import plotly.express as px
from data_plot import plot_bar_chart, plot_pie_chart, funnel_chart,plot_day_register,plot_weekly_register
from data_config import load_url_data_to_dataframe, get_latest_registrarions
import time

def main_app():
    st.set_page_config(page_title='ECOMONDO REGISTRO DASHBOARD', layout='wide')

    st.title('ECOMONDO REGISTROS')
    st.markdown('##')

    if 'df' not in st.session_state:
        st.session_state['df'] = pd.DataFrame()
    
    if 'num-eco' not in st.session_state:
        st.session_state['num-eco'] = None
    

    if 'data_refreshed' not in st.session_state:
        st.session_state['data_refreshed'] = False

    if st.button('Cargar Datos'):
        st.session_state['data_refreshed'] = True

    # Make sure this condition correctly checks and loads the data
    if st.session_state.get('data_refreshed', False):
        try:
            df = load_url_data_to_dataframe(st.secrets['url_eco'])
            num_registrations_eco = get_latest_registrarions(df, 'fecharegistro')
            st.session_state['df'] = df
            st.session_state['num-eco'] = num_registrations_eco
        except Exception as e:
            st.error(f'Error fetching data: {e}')
        finally:
            # Always reset the data_refreshed flag after attempting to load data
            st.session_state['data_refreshed'] = False

        
    if 'data_refreshed' in st.session_state:

        df = st.session_state['df']
        num_registrations_eco = st.session_state['num-eco']

        col1, col2, = st.columns(2)

        col1.metric('Total de Registros', len(df))
        col2.metric('Registros el día de hoy', num_registrations_eco)

        # if st.button('Cambio de vista Semana/Dia'):
        #     # Use session state to store the toggle status
        #     st.session_state.toggle = not st.session_state.get('toggle', False)

        # # Default to daily view if toggle state is not set
        # view_daily = st.session_state.get('toggle', True)

        # if view_daily:
            # Plot daily data
        fig_registro = plot_day_register(df, 'fecharegistro')
        fig_registro.update_layout(
            title = 'Registros por Dia',
            yaxis_title= 'Fecha de Registro',
            xaxis_title= ''
        )
        st.plotly_chart(fig_registro, use_container_width=True)
        # else:
            # Plot weekly data
        fig_registro_week = plot_weekly_register(df, 'fecharegistro')
        fig_registro_week.update_layout(
            title= 'Registros por Semana',
            yaxis_title = 'Fecha de Registro',
            xaxis_title= ''
        )
        st.plotly_chart(fig_registro_week, use_container_width=True)



        fig_presupuesto = funnel_chart(df, 'presupuesto')

        fig_presupuesto.update_layout(
        title = 'Distribución de Presupuesto'
        )

        st.plotly_chart(fig_presupuesto, use_container_width=True)


        fig_cargo = plot_bar_chart(df, 'edad')

        fig_cargo.update_layout(
        title='Edades de los vistantes',
        xaxis_title='',
        yaxis_title='Conteo',
        legend_title_text = 'Edades'
        )

        st.plotly_chart(fig_cargo, use_container_width=True)

        fig_industria = plot_bar_chart(df, 'industria')

        fig_industria.update_layout(
            title = 'Distribución de registros por Industria',
            xaxis_title = '',
            yaxis_title = 'Conteo',
            #legend_title_text = 'Industrias'
            showlegend=False
        )
        #fig_industria.update_xaxes(showticklabels=False)

        st.plotly_chart(fig_industria, use_container_width=True)

        pie1, pie2 = st.columns(2)

        with pie1:

            fig_categoria = plot_pie_chart(df, 'categoria')
            st.plotly_chart(fig_categoria, use_container_width=True)

        with pie2:
            fig_media = plot_pie_chart(df, 'decision_compra')
            st.plotly_chart(fig_media, use_container_width=True)

        fig_producto = plot_bar_chart(df, 'industria')

        fig_producto.update_layout (
            title = 'Distribución de visitantes por producto de interés',
            xaxis_title = '',
            yaxis_title = 'Conteo',
            #legend_title_text = 'Productos de interés'
            showlegend=False
        )

        st.plotly_chart(fig_producto, use_container_width=True)


main_app()  