import streamlit as st
import pandas as pd



#HEADER
st.sidebar.title('MODULE ONE PORJECT: DASHBOARD')

#SELECCTION
challenge = st.sidebar.selectbox('Select the exercise to display',['Exercise 1','Bonus 1', 'Bonus 2'])





#CHALLENGE 1     #######################################################################################################
challenge_1_path =  'data/results/result_challenge1.csv'
challenge_1_df = pd.read_csv(challenge_1_path)


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


# BONUS 1    ###########################################################################################################
bonus_1_path = 'data/results/result_bonus1_procons_args.csv'
bonus_1_df = pd.read_csv(bonus_1_path)

bonus_pro_path = 'data/processed/arguments_pro_cleaned.csv'
bonus_against_path = 'data/processed/arguments_against_cleaned.csv'
bonus_1_pro_args = pd.read_csv(bonus_pro_path)
bonus_1_against_args = pd.read_csv(bonus_against_path)

bonus_1_pro_args.columns = ['Argument','Number']
bonus_1_against_args.columns = ['Argument','Number']







#    --------------------------------------------------------------------------------------------------------



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


    elif challenge == 'Bonus 1':
        st.title('BONUS 1 TABLE')
        st.table(bonus_1_df)
        st.write()
        st.write()
        st.subheader('PRO ARGUMENTS TABLE')
        st.table(bonus_1_pro_args)
        st.write()
        st.write()
        st.subheader('AGAINST ARGUMENTS TABLE')
        st.table(bonus_1_against_args)

    else:
        st.title('BONUS 2 TABLE')






###################################################################################################


