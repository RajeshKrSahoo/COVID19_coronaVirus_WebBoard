##****IMPORTANT****####

##This is the lastest code been used in http://muxtrap.pythonanywhere.com/ and also this is the latest codes!



'''Below are the learning refernce articles i found'''
# from werkzeug.wrappers import Request, Response # for running Flask on Jupyter Lab
# https://hplgit.github.io/web4sciapps/doc/pub/._web4sa_flask013.html
## https://jakevdp.github.io/PythonDataScienceHandbook/04.01-simple-line-plots.html
### https://www.viralml.com/video-content.html?v=Z-um0QoVy18&Title=Starting%20a%20New%20Business?%20Dynamic%20Charting%20with%20Flask,%20Matplotlib,%20Chart.JS%20-%20Part%204
#### https://towardsdatascience.com/python-plotting-api-expose-your-scientific-python-plots-through-a-flask-api-31ec7555c4a8

###https://www.bogotobogo.com/python/pytut.php
###https://blog.ruanbekker.com/

##https://www.bogotobogo.com/python/Flask/Python_Flask_Embedding_Machine_Learning_2.php
#####

# from flask import Flask, jsonify,redirect, request, render_template, url_for, Markup
# from coronaScrap import *
# from VaccineSlotCOVID import *


import datetime
from flask import Flask, jsonify,redirect, request, render_template, url_for, Markup
from coronaScrap import *
from VaccineSlotCOVID import vaccineSlotsByDist
# mpld3

from multiprocessing import Value                    #This is Multithreading lib

counter = Value('i', 0)
app = Flask(__name__)

a = []
help_message = """
WEB Usage:
 
 for country specific

- GET    /corona/<str

"""


def id_generator():
    '''
    This function that will generate id’s for each document.
    '''
    with counter.get_lock():
        counter.value += 1
        return counter.value


@app.route("/")
# def home():
#     return render_template('home.html')


@app.route("/corona")
def corona():
    posts=covid_info()
    print(posts,"++++")
    if posts==None:
        posts='<h3> <font color="RED">Tempoararliy Data is not present for Global :( </font></h3)'
        return render_template('corona.html', posts=posts, title = '<h3>Corona Info</h3>')
    else:

        return render_template('corona.html', posts=posts, title = '<h3>Corona Info</h3>')


'''Indian State'''
@app.route("/corona/ind/state")
def corona_ind():
    posts=scrap_coronaData_Ind()
    return render_template('state.html', posts=posts, title = '<h3>India Corona Info</h3>')

@app.route("/corona/ind/state/search")
def stateSearch():
    
    
    # '''search' is the key and your input is the value'''
    post_val = request.args.get('search')
    print(post_val)
    print(type(post_val))

    if post_val == '':
        print('redirected the website as None search')
        return redirect(url_for('state.html')) ## for URL Routing -->1) the redirect(url_for(func_name_to_route))
    #     post_val=None
        
        
    posts=scrap_coronaData_Ind(post_val)
    # posts=Markup(posts) # incase if we want to skil |safe in jinja2 template

    return render_template('state.html', posts=posts, title = '<h3>India Corona Info</h3>')

    '''Indian State'''   



'''the below function is to render webpages on direct manual enter in the website not in websearch'''
@app.route('/corona/<string:_country>', methods=['GET'])
def get_info(_country):

    posts=covid_info(_country)
    # posts=Markup(posts) # incase if we want to skil |safe in jinja2 template

    return render_template('corona.html', posts=posts, title = '<h3>Corona Info</h3>')

@app.route('/corona/search', methods=['GET'])
def search_val():
    
    
    # '''search' is the key and your input is the value'''
    post_val = request.args.get('search')
    print(post_val)
    print(type(post_val))

    if post_val == '':
        print('redirected the website as None search')
        return redirect(url_for('corona')) ## for URL Routing -->1) the redirect(url_for(func_name_to_route))
    #     post_val=None
        
        
        

    
    posts=covid_info(post_val)
    # posts=Markup(posts) # incase if we want to skil |safe in jinja2 template

    return render_template('corona.html', posts=posts, title = '<h3>Corona Info</h3>')
    # return key



@app.route("/corona/ind/dist")
def stateDisSearch():
    posts=scrap_districtData()
    return render_template('districts.html', posts=posts, title = '<h3>Corona Districts Info</h3>')



@app.route("/corona/ind/dist/search",methods=['GET'])
def stateDis_Search():
    
    
    # '''search' is the key and your input is the value'''
    post_val = request.args.get('search')
    print(post_val)
    print(type(post_val))
    

    if post_val == '':
        print('redirected the website as None search')
        return redirect(url_for('districts.html')) ## for URL Routing -->1) the redirect(url_for(func_name_to_route))
    #     post_val=None
    
    ## for reolving the issue naming convetion
    if len(post_val.split()) >=2:
        post_val=[i.capitalize() for i in post_val.split()]
        print(post_val)
        post_val=' '.join(post_val)
        print(post_val)

    else:
        post_val=post_val.capitalize()

    posts=scrap_districtData(post_val)
    
    print(post_val)
    # posts=Markup(posts) # incase if we want to skil |safe in jinja2 template

    return render_template('districts.html', posts=posts, title = '<h3><b>{}</b> Districts COVID Info</h3>'.format(post_val))




