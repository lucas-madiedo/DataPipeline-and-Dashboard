import streamlit as st
import pandas as pd


challenge_1_path =  'data/results/result_challenge1.csv'
challenge_1_df = pd.read_csv(challenge_1_path)

#HEADER
st.title('PROJET 1 INFORMATION DASHBOARD')
st.header('header')
st.subheader('CHALLENGE 1')
st.text('this is a text')
st.write(' this is a text with write')

#SELECCTION
challenge = st.selectbox('Select the exercise to display',['Exercise 1','Bonus 1', 'Bonus 2'])


#Challenge 1:

###################################################################################################



def select_job(df):
    #incluir opción mostrar todos / todos menos no job / seleecionar uno : muestra cuadro
    list_of_jobs = list(df['Job Title'].unique())
    selected_job = st.selectbox('select jobs to list', list_of_jobs)
    filter_df = df['Job Title'] == selected_job
    return df[filter_df]

def select_countries(df):
    list_of_countries = list(df['Country'].unique())
    selected_countries = st.multiselect('select counties to list', list_of_countries, default=list_of_countries)
    filter_df = df['Country'].isin(selected_countries)
    return df[filter_df]

def select_age(df):
    min_ed = int(df['Age'].min())
    max_ed = int(df['Age'].max())

    ages_on_df = [min_ed, max_ed]
    age = st.slider('How old are you?', min_ed, max_ed, ages_on_df)

    min_ed_selected = age[0]
    max_ed_selected = age[1]

    filter_df = (df['Age'] >= min_ed_selected) & (df['Age'] <= max_ed_selected)
    return df[filter_df]


def challenge1(df):
    filtered_job = select_job(df)
    filtered_job_country = select_countries(filtered_job)
    filtered_3_job_country_age = select_age(filtered_job_country)
    return filtered_3_job_country_age

table_1 = challenge1(challenge_1_df)

max_results = table_1.shape[0]
results_to_show = st.number_input('Results to display', min_value=1, max_value=max_results,value=10)

st.table(table_1.head(results_to_show))

###################################################################################################
'''#select jobs to show:
jobs= list(challenge_1_df['Job Title'].unique())
jobs = st.selectbox('select jobs to list', jobs)

#  Show select countries
countries= list(challenge_1_df['Country'].unique())
countries = st.multiselect('select counties to list', countries, default=countries)

#  Show define number of rows
max_results = challenge_1_df.shape[0]
results_to_show = st.number_input('Results to display', min_value=1, max_value=max_results)



#select range of ages:
min_ed = int(challenge_1_df['Age'].min())
max_ed = int(challenge_1_df['Age'].max())

ages_on_df = [min_ed,max_ed]
age = st.slider('How old are you?', min_ed, max_ed, ages_on_df)

min_ed_selected = age[0]
max_ed_selected = age[1]



#SHOW TABLE
st.table(challenge_1_df.head(results_to_show))

'''

'''radio buton show todo dataframe:  st.dataframe(challenge)'''
if st.checkbox('show full Dataset'):
    st.dataframe(challenge_1_df)