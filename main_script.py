import argparse
from p_acquisition import m_acquisition
from p_wrangling import m_wrangling
from p_reporting import m_reporting
import os


API_URL = 'http://api.dataatwork.org/v1/jobs/'
OPTIONS = ['high','medium','low','no']

def argument_parser():
    parser = argparse.ArgumentParser(description='Specify a county . leave empty for all countries')
    parser.add_argument("-c","--country", type=str, help='specify a country', required=False)

    args = parser.parse_args()
    return args

def main(args):
    print('\nStarting Pipelie______________________\n')
    db_path = 'data/raw/raw_data_project_m1.db'

    print('Starting Data Acquisition Process\n')
    conection = m_acquisition.create_sql_conexion(db_path)
    m_acquisition.clean_personal_db(conection)
    poll_df = m_acquisition.clean_poll_df(conection)
    job_code = m_acquisition.countries_info_extract(conection)
    m_acquisition.extract_carrer_info(conection)

    print('\nStarting Data Wrangling Process\n')
    raw_df = m_wrangling.create_full_raw_table()

    print('Starting Data Reporting Process\n')
    m_reporting.main_table_ch1(raw_df,args.country)
    m_reporting.bonus_1_function(poll_df)
    #m_wrangling.create_bonus_poll_tables(poll_df) #<------------------- Comentar para la presentación
    m_reporting.create_bonus2_df_and_csv(raw_df,OPTIONS)

    print('\nPipeline is complete__________\n\n')
    os.system('streamlit run dashboard.py')

if __name__ == "__main__":
    arguments = argument_parser()
    main(arguments)