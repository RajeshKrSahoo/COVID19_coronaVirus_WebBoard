
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
##this above import is to minismise SSL Security warning in Macbook


def scrap_districtData(dist=None):
    '''District datas Corona in Indian States'''
    try:
        url_graph=r'https://api.covid19india.org/v2/state_district_wise.json'
        r = requests.get(url_graph,  verify=False)
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
        r = requests.get(url,verify=False)
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
    



def scrap_coronaData_glob():
    '''Replacement to scrap_coronaData() function , data is from John Hopkins University'''
   

    try:

        # get data directly from github. The data source provided by Johns Hopkins University.
        url_confirmed = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
        url_deaths = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
        url_recovered = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv'

        # Data can also be saved locally and read from local drive
        # url_confirmed = 'time_series_covid19_confirmed_global.csv'
        # url_deaths = 'time_series_covid19_deaths_global.csv'
        # url_recovered = 'time_series_covid19_recovered_global.csv'

        df_confirmed = pd.read_csv(url_confirmed)
        df_deaths = pd.read_csv(url_deaths)
        df_recovered = pd.read_csv(url_recovered)

        ##############################################################################################################################
        # Moving Any country to the first row in the datatable (You can choose any country of interest to be display on the first row)
        ## not using this line as this was duplicated twice
        ##############################################################################################################################

        # def df_move1st_sg(df_t):

            #Moving Singapore to the first row in the datatable
            # df_t["new"] = range(1,len(df_t)+1)
            # df_t.loc[df_t[df_t['Country/Region'] == 'Singapore'].index.values,'new'] = 0
            # df_t = df_t.sort_values("new").drop('new', axis=1)
            # return df_t

        #########################################################################################
        # Data preprocessing for getting useful data and shaping data compatible to plotly plot
        #########################################################################################

        # Total cases
        df_confirmed_total = df_confirmed.iloc[:, 4:].sum(axis=0)
        df_deaths_total = df_deaths.iloc[:, 4:].sum(axis=0)
        df_recovered_total = df_recovered.iloc[:, 4:].sum(axis=0)

        # modified deaths dataset for mortality rate calculation
        df_deaths_confirmed=df_deaths.copy()
        df_deaths_confirmed['confirmed'] = df_confirmed.iloc[:,-1]

        #Sorted - df_deaths_confirmed_sorted is different from others, as it is only modified later. Careful of it dataframe structure
        df_deaths_confirmed_sorted = df_deaths_confirmed.sort_values(by=df_deaths_confirmed.columns[-2], ascending=False)[['Country/Region',df_deaths_confirmed.columns[-2],df_deaths_confirmed.columns[-1]]]
        df_recovered_sorted = df_recovered.sort_values(by=df_recovered.columns[-1], ascending=False)[['Country/Region',df_recovered.columns[-1]]]
        df_confirmed_sorted = df_confirmed.sort_values(by=df_confirmed.columns[-1], ascending=False)[['Country/Region',df_confirmed.columns[-1]]]

        #Single day increase
        df_deaths_confirmed_sorted['24hr'] = df_deaths_confirmed_sorted.iloc[:,-2] - df_deaths.sort_values(by=df_deaths.columns[-1], ascending=False)[df_deaths.columns[-2]]
        df_recovered_sorted['24hr'] = df_recovered_sorted.iloc[:,-1] - df_recovered.sort_values(by=df_recovered.columns[-1], ascending=False)[df_recovered.columns[-2]]
        df_confirmed_sorted['24hr'] = df_confirmed_sorted.iloc[:,-1] - df_confirmed.sort_values(by=df_confirmed.columns[-1], ascending=False)[df_confirmed.columns[-2]]

        #Aggregate the countries with different province/state together
        df_deaths_confirmed_sorted_total = df_deaths_confirmed_sorted.groupby('Country/Region').sum()
        df_deaths_confirmed_sorted_total=df_deaths_confirmed_sorted_total.sort_values(by=df_deaths_confirmed_sorted_total.columns[0], ascending=False).reset_index()
        df_recovered_sorted_total = df_recovered_sorted.groupby('Country/Region').sum()
        df_recovered_sorted_total=df_recovered_sorted_total.sort_values(by=df_recovered_sorted_total.columns[0], ascending=False).reset_index()
        df_confirmed_sorted_total = df_confirmed_sorted.groupby('Country/Region').sum()
        df_confirmed_sorted_total=df_confirmed_sorted_total.sort_values(by=df_confirmed_sorted_total.columns[0], ascending=False).reset_index()

        #Modified recovery csv due to difference in number of rows. Recovered will match ['Province/State','Country/Region']column with Confirmed ['Province/State','Country/Region']
        df_recovered['Province+Country'] = df_recovered[['Province/State','Country/Region']].fillna('nann').agg('|'.join,axis=1)
        df_confirmed['Province+Country'] = df_confirmed[['Province/State','Country/Region']].fillna('nann').agg('|'.join,axis=1)
        df_recovered_fill = df_recovered
        df_recovered_fill.set_index("Province+Country")
        df_recovered_fill.set_index("Province+Country").reindex(df_confirmed['Province+Country'])
        df_recovered_fill = df_recovered_fill.set_index("Province+Country").reindex(df_confirmed['Province+Country']).reset_index()
        #split Province+Country back into its respective columns
        new = df_recovered_fill["Province+Country"].str.split("|", n = 1, expand = True)
        df_recovered_fill['Province/State']=new[0]
        df_recovered_fill['Country/Region']=new[1]
        df_recovered_fill['Province/State'].replace('nann','NaN')
        #drop 'Province+Country' for all dataset
        df_confirmed.drop('Province+Country',axis=1,inplace=True)
        df_recovered.drop('Province+Country',axis=1,inplace=True)
        df_recovered_fill.drop('Province+Country',axis=1,inplace=True)

        # Data preprocessing for times series countries graph display 
        # create temp to store sorting arrangement for all confirm, deaths and recovered.
        df_confirmed_sort_temp = df_confirmed.sort_values(by=df_confirmed.columns[-1], ascending=False)

        df_confirmed_t = df_confirmed_sort_temp #df_move1st_sg(df_confirmed_sort_temp)
        df_confirmed_t['Province+Country'] = df_confirmed_t[['Province/State','Country/Region']].fillna('nann').agg('|'.join,axis=1)
        df_confirmed_t=df_confirmed_t.drop(['Province/State','Country/Region','Lat','Long'],axis=1).T

        df_deaths_t = df_deaths.reindex(df_confirmed_sort_temp.index)
        df_deaths_t = df_deaths_t #df_move1st_sg(df_deaths_t)
        df_deaths_t['Province+Country'] = df_deaths_t[['Province/State','Country/Region']].fillna('nann').agg('|'.join,axis=1)
        df_deaths_t=df_deaths_t.drop(['Province/State','Country/Region','Lat','Long'],axis=1).T
        # take note use reovered_fill df
        df_recovered_t = df_recovered_fill.reindex(df_confirmed_sort_temp.index)
        df_recovered_t = df_recovered_t #df_move1st_sg(df_recovered_t)
        df_recovered_t['Province+Country'] = df_recovered_t[['Province/State','Country/Region']].fillna('nann').agg('|'.join,axis=1)
        df_recovered_t=df_recovered_t.drop(['Province/State','Country/Region','Lat','Long'],axis=1).T

        df_confirmed_t.columns = df_confirmed_t.iloc[-1]
        df_confirmed_t = df_confirmed_t.drop('Province+Country')

        df_deaths_t.columns = df_deaths_t.iloc[-1]
        df_deaths_t = df_deaths_t.drop('Province+Country')

        df_recovered_t.columns = df_recovered_t.iloc[-1]
        df_recovered_t = df_recovered_t.drop('Province+Country')

        df_confirmed_t.index=pd.to_datetime(df_confirmed_t.index)
        df_deaths_t.index=pd.to_datetime(df_confirmed_t.index)
        df_recovered_t.index=pd.to_datetime(df_confirmed_t.index)

        # Highest 10 plot data preprocessing
        # getting highest 10 countries with confirmed case
        name = df_confirmed_t.columns.str.split("|", 1)
        df_confirmed_t_namechange=df_confirmed_t.copy()
        # name0 = [x[0] for x in name]
        name1 = [x[1] for x in name]
        df_confirmed_t_namechange.columns = name1
        df_confirmed_t_namechange=df_confirmed_t_namechange.groupby(df_confirmed_t_namechange.columns,axis=1).sum()
        df_confirmed_t_namechange10 = df_confirmed_t_namechange.sort_values(by=df_confirmed_t_namechange.index[-1], axis=1, ascending=False).iloc[:,:10]
        df_confirmed_t_stack = df_confirmed_t_namechange10.stack()
        df_confirmed_t_stack=df_confirmed_t_stack.reset_index(level=[0,1])
        df_confirmed_t_stack.rename(columns={"level_0": "Date",'level_1':'Countries', 0: "Confirmed"}, inplace=True)
        # getting highest 10 countries with deceased case
        name = df_deaths_t.columns.str.split("|", 1)
        df_deaths_t_namechange=df_deaths_t.copy()
        # name0 = [x[0] for x in name]
        name1 = [x[1] for x in name]
        df_deaths_t_namechange.columns = name1
        df_deaths_t_namechange=df_deaths_t_namechange.groupby(df_deaths_t_namechange.columns,axis=1).sum()
        df_deaths_t_namechange10 = df_deaths_t_namechange.sort_values(by=df_deaths_t_namechange.index[-1], axis=1, ascending=False).iloc[:,:10]
        df_deaths_t_stack = df_deaths_t_namechange10.stack()
        df_deaths_t_stack=df_deaths_t_stack.reset_index(level=[0,1])
        df_deaths_t_stack.rename(columns={"level_0": "Date",'level_1':'Countries', 0: "Deceased"}, inplace=True)

        # Recreate required columns for map data
        map_data = df_confirmed[["Province/State", "Country/Region", "Lat", "Long"]]
        map_data['Confirmed'] = df_confirmed.loc[:, df_confirmed.columns[-1]]
        map_data['Deaths'] = df_deaths.loc[:, df_deaths.columns[-1]]
        map_data['Recovered'] = df_recovered_fill.loc[:, df_recovered_fill.columns[-1]]
        map_data['Recovered']=map_data['Recovered'].fillna(0).astype(int) #too covert value back to int and fillna with zero
        #last 24 hours increase
        map_data['Deaths_24hr']=df_deaths.iloc[:,-1] - df_deaths.iloc[:,-2]
        map_data['Recovered_24hr']=df_recovered_fill.iloc[:,-1] - df_recovered_fill.iloc[:,-2]
        map_data['Confirmed_24hr']=df_confirmed.iloc[:,-1] - df_confirmed.iloc[:,-2]
        map_data.sort_values(by='Confirmed', ascending=False,inplace=True)
        #Moving Singapore to the first row in the datatable
        map_data["new"] = range(1,len(map_data)+1)
        # map_data.loc[map_data[map_data['Country/Region'] == 'Singapore'].index.values,'new'] = 0
        map_data = map_data.sort_values("new").drop('new', axis=1)


        ###for the Whole data to show!
        map_data_Whole=map_data.replace(np.nan,0)

        map_data_Whole['Active Cases']=map_data_Whole.apply(lambda row: row.Confirmed - row.Recovered- row.Deaths,  axis=1)

        map_data_Whole=map_data_Whole[['Country/Region','Confirmed','Deaths','Active Cases','Recovered','Deaths_24hr','Recovered_24hr','Confirmed_24hr']]

        # map_data_Whole=map_data_Whole.to_html()

        # html_ind_corona = map_data_Whole.replace('<thead>','<thead class="thead-dark">')
        
        return map_data_Whole

    except Exception as e:
        print(e)







