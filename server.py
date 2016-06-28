import json
import os
import re

from dotenv import Dotenv
from flask import Flask
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import request
from flask import send_from_directory
from flask import session
from functools import wraps
import requests

from auth0.v2.management import Auth0
import constants

# Load Env variables
env = None

try:
    env = Dotenv('./.env')
except IOError:
    env = os.environ

app = Flask(__name__, static_url_path= '')
app.secret_key = '@mgonto'
app.debug = True

# Requires authentication annotation

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if constants.PROFILE_KEY not in session:
            return redirect('/')
        return f(*args, **kwargs)      
    return decorated

@app.route('/')
def home():
    return render_template('home.html', env=env)	

@app.route('/error')
def error():
    return render_template('error.html', env=env)

@app.route('/dashboard')
@requires_auth
def dashboard():

    domain = env[constants.AUTH0_DOMAIN_KEY]
    token = constants.AUTH0_TOKEN
                       
    auth0 = Auth0(domain, token)
    applications = auth0.clients.all(fields=[constants.NAME_KEY]) 	
    rules = auth0.rules.all(fields=[constants.NAME_KEY, constants.SCRIPT_KEY])				
    return render_template('dashboard.html', user=session[constants.PROFILE_KEY], applications=applications, rules=rules)

@app.route('/public/<path:filename>')
def static_files(filename):
    return send_from_directory('./public', filename)

@app.route('/callback')
def callback_handling():
    code = request.args.get('code')
    
    json_header = {constants.CONTENT_TYPE_KEY: constants.APPLICATION_JSON_KEY}
    
    token_url = "https://{domain}/oauth/token".format(domain=env[constants.AUTH0_DOMAIN_KEY])
    token_payload = {
        constants.CLIENT_ID_KEY : env[constants.AUTH0_CLIENT_ID_KEY], 
        constants.CLIENT_SECRET_KEY : env[constants.AUTH0_CLIENT_SECRET_KEY], 
        constants.REDIRECT_URI_KEY : env[constants.AUTH0_CALLBACK_URL_KEY], 
        constants.CODE_KEY : code, 
        constants.GRANT_TYPE_KEY : constants.AUTHORIZATION_CODE_KEY
    }
    
    token_info = requests.post(token_url, data=json.dumps(token_payload), headers = json_header).json()   
    if constants.ACCESS_TOKEN_KEY in token_info:
        user_url = "https://{domain}/userinfo?access_token={access_token}".format(
            domain=env[constants.AUTH0_DOMAIN_KEY], 
            access_token=token_info[constants.ACCESS_TOKEN_KEY])
			
        user_info = requests.get(user_url).json() 
        session[constants.PROFILE_KEY] = user_info
        return redirect('/dashboard')		  
    else:
        if constants.ERROR_KEY in token_info:        
            return redirect('/error')	

			
if __name__ == "__main__":
    app.run(host='0.0.0.0', port = int(os.environ.get('PORT', 3000)))