@app.route("/vaccineSlot",methods=['POST'])
def covidSlot():
    if request.method == 'POST':
        # req_data = request.get_json(force=True)
        # data = request.form.to_dict(flat=False)
        # a=jsonify(data)

        ##---Used for browser leverl entry an getting the value
        data = request.get_json()
        name_state =  request.form.get('state_name', '')
        name_dist =  request.form.get('district_name', '')
        age_name =  request.form.get('age', '')


###*********************************************************************************************
        ##use for POSTMAN level code testing as upper line coes does not yeiel any value
        # data=request.json
        # print(data)

        # name_state =  data['state_name']
        # name_dist =  data['district_name']
        # age_name =  data['age']
###*********************************************************************************************



        print("Value StateName:",name_state)
        print("Value distName:",name_dist)
        print("AGE: ",age_name)
        # print("Value Dist Name:",district_name)
        # age=54
        try:
            age=int(age_name)
        except Exception as e:
            print(e)
        district_name=name_dist
        state=name_state
        html=vaccineSlotsByDist(age,district_name,state)
        print("HTML>>>",html)

        ##checking if the atframe has value
        if html==None:
            return render_template('vaccineSlot.html', posts="Data Not availble for the given Inputs please check!", title = '<h3><b>{}</b> </h3>'.format('NO Vaccine Slot Availability'))

        else:
            return render_template('vaccineSlot.html', posts=html, title = '<h3><b>{} {}</b> </h3>'.format('Vaccine Slot Availability for age: ',age))
        

    else:

        return render_template('vaccineSlot.html', posts="", title = '<h3><color="red"><b>{}</b> </h3>'.format('Enter Values to get the Vaccination slots availabilty Info'))







@app.route("/graph")
def graph_state():

    # url_graph=r'https://api.covid19india.org/states_daily.json'

    # r = requests.get(url_graph)#  verify=False)
    # bar_val=r.json()
    # # bar_val

    # df=pd.DataFrame(bar_val['states_daily'])
    # df
    # bar_val['states_daily']
    # df[['or','date']]   
    # dates=df['date'].to_list()
    # new_df=pd.DataFrame(bar_val['states_daily'])#,index=dates)
    # new__d=new_df[['or']]
    # new_df[['or','date']]

    # new_df['or']=new_df['or'].apply(pd.to_numeric) 
    # # new_df.groupby(['Fruit','Name'])['Number'].sum().reset_index()
    # # new_df.groupby('or').sum()
    # # groupby__d=new_df[['karnataka','odisha','kerala']]
    # # new__d
    # # groupby__d
    # df['or']=df['or'].apply(pd.to_numeric)
    # df=df[['or','date']]
    # new__df=df.groupby(['date'])['or'].sum().reset_index()
    # val=pd.DataFrame(new__df['or'].to_list(),columns=['Odisha'],index=new__df['date'].to_list())
    # plot=val.plot(kind='bar')
    # '''fig to HTML file'''
    from io import BytesIO
    # figfile = BytesIO()
    # fig = plot.get_figure()
    # # fig.savefig(figfile, format='png')
    # # figfile.seek(0)  # rewind to beginning of file
    # # import base64
    # # figdata_png = base64.b64encode(figfile.getvalue())
    # fig.savefig(figfile, format='svg')
    # figfile.seek(0)
    # figdata_svg = '<svg' + figfile.getvalue().split('<svg')[1]
    # figdata_svg = str(figdata_svg, 'utf-8')
    # print(figdata_svg)

    # import matplotlib.pyplot as plt ,mpld3

# x-coordinates of left sides of bars 
    left = [1, 2, 3, 4, 5] 

    # heights of bars 
    height = [10, 24, 36, 40, 5] 

    # labels for bars 
    tick_label = ['one', 'two', 'three', 'four', 'five'] 

    # plotting a bar chart 
    # plt.bar(left, height, tick_label = tick_label, 
    width = 0.8; color = ['red', 'green']

    # # naming the x-axis 
    # plt.xlabel('x - axis') 
    # # naming the y-axis 
    # plt.ylabel('y - axis') 
    # # plot title 
    # plt.title('My bar chart!') 

    # # function to show the plot 
    # plt.show() 
    # Make Matplotlib write to BytesIO file object and grab
    # return the object's string
    # from io import BytesIO
    # figfile = BytesIO()
    # plt.savefig(figfile, format='png')
    # figfile.seek(0)  # rewind to beginning of file
    # import base64
    # figdata_png = base64.b64encode(figfile.getvalue())
    # return figdata_png

    # figfile = BytesIO()
    # # plt.savefig(figfile, format='svg')
    # figfile.seek(0)
    # figdata_svg = '<svg' + figfile.getvalue().split('<svg')[1]
    # figdata_svg = str(figdata_svg, 'utf-8')
    # print(figdata_svg)
    # import matplotlib.pyplot as plt, mpld3
    # fig, ax = plt.subplots()
    # ax.plot(x, y)
    # html_text = mpld3.fig_to_html(fig)

    vacc_tot=total_vaccination()

    body='<h3> <font color="Green">{}% </font></h3> <h4> <font color="black">of India till Date:{} </font></h3> <br><br><br> '.format(vacc_tot,datetime.now())


    return render_template('graph.html', posts=body, title = '<h3>videos</h3>')

    


if __name__ == '__main__':
    
    app.run(debug=True)
    # app.run()

    ##Used below codes for running on Jupyter Notebook
    # from werkzeug.serving import run_simple
    # run_simple('localhost', 9002, app)
