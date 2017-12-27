from tweepy import StreamListener
import json, time, sys
import smtplib
import re

class SListener(StreamListener):

    def __init__(self, api = None, fprefix = 'streamer'):
        self.api = api or API()
        self.counter = 0
	self.totalcounter = 0
        self.fprefix = fprefix
        self.output  = open(fprefix + '.' 
                            + time.strftime('%Y%m%d-%H%M%S') + '.json', 'w')
        self.delout  = open('delete.txt', 'a')
	self.twitter_info = ""
	self.twitter_info_cve = ""
	self.twitter_info_iot = ""
	self.dict = {}
    def sendGmail(self,FROM,TO,SUBJECT,TEXT,SERVER):
    # Send the mail
        message = """From: IOT Security Inspection  <%s>
To: To Person <%s>
MIME-Version: 1.0
Content-type: text/html
Subject: %s

<h1>This is IOT security inspection message.</h1>

%s
					
<h1>This is endline.</h1>
""" % (FROM,TO,SUBJECT,TEXT)

    	#print message
    	print "ready to send"
    	server = smtplib.SMTP(SERVER)
	#    "New part"
    	server.ehlo()
    	server.starttls()
    	server.login('name@gmail.com', 'password!')
    	server.sendmail(FROM, TO.split(","), message)
   	server.quit()
    	print "send successfully"
    def on_data(self, data):
	#print data
        if  'in_reply_to_status' in data:
            self.on_status(data)
        elif 'delete' in data:
            delete = json.loads(data)['delete']['status']
            if self.on_delete(delete['id'], delete['user_id']) is False:
                return False
        elif 'limit' in data:
            if self.on_limit(json.loads(data)['limit']['track']) is False:
                return False
        elif 'warning' in data:
            warning = json.loads(data)['warnings']
            print warning['message']
            return false

    def on_status(self, status):
        #self.output.write(status + "\n")
        #print status
        filter_str = ["RT @", "REJECT","#VulnAlert","sql injection","XSS","linux_kernel","#CVE-2017-","GPU","Google Android"]
        filter_str_1 = "CVE-2017-"
	twitter_created_at = json.loads(status)['created_at'].encode('ascii', 'ignore')
	twitter_text = json.loads(status)['text'].encode('ascii', 'ignore')
	try:
            #if "RT @" not in twitter_text and "REJECT" not in twitter_text and "#VulnAlert " not in twitter_text \
            #    and "sql injection" not in twitter_text:
            for elem in filter_str:
                if elem in twitter_text:
                    return      
            if twitter_text.find(filter_str_1) == 0:
                return
            res = re.search("CVE-2017-[0-9]{4,5}",twitter_text,re.IGNORECASE)
            if res:
                if self.dict.has_key(res.group(0)):
                    return
                self.dict[res.group(0)] = 1
                self.twitter_info_cve = "CVE:->"+ res.group(0) + " " + twitter_text + "<br/>" + self.twitter_info_cve
                print '%s' % self.twitter_info
            else:
                if self.dict.has_key(twitter_text[0:5]):
                    return
                self.dict[twitter_text[0:5]] = 1
                self.twitter_info_iot = "IOT:->" + twitter_text + "<br/>" + self.twitter_info_iot
            self.counter += 1
            print str(self.counter)
        except:
	    print "exception!!!!!!!!"
	#print '%s' % (json.loads(status)['text'].encode('ascii', 'ignore'))

        if self.counter >= 25:
            #self.output.close()
            #self.output = open('../streaming_data/' + self.fprefix + '.' 
            #                   + time.strftime('%Y%m%d-%H%M%S') + '.json', 'w')
	    self.twitter_info = self.twitter_info_iot + "<br/>-------------CVE------------<br/>" + self.twitter_info_cve
	    if self.twitter_info == "":
                print "no update"
    	    else:
                self.sendGmail('name@gmail.com','xx@gmail.com,yy@gmail.com','IOT&CVE-Twitter',self.twitter_info,'smtp.gmail.com:587')
                print "----------send gmail successfully----------"
		self.twitter_info = ""
		self.twitter_info_cve = ""
		self.twitter_info_iot = ""
		#self.dict.clear()
            self.totalcounter += self.counter
            if self.totalcounter > 200:
		self.dict.clear()
	        self.totalcounter = 0
            self.counter = 0

        return

    def on_delete(self, status_id, user_id):
        self.delout.write( str(status_id) + "\n")
        return

    def on_limit(self, track):
        sys.stderr.write(track + "\n")
        return

    def on_error(self, status_code):
        sys.stderr.write('Error: ' + str(status_code) + "\n")
        return False

    def on_timeout(self):
        sys.stderr.write("Timeout, sleeping for 60 seconds...\n")
        time.sleep(60)
        return 
