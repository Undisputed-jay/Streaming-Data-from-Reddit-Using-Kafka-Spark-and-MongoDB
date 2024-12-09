import os
import configparser

parser = configparser.ConfigParser()
parser.read('config/reddit.conf')

client_id = parser.get('reddit', 'CLIENT_ID')
client_secret = parser.get('reddit', 'CLIENT_SECRET')
user_agent = parser.get('reddit', 'USER_AGENT')