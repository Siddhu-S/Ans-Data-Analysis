import pandas as pd
'''
Date: '7/23/2025'
Day: 'Wednesday'
Group Size: Int
Pozetti: 'L/R'
Start Time: '15:11:39'
End Time: '15:11:39'
Checkout Time: '15:11:39'
Flavor Tour: Boolean
'''


df = pd.read_csv('alldata270735.csv')
df['Start Time'] = pd.to_datetime(df['start_time'], errors='coerce', format="%Y-%m-%d %H:%M:%S")
df['End Time'] = pd.to_datetime(df['end_time'], errors='coerce', format="%Y-%m-%d %H:%M:%S")
df['Checkout Time'] = pd.to_datetime(df['checkout_time'], errors='coerce', format="%Y-%m-%d %H:%M:%S")

df['Transaction Time'] = round((df['end_time'] - df['start_time']).dt.total_seconds() / 60, 2)

flavor_tour = df[df['flavor_tour'] == 'Yes']
no_flavor_tour = df[df['flavor_tour'] == 'No']

print(flavor_tour['Transaction Time'].describe())
print(no_flavor_tour['Transaction Time'].describe())
def calculate_avg_transaction_time(file):
    pass