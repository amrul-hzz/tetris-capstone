import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(
    page_title="Education in Aceh Throughout Regions",
    layout="wide"
)

df_jmlh_sekolah  = pd.read_csv('df_jmlh_sekolah.csv')
df_jumlah_peserta_didik  = pd.read_csv('df_jmlh_peserta_didik.csv')
df_hls  = pd.read_csv('df_hls.csv')

st.title("Exploring High School Trends Throughout Cities and Regencies in Aceh, 2020-2022")

st.write("""
insert background, stakeholders.
         
""")

st.write("""
## Problem Statement
         
The following analysis aims to discover trends in education across Aceh throughout the year 2020-2022, 
investigating how location factors into education received by students.
Specifically, we will focus on **Expected Years of Schooling (EYS)** as the metric for education.
         
""")

st.write("""
## About EYS
""")

# ==============================================================================================================================================

st.write("""
## Question #1: How does the EYS grow in each city/regency?
""")

cities = ['banda aceh', 'langsa', 'subulussalam', 'lhokseumawe', 'sabang']

def create_chart_1(df, year):
    filtered_df = df[['daerah', f'hls_{year}']].rename(columns={f'hls_{year}': 'EYS', 'daerah':'Region'})

    chart = alt.Chart(filtered_df).mark_bar().encode(
        x=alt.X('Region:N', sort='-y'),
        y=alt.Y('EYS:Q', axis=alt.Axis(tickMinStep=0.1)),
        color=alt.condition(
            alt.FieldOneOfPredicate(field='Region', oneOf=cities),
            alt.value('orange'),
            alt.value('steelblue')  
        )
    ).properties(
        width=600,
        height=400,
        title=f'Expected Years of Schooling in {year}'
    )
    
    return chart

selected_year = st.slider('Select Year', min_value=2020, max_value=2022, step=1)
chart_1 = create_chart_1(df_hls, selected_year)
st.altair_chart(chart_1, use_container_width=True)

st.write("""
From the barchart above, we can see that the **top 3** and **bottom 3** regions in terms of EYS stay virtually the same over the years. 
         The top 3 all being cities: **Banda Aceh, Langsa, and Lhokseumawe** and the bottom 3 all being regencies: **Bener Meriah, Aceh Barat Daya, and Aceh Timur**.
         It is very apparent that Banda Aceh, the capital of the province, is ahead by a large margin even amongst the top 3 regions.
         
         
""")

st.write("Let's see the net growth of the top 3 and bottom 3 regions from one year to the next.")

top_3 = ['banda aceh', 'langsa', 'lhokseumawe']
bottom_3 = ['bener meriah', 'aceh barat daya', 'aceh timur']

# Filter data for top 3 cities and bottom 3 regencies
filtered_df_top_bottom = df_hls[df_hls['daerah'].isin(top_3 + bottom_3)]

# Filter data for selected years
filtered_df_top_bottom_selected_years = filtered_df_top_bottom[['daerah', 'hls_2020', 'hls_2021', 'hls_2022']]

# Melt the DataFrame to convert it to long format
melted_df = pd.melt(filtered_df_top_bottom_selected_years, id_vars=['daerah'], value_vars=['hls_2020', 'hls_2021', 'hls_2022'], var_name='Year', value_name='EYS')

# Map colors for top 3 cities and bottom 3 regencies
color_mapping = {
    'banda aceh': 'yellow',
    'langsa': 'orange',
    'lhokseumawe': 'red',
    'bener meriah': 'green',
    'aceh barat daya': 'blue',
    'aceh timur': 'purple'
}

# Create line chart
line_chart = alt.Chart(melted_df).mark_line().encode(
    x='Year:N',
    y=alt.Y('EYS:Q', scale=alt.Scale(domain=[13, 18])),
    color=alt.Color('daerah', scale=alt.Scale(domain=list(color_mapping.keys()), range=list(color_mapping.values())))
).properties(
    width=100,
    height=400,
    title='EYS Growth for Top 3 Cities and Bottom 3 Regencies (2020-2022)'
)

# Display line chart
st.altair_chart(line_chart, use_container_width=True)

st.write("""
Although not always very significant, the top 3 regions and bottom 3 regions **all show positive net growth**. Most notably, Langsa and Bener Meriah exhibit steeper increases than the rest.
""")

# =============================================================================================================================================================

st.write("""
## Question #2: How does the number of schools in a region grow in comparison to the number of students enrolling there that year?
""")

# st.write("""
# ## Question #3: How does the EYS of a region compare to its neighbours through the years?
# """)

st.write("""
## What then?
""")