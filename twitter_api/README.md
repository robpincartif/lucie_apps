twitter_api
==============

Utility package containing a node that can be used to manage twitter accounts from ROS


## Installation

Install Twython via pip

```
    $ pip install twython
```

or, with easy_install

```
    $ easy_install twython
```

## Starting Out


  * Go to ` https://dev.twitter.com/apps ` and register an application
  * If the application is registered, hit the ` Test OAuth `. Skip the two following steps.
  * Go to the settings tab and chage permitions to ` Read, Write and Access direct messages `
  * Go back to the Details tab and at the botton hit the ` Create Access Token Button `
  * Go to OAuth tool tab and get the <strong>Consumer key</strong>, <strong>Consumer secret</strong>, <strong>Access token</strong> and <strong>Access token secret</strong> and save them on `/opt/strands/strands_catkin_ws/src/strands_deployment/strands_parameters/defaults/twitter_params.yaml` with the format as follows:
    ``` 
    twitter: 
        appKey: '<ConsumerKey>'
        appSecret: '<ConsumerSecret>'
        oauthToken: '<AccessToken>'
        oauthTokenSecret: '<AccessTokenSecret>'
    
    ```

  * Save the parameters on your files <strong>tweet.py</strong> and <strong>streamer.py</strong>:

``` 
	APP_KEY='Nkq8oSHsrSSICjnZuSf88bray'
	APP_SECRET='V0scqfG9u3j0KJCzV4y2HKSIma4NXw5NizXViebvkz9qt9f3LK'
	OAUTH_TOKEN='3499297936-gTkxBYcgYNehOyEdldu8n7ncvIoIOYNHgcholQ6'
	OAUTH_TOKEN_SECRET ='TfY8CLUKLx74dQ7hoaYMZuAhezI6DZ3uLtkUIpHoJKawO'
    
```

  * Now you are ready to go!

## Tweeting

The twitter count <strong>@LucieLAMoR</strong>, <strong>password:lamor2015</strong>
The incomming tweet must to include:
  * @LucieLAMoR and:
  	* <strong>good robot, cool robot, great robot</strong>kicks the hormone down if the service /aes/nasty is called
  	* <strong>bad robot, rubbish robot</strong>kicks the hormone down if the service /aes/nasty is called
  	* <strong>coffee,  #Coffee, </strong>the server <strong>find_object</strong> is called
