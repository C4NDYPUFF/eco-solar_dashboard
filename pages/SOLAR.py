import streamlit as st 
import pandas as pd 
import plotly.express as px
from data_plot import plot_bar_chart, plot_pie_chart, funnel_chart, plot_day_register, plot_weekly_register
from data_config import load_url_data_to_dataframe, get_latest_registrarions


def solar_app():
    st.set_page_config(page_title='SOLAR REGISTRO DASHBOARD', layout='wide')

    st.title('SOLAR REGISTROS')
    st.markdown('##')


    if 'df_2' not in st.session_state:
        st.session_state['df_2'] = pd.DataFrame()

    if 'num-solar' not in st.session_state:
        st.session_state['num-solar'] = None
    
    if 'data_refreshed_2' not in st.session_state:
        st.session_state['data_refreshed_2'] = False

    if st.button('Cargar Datos'):
        st.session_state['data_refreshed_2'] = True
    
    if 'data_refreshed_2' not in st.session_state or st.session_state['data_refreshed_2']:
        try:
            df_solar = load_url_data_to_dataframe(st.secrets['url_solar'])
            num_registrations_solar = get_latest_registrarions(df_solar, 'fecha_registro')
            st.session_state['num-solar'] = num_registrations_solar
            st.session_state['df_2'] = df_solar
            
        except Exception as e:
            st.error(f'Error fetching data: {e}')
        finally:
            st.session_state['data_refreshed_2'] = False
        
    if 'data_refreshed_2' in st.session_state:
        df_solar = st.session_state['df_2']
        num_registrations_solar = st.session_state['num-solar']
    
        col1, col2, = st.columns(2)

        col1.metric('Total de Registros', len(df_solar))
        col2.metric('Registros el día de hoy', num_registrations_solar)

        # if st.button('Cambio de vista Semana/Dia'):
        #     # Use session state to store the toggle status
        #     st.session_state.toggle = not st.session_state.get('toggle', False)

        # # Default to daily view if toggle state is not set
        # view_daily = st.session_state.get('toggle', True)

        # if view_daily:
            # Plot daily data
        fig_registro_solar = plot_day_register(df_solar, 'fecha_registro')
        fig_registro_solar.update_layout(
            title = 'Registros por Dia',
            yaxis_title= 'Fecha de Registro'
        )
        st.plotly_chart(fig_registro_solar, use_container_width=True)
        # else:
        # Plot weekly data
        fig_registro_week_solar = plot_weekly_register(df_solar, 'fecha_registro')
        fig_registro_week_solar.update_layout(
            title= 'Registros por Semana',
            yaxis_title = 'Fecha de Registro'
        )
        st.plotly_chart(fig_registro_week_solar, use_container_width=True)



        fig_presupuesto = funnel_chart(df_solar, 'presupuesto')

        fig_presupuesto.update_layout(
        title = 'Distribución de Presupuesto'
        )

        st.plotly_chart(fig_presupuesto, use_container_width=True)


        fig_cargo = plot_bar_chart(df_solar, 'edad')

        fig_cargo.update_layout(
        title='Edades de los vistantes',
        xaxis_title='',
        yaxis_title='Conteo',
        legend_title_text = 'Edades'
        )

        st.plotly_chart(fig_cargo, use_container_width=True)

        fig_industria = plot_bar_chart(df_solar, 'industria')
        
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

            fig_categoria = plot_pie_chart(df_solar, 'categoria')
            st.plotly_chart(fig_categoria, use_container_width=True)
        
        with pie2:
            fig_media = plot_pie_chart(df_solar, 'como_se_entero')
            st.plotly_chart(fig_media, use_container_width=True)

        fig_producto = plot_bar_chart(df_solar, 'producto_de_interesdes')

        fig_producto.update_layout (
            title = 'Distribución de visitantes por producto de interés',
            xaxis_title = '',
            yaxis_title = 'Conteo',
            #legend_title_text = 'Productos de interés'
            showlegend=False
        )

        st.plotly_chart(fig_producto, use_container_width=True)


solar_app()