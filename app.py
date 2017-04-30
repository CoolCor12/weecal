from flask import Flask, redirect, url_for, session, request, render_template
from apiclient import discovery
from oauth2client import client
from urllib2 import Request, urlopen, URLError
from flask_oauth import OAuth
from json import dumps, load, loads
import httplib2

PARAMS = load(open('auth.json', 'r'))
GOOGLE_CLIENT_ID = PARAMS['google_client_id']
GOOGLE_CLIENT_SECRET = PARAMS['google_client_secret']
 
app = Flask(__name__)
app.debug = True
app.secret_key = 'development key'

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    if 'credentials' not in session:
        return redirect(url_for('oauth2callback'))
    
    credentials = client.OAuth2Credentials.from_json(session['credentials'])
    if credentials.access_token_expired:
        return redirect(url_for('oauth2callback'))
    else:
        #http_auth = credentials.authorize(httplib2.Http())
        #service = discovery.build('calendar', 'v3', http = http_auth)
        #service = discovery.build('calendar', 'v3', http = http_auth)
        return dumps({'success': True})
    
@app.route('/oauth2callback')
def oauth2callback():
    flow = client.flow_from_clientsecrets('client_secrets.json',
                                          scope='https://www.googleapis.com/auth/calendar',
                                          redirect_uri=url_for('oauth2callback', _external=True))
    if 'code' not in request.args:
        auth_uri = flow.step1_get_authorize_url()
        return redirect(auth_uri)
    else:
        auth_code = request.args.get('code')
        credentials = flow.step2_exchange(auth_code)
        session['credentials'] = credentials.to_json()
        return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    if 'credentials' not in session:
        return redirect(url_for('login'))
    
    return render_template('calendar.html')