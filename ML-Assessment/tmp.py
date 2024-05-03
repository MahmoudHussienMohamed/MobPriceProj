import pandas
ds = pandas.read_csv('ML-Assessment/train.csv')
print(ds.iloc[0].to_dict())