import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup as bs




def scrap_coronaData():
    try:
#         corona_data=pd.read_html('https://www.worldometers.info/coronavirus/#countries')[0]#,header=None)[0]
        header = {
              "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
              "X-Requested-With": "XMLHttpRequest"
             }

        r = requests.get('https://www.worldometers.info/coronavirus/#countries', headers=header, timeout=10)
#         soup = bs(r.text, 'html.parser')
#         return soup
        
        '''We also can directly read the data from the get request and parse using Pandas table'''
        covid_data=pd.read_html(r.text)[0]
         #print(covid_data)
        covid_data.fillna(0,inplace=True)
        return covid_data #.sort_values('Country,Other')
    except Exception as exc:
        print(f'{exc}')
        
corona_data=scrap_coronaData()
    
def search_country(country=None,df=corona_data):


    if country == None:
        print(" Updating for all")
        # df=scrap_coronaData()
        return df
    
    else:
        
        country=' '.join([i.capitalize() for i in country.split()])

        # if any(str(elem) in ['Iran'] for elem in df['Country,Other'].tolist()):
        #     print('yes present')
        # else:
        #     print("The Country is not Availble")

        if country in df['Country,Other'].tolist():
            covid_outbreak=df.loc[df['Country,Other']==country]
            return covid_outbreak

        else:
            print("Nope The given Country information is not Avaialable")
            covid_outbreak=df.loc[df['Country,Other']==country]
            return covid_outbreak

    
#     return data




def highlight_vals(row, cols=['NewCases', 'NewDeaths'], color='red'):
    '''
    Function to highlight the cells on the table based on it's severity level 
    using Pandas style method useed in function
    '''
    a, b = cols
    styles = {col: '' for col in row.index}
#     print(row['Country,Other'])
    if int(float(row[b])) > 0:
        styles[a] = 'background-color: %s' % color
    if int(float(row[b])) > 0:
        if int(float(row[b])) > 3:
            styles[b] = 'background-color: %s' % color
        else:
            styles[b] = 'background-color: yellow'
        
    return styles



def covid19(df,cntry_code=None):
    # print("*****check*****",df)
    if df.empty:
        return '<h2><font color="red">The Country <font color="Green">{}</font> information is not available :(</font></h2>'.format(cntry_code)


    else:
        '''used stylo function as not able to highlight the cell in the table using df.to_html() method'''
        html=df.style.apply(lambda x: highlight_vals(x), axis=1).hide_index().render()
        html_str=html.replace('<thead>','<thead class="thead-dark">')
        return html_str
        

def covid_info(country=None):
    try:
        print(country)
        if country == None:
            df=search_country()
            data=covid19(df)

        else:
            df=search_country(country)
            # print('type:',type(df))
            data=covid19(df,country)
        return data

    except Exception as e:
        print(e)