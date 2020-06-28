import argparse
from p_acquisition import m_acquisition
from p_acquisition.m_acquisition import create_sql_conexion
from p_wrangling import m_wrangling
from p_reporting import m_reporting


def argument_parser():
    parser = argparse.ArgumentParser(description='Specify the path to the darta')
    parser.add_argument("-c","--country", type=str, help='specify companies list flies', required=False)

    args = parser.parse_args()
    return args

def main(args):
    print('starting Pipelie')
    db_path = 'data/raw/raw_data_project_m1.db'
    conection = m_acquisition.create_sql_conexion(db_path)
    m_acquisition.clean_personal_db(conection)
    m_acquisition.clean_poll_df(conection)
    m_acquisition.countries_info_extract(conection)
    m_acquisition.extract_carrer_info(conection)
    raw_df = m_wrangling.create_full_raw_table()
    m_reporting.main_table_ch1(raw_df,args.country)


    print('Pipeline is complete')

if __name__ == "__main__":
    arguments = argument_parser()
    main(arguments)