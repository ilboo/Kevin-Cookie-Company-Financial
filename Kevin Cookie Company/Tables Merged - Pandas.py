import pandas as pd

sales = pd.read_excel('Kevin Cookie Company Financials.xlsx', 'Cookie Sales', parse_dates=['Date'])
countries = pd.read_csv('Countries.csv', usecols=['Country or dependent territory', 'Population'])
countries = countries[countries['Country or dependent territory'].isin(['Canada', 'United States', 'Mexico', 'France', 'Germany'])]
countries.reset_index(drop=True, inplace=True) # optional
sales = pd.merge(sales, countries, left_on='Country', right_on='Country or dependent territory').drop('Country or dependent territory', axis=1)
sales['Units Sold'] = sales['Units Sold'].astype('uint32')
sales.rename(columns={'Month Name':'Month'}, inplace=True)
dates = sales.Date
sales.pivot_table(index=dates.dt.month, values='Profit', aggfunc=sum).rename_axis('Month')
sales.pivot_table(index='Country', values='Profit', aggfunc=sum)
sales.pivot_table(index='Product', values='Profit', aggfunc=sum)
sales.pivot_table(index='Product', values='Profit', aggfunc=sum).sort_values('Profit', ascending=False)
sales.pivot_table(index=['Country', 'Population'], values='Units Sold', aggfunc=sum)
sales.groupby(['Country', 'Population']).sum()[['Units Sold']] # same as the line above in this case
sales.groupby(['Country', 'Population']).sum()[['Units Sold']].reset_index('Population')
sales.groupby(['Country', 'Population']).sum()[['Units Sold']].reset_index('Population').sort_values('Units Sold', ascending=False)
profits_by_country = sales.groupby(['Country', 'Population']).sum()[['Units Sold']].reset_index('Population').sort_values('Units Sold', ascending=False)
profits_by_country.loc['Total'] = profits_by_country.sum() # Compare with sales.pivot_table(index=['Country'], values=['Population', 'Units Sold'], aggfunc={'Population':'mean', 'Units Sold':'sum'}, margins=True, margins_name='Total'). Also notice the difference between df['ColumnLabel'] and df.loc['RowLabel']