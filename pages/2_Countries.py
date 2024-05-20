import streamlit as st
import matplotlib.pyplot as plt
import geopandas as gpd 
import plotly.express as px

st.set_page_config(
  page_title='Countries',
  page_icon='🌍',
  layout='wide'
)

st.title('WorldEdStats 🎓')
st.subheader('Countries')


df_edu = st.session_state['edu']
df_countries_pop = st.session_state['pop']
countries = st.session_state['countries']
df_world = st.session_state['world']
df_flags = st.session_state['flags']
df_capitals = st.session_state['capitals']


lst_cnt = df_edu['Countries and areas'].sort_values( ascending=False).value_counts().index
# lst_cnt
country = st.sidebar.selectbox('Select the country',(lst_cnt))
col1,col2,col3 = st.columns(3)



try:
  
  flag = df_flags[df_flags['Country']==country]
  flag1 = flag['URL'].iloc[0]
  col1.image(flag1,width=150)
  
  col1.markdown(f"#### {country} ({flag['Alpha-3 code'].iloc[0]})")
except:
  col1.markdown(f"#### {country}")
  col1.write('Flag not found')


try:
  capital = df_capitals[df_capitals['Country/Territory']==country]
  continent = capital['Continent'].iloc[0]
  capital = capital['Capital'].iloc[0]

  col1.markdown(f'**Capital:** {capital}')
  col1.markdown(f'**Continent:** {continent}')
except: pass


# col1.markdown()
try:
  geo_df = gpd.GeoDataFrame.from_features(
      countries["features"]
  )
  geo_df = geo_df.set_crs(4326)

  plt.style.use('dark_background')
  fig, ax = plt.subplots(figsize=(0.5,0.5))
  ax.set_facecolor('green')
  ax.set_axis_off()
  geo_df = geo_df[geo_df['name']==country]

  geo_df.plot(ax=ax,color='white',linewidth=0.2,edgecolor='black')
  with col3.container(height=375):
    st.pyplot(plt,transparent=True,clear_figure=True)
  
except:
  col3.write('Geogriphcal Data not Found')
  
st.divider()
st.markdown('#### General Stats')
col1,col2=st.columns(2)
try:
  land = df_world[df_world['Country (or dependency)']==country]
  land_area = land['Land Area (Km²)'].iloc[0]
  pct_change = land['Yearly Change'].iloc[0]
  density = land['Density  (P/Km²)'].iloc[0]
  world_share = land['World Share'].iloc[0]
  col1.markdown(f'**Land Area:** {land_area} km²')
  col1.markdown(f'**Yearly Change:** {pct_change}')
  
  col2.markdown(f'**Density:** {density} P/Km²')
  col2.markdown(f'**World Share:** {world_share}')
  
  
except: 
  st.write('Data not found')



try:
  st.divider()
  col1,col2,col3=st.columns(3)

  pop22 = df_countries_pop[df_countries_pop['country']==country]
  # pop22
  pop23 = pop22['pop2023'].iloc[0]
  pop22 = pop22['pop2022'].iloc[0]
  growth = (pop23-pop22)/pop22

  col1.metric(label='Population (2023)',
              value=f'{pop23:,}',
              delta=f'{growth*100:.2f} %'
              )

  birth_rate = land['Fert. Rate'].iloc[0]
  col2.metric(label='Birth Rate',
              value=birth_rate)

  age = land['Med. Age'].iloc[0]
  col3.metric(label='Average Age',
              value=age)

  urb_pop = land['Urban Pop %'].iloc[0]
  urb_pop = int(urb_pop.split('%')[0])

  st.progress(text=f'Percentage of urban population ({urb_pop} %)',
              value=urb_pop)
except: pass
  

#?----------------------------------------------------------------
#? GRÁFICOS
edu_aux =df_edu[df_edu['Countries and areas']==country]
# edu_aux =edu_aux.set_index('Countries and areas')

st.progress(text=f"Unemployment Rate **({edu_aux['Unemployment_Rate'].iloc[0]} %)**",
            value=int(edu_aux['Unemployment_Rate'].iloc[0]))

col1,col2=st.columns(2)
oosr = edu_aux[['OOSR_Pre_Primary_Age_Male',
'OOSR_Pre_Primary_Age_Female',
'OOSR_Primary_Age_Male',
'OOSR_Primary_Age_Female',
'OOSR_Lower_Secondary_Age_Male',
'OOSR_Lower_Secondary_Age_Female',
'OOSR_Upper_Secondary_Age_Male',
'OOSR_Upper_Secondary_Age_Female',
]]

df_t = oosr.transpose().reset_index()
df_t.columns = ['Coluna', 'Valor']
fig = px.bar(df_t, x='Valor', y='Coluna', text='Valor', barmode='stack')
fig.update_traces(textposition='inside')

# fig = px.bar(edu_aux1, orientation='h')
fig.update_layout(title='Out-of-School Rate',
                  xaxis_title='Values',
                  yaxis_title='',
                  showlegend=True)

col1.plotly_chart(fig)



proficiency_disc = edu_aux[['Grade_2_3_Proficiency_Reading',
'Grade_2_3_Proficiency_Math',
'Primary_End_Proficiency_Reading',
'Primary_End_Proficiency_Math',
'Lower_Secondary_End_Proficiency_Reading',
'Lower_Secondary_End_Proficiency_Math',
]]

df_t = proficiency_disc.transpose().reset_index()
df_t.columns = ['Coluna', 'Valor']
fig = px.bar(df_t, x='Valor', y='Coluna', text='Valor', barmode='stack')
fig.update_traces(textposition='inside')

# fig = px.bar(edu_aux1, orientation='h')
fig.update_layout(title='Profieciency',
                  xaxis_title='Values',
                  yaxis_title='',
                  showlegend=True)

col2.plotly_chart(fig)


completion = edu_aux[['Completion_Rate_Primary_Male',
'Completion_Rate_Primary_Female',
'Completion_Rate_Lower_Secondary_Male',
'Completion_Rate_Lower_Secondary_Female',
'Completion_Rate_Upper_Secondary_Male',
'Completion_Rate_Upper_Secondary_Female',
]]

df_t = completion.transpose().reset_index()
df_t.columns = ['Coluna', 'Valor']
fig = px.bar(df_t, x='Valor', y='Coluna', text='Valor', barmode='stack')
fig.update_traces(textposition='inside')

# fig = px.bar(edu_aux1, orientation='h')
fig.update_layout(title='Completion',
                  xaxis_title='Values',
                  yaxis_title='',
                  showlegend=True)

col1.plotly_chart(fig)

literacy = edu_aux[['Youth_15_24_Literacy_Rate_Male',
'Youth_15_24_Literacy_Rate_Female'
]]

df_t = literacy.transpose().reset_index()
df_t.columns = ['Coluna', 'Valor']
fig = px.bar(df_t, x='Valor', y='Coluna', text='Valor', barmode='stack')
fig.update_traces(textposition='inside')

# fig = px.bar(edu_aux1, orientation='h')
fig.update_layout(title='Literacy',
                  xaxis_title='Values',
                  yaxis_title='',
                  showlegend=True)

col2.plotly_chart(fig)
