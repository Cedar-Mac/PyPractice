import pandas as pd
import sqlite3
import json
from lxml import etree

def save_to_csv(file):
    csv_file = f'{file[:-5]}.csv'
    dataframe = pd.read_excel(file, sheet_name='Vehicles', dtype=str)
    dataframe.to_csv(csv_file, index=None, header=True)
    if len(dataframe) == 1:
        print(f'1 line was imported to {csv_file}')
    else:
        print(f'{dataframe.shape[0]} lines were imported to {csv_file}')
    return csv_file[:-4], dataframe


def correct_values(dataframe):
    corrected_file = f'{file_name}[CHECKED].csv'
    dataframe_corrected = pd.DataFrame()

    for column in df:
        dataframe_corrected[column] = dataframe[column].str.extract(r'(\d+)', expand=False)
    n_corrections = int(dataframe_corrected.compare(dataframe).count(axis=1).sum() / 2)
    if n_corrections == 1:
        print(f'1 cell was corrected in {corrected_file}')
    else:
        print(f'{n_corrections} cells were corrected in {corrected_file}')
    dataframe_corrected = dataframe_corrected.astype(int)
    dataframe_corrected.to_csv(corrected_file, index=False, header=True)
    return dataframe_corrected


def save_to_sql(dataframe_corrected):
    with sqlite3.connect(f'{file_name}.s3db') as conn:
        cn = conn.cursor()
        try:
            cn.execute(f'''
                            CREATE TABLE convoy (
                            vehicle_id INT PRIMARY KEY,
                            engine_capacity INT NOT NULL,
                            fuel_consumption INT NOT NULL,
                            maximum_load INT NOT NULL,
                            score INT NOT NULL);
                        ''')
            dataframe_corrected.to_sql('convoy', conn, if_exists='append', index=False)
            if dataframe_corrected.shape[0] == 1:
                print(f'1 record was inserted into {file_name}.s3db')
            else:
                print(f'{dataframe_corrected.shape[0]} records were inserted into {file_name}.s3db')
        except sqlite3.OperationalError:
            dataframe_corrected.to_sql('convoy', conn, if_exists='replace', index=False)
        conn.commit()
        cn.close()


def save_to_json(dataframe_corrected):
    dataframe_corrected.to_json(path_or_buf=f'{file_name}.json', orient='records', indent=4)
    with open(f'{file_name}.json', 'r+') as file:
        data = json.load(file)
        dictionary = {"convoy": data}
        file.seek(0)
        json.dump(dictionary, file)
        file.truncate()
    if dataframe_corrected.shape[0] == 1:
        print(f'1 vehicle was saved into {file_name}.json')
    else:
        print(f'{dataframe_corrected.shape[0]} vehicles were saved into {file_name}.json')


def save_to_xml(dataframe_corrected):
    try:
        dataframe_corrected.to_xml(path_or_buffer=f'{file_name}.xml', index=False,
                                   root_name='convoy', row_name='vehicle', xml_declaration=False)
        if dataframe_corrected.shape[0] == 1:
            print(f'1 vehicle was saved into {file_name}.xml')
        else:
            print(f'{dataframe_corrected.shape[0]} vehicles were saved into {file_name}.xml')
    except KeyError:
        convoy = etree.Element('convoy')
        xml = etree.ElementTree(convoy)
        xml.write_c14n(f'{file_name}.xml')
        print(f'0 vehicles were saved into {file_name}.xml')


def score_df(dataframe_corrected):
    dataframe_corrected['score'] = 1
    dataframe_corrected.loc[(450 * dataframe_corrected['fuel_consumption'] / 100)
                            / dataframe_corrected['engine_capacity'] < 1, 'score'] += 2  # Number of stops < 1
    dataframe_corrected.loc[((450 * dataframe_corrected['fuel_consumption'] / 100) / dataframe_corrected['engine_capacity'] < 2) & (dataframe_corrected['score'] < 2), 'score'] += 1  # Number of stops < 2
    dataframe_corrected.loc[(dataframe_corrected['fuel_consumption'] / 100) * 450 <= 230, 'score'] += 1  # Total fuel consumed less than 230L
    dataframe_corrected.loc[dataframe_corrected['maximum_load'] >= 20, 'score'] += 2  # Maximum load > 20
    return dataframe_corrected


print('Input file name:')
input_file = str(input())

if '.xlsx' in input_file:
    file_name, df = save_to_csv(input_file)
    df_corrected = correct_values(df)
elif '[CHECKED]' in input_file:
    file_name, df_corrected = input_file[:-13], pd.read_csv(input_file)
elif '.csv' in input_file:
    file_name, df = input_file[:-4], pd.read_csv(input_file)
    df_corrected = correct_values(df)
elif '.s3db' in input_file:
    file_name = input_file[:-5]
    with sqlite3.connect(f'{file_name}.s3db') as con:
        df_corrected = pd.read_sql('SELECT * FROM convoy', con)


scored_df = score_df(df_corrected)
save_to_sql(scored_df)

df_json = scored_df.loc[scored_df['score'] > 3].drop(columns=['score']).reset_index(drop=True)
df_xml = scored_df.loc[scored_df['score'] <= 3].drop(columns=['score']).reset_index(drop=True)

save_to_json(df_json)
save_to_xml(df_xml)
