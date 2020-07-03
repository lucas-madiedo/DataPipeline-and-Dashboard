import sqlite3
import pandas as pd 
import requests
from bs4 import BeautifulSoup

#########################################   Shared Functions    #######################################################



def create_sql_conexion(path):
    conection = sqlite3.connect (path)
    return conection

def export_df_to_processed(df,name):
    export_processed_csv = f'data/processed/{name}_cleaned.csv'
    df.to_csv(export_processed_csv,index=False)



##############################################  PERSONAL_INFO TABLE   ###################################################


def extract_personal_table(conection):
    df = pd.read_sql_query ("SELECT * FROM personal_info", conection)
    return df

def gender_column(df):
    '''
    Unifies values on column "Gender" and gives a category type-
    ...........................
    input: DataFrame
    output: DataFrame
    '''
    fem_filter = df['gender'].str.contains('[Ff]',regex = True)
    
    #asing all ceils with an f to: felmale
    df.loc[fem_filter,'gender'] = 'female'

    #asing cell with no f to: male
    df.loc[-fem_filter,'gender'] = 'male' 

    #change data type to categoy
    df['gender'] = df['gender'].astype('category')

    return df

def children_column (df):

    yes_filter = df['dem_has_children'].str.contains('[Yy]',regex = True)

    df.loc[yes_filter,'dem_has_children'] = 'yes' #changes all ceils with an y to: yes
    df.loc[-yes_filter,'dem_has_children'] = 'no' #changes cell with no y to: no

    #change data type to categoy
    df['dem_has_children'] = df['dem_has_children'].astype('category')

    #Change column Name
    df.rename(columns={'dem_has_children':'has_children'}, inplace = True)

    return df

def age_column (df):
    #Extract just the numerical values and convert them tho an integer.
    df['age'] = df['age'].str.extract(r'(\d+)')
    df['age'] = pd.to_numeric(df['age'])

    #Calculating age of the ones with the year. We apply a function in every figure abobe 1000
    year_filter = df['age'] > 1000
    df.loc[year_filter,'age'] = df.loc[year_filter,'age'].apply(lambda x: 2016 - x)

    return df

def age_group (df):
    #Creamos dos filtros. Juveniles entre 14-25 y juveniles entre 26 y 39
    juvenile_filter_under_26 = (df['age_group'].str.contains('juvenile')) & (df['age'] <= 25)
    juvenile_filter_abobe_26 = (df['age_group'].str.contains('juvenile')) & (df['age'] > 25)

    #Sustituimos en cada caso los juvenile por el rango de edad al que corresponde
    df.loc[juvenile_filter_under_26,'age_group'] = df.loc[juvenile_filter_under_26,'age_group'] = '14_25'
    df.loc[juvenile_filter_abobe_26,'age_group'] = df.loc[juvenile_filter_abobe_26,'age_group'] = '26_39'

    return df

#METAFUNCTION PERSONAL_INFO TABLE

def clean_personal_db (conection):
    print('\tCleaning Personal table')
    name = 'db_personal_info'
    df = extract_personal_table(conection)
    df = gender_column(df)
    df = children_column (df)
    df = age_column(df)
    df = age_group(df)
    print('\tPersonal table cleaned')
    export_df_to_processed(df,name)
    print('\tCSV file created\n')





#################################################  POLL_INFO TABLE   ###################################################

def extract_poll_table(conection):
    df = pd.read_sql_query ("SELECT * FROM poll_info", conection)
    return df

def change_columns(df):
    new_col_names = [
                'uuid',
                'awareness',
                'vote',
                'effect',
                'arguments_for',
                'arguments_against'
                ]
    df.columns = new_col_names
    return df

def effect_column(df):
    df['effect'].value_counts(dropna = False)
    #Filter to select all rows starting with "‰Û_ "
    filter_odd_chars = df['effect'].str.contains('‰Û_ ')

    #Change the values of those rows for the content sliced and capitalized.
    df.loc[filter_odd_chars,'effect'] = df.loc[filter_odd_chars,'effect'].str[4:].str.capitalize()

    return df

#METAFUNCTION POLLL_INFO TABLE

def clean_poll_df(conection):
    print('\tCleaning  Poll table')
    name = 'db_poll_info'
    df = extract_poll_table (conection)
    df = change_columns(df)
    df = effect_column (df)
    print('\tPoll table cleaned')
    export_df_to_processed(df,name)
    print('\tCSV file created\n')
    return df



