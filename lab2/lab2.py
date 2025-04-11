import urllib.request
import os
import pandas as pd
from datetime import datetime as dt

folder = 'import_files'
os.makedirs(folder, exist_ok=True)
for file in os.listdir(folder):
    file_path = os.path.join(folder, file)
    if os.path.isfile(file_path):
        os.remove(file_path)

def task1_download(x):
    url = f"https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_TS_admin.php?country=UKR&provinceID={x}&year1=1981&year2=2024&type=Mean"

    wp = urllib.request.urlopen(url)
    if wp.status == 200:
        text = wp.read().decode('utf-8')
        text = text[9:-11]
        
        
        head = ['YEAR', 'WEEK', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI', 'EMPTY']
        from io import StringIO
        data = pd.read_csv(StringIO(text), header=1, names=head)

        d_t = dt.now()
        d_t_t = d_t.strftime("%d%m%Y%H%M%S")
        name = f"{i}_{d_t_t}.csv"
        path = os.path.join(folder, name)
        data.to_csv(path, index=False)
        print(f'New file: {name}')
    else:
        print(f'Status URL not 200: {wp.status}')

for i in range(1, 28):
    task1_download(i)

def dataframe(folder):
    files = [f for f in os.listdir(folder) if f.endswith(".csv")]
    print(files)

    if not files:
        print("No files")
        return None

    all_data = []  

    for file in files:
        file_path = os.path.join(folder, file)
        head = ['YEAR', 'WEEK', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI', 'EMPTY']
        data = pd.read_csv(file_path, header=1, names=head)
        
        id_file = int(file.split("_")[0])

        df = pd.read_csv(file_path, header=1, names=head)

        df.insert(0, 'ID', id_file)

        df = df[df["VHI"] != -1]

        all_data.append(df)

    all_df = pd.concat(all_data, ignore_index=True)
    print(f'Quantity:{len(files)}')
    return all_df

all_df = dataframe(folder)
# print(all_df. head())
# print(all_df.tail())

def change_index(df):
    regions = {1: 22, 2: 24, 3: 23, 4: 25, 5: 3, 6: 4, 7: 8, 8: 19, 9: 20, 10: 21, 11: 9, 12: 26, 13: 10, 14: 11, 15: 12, 16: 13, 17: 14, 18: 15, 19: 16, 20: 27, 21: 17, 22: 18, 23: 1, 24: 2, 25: 6, 26: 7, 27: 5}
    df['ID'] = df['ID'].map(regions)
    return df

all_df = change_index(all_df)
# print(all_df. head())
# print(all_df.tail())

def obl_VHI(df, id_file, year):
    v_y_df = df[(df['YEAR'] == year)&(df['ID'] == id_file)]
    return f"For year {year}, obl {id_file} VHI:{v_y_df['VHI']}"
    
def min_max_VHI(df, ids_file, years):
    v_y_df = df[(df['YEAR'].isin(years))&(df['ID'].isin(ids_file))]
    return f"min: {v_y_df['VHI'].min()}, max: {v_y_df['VHI'].max()}, median: {v_y_df['VHI'].median()}, mean: {v_y_df['VHI'].mean()}"
    
def obl_years_VHI(df, ids_file, year1, year2):
    v_y_df = df[((df['YEAR']>=year1)&(df['YEAR']<=year2))&(df['ID'].isin(ids_file))]
    return f"for {ids_file}, {year1}...{year2} VHI:{v_y_df['VHI']}"
    
def extreme_droughts(df, per):
    quantity_obl = per * 27 / 100
    new_df = []
    is_it_any = False
    for ids in df['ID'].unique():
        for years in df['YEAR'].unique():
            new = df[(df['YEAR']==years)&(df['ID']==ids)&(df['VHI']<=15)]
            new_df.append(new)
    all_new_df = pd.concat(new_df, ignore_index=True)
    print(all_new_df.head())
    for years in all_new_df['YEAR'].unique():
        quantity_real = all_new_df[(all_new_df['YEAR']==years)]['ID']
        if len(quantity_real.unique()) >= quantity_obl:
            print(f'Year: {years}, per: {per}%, quantity: {quantity_obl} id: {quantity_real.unique()}, VHI:')
            print(all_new_df[(all_new_df['YEAR']==years)&(all_new_df['ID'].isin(quantity_real.unique()))]['VHI'])
            is_it_any = True    
    if is_it_any == False:
        return f'Not such year that VHI <= 15 and quantity obl >= {per}%: {quantity_obl}'
    else:
        return f'That is all'
    
            
#print(obl_VHI(all_df, 10, 1982))
#ids = [21, 20]
#years = [2001, 2003, 2005]
#print(min_max_VHI(all_df, ids, years))
#ids = [21, 20]
#print(obl_years_VHI(all_df, ids, 2000, 2003))
# print(extreme_droughts(all_df, 20))