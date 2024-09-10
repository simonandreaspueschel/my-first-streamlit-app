import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from copy import deepcopy

# Title of the app
st.title("Oktoberfest: die Daten")

st.markdown("""
**Oktoberfest 1985 - 2023**

Datensatz des Open Data Portal der Stadt München.

Abgerufen am 10. September 2024.

[Quelle](https://opendata.muenchen.de/dataset/oktoberfest/resource/e0f664cf-6dd9-4743-bd2b-81a8b18bd1d2)
""")


def load_data(path):
    df = pd.read_csv(path)
    return df

mpg_df_raw = load_data(path ="./data/raw/oktoberfestgesamt19852023.csv") #for speed

df = deepcopy(mpg_df_raw) #for security

left_column, middle_column, right_column = st.columns([3, 1, 1])

auswahl = st.radio(
    label='Wählen Sie ihre Option aus', options=['Besucher pro Jahr', 
                                                 'Bierpreis pro Jahr', 
                                                 'Hendlpreis pro Jahr', 
                                                 'Durchschnittliche Besucher pro Fest-Dauer',
                                                   'Hendl-Konsum nach Hendl-Preis',
                                                     'Bierkonsum pro Jahr nach Festdauer'])

if auswahl == 'Besucher pro Jahr':
    fig_be = px.bar(
        df, 
        x='jahr', 
        y='besucher_gesamt', 
        title='Oktoberfest: Besucher pro Jahr',
        labels={'besucher_gesamt': 'Besucher in Millionen', 'jahr': 'Jahr'},
        hover_data={
            'jahr': True,  
            'besucher_gesamt': ':.2f'  
        }
    )
    st.markdown("**Deutlich zu sehen: Die wegen Corona abgesagten Wiesn 2020 und 2021**")
    st.plotly_chart(fig_be)
    
elif auswahl == 'Bierpreis pro Jahr':
    fig_bierpreis = px.line(
        df, 
        x='jahr', 
        y='bier_preis', 
        title='Oktoberfest: Bierpreis in Euro pro Jahr',
        labels={'bier_preis': 'Bierpreis in Euro', 'jahr': 'Jahr'},
        hover_data={
            'jahr': True,  
            'bier_preis': ':.2f'  
        }
    )
    st.markdown("**Stetig steigend: Der Bierpreis lag 2023 bei durchschnittlich 14.33 Euro pro Maß Bier. Im Jahr 2024 wird die Schallmauer von 15 Euro fallen**")
    st.plotly_chart(fig_bierpreis)

elif auswahl == 'Hendlpreis pro Jahr':
    fig_hendl = px.line(
        df, 
        x='jahr', 
        y='hendl_preis', 
        title='Oktoberfest: Hendlpreis in Euro pro Jahr',
        labels={'hendl_preis': 'Hendlpreis in Euro', 'jahr': 'Jahr'},
        hover_data={
            'jahr': True,  
            'hendl_preis': ':.2f'  
        }
    )

    st.markdown("**Was erklärt den sprunghaften Anstieg von rund fünf auf fast acht Euro auf das Jahr 2000?**")
    st.plotly_chart(fig_hendl, use_container_width=True)

elif auswahl == 'Durchschnittliche Besucher pro Fest-Dauer':
    df_besucherprotag_prodauer = df.groupby('dauer')['besucher_tag'].mean().reset_index()
    fig_besu_pro_jaht = px.bar(
        df_besucherprotag_prodauer, 
        x='dauer', 
        y='besucher_tag', 
        title='Oktoberfest: Durchschnittliche Besucher pro Tag nach Dauer des Festes',
        labels={'besucher_tag': 'Durchschnittliche Besucher pro Tag', 'dauer': 'Dauer in Tagen'},
        hover_data={
            'dauer': True,  
            'besucher_tag': ':.2f'  
        }
    )

    fig_besu_pro_jaht.update_layout(
        height=800,  
        width=800, 
        bargap=0.5,  
        title={'y': 0.9, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'} 
    )
    st.markdown("**Ist die Wiesn mit 16 Tagen am kürzesten, scheinen sich die Besucher stärker zu konzentrieren. Am wenigsten pro Tag kommen, wenn es 17 Tage sind.**")
    st.plotly_chart(fig_besu_pro_jaht)


elif auswahl == 'Hendl-Konsum nach Hendl-Preis':
    hendl_nach_preis = px.scatter(
        df, 
        x='hendl_preis', 
        y='hendl_konsum',
        title='Hendl-Konsum nach Hendl-Preis',
        labels={'hendl_preis': 'Hendl-Preis in Euro', 'hendl_konsum': 'Hendl-Konsum'},
        size_max=200
    )

    hendl_nach_preis.update_layout(
        height=600, 
        width=800,  
        xaxis_title='Hendl-Preis in Euro',
        yaxis_title='Hendl-Konsum'
    )
    st.markdown("**Hendl sind immer teuer - und werden deswegen immer weniger gegessen. Oder andersrum?**")
    st.plotly_chart(hendl_nach_preis)


elif auswahl == 'Bierkonsum pro Jahr nach Festdauer':
    bierkonsum_pro_jahr_nach = px.scatter(
        df, 
        x='jahr', 
        y='bier_konsum', 
        color='besucher_gesamt', 
        title='Bierkonsum pro Jahr nach Dauer des Festes',
        labels={'jahr': 'Jahr', 'bier_konsum': 'Bier-Konsum in Hektolitern'},
        size_max=200, 
        hover_data={'jahr': True, 'bier_konsum': True, 'besucher_gesamt': True}, 
        color_continuous_scale=px.colors.sequential.Plasma
    )

    bierkonsum_pro_jahr_nach.update_layout(
        height=600, 
        width=800,  
        xaxis_title='Jahr',
        yaxis_title='Bierkonsum in Hektolitern'
    )
    st.markdown("**Der Bierkonsum steigt stetig an**")
    st.plotly_chart(bierkonsum_pro_jahr_nach)
