import pandas as pd
df_q = pd.read_csv('CauHoi.csv')
df_a = pd.read_csv('Cautraloi.csv')
df_u = pd.read_csv('user.csv')

df_q['CreationDate'] = pd.to_datetime(df_q['CreationDate'])
df_a['AnswerDate'] = pd.to_datetime(df_a['AnswerDate'])
df_u['CreationDate'] = pd.to_datetime(df_u['CreationDate'])

df_q['Tags_Cleaned'] = df_q['Tags'].str.replace('>', ' ').str.replace('<', '')
df_q['Tags_List'] = df_q['Tags_Cleaned'].str.split()

df_q.to_csv('Cauhoi_cleaned.csv', index=False)
df_a.to_csv('CautraLoi_cleaned.csv', index=False)
df_u.to_csv('user_cleaned.csv', index=False)

