import streamlit as st
import pandas as pd


challenge_1_path =  'data/results/result_challenge1.csv'
challenge_1_df = pd.read_csv(challenge_1_path)

bonus_1_path = 'data/results/result_bonus1_procons_args.csv'
bonus_1_df = pd.read_csv(bonus_1_path)

bonus_1_raw_path = 'data/processed/db_poll_info_cleaned.csv'
bonus_1_raw_df = pd.read_csv(bonus_1_raw_path)


#HEADER
st.sidebar.title('MODULE ONE PORJECT: DASHBOARD')

#SELECCTION
challenge = st.sidebar.selectbox('Select the exercise to display',['Exercise 1','Bonus 1', 'Bonus 2'])


#CHALLENGE 1     #######################################################################################################

def number_of_jobs_to_show ():
    option = st.sidebar.radio('You can select one kind of data for Job Title column',('All Entries','All but No Full-Time Job','Select specific Job'))
    return option

def jobs_to_show(df):
    selected_jobs_to_show = number_of_jobs_to_show()

    if selected_jobs_to_show == 'All but No Full-Time Job':
        filtered_df_by_job = filter_no_current(df)

    elif selected_jobs_to_show == 'Select specific Job':
        filtered_df_by_job = select_job(df)

    else:
        filtered_df_by_job = df

    return filtered_df_by_job

def filter_no_current (df):
    filter_df = df['Job Title'] != 'No Full-Time Job'
    return df[filter_df]

def select_job(df):
    #incluir opción mostrar todos / todos menos no job / seleecionar uno : muestra cuadro
    list_of_jobs = list(df['Job Title'].unique())
    selected_job = st.sidebar.selectbox('select jobs to list', list_of_jobs)
    filter_df = df['Job Title'] == selected_job
    return df[filter_df]

def select_countries(df):
    list_of_countries = list(df['Country'].unique())
    selected_countries = st.sidebar.multiselect('Select as many countries you want to show', list_of_countries, default=list_of_countries)
    filter_df = df['Country'].isin(selected_countries)
    return df[filter_df]

def select_age(df):
    min_ed = int(df['Age'].min())
    max_ed = int(df['Age'].max())

    ages_on_df = [min_ed, max_ed]
    age = st.sidebar.slider('Select a min and a max age to show on Age column?', min_ed, max_ed, ages_on_df)

    min_ed_selected = age[0]
    max_ed_selected = age[1]

    filter_df = (df['Age'] >= min_ed_selected) & (df['Age'] <= max_ed_selected)
    return df[filter_df]

def recalculate_colums (df):
    df = df [['Country', 'Job Title', 'Age','Quantity']]
    df['Percentage'] = df['Quantity'] / df['Quantity'].sum() * 100
    df['Percentage'] = df['Percentage'].round(2).apply(lambda x: str(x) + '%')
    return df

def challenge1(df):
    '''lanza challenge 1.'''
    st.sidebar.subheader('Select whitch gorup of jobs do you want to show')
    selected_df = jobs_to_show(df)

    st.sidebar.subheader('Select Countries to show')
    filtered_job_country = select_countries(selected_df)

    st.sidebar.subheader('Select a age range')
    filtered_3_job_country_age = select_age(filtered_job_country)
    recalculated_df = recalculate_colums(filtered_3_job_country_age)
    return recalculated_df


# BONUS 2    ###########################################################################################################





def extract_values(df, column):
    respuestas_2 = df[column].to_list()
    result = list(
        set([e.strip() if '|' in element else element for e in element.split('|') for element in respuestas_2]))
    clean_df = pd.DataFrame(columns=result)

    def change(x):
        if x == False:
            return 0
        else:
            return 1

    for a in result:
        clean_df[a] = poll_df[column].str.contains(a)
        clean_df[a] = clean_df[a].apply(lambda x: change(x))

    new_df = pd.DataFrame(clean_df.sum())
    new_df = new_df.rename(columns={0: 'Suma'})
    new_df['Porcentaje'] = (new_df['Suma'] / new_df['Suma'].sum()) * 100

    return new_df


st.table(bonus_1_df)
#pros = extract_values(bonus_1_raw_df,'arguments_for')
#st.table(pros)
st.table(bonus_1_raw_df)
















if __name__ == '__main__':

    if challenge == 'Exercise 1':
        table_1 = challenge1(challenge_1_df)

        # Mostrar lineas totales del df
        st.write(f'Entries of the selected Dataframe: {table_1.shape[0]}')

        #Selecionar número de Lineas a mostrar
        max_results = table_1.shape[0]
        results_to_show = st.number_input('Results to display', min_value=1, max_value=max_results,value=10)

        # Mostrar tabla
        st.table(table_1.head(results_to_show))

        st.write('')
        st.write('')
        st.write('-------')
        if st.button('Show Complete DF'):
            st.dataframe(challenge_1_df)

        if st.button('Show created DF'):
            st.dataframe(table_1)










###################################################################################################


