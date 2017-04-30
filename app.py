from flask import Flask, redirect, url_for, session, request, render_template, jsonify
from apiclient import discovery
from oauth2client import client
from urllib2 import Request, urlopen, URLError
from flask_oauth import OAuth
import httplib2
from json import dumps

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

@app.route('/load_events')
def load_events():
    return jsonify(get_events())
    
@app.route('/create_event')
def create_event():
    """ creates an event """
    credentials = client.OAuth2Credentials.from_json(session['credentials'])
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)
    
    event = {
      'summary': req['name'],
      'description': req['descrip'],
      'start': {
        'dateTime': req['date'] + 'T' + req['starttime'],
        'timeZone': 'America/New_York',
      },
      'end': {
        'dateTime': req['date'] + 'T' + req['endtime'],
        'timeZone': 'America/New_York',
      },
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    return jsonify({'success': True})
    

@app.route('/edit_event')
def edit_event():
    """ edits an event """
    req = request.json
    credentials = client.OAuth2Credentials.from_json(session['credentials'])
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)
    
    event_id = req['event_id']
    
    event = service.events().get(calendarId='primary', eventId=event_id).execute()

    event['summary'] = req['name']
    event['description'] = req['descrip']
    event['start']['dateTime'] = req['date'] + 'T' + req['starttime']
    event['start']['timeZone'] = 'America/New_York'
    event['end']['dateTime'] = req['date'] + 'T' + req['endtime']
    event['end']['timeZone'] = 'America/New_York'

    updated_event = service.events().update(calendarId='primary', eventId=event['id'], body=event).execute()

    return jsonify({'success': True})
    

@app.route('/delete_event')
def delete_event():
    """ deletes an event """
    req = request.json
    credentials = client.OAuth2Credentials.from_json(session['credentials'])
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)
    
    event_id = req['event_id']
    
    service.events().delete(calendarId='primary', eventId= event_id).execute()
    
    return jsonify({'success': True})

def get_events():
    """Creates a Google Calendar API service object and outputs a list of all events and their pertinent info
    """
    # get credentials
    credentials = client.OAuth2Credentials.from_json(session['credentials'])
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)
    
    # while loop through all events
    page_token = None
    while True:
        events = service.events().list(calendarId='primary', pageToken=page_token).execute()

        # loop through all events
        events_list = []
        for event in events['items']:
            # event id
            eventid = event['id']
            # name
            name = event['summary']

            # description
            if 'description' in event:
                descrip = event['description']
            else:
                descrip = ''
                
            # date and time
            if 'dateTime' in event['start']:
                # date
                dateTime = event['start']['dateTime'].split('T')
                old_date = dateTime[0].split('-')
                new_date = '/'.join([str(old_date[1]),str(old_date[2]),str(old_date[0])])
                # time
                start_time = dateTime[1].split('-')[0]
                end_time = event['end']['dateTime'].split('T')
                end_time = end_time[1].split('-')[0]
            elif 'date' in event['start']:
                date = event['start']['date']
                old_date = date.split('-')
                new_date = '/'.join([str(old_date[1]),str(old_date[2]),str(old_date[0])])
                if len(new_date) == 10:
                    start_time = 'all day'
                    end_time = 'all day'
               
            # create dictionary for each event 
            if len(descrip) > 0:
                
                update_dict = {'name':name,'event_id':eventid,'date':new_date,'start time':start_time,'end time':end_time,'description':descrip}
            else:
                update_dict = {'name':name,'event_id':eventid,'date':new_date,'start time':start_time,'end time':end_time,}
                
            # append each dictionary to lsit
            events_list.append(update_dict)
        
        # end loop when no more events 
        page_token = events.get('nextPageToken')
        if not page_token:
            break
 
    events_dict = {'events': events_list}
    print(events_dict)
    return dumps(events_dict)

app.run()