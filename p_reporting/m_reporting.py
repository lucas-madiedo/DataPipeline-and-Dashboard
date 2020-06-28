import pandas as pd
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

    # se añade una columna sobre gender con la cuenta de pais, job, tabajo
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
    table = make_final_base_table(raw_df,country)
    final_table = pretty_df_percentage(table)
    name = 'result_challenge1.csv'
    result_to_csv(final_table,name)
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
    #df = pd.read_csv(path)
    df['Position'] = df['vote'].apply(lambda x: def_position(x))
    df['Number of Pro Arguments'] = df['arguments_for'].apply(lambda x: count_arguments(x))
    df['Number of Cons Arguments'] = df['arguments_against'].apply(lambda x: count_arguments(x))
    resumed_df = df[['Position', 'Number of Pro Arguments', 'Number of Cons Arguments']].groupby('Position').sum()
    resumed_df = resumed_df.reset_index().loc[[1, 0]]
    name = 'result_bonus1_procons_args.csv'
    result_to_csv(resumed_df, name)



########################################   Bonus 2: Pros and Cons   ################################################

