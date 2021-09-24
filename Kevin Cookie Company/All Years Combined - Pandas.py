from glob import glob
import pandas as pd

files = []
for f in glob('OrderDataFiles/*.xlsx'):
  try:
    int(f.split('\\')[1].split()[0])
  except: # in case an error occurs
    pass  # do nothing
  else:
    files.append(f)

order_data_dfs = [pd.read_excel(f) for f in files]

order_data = pd.concat(order_data_dfs, ignore_index=True)
order_data.drop(order_data[order_data['Order ID'] == 'XXXXXX'].index, inplace=True) # same as order_data = order_data[order_data['Order ID'] != 'XXXXXX']
customer_id_expanded = order_data['Customer ID'].str.split(' - ', expand=True)
order_data.drop('Customer ID', axis=1, inplace=True)
customer_id_expanded.columns = ['Customer ID', 'Customer Name']
customer_id_expanded['Customer ID'] = customer_id_expanded['Customer ID'].astype('uint32')
order_data = pd.concat([order_data, customer_id_expanded], axis=1)
order_data = order_data.reindex(columns=['Order ID', 'Customer ID', 'Customer Name', 'Cookies Shipped', 'Revenue', 'Cost', 'Order Date', 'Ship Date', 'Order Status'])
order_data.insert(6, 'Profit', order_data.Revenue - order_data.Cost)
order_data.insert(9, 'Days to ship', order_data['Ship Date'] - order_data['Order Date'])
order_date = order_data['Order Date']
order_data.pivot_table(index=order_date.dt.year, values='Profit', aggfunc=sum).rename_axis('Year')
# order_data.pivot_table(index=order_date.dt.year, values='Profit', aggfunc=sum).rename_axis('Year').plot(kind='bar') # optional
order_data.pivot_table(index=[order_date.dt.year, order_date.dt.quarter], values='Profit', aggfunc=sum).rename_axis(['Year', 'Quarter'])
order_data.pivot_table(index=[order_date.dt.year, order_date.dt.quarter, order_date.dt.month], values='Profit', aggfunc=sum).rename_axis(['Year', 'Quarter', 'Month'])

del order_data_dfs
# order_data.sort_values('Order Date', inplace=True) # optional
order_data['Order Date'] = order_data['Order Date'].dt.date # before running .to_excel(). column dtype changes from datetime to object
order_data['Ship Date'] = order_data['Ship Date'].dt.date   # before running .to_excel()
order_data.to_excel("All years combined by Pandas.xlsx", index=False) # optional