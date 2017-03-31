#!/usr/bin/python

from slackclient import SlackClient
import requests
import time
import ConfigParser

Config = ConfigParser.ConfigParser()
Config.read("settings.cfg")
slack_token = Config.get("Auth", "Token")
print "Token: ", slack_token
#slack_token = "xoxb-162589215410-Donj3LkEYbkhZqkA5sATfhMS"
sc = SlackClient(slack_token)

def get_user_from_id(userid):
    try:
        payload = {'token':slack_token, 'user':userid}
        r = requests.get('https://slack.com/api/users.info', params=payload)
        response = r.json()
        print "------"
        print response
        print "------"
        return response["user"]["name"]
    except:
        return "ResponseError"



def parse(msg):
    try:
        if msg == []:
            return

        if msg["type"] == "message":
            username = get_user_from_id(msg["user"])
            if msg["text"] == "Hi Bonsai":
                sc.rtm_send_message(msg["channel"], "Hola %s" % (username))
                sc.rtm_send_message("D4SJGRPC4", "%s hat mir gerade geschrieben" % (username) ) # should be the private channel between bot and weis
    except:
        print "Error"


if sc.rtm_connect():
    while True:
        got = sc.rtm_read()
        print sc.rtm_read()
        for g in got:
            parse(g)
        time.sleep(1)
else:
    print "Connection failed"
