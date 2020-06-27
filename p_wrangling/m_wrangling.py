import pandas as pd

FILES_BASE_PATH = 'data/processed/'

ws_file = 'ws_countries_info_cleaned.csv'
countries_db_file = 'db_countries_info_cleaned.csv'
api_file = 'api_carrer_info_cleaned.csv'
carrers_db_file = 'db_carrer_info_cleaned.csv'
personal_db_file = 'db_personal_info_cleaned.csv'


#########################################   Shared Functions    #######################################################

def create_df_from_csv_file(file_name):
    '''recives an csv path and returns a pandas DF'''
    file_path = FILES_BASE_PATH + file_name
    new_df = pd.read_csv(file_path)
    return new_df

def merge_df (df1,df2,on):
    'recives two dataframes and makes a left join on a specified column'
    new = df1.merge(df2, on=on)
    return  new

######################################   Working with Countries DF    ##################################################


def adding_extra_codes(df):
    '''includes missed pairs country-code in our df'''
    extra_codes = pd.DataFrame({'Country': ['United Kingdom', 'Greece'], 'Cod': ['GB', 'GR']})
    df_ws = df.append(extra_codes, ignore_index=True)
    return df_ws

def merge_countries(base, df_ws):
    '''merge countries and code dataframes and drop some extra columns '''
    countries_full = base.merge(df_ws, how='left', left_on='country_code', right_on='Cod')
    countries_full = countries_full[['uuid', 'country_code', 'Country', 'rural']]
    countries_full = countries_full.rename(columns={'Country': 'country'})
    return countries_full

# Countries Metafunction:

def full_countries_table():
    '''creates a clean dataframe wich combines our web scraping info and our countries db info'''
    ws_df = create_df_from_csv_file(ws_file)
    ws_df = adding_extra_codes(ws_df)
    base = create_df_from_csv_file(countries_db_file)
    countries_df = merge_countries(base, ws_df)
    countries_df['rural'] = countries_df['rural'].astype('category')
    countries_df['country'] = countries_df['country'].astype('category')
    countries_df['country_code'] = countries_df['country_code'].astype('category')
    print('countries info succesfully merged')
    return countries_df


########################################   Working with JOBS DF   ######################################################

def merge_jobs(base, api):
    '''returns a cleaned DF wich combines our api info and our db carrer_info '''
    jobs_full = base.merge(api, how='left', left_on='normalized_job_code', right_on='job_code')

    #Cleaning resulting dataframe:
    jobs_full = jobs_full[['uuid', 'dem_education_level', 'dem_full_time_job', 'job_code', 'title', 'parent_uuid']]
    jobs_full = jobs_full.rename( columns={'dem_education_level': 'education_level',
                                           'dem_full_time_job': 'full_time_job'})
    filter_no_job = jobs_full['full_time_job'] == 'no'
    jobs_full.loc[filter_no_job, 'title'] = jobs_full.loc[filter_no_job, 'title'] = 'No Full-Time Job'

    return jobs_full

# Countries Metafunction:
def full_jobs():

    base_df = create_df_from_csv_file(carrers_db_file)
    api_df = create_df_from_csv_file(api_file)
    df = merge_jobs(base_df,api_df)
    print('full job info merged')
    return df


#########################################  MERGING RESULTING DATAFRAMES   ##############################################

def create_full_raw_table():

    print(f'mergin all cleaned info in one single created')


    personal_df = create_df_from_csv_file(personal_db_file)
    jobs_df = full_jobs()
    countries_df = full_countries_table()
    df_per_jobs = merge_df(personal_df,jobs_df,'uuid')
    full_df = merge_df(df_per_jobs,countries_df,'uuid')

    name= FILES_BASE_PATH + '01_FULL_raw_table.csv'
    full_df.to_csv(name,index=False)

    print('full raw table succesfully created ')


    return full_df








