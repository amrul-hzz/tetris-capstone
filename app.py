import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(
    page_title="Education in Aceh Throughout Regions",
    layout="wide"
)

df_jmlh_sekolah  = pd.read_csv('df_jmlh_sekolah.csv')
df_jumlah_peserta_didik  = pd.read_csv('df_jmlh_peserta_didik.csv')
df_peserta_per_sekolah = pd.read_csv('df_peserta_per_sekolah.csv')
df_hls  = pd.read_csv('df_hls.csv')

st.title("Exploring High School Trends Throughout Cities and Regencies in Aceh, 2020-2022")

st.write("""
## About This Analysis
        
### Background
The disparity in the quality of education has been a persisting problem. 
The recent Pandemic has further revealed the vulnerabilities in our education system.
Analyzing education metrics can help shed light to the struggles the system is facing and where interventions are needed.
        
### Stakeholder(s) and Goal(s)
- Government: Make informed decisions on educational policy to level the education landscape across regions
       
###  Problem Statement        
The following analysis aims to discover trends in high school-level education across Aceh throughout the year 2020-2022, 
investigating how location factors into education received by students.
Specifically, we will focus on **Expected Years of Schooling (EYS)** as the metric for education and explore the **Student-to-School Ratio** in different regions.

### About EYS    
Click [here](https://dikmenjp1.blogspot.com/2021/03/penghitungan-rata-rata-lama-sekolah-dan.html#google_vignette) to read more about how EYS is calculated.
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

selected_year = st.slider('Select Year for Expected Years of Schooling Chart', min_value=2020, max_value=2022, step=1)
chart_1 = create_chart_1(df_hls, selected_year)
st.altair_chart(chart_1, use_container_width=True)

st.write("""
From the barchart above, we can see that the **top 3** and **bottom 3** regions in terms of EYS stay virtually the same over the years. 
- The top 3 were all cities: **Banda Aceh, Langsa, and Lhokseumawe**
- The bottom 3 were all regencies: **Bener Meriah, Aceh Barat Daya, and Aceh Timur**.

It is very apparent that Banda Aceh, the capital of the province, is ahead by a large margin even amongst the top 3 regions. 
Banda Aceh has an EYS index constantly above 17.0, meaning that students of Banda Aceh tend to be more likely to pursue higher education.
         
         
""")

st.write("Let's see the net growth of the top 3 and bottom 3 regions from one year to the next.")

top_3 = ['banda aceh', 'langsa', 'lhokseumawe']
bottom_3 = ['bener meriah', 'aceh barat daya', 'aceh timur']

# Filter data for top 3 cities and bottom 3 regencies
filtered_df_top_bottom = df_hls[df_hls['daerah'].isin(top_3 + bottom_3)]

# Filter data for selected years
filtered_df_top_bottom_selected_years = filtered_df_top_bottom[['daerah', 'hls_2020', 'hls_2021', 'hls_2022']].rename(columns={'hls_2020': '2020', 'hls_2021': '2021', 'hls_2022': '2022'})

# Melt the DataFrame to convert it to long format
melted_df = pd.melt(filtered_df_top_bottom_selected_years, id_vars=['daerah'], value_vars=['2020', '2021', '2022'], var_name='Year', value_name='EYS')

# Map colors for top 3 cities and bottom 3 regencies
color_mapping = {
    'banda aceh': 'yellow',
    'langsa': 'orange',
    'lhokseumawe': 'red',
    'bener meriah': 'green',
    'aceh barat daya': 'blue',
    'aceh timur': 'purple'
}

line_chart = alt.Chart(melted_df).mark_line().encode(
    x='Year:N',
    y=alt.Y('EYS:Q', scale=alt.Scale(domain=[13, 18])),
    color=alt.Color('daerah', scale=alt.Scale(domain=list(color_mapping.keys()), range=list(color_mapping.values())))
).properties(
    width=100,
    height=400,
    title='EYS Growth for Top 3 Cities and Bottom 3 Regencies (2020-2022)'
)



st.altair_chart(line_chart, use_container_width=True)

st.write("""
Although not always very significant, the top 3 regions and bottom 3 regions **all show positive net growth**. Most notably, Langsa and Bener Meriah exhibit steeper increases than the rest.
""")

# =============================================================================================================================================================

st.write("""
## Question #2: How does the number of schools in a region grow in comparison to the number of students studying there that year?
""")

st.write("""
        <span style="color:yellow"> 
        <b>Limitation</b> : The analyses below assume that each school holds a similar amount of students. 
        In practice, this is not very accurate. For example, private schools tend to have less students than public schools.
        That being said, the number of private schools are usually small compared to public schools so we assume that the numbers would not shift by much.
         </span>
""", unsafe_allow_html=True)
st.write("### Senior High School (SMA)")

def create_chart_2a(df, year):
    filtered_df = df[['daerah', 'tahun', 'rasio_peserta_sma']].rename(columns={'daerah':'Region', 'tahun':'Year', 'rasio_peserta_sma': 'Student per School (SMA)'})
    filtered_df = filtered_df[filtered_df['Year'] == year]

    chart = alt.Chart(filtered_df).mark_bar().encode(
        x=alt.X('Region:N', sort='-y'),
        y=alt.Y('Student per School (SMA):Q', scale=alt.Scale(domain=[0, 1200])),
        color=alt.condition(
            alt.FieldOneOfPredicate(field='Region', oneOf=cities),
            alt.value('orange'),
            alt.value('steelblue')  
        )
    ).properties(
        width=600,
        height=400,
        title=f'Student to School Ratio (SMA) in {year}'
    )
    
    return chart

selected_year2a = st.slider('Select Year for Student to School Ratio (SMA) Chart', min_value=2020, max_value=2022, step=1)
chart_2a = create_chart_2a(df_peserta_per_sekolah, selected_year2a)
st.altair_chart(chart_2a, use_container_width=True)

st.write("""
         - **Density**: Quite dense. Initially denser in cities, but not so much after 2020
         - **Fluctuation**: Aside from Banda Aceh, the top 3 and bottom 3 positions are very fluctuating throughout 2020-2022.
        One of the first things that comes to mind hearing that period of years is how education systems had to implement social distancing due to Covid-19. 
        The fluctuations may suggest that outside of the capital, the infrastructure and resources were not robust enough to adapt to the new learning conditions.
         - **Growth over the years**: There is a noticeable drop from 2020 to 2021. The source data confirms that it is the number of students that are in significant decline, 
        not an increase in the number of schools, that caused the ratio to dwindle. This is supported by the fact that during the Pandemic, many students
        were forced to dropout due to numerous reasons, such as schools closing down or having struggled with economy.
         - **Other point(s) of interest**: Sabang started off as the 2nd densest region, but that density decreased over the years and it placed last in 2022.
         """)

st.write("### Vocational High School (SMK)")

def create_chart_2b(df, year):
    filtered_df = df[['daerah', 'tahun', 'rasio_peserta_smk']].rename(columns={'daerah':'Region', 'tahun':'Year', 'rasio_peserta_smk': 'Student per School (SMK)'})
    filtered_df = filtered_df[filtered_df['Year'] == year]

    chart = alt.Chart(filtered_df).mark_bar().encode(
        x=alt.X('Region:N', sort='-y'),
        y=alt.Y('Student per School (SMK):Q', scale=alt.Scale(domain=[0, 1200])),
        color=alt.condition(
            alt.FieldOneOfPredicate(field='Region', oneOf=cities),
            alt.value('orange'),
            alt.value('steelblue')  
        )
    ).properties(
        width=600,
        height=400,
        title=f'Student to School Ratio (SMK) in {year}'
    )
    
    return chart

selected_year2b = st.slider('Select Year for Student to School Ratio (SMK) Chart', min_value=2020, max_value=2022, step=1)
chart_2b = create_chart_2b(df_peserta_per_sekolah, selected_year2b)
st.altair_chart(chart_2b, use_container_width=True)

st.write("""
         - **Density**: Very dense in the cities.
         - **Fluctuation**: The top 3 densest regions seem to be less fluctuating than the bottom 3, with Banda Aceh being the exception.
         - **Growth over the years**: There is a significant drop in Banda Aceh in 2021 to 2022, where the numbers were cut by around half.
         """)

st.write("### Special Needs School (SLB)")

def create_chart_2c(df, year):
    filtered_df = df[['daerah', 'tahun', 'rasio_peserta_slb']].rename(columns={'daerah':'Region', 'tahun':'Year', 'rasio_peserta_slb': 'Student per School (SLB)'})
    filtered_df = filtered_df[filtered_df['Year'] == year]

    chart = alt.Chart(filtered_df).mark_bar().encode(
        x=alt.X('Region:N', sort='-y'),
        y=alt.Y('Student per School (SLB):Q', scale=alt.Scale(domain=[0, 1200])),
        color=alt.condition(
            alt.FieldOneOfPredicate(field='Region', oneOf=cities),
            alt.value('orange'),
            alt.value('steelblue')  
        )
    ).properties(
        width=600,
        height=400,
        title=f'Student to School Ratio (SLB) in {year}'
    )
    
    return chart


selected_year2c = st.slider('Select Year for Student to School Ratio (SLB) Chart', min_value=2020, max_value=2022, step=1)
chart_2c = create_chart_2c(df_peserta_per_sekolah, selected_year2c)
st.altair_chart(chart_2c, use_container_width=True)

st.write("""
         - **Density**: Denser in the regencies, especially in Aceh Tamiang.
         - **Fluctuation**: Very stable compared to the other two school types.
         - **Growth over the years**: Actually experience a slight increase overall throughout 2021-2022.
         """)



# =============================================================================================================================================================
st.write("""
## Insight Summary
- Although EYS growth across regions show a net positive, Banda Aceh's EYS still stands out (even amongst the top 3). This indicates that
education is still very much centered in the capital.

- The number of students in the system declined during the pandemic. Outside of the capital, student distributions across regions fluctuated. This may suggest the infrastructure and resources were not robust enough to adapt to the new learning conditions.

- Senior high schools (SMA) and vocational high schools (SMK) are denser in the cities, while special needs schools (SLB) are denser in the regencies.
""")


st.write("""
## What then?
Here are some actionable recommendations that can be taken towards a more equal opportunity for education.
            
**Promote Educational Growth Outside the Capital**
- Decentralize resources, for example, in the form of funding, teacher training programs, and educational materials
- Increase access to quality education by improving transportation and accommodation for students in remote areas.

**Engage Communities and Partners**
- Involve local communities in educational planning and decision-making processes to validate and verify requirements.
- Partner with NGOs to fund educational programs, especially in under-resourced areas.

**Monitoring and Evaluation**
- Establish a monitoring system for educational trends and metrics to identify room for improvement.
- Facilitate swift feedback from students, parents, and teachers so adjustments can be made faster.
""")
