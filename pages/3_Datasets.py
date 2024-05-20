import webbrowser
import streamlit as st

st.set_page_config(
  page_title='Datasets',
  page_icon='📊',
  layout='wide'
)

st.title('WorldEdStats 🎓')

st.subheader('Datasets')

btn_edu = st.button('Acesse o Dataset sobre educação')
btn_pop = st.button('Acesse o Dataset sobre população')

if btn_pop:
  webbrowser.open_new_tab('https://www.kaggle.com/datasets/muhammedtausif/world-population-by-countries?select=world-population-forcast-2020-2050.csv')
  webbrowser.open_new_tab('https://www.kaggle.com/datasets/rajkumarpandey02/2023-world-population-by-country')
  
if btn_edu:
  webbrowser.open_new_tab('https://www.kaggle.com/datasets/nelgiriyewithana/world-educational-data')
  
  
st.markdown(
  '''
  WorldEdStats is a powerful web application designed to offer a comprehensive understanding of global education and population data. 
  The platform's primary objective is to empower educators, policymakers, researchers, and the general public by providing a user-friendly interface to explore and analyze worldwide educational landscapes. 
  With features such as interactive data visualizations, historical trend analysis, and comparative assessments, WorldEdStats facilitates informed decision-making and collaboration. 
  The platform aims to contribute to the global conversation on education by offering insights that can shape effective policies, address disparities, and highlight successful strategies. 
  Through transparent data practices and a commitment to data integrity, 
  WorldEdStats serves as a valuable resource for those seeking to navigate the complexities of the global education landscape and make informed decisions for the future.
  '''
)

st.text('Developed by Gustavo Amancio Affonso')