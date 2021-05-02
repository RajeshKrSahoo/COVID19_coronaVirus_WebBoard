import pandas as pd
import numpy as np
import requests as rq
from bs4 import BeautifulSoup as bs
import datetime
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
##this above import is to minismise SSL Security warning in Macbook


'''
Scripts to get the Vaccination available slot fro covid-19 centers with ease 

Open public API: https://apisetu.gov.in/public/marketplace/api/cowin
'''

base = datetime.datetime.today()
print(base)

numdays = 25
date_list = [base + datetime.timedelta(days=x) for x in range(numdays)]
print(date_list)
date_str = [x.strftime("%d-%m-%Y") for x in date_list]
date_str
age=58
print_flag = 'y'
print_flag = 'y'
def vaccine_state_data():
    '''function to print the state and its correponsding district names'''

    try:
        ## Checking statecode avaialble
        response_state = rq.get("https://cdn-api.co-vin.in/api/v2/admin/location/states",verify=False)
        json_data_state = json.loads(response_state.text)
        json_data_state['states']

        data_dist=[]
        for state_id in range(1,40):
            ##Checking till 40 state code as i checked there are 40 statecode availble!
            try:
                print("For State_code:{} State_name: {} ".format(state_id,next(i['state_name'] for i in json_data_state['states'] if i['state_id']==state_id)))
            except:
                print("For State_code:{} State_name: {}".format(state_id,'Not Available') )
                pass
            response_dist = rq.get("https://cdn-api.co-vin.in/api/v2/admin/location/districts/{}".format(state_id),verify=False)
            json_data = json.loads(response_dist.text)
            for _ in json_data["districts"]:
                
                # print(_["district_id"],'\t', _["district_name"])
                try:
                    data_dist.append([_["district_id"], _["district_name"],next(i['state_name'] for i in json_data_state['states'] if i['state_id']==state_id),state_id])
                except:
                    data_dist.append([_["district_id"], _["district_name"],None,state_id])
            # print("\n")

        df = pd.DataFrame(data_dist, columns = ['district_id', 'district_name','State_name','State_id'],index=None)
        df=df.sort_values(by=['State_id'], ascending=True)
        df_vacc_state = df.reindex(columns=['State_id','State_name','district_name','district_id'])
        print(len(df_vacc_state['district_id']))
        df_vacc_state['State_id'].nunique()
        return df_vacc_state


    except Exception as e:
        print("Exception ",e)



def vaccineSlotsByDist(age,district_name,state):
    try:
        available_df=[]
        age=age
        
        df_vacc_state=vaccine_state_data()
        try:
            DIST_ID=list(df_vacc_state[(df_vacc_state['State_name']== state) & (df_vacc_state['district_name']==district_name)]['district_id'])[0]

        except:
            print("No Combintaiont found")
            return None
            pass

        for inp_date in date_str:
            URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={}&date={}".format(DIST_ID, inp_date)
            response = rq.get(URL,verify=False)
            if response.ok:
                resp_json = response.json()
                # print(json.dumps(resp_json, indent = 1))
                if resp_json["centers"]:
                    print("Available on: {}".format(inp_date))
                    if(print_flag=='y' or print_flag=='Y'):
                        for center in resp_json["centers"]:
                            for session in center["sessions"]:
                                if session["min_age_limit"] <= age:
                                    print("\t", center["name"])
                                    print("\t", center["block_name"])
                                    print("\t Price: ", center["fee_type"])
                                    print("\t Available Capacity: ", session["available_capacity"])
                                    if(session["vaccine"] != ''):
                                        print("\t Vaccine: ", session["vaccine"])
                                    else:
                                        
                                        session["vaccine"]='No Information'
                                    print("\n\n")
                                    available_df.append([center["name"],center["block_name"],center["fee_type"],session["vaccine"],\
                                                        center['district_name'],center['state_name'],\
                                                        
                                                        center['pincode'],inp_date
                                                        
                                                        ])
                                                        
                           
                                 

                        
                else:
                    print("No available slots on {}".format(inp_date))


                available_df[0]



        # Create the pandas DataFrame for re grouping whole data into one particlur data frames
        info_vaccination = pd.DataFrame(available_df, columns = ['Vaccination Center', 'Block_name','Fee_type','Vaccine Type',\
            'District','State Name','pincode','Available Date'],index=None)
       
        html=info_vaccination.set_index(['Available Date', 'State Name','District','pincode'])

        html= html.to_html()#classes='table table-hover ')
        html_ind_corona = html.replace('<thead>','<thead class="thead-dark">')
        return html_ind_corona

    except Exception as e:
        print("Exception ",e)

    






