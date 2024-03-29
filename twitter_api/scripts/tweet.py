#!/usr/bin/env python


import rospy

from PIL import Image
from twython import Twython, TwythonError
import actionlib
from strands_tweets.srv import *
import strands_tweets.msg
import sensor_msgs.msg #import Image
import cv2
from cv_bridge import CvBridge, CvBridgeError

class tweetsServer(object):

    _feedback = strands_tweets.msg.SendTweetFeedback()
    _result   = strands_tweets.msg.SendTweetResult()

    def __init__(self, name):
        
        APP_KEY='Nkq8oSHsrSSICjnZuSf88bray'
        APP_SECRET='V0scqfG9u3j0KJCzV4y2HKSIma4NXw5NizXViebvkz9qt9f3LK'
        OAUTH_TOKEN='3499297936-gTkxBYcgYNehOyEdldu8n7ncvIoIOYNHgcholQ6'
        OAUTH_TOKEN_SECRET ='TfY8CLUKLx74dQ7hoaYMZuAhezI6DZ3uLtkUIpHoJKawO'
        
        #SACARINO
       # APP_KEY='pPKcg6UOpp6uGHCB0RKw'
       # APP_SECRET='4bpDH6Zzzhi7ckr55B3aU97yuuoEdEXGZqw5HYnqzuo'
       # OAUTH_TOKEN='494767183-48FI8MVLGrfnUhoKaXjFHjoB6cPXpq21X2jnJnkU'
       # OAUTH_TOKEN_SECRET ='FjelXTM6CTaXPZXQGWyKarLxLTvF56tuQYq8tPGXY'
        
        #APP_KEY = rospy.get_param("/twitter/appKey")
        #APP_SECRET = rospy.get_param("/twitter/appSecret")
        #OAUTH_TOKEN = rospy.get_param("/twitter/oauthToken")
        #OAUTH_TOKEN_SECRET = rospy.get_param("/twitter/oauthTokenSecret")
        self._twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
        self._tweet_srv = rospy.Service("/strands_tweets/Tweet",Tweet,self._tweet_srv_cb)
        self.tw_pub = rospy.Publisher('/strands_tweets/tweet', strands_tweets.msg.Tweeted)

        self.cancelled = False
        self._action_name = name
        rospy.loginfo("Creating action servers.")
        self._as = actionlib.SimpleActionServer(self._action_name, strands_tweets.msg.SendTweetAction, execute_cb = self.executeCallback, auto_start = False)
        self._as.register_preempt_callback(self.preemptCallback)

        rospy.loginfo(" ...starting")
        self._as.start()
        rospy.loginfo(" ...done")

        rospy.loginfo("Ready to Tweet ...")
        rospy.spin()


    def _tweet_srv_cb(self, req):
        result = self._send_tweet(req.text)
        return TweetResponse(result)


    def executeCallback(self, goal):
        self._feedback.tweet = 'tweeting...'
        self._as.publish_feedback(self._feedback)
        #print goal
        rospy.loginfo('%s: Tweeting %s' % (self._action_name, goal.text))
        if goal.with_photo :            
            result=self._send_photo_tweet(goal)
        else:
            result=self._send_tweet(goal.text)
        if not self.cancelled :
            self._result.success = result
            self._feedback.tweet = goal.text
            self._as.publish_feedback(self._feedback)
            self._as.set_succeeded(self._result)


    def _send_tweet(self, text):
        self.cancelled = False
        nchar=len(text)
        rospy.loginfo("Tweeting %s ... (%d)", text, nchar)
        if nchar < 140:
            try:
                self._twitter.update_status(status=text)
                result=True
            except TwythonError as e:
                print e
                result=False
            return result
        else:
            if not req.force:
                result=False
                rospy.loginfo("You can't send tweet with more than 140 characters unless you set the force parameter to True, your tweet had %d characters", nchar)
                return result
            else:
                ntotaltweets=1+(nchar/130)
                rospy.loginfo("You will need %d tweets to publish this", ntotaltweets)
                line = text
                n = 130
                outtext=list([line[i:i+n] for i in range(0, len(line), n)])
                outtext.reverse()
                ntweets=ntotaltweets
                for w in outtext:
                    wo = "(%d/%d) %s" % (ntweets, ntotaltweets, w)
                    try:
                        self._twitter.update_status(status=wo)
                        result=True
                    except TwythonError as e:
                        print e
                        result=False
                    ntweets= ntweets-1
                return result

    def _send_photo_tweet(self, goal):
        self.cancelled = False
        nchar=len(goal.text)
        rospy.loginfo("Tweeting %s ... (%d)", goal.text, nchar)
        if nchar < 140:
            try:
                bridge = CvBridge()
                photo = bridge.imgmsg_to_cv2(goal.photo, "bgr8")

                tweettext = strands_tweets.msg.Tweeted()
                tweettext.text = goal.text
                tweettext.photo = goal.photo
                #tweettext.depth = depth
                self.tw_pub.publish(tweettext)

                ### I MUST CHANGE THIS AS SOON AS POSSIBLE ###
                cv2.imwrite('/tmp/temp_tweet.png', photo)
                photo2 = open('/tmp/temp_tweet.png', 'rb')
                self._twitter.update_status_with_media(status=goal.text, media=photo2)
                
                result=True
            except TwythonError as e:
                print e
                result=False
            return result
        else:
            result=False
            rospy.loginfo("You can't send tweet and send an image with more than 140 characters, your tweet had %d characters", nchar)
            return result



    def preemptCallback(self):
        self.cancelled = True
        self._result.success = False
        self._as.set_preempted(self._result)
        

if __name__ == '__main__':
    rospy.init_node('lamor_tweets')
    server = tweetsServer(rospy.get_name())


