import pandas as pd
import numpy as np

class Preprocessor():
    def __init__(self):
        print("Preprocessor is Operating")

    def preprocessing(self, dir):
        df = pd.read_csv(dir)

        drop_df_candidate = df[(df['DAYS_EMPLOYED']) > 0].index
        df.loc[drop_df_candidate, 'DAYS_EMPLOYED'] = 0

        drop_columns = ['index', 'FLAG_MOBIL', 'child_num', 'occyp_type']
        df.drop(columns=drop_columns, axis=1, inplace=True)

        object_variables = ["house_type", "income_type"]

        df = encode_all_order_type(df)
        # df = dummy_object(df, object_variables)

        df = encode_YN(df)

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

def dummy_object(df, object_variables):
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
    df["edu_type"] = df["edu_type"].apply(encode_edu_type)
    df["family_type"] = df["family_type"].apply(encode_family_type)

    return df

def encode_family_type(item):
    types = ['Married', 'Civil marriage', 'Separated', 'Single / not married', 'Widow']

    return types.index(item)

def encode_edu_type(item):
    types = ['Higher education', 'Secondary / secondary special', 'Incomplete higher', 'Lower secondary',
             'Academic degree']

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
    train.drop(outlier_index, axis=0, inplace=True)

    return train
