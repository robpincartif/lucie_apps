#!/usr/bin/env python

import rospy
from time import sleep
from strands_tweets.srv import *
import rospy
from twython import Twython, TwythonError
import scitos_msgs.msg
import actionlib
from wait_action.msg import *
import time
import std_srvs.srv

from twython import TwythonStreamer

class MyStreamer(TwythonStreamer):

    def on_success(self, data):
        if 'text' in data:
            #received = data['text'].encode('utf-8')
            received = data['text']
            print received
            print data
            print data['in_reply_to_screen_name']
            user = data['user']['screen_name']
            print user
            #hashtags= data['hashtags']['text']
            #print hashtags
            if 'entities' in data:
                entities=data['entities']
                print entities
                hashtags=entities['hashtags']
                for j in hashtags:
                    text_2=j['text']
                    print (text_2)

            if '@LucieLAMoR' in received :
                request = received.replace("@LucieLAMoR", "");
                
                code = self._get_req_code_hashtags(request)
                if code ==-1:
                    code = self._get_req_code_text(request)
                print code
                understood = False
                
                #Battery
                if code == 1 :
                    charsubs = rospy.Subscriber("/battery_state", scitos_msgs.msg.BatteryState, self._battery_callback)
                    timeout=0
                    self._battery_received=False
                    while (not self._battery_received) and timeout < 100 :
                        sleep(0.05)
                        timeout=timeout+1
                    charsubs.unregister()
                    if timeout >= 100 :
                        answer = "@%s I can\'t tell you right now, try again later" %user
                    else :
                        if self._at_charger :
                            answer = "@%s my battery level is %d, and I am charging" %(user,self._battery_level)
                        else :
                            answer = "@%s my battery level is %d" %(user,self._battery_level)

                    
                #Coffe
                if code == 3 :
                    understood = True
                    answer = "@%s Ok. I will be looking for some coffee " %user
                    print answer
                    wait_secs = 5
    
                    # wait a duration
                    client = actionlib.SimpleActionClient('find_object', WaitAction)
                    client.wait_for_server()
                    goal = WaitGoal(wait_duration=rospy.Duration(wait_secs))
                    client.send_goal(goal)
                    client.wait_for_result()
                                #Nice
                if code == 4 :
                    answer = "@%s Thank you" %user
                    print answer
    
                    # wait a duration
                    answer=''+answer+ '  #'+time.strftime("%x")+'_'+ time.strftime("%X") 
                    print answer
                    twitter.update_status(status=answer)
                    rospy.wait_for_service('aes/nice')
                    try:
                        s = rospy.ServiceProxy(name,std_srvs.srv.Trigger)
                        resp = s()
                    except rospy.ServiceException,e:
                        print "Failed: %s" % e

                                #Nice
                if code == 5 :
                    answer = "@%s That\'s rude" %user
                    print answer
                    
                    answer=''+answer+ '  #'+time.strftime("%x")+'_'+ time.strftime("%X") 
                    print answer
                    twitter.update_status(status=answer)
    
                    # wait a duration
                    rospy.wait_for_service('aes/nasty')
                    try:
                        s = rospy.ServiceProxy(name,std_srvs.srv.Trigger)
                        resp = s()
                    except rospy.ServiceException,e:
                        print "Failed: %s" % e
              
                # not understood    
                if not understood: 
                    answer = "@%s I still don\'t know what you are talking about, but I will soon" %user
                    print answer
                
                answer=''+answer+ '  #'+time.strftime("%x")+'_'+ time.strftime("%X") 
                print answer
                twitter.update_status(status=answer)


            
        # Want to disconnect after the first result?
        # self.disconnect()

    def _get_req_code_text(self, request):
        code = -1
        if 'I need some coffee' in request:
            code = 3
        if 'I need a cup of coffee' in request:
            code = 3
        if 'coffee' in request:
            code = 3
        if 'good robot' in request:
            code = 4
        if 'great robot' in request:
            code = 4
        if 'cool robot' in request:
            code = 4
        if 'smart robot' in request:
            code = 4
        if 'bad robot' in request:
            code = 5
        if 'rubbish robot' in request:
            code = 5
            
        return code
        
    def _get_req_code_hashtags(self, request):
        code = -1
        if 'Battery' in request:
            code = 1
        if 'battery' in request:
            code = 1
        if 'Position' in request:
            code = 2
        if 'position' in request:
            code = 2
        if 'Coffee' in request:
            code = 3
        if 'coffee' in request:
            code = 3
            
        return code

    def on_error(self, status_code, data):
        print status_code, data

    def _battery_callback(self, data):
        print "."
        self._at_charger=data.charging
        self._battery_level=data.lifePercent
        self._battery_received=True


if __name__ == '__main__':
    rospy.init_node('lamor_tweet_replier')

    print "Init node"
    #APP_KEY = rospy.get_param("/twitter/appKey")
    #APP_SECRET = rospy.get_param("/twitter/appSecret")
    #OAUTH_TOKEN = rospy.get_param("/twitter/oauthToken")
    #OAUTH_TOKEN_SECRET = rospy.get_param("/twitter/oauthTokenSecret")
    APP_KEY='Nkq8oSHsrSSICjnZuSf88bray'
    APP_SECRET='V0scqfG9u3j0KJCzV4y2HKSIma4NXw5NizXViebvkz9qt9f3LK'
    OAUTH_TOKEN='3499297936-gTkxBYcgYNehOyEdldu8n7ncvIoIOYNHgcholQ6'
    OAUTH_TOKEN_SECRET ='TfY8CLUKLx74dQ7hoaYMZuAhezI6DZ3uLtkUIpHoJKawO'
    print "Creating Twitter Object"
    twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    print "Creating Streamer"
    stream = MyStreamer(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    stream.user()
    self.disconnect()

    #stream.site(follow='twitter')