#########################################     COUNTRIES (WEBSCRAPING AND DB)     ##################################################

URL = 'https://ec.europa.eu/eurostat/statistics-explained/index.php/Glossary:Country_codes'
PARSER = 'lxml'

def extract_info_web():
    '''extrae la info de la web y crea una lista con todos los paises y códigos'''
    content = requests.get(URL).content
    soup = BeautifulSoup(content,PARSER)
    row_def = []

    for table in soup.find_all('table'):
        for table_row in table.find_all('tr'):
            row_data = table_row.text
            row_def.append(row_data)

    raw_country_list = [a.split('\n') for a in row_def]
        # separa el string y crea una lsta de listas por fila pero con espacios en blanco
    county_list = [val.strip() for sublist in raw_country_list for val in sublist if len(val) > 0]
        # Crea una lista ordenada con todos los paises y codigos.

    return county_list

def create_country_dict(web_data):
    '''recibe una lista y crea un diccionario 1:2,3:4,5:6'''
    dict_paises = {web_data[i]: web_data[i + 1] for i in range(0, len(web_data), 2) if len(web_data[i])>0}
    return dict_paises

def create_countries_df(country_dict):
    '''recibe un diccionario y devuelve un dataframe de pandas'''
    counties_df = pd.DataFrame(list(country_dict.items()), columns=['Country', 'Cod'])
    counties_df['Cod'] = counties_df['Cod'].str.extract(pat='([A-Z]{2})')
    return counties_df

def extract_country_info_table(conection):
    df = pd.read_sql_query ("SELECT * FROM country_info", conection)
    return df

#METAFUNCTIONS COUNTRIES INFORMATIO

#web Sraping
def extract_countries_web():
    print('\tIniciating webscraping process')
    name = 'ws_countries_info'
    web_data = extract_info_web()
    country_dict = create_country_dict(web_data)
    print('\tCreating dataframe from webscraping info')
    dataframe = create_countries_df(country_dict)
    export_df_to_processed(dataframe,name)
    print('\tCSV file created')

#Extract BBDD
def extract_countries_table(conection):
    name = 'db_countries_info'
    df = extract_country_info_table(conection)
    export_df_to_processed(df, name)
    print('\tCountries table cleaned')

#Agrupada
def countries_info_extract(conection):
    extract_countries_web()
    extract_countries_table(conection)
    print('\tCountries info succesfully combinated\n')



#########################################     JOB INFO (API RESQUEST AND DB)     ##################################################

def extract_carrer_table (conection):
    df = pd.read_sql_query ("SELECT * FROM career_info", conection)
    return df

def extract_unique_job_code(df):
    '''from df return a list of unique codes of jobs'''
    lista_raw = df['normalized_job_code'].to_list()
    jobs = [job for job in lista_raw if job ]
    return list(set(jobs))

def api_info (job_code_list):
    '''make a api request for each  code job of the given list and returns a json'''

    base_url =  'http://api.dataatwork.org/v1/jobs/'
    json = []
    i = 0
    for job_cod in job_code_list[:10]: # <--------------------------------------------CAPADO AQUI  job_code_list[:10]:
        i += 1
        url = base_url+job_cod
        response = requests.get(url)
        job_info = response.json()
        json.append(job_info)
        print(f'\tExtracting jobs from API: {i}/{len(job_code_list)}',end='\r')
    print('')
    return json

def create_df(json):
    '''from a json creates a df with the jobs and its code'''
    df = pd.DataFrame(json)
    df = df.rename(columns={'uuid':'job_code'})
    return df

#METAFUNCTIONS JOB INFO

def extract_carrers(conection):
    df = extract_carrer_table(conection)
    return df

def api_requests(df):
    job_list = extract_unique_job_code(df)
    json = api_info(job_list)
    jobs_df = create_df(json)
    return jobs_df

def extract_carrer_info(conection):
    print('\tCleaning JobInfo table')
    df = extract_carrers(conection)
    name_table_df = 'db_carrer_info'
    export_df_to_processed(df,name_table_df)
    print('\tJobsInfo succesfully created')
    print('\tMaking API request')

    jobs_df = api_requests(df)
    name_api_df = 'api_carrer_info'
    export_df_to_processed(jobs_df,name_api_df)
    
    return jobs_df

    print('\tCSV file created\n\n')

