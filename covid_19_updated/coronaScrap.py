import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime
def scrap_districtData(dist=None):
    '''District datas Corona in Indian States'''
    try:
        url_graph=r'https://api.covid19india.org/v2/state_district_wise.json'
        r = requests.get(url_graph)#  verify=False)
        bar_val=r.json()
        df=pd.DataFrame(bar_val)
        df_list={}
        for i,j in enumerate(df['state']):
            for k in df['districtData'][i]:
#                 li=[]
        #         df_list.append([j,k['district'],k['confirmed']])
                df_list.update({(j,k['district']):k['confirmed']})

        covid_data_state = pd.Series(df_list)#,index=index)
    
    
        # pop#['Kerala']['Thrissur']
        print(covid_data_state)
        covid_data_state.index.names=['State','District']
        covid_data_state=covid_data_state.to_frame()
        covid_data_state.columns=['Total Cases']
        covid_data_state#['Kerala','Thrissur']
        # pop.loc['Kerala','Thrissur']['Total Cases']
        
        if dist != None:
            # if state.upper() in [x.upper() for x in covid_data_state['Name of State / UT'].tolist()]:
            # if dist.upper() in [x.upper() for x in covid_data_state.loc['State'].tolist()]:
                
            '''commented below as we are fetching data using APIs'''
                # covid_data_state=covid_data_state[covid_data_state['Name of State / UT'].str.upper() ==state.upper()]
            # dist=dist.capitalize()
            print(dist)
            print(covid_data_state.loc[dist])
            covid_data_state=covid_data_state.loc[dist]#covid_data_state[covid_data_state.loc[dist]== dist]
            html= covid_data_state.to_html()#classes='table table-hover ')
            html_ind_corona = html.replace('<thead>','<thead class="thead-dark">')
            return html_ind_corona

        # else:
        #     return '<h2><font color="red">The State <font color="Green">{}</font> information is not available :(</font></h2>'.format(state)

        else:
            html= covid_data_state.to_html()#classes='table table-hover ')
            html_ind_corona = html.replace('<thead>','<thead class="thead-dark">')
            return html_ind_corona #.sort_values('Country,Other')
    except Exception as e:
        print("Exception ",e)




