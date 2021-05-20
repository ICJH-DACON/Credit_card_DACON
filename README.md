# Credit_card_DACON
https://dacon.io/competitions/official/235713/overview/description/

<hr>
#### family type , edu order
0.7428531031, DACON점수

최소값으로 정규화한 결과는 동일 
<hr>
#### employed_date 0이상을 drop으로 바꿨을 때 
0.7438235671, DACON점수
비슷함
<hr>
#### family type을 더미할 때 
![image-3.png](attachment:image-3.png)
살짝 떨어짐
<hr>
#### 변수 후진제거 했을 때(과적합)
1.1531252015	

<hr>

### pycaret 모델 생성 
**preprocessor 
'''
    def preprocessing(self, dir):
        df = pd.read_csv(dir)

        drop_df_candidate = df[(df['DAYS_EMPLOYED']) > 0].index
        df.loc[drop_df_candidate, 'DAYS_EMPLOYED'] = 0

        drop_columns = ['index', 'FLAG_MOBIL', 'child_num', 'occyp_type']
        df.drop(columns=drop_columns, axis=1, inplace=True)

        df = encode_all_order_type(df) #edu_type, family_type
        df = encode_YN(df)

        return df
'''

> https://blog.naver.com/dalgoon02121/222340409616 보고 참고
> pycaret 사용법(가상환경 설정) https://pycaret.org/install/


