import urllib.request
import os
import pandas as pd
from datetime import datetime as dt
import sys

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

def change_index(df):
    regions = {1: 22, 2: 24, 3: 23, 4: 25, 5: 3, 6: 4, 7: 8, 8: 19, 9: 20, 10: 21, 11: 9, 12: 26, 13: 10, 14: 11, 15: 12, 16: 13, 17: 14, 18: 15, 19: 16, 20: 27, 21: 17, 22: 18, 23: 1, 24: 2, 25: 6, 26: 7, 27: 5}
    df['ID'] = df['ID'].map(regions)
    return df

all_df = change_index(all_df)

import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

regions = {
    0: 'None', 1: 'Vinnytsia', 2: 'Volyn', 3: 'Dnipropetrovsk', 4: 'Donetsk', 5: 'Zhytomyr',
    6: 'Zakarpattia', 7: 'Zaporizhia', 8: 'Ivano-Frankivsk', 9: 'Kyiv', 10: 'Kirovohrad',
    11: 'Luhansk', 12: 'Lviv', 13: 'Mykolaiv', 14: 'Odesa', 15: 'Poltava',
    16: 'Rivne', 17: 'Sumy', 18: 'Ternopil', 19: 'Kharkiv', 20: 'Kherson',
    21: 'Khmelnytskyi', 22: 'Cherkasy', 23: 'Chernivtsi', 24: 'Chernihiv',
    25: 'Crimea', 26: 'Kyiv_City', 27: 'Sevastopal'
}
add_sidebar=st.sidebar.table(regions)
o1_list = ['None','VCI','TCI','VHI']
a_order = False
d_order = False

col1, col2 = st.columns([1, 2])   

if 'option1' not in st.session_state:
    st.session_state.option1 = o1_list[0]
    
if 'option2' not in st.session_state:
    st.session_state.option2 = list(regions.keys())[0]
    
if 'slider1' not in st.session_state:
    st.session_state.slider1 = (0,0)

if 'slider2' not in st.session_state:
    st.session_state.slider2 = (1980,1980)
with col1:
    st.session_state.option1 = st.selectbox('VCI/TCI/VHI:', o1_list, index = o1_list.index(st.session_state.option1))
    st.session_state.option2 = st.selectbox('Region:', list(regions.keys()), index = list(regions.keys()).index(st.session_state.option2))
    st.session_state.slider1 = st.slider('Weeks:', 0, 52, st.session_state.slider1)
    st.session_state.slider2 = st.slider('Years(1981-2024):', 1980, 2024, st.session_state.slider2)

    a_order = st.checkbox('Sort data in ascending order')
    d_order = st.checkbox('Sort data in descending order')    

    if st.button("Reset filters:"):
        st.session_state.option1 = o1_list[0]
        st.session_state.option2 = list(regions.keys())[0]
        st.session_state.slider1 = (0,0)
        st.session_state.slider2 = (1980,1980)
    
    
    if st.button("Show filters:"):
        st.session_state.option1
        st.session_state.option2
        st.session_state.slider1
        st.session_state.slider2
        a_order
        d_order
        
with col2:
    tab1, tab2, tab3 = st.tabs(['Table', 'Corresponding graph', 'Comparing data graph'])
    with tab1:
        if (st.session_state.option1 != o1_list[0])and(st.session_state.option2 != list(regions.keys())[0])and((st.session_state.slider1[0] != 0)and(st.session_state.slider1[1] != 0))and((st.session_state.slider2[1] != 1980)and(st.session_state.slider2[0] != 1980)):
            filtered = all_df[((all_df['WEEK']>=st.session_state.slider1[0])&(all_df['WEEK']<=st.session_state.slider1[1]))&((all_df['YEAR']>=st.session_state.slider2[0])&(all_df['YEAR']<=st.session_state.slider2[1]))&(all_df['ID']==st.session_state.option2)]
            prefiltered = filtered
            if a_order and d_order:
                st.write('Both checkboxes are checked, uncheck one (No sorting)')
                filtered = prefiltered
            elif a_order:
                filtered.sort_values(by=st.session_state.option1, ascending=True, inplace=True)
            elif d_order:
                filtered.sort_values(by=st.session_state.option1, ascending=False, inplace=True)
            else:
                filtered = prefiltered
                st.write('No sorting')
            filtered
        else:
            st.write('Not all filters are selected!')
    with tab2:
        if (st.session_state.option1 != o1_list[0])and(st.session_state.option2 != list(regions.keys())[0])and((st.session_state.slider1[0] != 0)and(st.session_state.slider1[1] != 0))and((st.session_state.slider2[1] != 1980)and(st.session_state.slider2[0] != 1980)):
            filtered = all_df[((all_df['WEEK']>=st.session_state.slider1[0])&(all_df['WEEK']<=st.session_state.slider1[1]))&((all_df['YEAR']>=st.session_state.slider2[0])&(all_df['YEAR']<=st.session_state.slider2[1]))&(all_df['ID']==st.session_state.option2)]
            filtered['DATE'] = pd.to_datetime( filtered['YEAR'].astype(str) + filtered['WEEK'].astype(str).str.zfill(2) + "1", format="%Y%W%w")
            fig, ax = plt.subplots()
            sns.lineplot(data=filtered, x='DATE', y=st.session_state.option1, ax=ax)
            ax.set_title(f"Time series for element years, limited by the interval of weeks:{st.session_state.option1}")
            st.pyplot(fig)
        else:
            st.write('Not all filters are selected!')
    with tab3:
        if (st.session_state.option1 != o1_list[0])and(st.session_state.option2 != list(regions.keys())[0])and((st.session_state.slider1[0] != 0)and(st.session_state.slider1[1] != 0))and((st.session_state.slider2[1] != 1980)and(st.session_state.slider2[0] != 1980)):
            filtered = all_df[((all_df['WEEK']>=st.session_state.slider1[0])&(all_df['WEEK']<=st.session_state.slider1[1]))&((all_df['YEAR']>=st.session_state.slider2[0])&(all_df['YEAR']<=st.session_state.slider2[1]))]
            filtered['DATE'] = pd.to_datetime( filtered['YEAR'].astype(str) + filtered['WEEK'].astype(str).str.zfill(2) + "1", format="%Y%W%w")
            filtered['CAT'] = filtered["ID"].apply(lambda x: f"{st.session_state.option2}" if x == st.session_state.option2 else "Other")
            fig, ax = plt.subplots()
            sns.lineplot(data=filtered, x='DATE', y=st.session_state.option1, hue='CAT', ax=ax)
            ax.set_title(f"Graph display a comparison of the:{st.session_state.option1} for the {st.session_state.option2} with all other areas for the specified time interval")
            st.pyplot(fig)
        else:
            st.write('Not all filters are selected!')

