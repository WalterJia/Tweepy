import re
from slistener import SListener
import time, tweepy, sys

## authentication
consumer_key='ADkRaS6DPMtkTUrFLNh274epu'
consumer_secret='aXL9XGEzxaWIfWUJ0xAtUTPmWAa923i6PxDSXjKnpYNLsY6yWs'
access_token='720837975165112321-JiHizpiyFLaJlCYXVLhAjUYRNsCujEV'
access_token_secret='7vAZMk4D1IVMKRq7FZDBuXH4uJvBjsAD82RNhcuJDVvxE'

def main():
    #track = ['obama', 'romney']
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api      = tweepy.API(auth)
    track = ['IOT backdoor','Zero-Day','zeroday','Remote Command Execution','CVE-2017','0day exploit']
 
    listen = SListener(api, 'myprefix')
    while True:
        stream = tweepy.Stream(auth, listen)
        print "Streaming started..."

        #stream.filter(track = track)
        try: 
            stream.filter(track = track)
            #stream.filter(track = track, async=True)
        except:
            print "exception error!"
            continue
            #stream.disconnect()

if __name__ == '__main__':
    main()
