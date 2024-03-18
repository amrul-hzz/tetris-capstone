import streamlit as st
import pandas as pd
import altair as alt

df_jmlh_sekolah  = pd.read_csv('df_jmlh_sekolah.csv')
df_jumlah_peserta_didik  = pd.read_csv('df_jmlh_peserta_didik.csv')
df_peserta_per_sekolah = pd.read_csv('df_peserta_per_sekolah.csv')
df_hls  = pd.read_csv('df_hls.csv')
df_penduduk_by_usia = pd.read_csv('df_penduduk_by_usia.csv')
df_jmlh_pt_aceh = pd.read_csv('df_jmlh_pt_aceh.csv')
df_hls_indo = pd.read_csv('df_hls_indo.csv')

cities = ['banda aceh', 'langsa', 'subulussalam', 'lhokseumawe', 'sabang']

st.set_page_config(
    page_title="Education in Aceh Throughout Regions",
    layout="wide"
)

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
Specifically, we will focus on **Expected Years of Schooling (EYS)** as the metric for education as well as explore the **Student-to-School Ratio** in different regions.

### About EYS    
Expected Years of Schooling (EYS), or Harapan Lama Sekolah (HLS) in indonesian, tells us how likely someone is to pursue higher education. Click [here](https://dikmenjp1.blogspot.com/2021/03/penghitungan-rata-rata-lama-sekolah-dan.html#google_vignette) to read more about how EYS is calculated.

""")


# ==============================================================================================================================================

st.write("""
## Question #1: How does the EYS grow in each city/regency?
""")

st.write("""
            Before we talk about the EYS indices of regions in Aceh, let's first examine the EYS of all provinces in Indonesia and see how Aceh fares.
         """)

def show_indo_eys(df_hls_indo):
    # Create a slider for the years
    selected_year = st.slider('Select Year for Expected Years of Schooling in Indonesia', min_value=2020, max_value=2022, step=1)

    # Melt the DataFrame to have 'year' and 'hls' in separate columns
    df_melted = df_hls_indo.melt(id_vars=['provinsi'], var_name='year', value_name='hls')

    # Extract year numbers from 'year' to make the slider work correctly
    df_melted['year'] = df_melted['year'].str.extract('(\d+)').astype(int)

    df_filtered = df_melted[df_melted['year'] == selected_year]

    # Filter to include only the top 10 provinces
    top_10_provinces = df_filtered.groupby('provinsi')['hls'].mean().nlargest(10).index
    df_top_10 = df_filtered[df_filtered['provinsi'].isin(top_10_provinces)]

    # Create the bar chart
    chart = alt.Chart(df_top_10).mark_bar().encode(
        x=alt.X('hls:Q', title='HLS', axis=alt.Axis(title='EYS')),  # Rename x-axis
        y=alt.Y('provinsi:N', sort='-x', title='Provinsi', axis=alt.Axis(title='Province')),  # Rename y-axis
        tooltip=['provinsi:N', 'hls:Q', 'year:O'],
        color=alt.condition(
            alt.datum.provinsi == 'aceh',
            alt.value('orange'),  
            alt.value('steelblue')    
        )
    ).properties(
        width=600,
        height=400,
        title=f'Top 10 Provinces by EYS in {selected_year}'
    )

    st.altair_chart(chart, use_container_width=True)

show_indo_eys(df_hls_indo)

st.write("""
         It turns out that Aceh has constantly been in the top ranks in terms of EYS throughout 2020-2022. 
         The EYS for a province is calculated by averaging the EYS numbers across regencies and cities, so it is worth asking if
         this relatively high EYS means that education across Aceh is already doing well or if it's **the work of outliers**.
         
         Let us examine each region more closely.
         """)



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
selected_year = st.slider('Select Year for Expected Years of Schooling in Aceh', min_value=2020, max_value=2022, step=1)
chart_1 = create_chart_1(df_hls, selected_year)
st.altair_chart(chart_1, use_container_width=True)

st.write("""
From the barchart above, we can see that the **top 3** and **bottom 3** regions in terms of EYS stay virtually the same over the years. 
- The top 3 were all cities: **Banda Aceh, Langsa, and Lhokseumawe**
- The bottom 3 were all regencies: **Bener Meriah, Aceh Barat Daya, and Aceh Timur**.
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
         
It is very apparent from the above charts that Banda Aceh, the capital of the province, is ahead by a large margin even amongst the top 3 regions. 
Banda Aceh has an EYS index cosntantly above 17.0, meaning that students of Banda Aceh tend to be more likely to pursue higher education. If we think about it, this could be the result of students **moving** to areas known to have higher education quality to continue their education so let's 
check the distribution of colleges across Aceh.
""")


st.write("""
        <span style="color:yellow"> 
            <b>Limitation</b> : The following data was acquired from less authenticated resources and thus should only be used as secondary context.
        </span>        
""", unsafe_allow_html=True)

st.write("")

# Fill missing values with 0
df_jmlh_pt_aceh.fillna(0, inplace=True)
df_jmlh_pt_aceh.columns = ['Province', 'negeri', 'swasta', 'total']

# Calculate total for each region
df_jmlh_pt_aceh['total'] = df_jmlh_pt_aceh['negeri'] + df_jmlh_pt_aceh['swasta']

# Calculate percentages for negeri
sum_negeri = df_jmlh_pt_aceh['negeri'].sum()
df_jmlh_pt_aceh['% negeri'] = df_jmlh_pt_aceh['negeri'] * 100 / sum_negeri

# Create the pie chart for negeri
chart_negeri = alt.Chart(df_jmlh_pt_aceh).mark_arc().encode(
    # Define angles for the pie chart
    theta=alt.Theta('% negeri:Q', stack=True),
    # Define colors based on daerah
    color=alt.Color('Province:N', scale=alt.Scale(scheme='category20')),
    # Define tooltip
    tooltip=['Province:N', '% negeri:Q'],
     # Add percentages
    text=alt.Text('% negeri:Q', format='.2f')
).properties(
    # Set title
    title='Percentage of Public Colleges by Region'
).interactive()

# Calculate percentages for swasta
sum_swasta = df_jmlh_pt_aceh['swasta'].sum()
df_jmlh_pt_aceh['% swasta'] = df_jmlh_pt_aceh['swasta'] * 100 / sum_swasta

# Create the pie chart for swasta
chart_swasta = alt.Chart(df_jmlh_pt_aceh).mark_arc().encode(
    # Define angles for the pie chart
    theta=alt.Theta('% swasta:Q', stack=True),
    # Define colors based on daerah
    color=alt.Color('Province:N', scale=alt.Scale(scheme='category20')),
    # Define tooltip
    tooltip=['Province:N', '% swasta:Q'],
     # Add percentages
    text=alt.Text('% swasta:Q', format='.2f')
).properties(
    # Set title
    title='Percentage of Private Colleges by Region'
).interactive()

col1, col2 = st.columns([1, 1]) 
with col1:
    chart_negeri
with col2:
    chart_swasta

st.write("It does seem like Banda Aceh has the most colleges out of all the regions so it is a likely hypothesis.")

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
        One of the first things that come to mind hearing that period of years is how education systems had to implement social distancing due to Covid-19. 
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
         - **Fluctuation**: The top 3 densest regions seem to less fluctuating than the bottom 3, with Banda Aceh being the exception.
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


st.write("""
         ### Extra
         Additionally, let's see if the number of students of highschool age has anything to do with this density ratio.
         """)

st.write("""
        <span style="color:yellow"> 
        <b>Limitation</b> : Due to the (un)availability of data, we will take 16-18 as highschool age in this context.
         </span>
""", unsafe_allow_html=True)


def convert_decimal_separator(value):
    if isinstance(value, float):
        return int(f"{value:.2f}".replace('.', ''))
    return value

# Apply the function to the entire DataFrame
df_penduduk_by_usia = df_penduduk_by_usia.applymap(convert_decimal_separator)

# selection = alt.selection_single(
#     fields=['tahun'],
#     name='Select',
#     bind=alt.binding_select(options=sorted(df_penduduk_by_usia['tahun'].unique().tolist()))
# )

# base = alt.Chart(df_penduduk_by_usia).add_selection(selection)

# bar_chart = base.mark_bar().encode(
#     x=alt.X('daerah:N', sort='-y', axis=alt.Axis(title='Region')),
#     y=alt.Y('16-18 tahun:Q', axis=alt.Axis(title='Number of People Aged 16-18')),
#     color=alt.condition(
#         alt.datum['daerah'] == alt.value('Region A'),
#         alt.value('orange'),
#         alt.value('steelblue')
#     )
# ).transform_filter(
#     selection
# ).properties(
#     width=500,
#     height=300,
#     title='Number of People Aged 16-18 by Region'
# )

# selector = base.mark_text(align='center', baseline='middle').encode(
#     text='tahun:N'
# )

# final_chart = selector & bar_chart

# final_chart

selected_year = st.slider('Select Year for Population by Age', min_value=2020, max_value=2021, step=1)

df_filtered = df_penduduk_by_usia[df_penduduk_by_usia['tahun'] == selected_year]

# Create the bar chart with switched x and y axes
chart = alt.Chart(df_filtered).mark_bar().encode(
    y=alt.Y('16-18 tahun:Q', title='16-18 tahun', axis=alt.Axis(title='Population of Highschool Age')),  # Switched to y-axis
    x=alt.X('daerah:N', sort='-y', title='daerah', axis=alt.Axis(title='Region')),  # Switched to x-axis
    tooltip=['daerah:N', '16-18 tahun:Q', 'year:O'],
    color=alt.condition(
            alt.FieldOneOfPredicate(field='daerah', oneOf=cities),
            alt.value('orange'),
            alt.value('steelblue')  
        )
).properties(
    width=600,
    height=400,
    title=f'Population of Highschool Age in {selected_year}'
)


st.altair_chart(chart, use_container_width=True)

st.write("""
    The rankings for number of students of highschool age don't look much alike with the the rankings for student-to-school density. 
    Perhaps some guesses could be made from this information:
    - Regions with high number of students of highschool age with low student-to-school density (ex: Aceh Utara) may have a lot of people who are not receiving education at their age level, if any
    - Regions with low number of students of highschool age with high student-to-school density (ex: Sabang) may be regions with few number of schools
""")

# =============================================================================================================================================================
st.write("""
## Insight Summary
- Although EYS growth across regions show a net positive, Banda Aceh's EYS still stands out (even amongst the top 3). This indicates that
education is still very much centered in the capital. Aceh consistently having the 2nd highest EYS out of all provinces in Indonesia does not guarantee equal education quality across regions.

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