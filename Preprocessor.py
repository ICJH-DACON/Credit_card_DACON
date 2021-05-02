import pandas as pd
import numpy as np

class Preprocessor():
    def __init__(self):
        print("Preprocessor is Operating")

    def preprocessing(self, dir):
        df = pd.read_csv(dir)

        drop_df_candidate = df[(df['DAYS_EMPLOYED']) > 0].index
        df.drop(drop_df_candidate, axis=0, inplace=True)

        drop_columns = ['index', 'FLAG_MOBIL', 'child_num', 'occyp_type']
        df.drop(columns=drop_columns, axis=1, inplace=True)

        df = dummy_object(df)
        df = encode_YN(df)
        df = encode_all_order_type(df)

        return df

    def preprocessing_for_analysis(self, dir):
        df = pd.read_csv(dir)

        drop_columns = ['index', 'FLAG_MOBIL']
        df.drop(columns=drop_columns, axis=1, inplace=True)

        df = control_outliner(df)
        df = encode_date(df)
        df = encode_YN(df)
        return df

def control_outliner(df):
    df.loc[df['child_num'] > 2, 'child_num'] = 3

    df['occyp_type'] = df['occyp_type'].fillna('NAN')

    return df

def dummy_object(df):
    object_variables = ["house_type", "income_type"]

    dummied_df = pd.get_dummies(df[object_variables])
    concat_df  = pd.concat([df, dummied_df], axis=1)
    concat_df  = concat_df.drop(columns=object_variables)
    return concat_df

def encode_YN(df):
    df['reality'] = df['reality'].apply(encode_yes_no)
    df['gender'] = df['gender'].apply(encode_gender)
    df['car'] = df['car'].apply(encode_yes_no)

    return df

def encode_gender(item):
    if item == 'M' or item == 1:
        return 1
    else:
        return 0

def encode_yes_no(item):
    if item == 'Y' or item == 1:
        return 1
    else:
        return 0

def encode_all_order_type(df) :
    order_variables = ["family_type", "edu_type"]

    for order_variable in order_variables:
        df[order_variable] = df[order_variable].apply(encode_order_type)
    return df

def encode_order_type(item):
    types = ['Commercial associate', 'Working', 'State servant', 'Pensioner', 'Student']
    if item in types:
        return types.index(item)

    types = ['Higher education' ,'Secondary / secondary special', 'Incomplete higher', 'Lower secondary', 'Academic degree']
    if item in types:
        return types.index(item)

    types = ['Married', 'Civil marriage', 'Separated', 'Single / not married', 'Widow']
    if item in types:
        return types.index(item)

    types = ['Municipal apartment', 'House / apartment', 'With parents', 'Co-op apartment', 'Rented apartment', 'Office apartment']
    if item in types:
        return types.index(item)

    types = ['Municipal apartment', 'House / apartment', 'With parents', 'Co-op apartment', 'Rented apartment',
             'Office apartment']
    if item in types:
        return types.index(item)

def remove_outlier(train, column):
    df = train[column]
    # 1분위수
    quan_25 = np.percentile(df.values, 25)

    # 3분위수
    quan_75 = np.percentile(df.values, 75)

    iqr = quan_75 - quan_25

    lowest = quan_25 - iqr * 1.5
    highest = quan_75 + iqr * 1.5
    outlier_index = df[(df < lowest) | (df > highest)].index
    print('outlier의 수 : ', len(outlier_index))
    train.drop(outlier_index, axis=0, inplace=True)

    return train
