import pandas as pd

columns = ['col1', 'col2', 'val']
df = pd.DataFrame(columns=columns)
df.loc[0] = [1, 1, 3]
df.loc[1] = [1, 2, 8]
df.loc[2] = [1, 1, 2]
df.loc[3] = [1, 2, 9]
df.loc[4] = [2, 3, 2]
df.loc[5] = [2, 4, 7]
df.loc[6] = [2, 3, 9]
df.loc[7] = [2, 4, 1]
df.loc[8] = [3, 5, 11]
df.loc[9] = [3, 6, 4]
df.loc[10] = [3, 5, 35]
df.loc[11] = [3, 6, 79]

print(df)

print(df[['col1', 'col2', 'avg']].groupby(['col1', 'col2']).mean())

