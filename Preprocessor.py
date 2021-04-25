import pandas as pd

class Preprocessor():
    def __init__(self):
        print("Preprocessor is Operating")

    def preprocessing(self, dir):
        df = pd.read_csv(dir)

        df.drop(columns="index", axis=1, inplace=True)
        df.drop('FLAG_MOBIL', axis=1, inplace=True)

        df = control_outliner(df)
        df = dummy_object(df)
        df = encode_date(df)
        df = encode_columns(df)
        return df

def control_outliner(df):
    df.loc[df['child_num'] > 2, 'child_num'] = 3

    df['occyp_type'] = df['occyp_type'].fillna('NAN')

    return df

def dummy_object(df):
    object_variables = ["family_type", "house_type", "income_type", "edu_type", "occyp_type"]

    dummied_df = pd.get_dummies(df[object_variables])
    concat_df  = pd.concat([df, dummied_df], axis=1)
    concat_df  = concat_df.drop(columns=object_variables)
    return concat_df

def encode_date(df):
    df['DAYS_BIRTH']    = round(df['DAYS_BIRTH']    / -365)
    df['DAYS_EMPLOYED'] = round(df['DAYS_EMPLOYED'] / -365)

    df['begin_month'] = df['begin_month'] * -1

    df.loc[df['DAYS_EMPLOYED'] >= 35, 'DAYS_EMPLOYED'] = 35
    df.loc[df['DAYS_EMPLOYED'] < 0, 'DAYS_EMPLOYED'] = -1

    return df

def encode_columns(df):
    df['reality'] = df['reality'].apply(encode_yes_no)
    df['gender'] = df['gender'].apply(encode_gender)
    df['car'] = df['car'].apply(encode_yes_no)

    return df

def encode_gender(index):
    if index == 'M' or index == 1:
        return 1
    else:
        return 0

def encode_yes_no(index):
    if index == 'Y' or index == 1:
        return 1
    else:
        return 0