def scrap_coronaData_Ind(state=None):
    '''Corona Indian State Datas'''
    try:
        file_name_state='nCOV_Ind.csv'
        file_name_state_1='nCOV_Ind'+datetime.now().strftime("%d-%m-%Y")+'.csv'
        ###====================== Indian State Data ========================###
        # r_state = requests.get('https://www.mohfw.gov.in/',verify=False)# headers=header, timeout=10)

        # '''We also can directly read the data from the get request and parse using Pandas table'''


        # ### ++++++ As below did not work so went for Using webscrapping ++++++++

        # # covid_data_state=pd.read_html(r_state.text)[1] # As [1] it hs tow table

        # ## for website to read from file##
        # # covid_data_state=pd.read_csv(file_name_state)
        # # print(covid_data_state)

        # ### ++++++ As below did not work so went for Using webscrapping ++++++++

        # #### ------Using webscrapping method to scrap data ---------###
        # soup = bs(r_state.text, 'html.parser')
        # # table =soup.find('div', id="cases")##.get_text()
        # table =soup.find('div',attrs={'class':'data-table table-responsive'})
        # print(type(table))
        # covid_table=[]
        # table_head= table.find_all('th')

        # thead=[i.text.strip() for i in table_head]
        # print(thead)
        # thead_len=len(thead)

        # table_rows= table.find_all('tr')
        # for count,tr in enumerate(table_rows):
        #     td= tr.find_all('td')
        #     rows = [i.text.strip() for i in td]
        #     print(rows)
        #     if all(v==0 for v in rows):
        #     # if all(rows):
        #         continue
            
        #     ## for inserting into the SI index for printing the value
        #     if len(rows)<thead_len:
        #         rows.insert(0,count)

        #     covid_table.append(rows)
            
        # print(covid_table)
        # covid_data_state=pd.DataFrame(covid_table,columns=thead,dtype = int)
        # print("********")
        # print(covid_data_state)
        # covid_data_state=covid_data_state.replace('None', np.nan).dropna(how='all')
        # covid_data_state.fillna(0,inplace=True)
        # covid_data_state.drop(['S. No.'], axis = 1,inplace=True)


        # covid_data_state.drop(covid_data_state.columns[0], axis=1, inplace=True)
        ###====================== Indian State Data ========================###

        #####++++++++++++++++Using API+++++++++++++++++##
        url=r'https://api.covid19india.org/data.json'
        r = requests.get(url)
        val=r.json()
        state_val=val['statewise']
        df=pd.DataFrame(state_val)
        # df.drop(['delta'],axis=1, inplace=True)
        
        # df.drop([df.columns[-1]],axis=1, inplace=True)
        # df.drop(['recovered'],axis=1, inplace=True)
        cols = list(df.columns)
        df.columns=[i.capitalize() for i in cols]
        df.drop(['Deltaconfirmed','Deltadeaths','Deltarecovered'],axis=1,errors='ignore',inplace=True)
        cols = list(df.columns)
        # cols=cols[:-2]
        cols = [cols[-1]]+[cols[-2]]+ cols[:-1]
        # cols = [i.strip().upper() for i in cols]
        # cols=cols[:-1]
        # cols = [cols[0]]+cols[2:-1]+[cols[1]]+[cols[-1]]

        # df.drop([df.columns[-1]], axis=1, inplace=True)
        covid_data_state = df[cols[:-1]]
        #####++++++++++++++++Using API+++++++++++++++++##


        covid_data_state.fillna(0,inplace=True)
        print(covid_data_state['State'])

        covid_data_state.to_csv(file_name_state, sep=',', index=False)
        
        
        covid_data_state['dateLog'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
       
        covid_data_state.to_csv(file_name_state_1, sep=',', index=False)
        covid_data_state=covid_data_state.drop(['dateLog'], axis = 1)
    
        # html_str=html_val+html.replace('<thead>','<thead class="thead-dark">')+'''</div></body></html>'''
        if state != None:
            # if state.upper() in [x.upper() for x in covid_data_state['Name of State / UT'].tolist()]:
            if state.upper() in [x.upper() for x in covid_data_state['State'].tolist()]:
                
                '''commented below as we are fetching data using APIs'''
                # covid_data_state=covid_data_state[covid_data_state['Name of State / UT'].str.upper() ==state.upper()]
                covid_data_state=covid_data_state[covid_data_state['State'].str.upper() ==state.upper()]
                html= covid_data_state.to_html()#classes='table table-hover ')
                html_ind_corona = html.replace('<thead>','<thead class="thead-dark">')
                return html_ind_corona

            else:
                return '<h2><font color="red">The State <font color="Green">{}</font> information is not available :(</font></h2>'.format(state)

        else:
            html= covid_data_state.to_html()#classes='table table-hover ')
            html_ind_corona = html.replace('<thead>','<thead class="thead-dark">')
            return html_ind_corona #.sort_values('Country,Other')



    except Exception as exc:
        print(exc)
    



def scrap_coronaData():
    try:
        file_name_1='nCOV'+datetime.now().strftime("%d-%m-%Y")+'.csv'
        file_name='nCOV.csv'
        
#         corona_data=pd.read_html('https://www.worldometers.info/coronavirus/#countries')[0]#,header=None)[0]
        header = {
              "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
              "X-Requested-With": "XMLHttpRequest"
             }
    ########-----------------------############----------------------#######
        r = requests.get('https://www.worldometers.info/coronavirus/#countries',verify= False)# headers=header, timeout=10)
        # soup = bs(r.text, 'html.parser')
#         return soup
        
        '''We also can directly read the data from the get request and parse using Pandas table'''
        covid_data=pd.read_html(r.text)[0]

###########---------------------#############---------------------########
#--------------------#  Corona Test  #-----------------------------------
        # covid_data=pd.read_csv(file_name)
        # print(covid_data)

      

         #print(covid_data)
        covid_data.fillna(0,inplace=True)
        
        
        ## saving  data as csv for future analysis
        covid_data.to_csv(file_name, sep=',', index=False)
        


        covid_data['dateLog'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
       
        covid_data.to_csv(file_name_1, sep=',', index=False)
       
        covid_data=covid_data.drop(['dateLog'], axis = 1)

        return covid_data #.sort_values('Country,Other')
    except Exception as exc:
        print(f'{exc}')
        
# corona_data=scrap_coronaData()
    
def search_country(country=None):


    if country == None:
        print(" Updating for all")
        df=scrap_coronaData()
        return df
    
    else:
        ## Not needed below code as we can directly convert all into upper case and
        # country=' '.join([i.capitalize() for i in country.split()])


        # if any(str(elem) in ['Iran'] for elem in df['Country,Other'].tolist()):
        #     print('yes present')
        # else:
        #     print("The Country is not Availble")
        df=scrap_coronaData()

        # if country in df['Country,Other'].tolist():
        #     covid_outbreak=df[df['Country,Other']==country]
        #     return covid_outbreak
        if country.upper() in [x.upper() for x in df['Country,Other'].tolist()]:
            
            covid_outbreak=df[df['Country,Other'].str.upper() ==country.upper()]
            return covid_outbreak

        else:
            print("Nope The given Country information is not Avaialable")
            covid_outbreak=df[df['Country,Other']==country] ## Note needed for as we just pass empty df so we did it or not needed
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
    try:
        if int(float(row[b])) > 0:
            styles[a] = 'background-color: %s' % color
        if int(float(row[b])) > 0:
            if int(float(row[b])) > 3:
                styles[b] = 'background-color: %s' % color
            else:
                styles[b] = 'background-color: yellow'

    except:
        pass
        
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