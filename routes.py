import os
from flask import Flask,request,make_response,redirect,url_for

app = Flask(__name__)

@app.route('/')
def index():
    my_var = request.cookies.get('my_var')
    if my_var is None:
        i = 0
    else:
        try:
            i = int(my_var)
        except:
            i = 0

    resp = make_response("<span style='color:red'>I've been called " + str(i) + " times!</span>")
    resp.set_cookie('my_var', str(i+1))
    return resp

@app.route('/comic')
def comic():
    return redirect(url_for('static', filename='index.html'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=true)
