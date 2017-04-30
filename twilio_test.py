"""twilio test program
"""
from __future__ import print_function
from twilio.rest import Client

def send_notification(to_num,text):
    
    # open authentifcation credentials
    infile = open('twilio_auth.txt','r')
    account_sid = infile.readline()[:-1]
    auth_token = infile.readline()
    
    # create client object
    client = Client(account_sid, auth_token)

    # send text
    client.messages.create(
        to = to_num,
        from_ = "6176066087",
        body = text
        media_url = "https://img.buzzfeed.com/buzzfeed-static/static/enhanced/webdr02/2012/12/15/17/anigif_enhanced-buzz-3799-1355608849-1.gif")