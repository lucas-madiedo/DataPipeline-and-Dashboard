import pandas as pd

#########################################   Challenge 1: Basic Table    ################################################
path='data/processed/01_FULL_raw_table.csv'
raw_df = pd.read_csv(path)


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
        df['Percentage'] = df['Quantity'] / df['Country'].count() * 100
        df = df.sort_values(by=['Percentage'], ascending=False)
        return df

    # Si se mete valor, hace un filtro y recalcula el porcentaje.
    else:
        filter_country = df['Country'] == country
        df = df[filter_country]
        df['Percentage'] = df['Quantity'] / df['Country'].count() * 100
        df = df.sort_values(by=['Percentage'], ascending=False)
        return df


def pretty_df_percentage(df):
    df['Percentage'] = df['Percentage'].round(2).apply(lambda x : str(x)+'%')
    return df

def main_table_ch1 (raw_df,pais='all'):
    pais = 'France'
    table = make_final_base_table(raw_df,pais)
    final_table = pretty_df_percentage(table)

    FILES_BASE_PATH = 'data/results/'
    name = FILES_BASE_PATH + 'challenge1.csv'
    final_table.to_csv(name, index=False)

    return final_table


