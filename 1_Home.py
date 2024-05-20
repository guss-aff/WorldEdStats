import pandas as pd 
from datetime import datetime
import streamlit as st
import folium
import numpy as np
import requests
from streamlit_folium import folium_static
import geopandas as gpd

st.set_page_config(
  page_title='Home',
  page_icon='🏠',
  layout='wide'
)


st.title('WorldEdStats 🎓')
st.subheader('World')
st.markdown('This application aims to present some relevant data to the global context of education.')

if 'pop' not in st.session_state:
  df_countries_pop = pd.read_csv('Data\countries-table.csv')
  st.session_state['pop'] = df_countries_pop
if 'edu' not in st.session_state:
  df_edu = pd.read_csv('Data\Global_Education.csv',encoding='Latin1')
  df_edu['Countries and areas'] =df_edu['Countries and areas'].replace('United States','United States of America' )
  df_edu['Countries and areas'] =df_edu['Countries and areas'].replace('Guinea0Bissau','Guinea Bissau' )
  df_edu = df_edu.sort_values(by='Countries and areas')
  st.session_state['edu'] = df_edu
if 'flags' not in st.session_state:
  df_flags = pd.read_csv(r'Data\flags_iso.csv')
  st.session_state['flags']=df_flags
if 'countries' not in st.session_state:
  countries = requests.get('https://raw.githubusercontent.com/python-visualization/folium-example-data/main/world_countries.json').json()
  st.session_state['countries']=countries
if 'capitals' not in st.session_state:
  df_capitals = pd.read_csv(r'Data\countries-continents-capitals.csv',encoding='Latin1')
  st.session_state['capitals'] = df_capitals
if 'world' not in st.session_state:
  df_world = pd.read_csv(fr'Data\world-population-by-country-2020.csv')
  df_world['Fert. Rate']= df_world['Fert. Rate'].str.replace('N.A.','0')
  df_world['Fert. Rate'] = df_world['Fert. Rate'].astype('float64')
  st.session_state['world']=df_world
  
df_edu = st.session_state['edu']
df_countries_pop = st.session_state['pop']
df_world = st.session_state['world']
countries = st.session_state['countries']
choices = [col for col in df_edu.columns if col not in ['Countries and areas','Latitude ','Longitude']]



#? SIDEBAR
choice = st.sidebar.selectbox('Choose the Stat',( choices))


pop23 = df_countries_pop['pop2023'].sum()
pop22 = df_countries_pop['pop2022'].sum()

growth = ((pop23-pop22)/pop22)*100
if growth>0:
  m1 = 'green'
else:
  m1='red'

#?------------------------------------------------------------------------------

col1,col2,col3 = st.columns(3)
col1.metric(
  label='World Population (2023)',
  value=f'{pop23:,}',
  delta=f'{growth:.3f}%',
  
)

col2.metric(
  label='Countries',
  value=df_edu.shape[0]
)

unemployment_rate = df_edu.Unemployment_Rate.mean()

col3.metric(
  label='Unemployment Rate',
  value=f'{unemployment_rate}%'
)

#?------------------------------------------------------------------------------
col1,col2,col3 = st.columns(3)



birth_rate = df_world['Fert. Rate'].mean()

col1.metric(
  label='Birth Rate',
  value=f'{birth_rate:.2f}'
)

secondary = df_edu.Completion_Rate_Upper_Secondary_Male.sum() + df_edu.Completion_Rate_Upper_Secondary_Female.sum()

col2.metric(
  label='Secondary Completion',
  value=f'{secondary/202:.4}%',
)

youth = df_edu.Youth_15_24_Literacy_Rate_Male.sum() + df_edu.Youth_15_24_Literacy_Rate_Female.sum()

col3.metric(
  label='Youth Literacy (15-24)',
  value=f'{youth/202:.4}%',
)

st.divider()

filtereddf =  df_edu[df_edu[choice]==df_edu[choice].max()]
country = filtereddf['Countries and areas'].iloc[0]
mmax = filtereddf[choice].iloc[0]

filtereddf1 =  df_edu[df_edu[choice]==df_edu[choice].min()]
country1 = filtereddf1['Countries and areas'].iloc[0]
mmin = filtereddf1[choice].iloc[0]

st.markdown(f'The country with the highest value {choice} is {country}, with {mmax}%.')
# st.markdown(f'The country with the lowest value {choice} is {country1}, with {mmin}%.')



m = folium.Map([0,0],zoom_start=2.2)

df_edu['name']=df_edu['Countries and areas']

folium.Choropleth(
  geo_data=countries,
  data=df_edu,
  columns=['Countries and areas',choice],
  key_on='feature.properties.name',
  fill_color='OrRd',
  nan_fill_color='blue',
  nan_fill_opacity=0.3,
  fill_opacity=0.6,
  line_weight=0.2,
  line_opacity=0.1,

).add_to(m)

geo_df = gpd.GeoDataFrame.from_features(
    countries["features"]
)
geo_df = geo_df.set_crs(4326)
df2 = geo_df.merge(df_edu,on='name',how='left')

df2 = df2.fillna(0)

tooltip = folium.GeoJsonTooltip(
    fields=["name", "Unemployment_Rate", "Birth_Rate"],
    aliases=["Country:", "Unemployment:", "Birth:"],
    localize=True,
    sticky=False,
    labels=True,
    style="""
        background-color: #F0EFEF;
        border: 2px solid black;
        border-radius: 3px;
        box-shadow: 3px;
    """,
    max_width=800,
)

folium.TileLayer('cartodbdark_matter').add_to(m)
folium.features.GeoJson(df2,
                        name='Country',
                        popup=folium.features.GeoJsonPopup(fields=['name']),
                        tooltip=tooltip
                        ).add_to(m)

folium_static(m,width=900,height=400)

st.markdown('**Obs**: Countries in blue are those that do **NOT** have available data.')