def scrap_coronaData():
    '''This fucntion to scrap data from worldmeter to show the global corona outbreak report'''

    '''*****FUNCTION IS NOT BEING USED BECAUSE THE LINK NO MORE WORKS SO SWITCHING TO UPPER FUNCTION  scrap_coronaData_glob'''
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
        df=scrap_coronaData_glob()
        return df
    
    else:
        ## Not needed below code as we can directly convert all into upper case and
        # country=' '.join([i.capitalize() for i in country.split()])


        # if any(str(elem) in ['Iran'] for elem in df['Country,Other'].tolist()):
        #     print('yes present')
        # else:
        #     print("The Country is not Availble")
        df=scrap_coronaData_glob()

        # if country in df['Country,Other'].tolist():
        #     covid_outbreak=df[df['Country,Other']==country]
        #     return covid_outbreak
        if country.upper() in [x.upper() for x in df['Country/Region'].tolist()]:
            
            covid_outbreak=df[df['Country/Region'].str.upper() ==country.upper()]
            return covid_outbreak

        else:
            print("Nope The given Country information is not Avaialable")
            covid_outbreak=df[df['Country/Region']==country] ## Note needed for as we just pass empty df so we did it or not needed
            return covid_outbreak

    
#     return data




def highlight_vals(row, cols=['Confirmed_24hr', 'Deaths_24hr'], color='red'):
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



def total_vaccination():
    try:
        try:
            r_state = requests.get('https://www.mohfw.gov.in/')#,verify=False)# headers=header, timeout=10)
        except:
            return None
        #### ------Using webscrapping method to scrap data ---------###
        soup = bs(r_state.text, 'html.parser')
        # table =soup.find('div', id="cases")##.get_text()
        table =soup.find('div',attrs={'class':'fullbol'})
        print(type(table))
        table

        # soup.select_one("span[title*=RAM]").text
        ae=table.find("span", {"class": "coviddata"}).text.strip()
        # ae=table.findAll('span')
        ae
        val = ae.split (",")
        print("total vaccinated: ")
        vacc_pop=int(''.join(val))

        total_pop=1391575756

        total_vacc_perc=(vacc_pop/total_pop)*100
        print(total_vacc_perc,"% of India till Date:",datetime.now())
        return total_vacc_perc

    except Exception as e:
        print("Exception in total_vaccination",e)