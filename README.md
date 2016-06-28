# Auth0's Exercise

Language: Python

The following App demonstrates the use of Auth0's Management API (APIv2) to retrieve the list of Applications and the Rules from the Tenant. Then, by analizing the rules' script function, it determines if it applies or not to a certain application and then shows this in `dashboard.html`.

Auth0's sample webapp was modified to achieve this. It was also slightly optimized by putting most of the hardcoded strings to a constants file.

# Installation

A `.env` file with my credentials is already provided, so run `pip install -r requirements.txt` to install the dependencies. Then, run `python server.py` and try calling http://localhost:3000/ Use the credentials provided in [Users](Users)

# Management API

First, Auth0's object was imported as follows: 

```python
from auth0.v2.management import Auth0
```

Then, it was instantiated with my Auth0's domain and token (which was generated using https://auth0.com/docs/api/v2)

```python
    domain = env[constants.AUTH0_DOMAIN_KEY]
    token = constants.AUTH0_TOKEN
                       
    auth0 = Auth0(domain, token)
    applications = auth0.clients.all(fields=[constants.NAME_KEY]) 	
    rules = auth0.rules.all(fields=[constants.NAME_KEY, constants.SCRIPT_KEY])			
    return render_template('dashboard.html', user=session[constants.PROFILE_KEY], applications=applications, rules=rules)
```

Since the App was intended to be a PoC to demonstate the use of Auth0's Management API, to determine if the rule applies to a certain app, it was checked if the name of the app is present in the rule's script in the template. 

```
<h2> Application's List:</h2>
{%- for application in applications%}			
<h1> {{application['name']}}</h1>
{%- for rule in rules %}				
{%- if application['name'] in rule['script'] %}
<p><b> Rule</b>: {{rule['name']}}</p>
{%- endif %}
{%- endfor %}
{%- endfor %}
```

# Users

## Authorized Users
email: annyv2.0@gmail.com
password: TestPass

email: annybell.villarroel@techaid.co
password: TestPass

## Unauthorized User
email: annyv2.0@hotmail.com
password: TestPass