import pandas as pd
import requests

def result_to_csv (df,name):
    FILES_BASE_PATH = 'data/results/'
    file_name = FILES_BASE_PATH + name
    df.to_csv(file_name, index=False)

#########################################   Challenge 1: Basic Table    ################################################

def make_final_base_table(raw_df, country):
    # creamos un nuevo df con las columnas necesarias más una
    df = raw_df[['country', 'title', 'age', 'gender']]

    df = df.rename(columns={'country': 'Country',
                            'title': 'Job Title',
                            'age': 'Age',
                            'gender': 'Quantity'
                            })

    # se añade una columna sobre gender con la cuenta de pais, job, trabajo
    df = df.groupby(['Country', 'Job Title', 'Age']).agg('count').reset_index()
    df = df[df['Quantity'].notna()]


    # Si no se mete valor, devuelve el df tal cual.
    if country == None:
        df['Percentage'] = df['Quantity'] / df['Quantity'].sum() * 100
        df = df.sort_values(by=['Percentage'], ascending=False)
        return df

    # Si se mete valor, hace un filtro y recalcula el porcentaje.
    else:
        filter_country = df['Country'] == country
        df = df[filter_country]
        df['Percentage'] = df['Quantity'] / df['Quantity'].sum() * 100
        df = df.sort_values(by=['Percentage'], ascending=False)
        return df


def pretty_df_percentage(df):
    df['Percentage'] = df['Percentage'].round(2).apply(lambda x : str(x)+'%')
    return df

def main_table_ch1 (raw_df,country='all'):
    print('\tCreating challenge 1 table')
    table = make_final_base_table(raw_df,country)
    final_table = pretty_df_percentage(table)
    name = 'result_challenge1.csv'
    result_to_csv(final_table,name)
    print('\tChallenge 1 table succesfully created\n')
    return final_table

########################################   Bonus 1: Pros and Cons   ################################################

def def_position(x):
    if x == 'I would probably vote for it' or x == 'I would vote for it':
        return 'In Favor'
    elif x == 'I would not vote':
        return 'Neutral'
    else:
        return 'Against'

def count_arguments (x):
    if x == 'None of the above':
        return 0
    else:
        return (len(x.split("|")))

def bonus_1_function(df):
    print('\tStarting Process for Bonus 1 ')
    print('\tCreating Bonus 1 table')
    df['Position'] = df['vote'].apply(lambda x: def_position(x))
    df['Number of Pro Arguments'] = df['arguments_for'].apply(lambda x: count_arguments(x))
    df['Number of Cons Arguments'] = df['arguments_against'].apply(lambda x: count_arguments(x))
    resumed_df = df[['Position', 'Number of Pro Arguments', 'Number of Cons Arguments']].groupby('Position').sum()
    resumed_df = resumed_df.reset_index().loc[[1, 0]]
    name = 'result_bonus1_procons_args.csv'
    result_to_csv(resumed_df, name)
    print('\tBonus 1 table succesfully created\n')



########################################   Bonus 2: SKILLS FOR ED LEV   ################################################




def make_sub_by_cat(full_raw_df, text):
    ''' makes a list from a df wich is filtered by a given value'''

    reduced_raw = full_raw_df[['uuid', 'education_level', 'job_code']]
    reduced_raw = reduced_raw[reduced_raw['job_code'].notna()]
    reduced_raw = reduced_raw[reduced_raw['education_level'].notna()]

    filter_edu = reduced_raw['education_level'] == text
    list_of_works = reduced_raw[filter_edu]['job_code'].to_list()

    return list(set(list_of_works))


def api_skill_json(list_of_jobs, text):
    '''returns a json file with the api info for each value of a given job list'''

    base_url = 'http://api.dataatwork.org/v1/jobs/'
    append_url = '/related_skills'

    json = []
    len_jobs = len(list_of_jobs)

    for i, job_cod in enumerate(list_of_jobs[:3]): #<-----------------------------------------capar aqui list_of_jobs[:10]
        i += 1
        url = base_url + job_cod + append_url

        response = requests.get(url)
        job_info = response.json()
        json.append(job_info)

        print(f'\t{text.title()} education jobs examinated for skills: {i}/{len_jobs}', end='\r')
    print()
    return json


def create_list_skills_from_json(json):
    '''from a json given returns a list of skills'''

    list_of_skills = []
    for i in range(len(json)):
        try:
            for e in range(10):
                skill = json[i]['skills'][e]['skill_name']
                list_of_skills.append(skill)

        except:
            pass

    return list_of_skills

def created_sorted_dictionary (list_of_skills):
    '''from a list of skills, returns an ordered a dictionary where the key is the skill and the value the number
    of times wich appeas in the list'''

    base_dict = {i:list_of_skills.count(i) for i in list_of_skills}
    ordered_dict = sorted(base_dict.items(), key=lambda x: x[1], reverse=True)
    return ordered_dict


def extract_top_skills(full_raw_df, text):
    '''combines all the above functions and return a list of the top 10 skills for a given level of education'''

    list_jobs_by_ed = make_sub_by_cat(full_raw_df, text)
    json = api_skill_json(list_jobs_by_ed, text)  #<--------------   capar aquí  (api_skill_json(list_jobs_by_ed[:X],text) )
    list_of_skills = create_list_skills_from_json(json)
    top_10_skills = created_sorted_dictionary(list_of_skills)[:10]
    lista = [f'{a[0].title()} ({a[1]})' for a in top_10_skills]

    return lista


def create_bonus2_df_and_csv(full_raw_df, options):
    'makes a df and a csv file with all the info'
    print('\tStarting Process for Bonus 2')
    print('\tCreating Bonus 2 table')

    dictionary = {option: extract_top_skills(full_raw_df, option) for option in options}

    df = pd.DataFrame()
    df = pd.DataFrame(dictionary).T.reset_index()

    df.columns = ['Education Level', '1st Skill', '2nd Skill', '3th Skill', '4th Skill', '5th Sikill',
                  '6th Skill', '7th Skill', '8th Skill', '9th Skill', '10th Skill']

    name = 'result_bonus2.csv'
    result_to_csv(df, name)

    # Fin del comentario.

    print('\tBonus2 table succesfully created')
    return df