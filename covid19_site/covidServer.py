
# from werkzeug.wrappers import Request, Response # for running Flask on Jupyter Lab

from flask import Flask, jsonify,redirect, request, render_template, url_for, Markup
from coronaScrap import *

from multiprocessing import Value                    #This is Multithreading lib

counter = Value('i', 0)
app = Flask(__name__)

a = []
help_message = """
WEB Usage:
 
 for country specific

- GET    /corona/<str
- POST   /api/add data={"key": "value"}
- GET    /api/get/<id>
- PUT    /api/update/<id> data={"key": "value_to_replace"}
- DELETE /api/delete/<id> 

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
    return render_template('corona.html', posts=posts, title = '<h3>Corona Info</h3>')


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




if __name__ == '__main__':
    
    app.run(debug=True)
    # app.run()

    ##Used below codes for running on Jupyter Notebook
    # from werkzeug.serving import run_simple
    # run_simple('localhost', 9002, app)
