import argparse
from p_acquisition import m_acquisition
from p_wrangling import m_wrangling


def argument_parser():
    parser = argparse.ArgumentParser(description='Specify the path to the darta')
    parser.add_argument("-p","--path", type=str, help='specify companies list flies', required=True)
    args = parser.parse_args()
    return args

def main(args):
    print('starting Pipelie')

    conection = m_acquisition.create_sql_conexion(args.path)
    m_acquisition.clean_personal_db(conection)
    m_acquisition.clean_poll_df(conection)
    m_acquisition.countries_info_extract(conection)
    m_acquisition.extract_carrer_info(conection)

    m_wrangling.create_full_raw_table()



    print('========================= Pipeline is complete =========================')

if __name__ == "__main__":
    arguments = argument_parser()
    main(arguments)