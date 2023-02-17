import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder
import os
import requests

# Checking ../Data directory presence
if not os.path.exists('../Data'):
    os.mkdir('../Data')

# Download data if it is unavailable.
if 'nba2k-full.csv' not in os.listdir('../Data'):
    print('Train dataset loading.')
    url = "https://www.dropbox.com/s/wmgqf23ugn9sr3b/nba2k-full.csv?dl=1"
    r = requests.get(url, allow_redirects=True)
    open('../Data/nba2k-full.csv', 'wb').write(r.content)
    print('Loaded.')

data_path = "../Data/nba2k-full.csv"
pd.set_option('display.max_columns', None)


def clean_data(path):
    df = pd.read_csv(path, parse_dates=True)
    df['b_day'] = pd.to_datetime(df['b_day'], format='%m/%d/%y')
    df['draft_year'] = pd.to_datetime(df['draft_year'], format='%Y')
    df['team'].fillna(value='No Team', inplace=True)
    df['college'].fillna(value='No College', inplace=True)
    df['height'] = [float(i.split()[2]) for i in df['height']]
    df['weight'] = [float(i.split()[3]) for i in df['weight']]
    df['salary'] = [float(i[1:]) for i in df['salary']]
    df['country'] = ['USA' if i == 'USA' else 'Not-USA' for i in df['country']]
    df['draft_round'] = ['0' if i == 'Undrafted' else i for i in df['draft_round']]
    return df


def feature_data(df):
    df['version'] = pd.to_datetime(df['version'].apply(lambda x: x.replace('NBA2k', '20')), format='%Y')
    df['age'] = pd.DatetimeIndex(df['version']).year - pd.DatetimeIndex(df['b_day']).year
    df['experience'] = pd.DatetimeIndex(df['version']).year - pd.DatetimeIndex(df['draft_year']).year
    df['bmi'] = df['weight'] / (df['height'] ** 2)
    df.drop(columns=['version', 'b_day', 'draft_year', 'weight', 'height', 'college'], inplace=True)
    for i in df.columns:
        if df[i].nunique() > 50 and i not in ['age', 'experience', 'bmi', 'salary']:
            df.drop(i, axis=1, inplace=True)
    return df


def multicol_data(df):
    corr = df.corr()
    corr_dict = {}
    for index, row in corr.iterrows():
        for col in corr.columns:
            if row.name != col and row.name != 'salary' and col != 'salary':
                if row[col] > 0.5 or row[col] < -0.5:
                    corr_dict.update({col: corr.salary[col]})
    df.drop('age', axis=1, inplace=True)
    return df


def transform_data(df):
    y = df['salary']
    num_feat_df = df.select_dtypes('number').drop(columns=['salary'])
    cat_feat_df = df.select_dtypes('object')
    num_scaler = StandardScaler()
    num_scaler = num_scaler.fit(num_feat_df)
    num_feats = num_scaler.transform(num_feat_df)
    scaled_nums_df = pd.DataFrame(num_feats, columns=num_feat_df.columns)
    cat_encoder = OneHotEncoder()
    cat_encoder.fit(cat_feat_df)
    cat_feats = cat_encoder.transform(cat_feat_df).toarray()
    cat_cols = []
    for i, column in enumerate(cat_feat_df.columns):
        j = 0
        while j < len(cat_encoder.categories_[i]):
            cat_cols.append(cat_encoder.categories_[i][j])
            j += 1
    print(cat_cols)
    scaled_cats_df = pd.DataFrame(cat_feats, columns=['Atlanta Hawks', 'Boston Celtics', 'Brooklyn Nets', 'Charlotte Hornets',
                                   'Chicago Bulls', 'Cleveland Cavaliers', 'Dallas Mavericks', 'Denver Nuggets',
                                   'Detroit Pistons', 'Golden State Warriors', 'Houston Rockets', 'Indiana Pacers',
                                   'Los Angeles Clippers', 'Los Angeles Lakers', 'Memphis Grizzlies', 'Miami Heat',
                                   'Milwaukee Bucks', 'Minnesota Timberwolves', 'New Orleans Pelicans', 'New York Knicks',
                                   'No Team', 'Oklahoma City Thunder', 'Orlando Magic', 'Philadelphia 76ers', 'Phoenix Suns',
                                   'Portland Trail Blazers', 'Sacramento Kings', 'San Antonio Spurs', 'Toronto Raptors',
                                   'Utah Jazz', 'Washington Wizards', 'C', 'C-F', 'F', 'F-C', 'F-G', 'G', 'G-F',
                                   'Not-USA', 'USA', '0', '1', '2'])
    return pd.concat([scaled_nums_df, scaled_cats_df], axis=1), y


cleaned_data = clean_data(data_path)
features = feature_data(cleaned_data)
best_features = multicol_data(features)
final_df = transform_data(best_features)

