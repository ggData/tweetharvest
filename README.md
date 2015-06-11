# tweetharvest

`tweetharvest` is a Python utility to monitor Twitter conversations around a small set of hashtags, and to store statuses (tweets) from that stream to a MongoDB database. The intended use case: collecting tweets from discussions around a given event or campaign, and storing them locally for later analysis. `tweetharvest` does not contain any analytic functions; it [does one thing well](http://en.wikipedia.org/wiki/Unix_philosophy#Do_One_Thing_and_Do_It_Well): data collection from the Twitter API.

## Setting Up

The program has been developed on Python 2.7 on Mac OSX. It has run successfully on Windows 7 and on Ubuntu.

The setup process assumes Python 2.7 is installed on the system you are using. Further installation requires:

1. Cloning this repository
2. Installation of MongoDB and starting the MongoDB server
3. Installation of selected Python libraries
4. Creation of a Twitter App and authorisation of the App on the harvesting machine
5. Selection of hashtags to be monitored
6. Running a harvest session

These steps will be described in detail.

### Clone this repository

You can download this repository as a [zip file](https://github.com/ggData/tweetharvest/archive/master.zip) or clone it:

    $ git clone https://github.com/ggData/tweetharvest

After unpacking the zip archive or cloning, `cd` into the `tweetharvest` directory:

    $ cd tweetharvest

### Install MongoDB

Download the appropriate [MongoDB installer](https://www.mongodb.org/downloads) for your system and follow the instructions to set it up on Linux (installation instructions vary by distro; see [the relevant download page](https://www.mongodb.org/downloads#linux-new)), [Windows](http://docs.mongodb.org/manual/tutorial/install-mongodb-on-windows/?_ga=1.167442750.1237211192.1434015304), or [Mac OSX](http://docs.mongodb.org/manual/tutorial/install-mongodb-on-os-x/?_ga=1.259119114.1237211192.1434015304).

### Start the MongoDB Server

In order to start storing statuses, we need to start up the MongoDB server:

    $ cd data
    $ mongod --dbpath .

MongoDB starts up, reserves disk space, and creates blank journal files, all ready to start receiving tweets for storage.

**Note**: if at any time you want to stop the MongoDB server, go to the console window where it is running and press `Control-C`.

Leave the MongoDB server running in this window and open a new terminal/console window. `cd` to the tweetharvest directory:

    $ cd path/to/tweetharvest

### Installation of Python Packages

The harvest program requires three external Python packages, which now need to be installed.

- It uses [Delorean](https://pypi.python.org/pypi/Delorean/0.4.5), "library for manipulating datetimes with ease and clarity". The [installation instructions](http://delorean.readthedocs.org/en/latest/install.html) in most cases reduces to a simple:

    `$ pip install delorean`

- [PyMongo](http://api.mongodb.org/python/current/) "is a Python distribution containing tools for working with MongoDB, and is the recommended way to work with MongoDB from Python". Installation [instructions are provided here](http://api.mongodb.org/python/current/installation.html), but again in most cases, all we need is:

    `$ pip install pymongo`

- Finally we need the [twitter](https://pypi.python.org/pypi/twitter) package, a "minimalist Twitter API for Python". The [installation instructions]() suggest you should use `setuptools` to install the package but again, I found this to be sufficient:

    `$ pip install twitter`

### Creation of a Twitter App

In order to harvest statuses from the Twitter stream, you need to have a Twitter account and to create a "Twitter App". Both are free and easy to create.

1. You probably already have a Twitter acccount. If not, head over to the [home page](https://twitter.com/) and sign up.
2. **Create an app**: Head over to the [application management dashboard](https://apps.twitter.com/) and hit the `Create New App` button.

When creating an app, provide the app **name** (e.g. 'Happy Harvester'), **description** (e.g. 'An app to collect tweets with the emotional hashtags like #happy'), and *website** (if you do not have a website, you may have a placeholder such as `http://www.example.com` and update this later when you do set up a website). Do not fill in the **Callback URL** field. Don't forget to check the box `Yes, I agree` below the Developer Agreement, and click the button to `Create your Twitter application`.

### Authorisation of the App

If the application creation process succeeded, you will be taken to the its home screen. Switch to the tab _Keys and Access Tokens_. Make a note of the Consumer Key and the Consumer Secret that you see there (for example, copy and paste them to a text editor). These should never be shared with anyone as they represent your app's credentials with Twitter; otherwise anyone who has access to them could use them masquerade as your app.

You will now need to insert these credentials into the program. Navigate to the `secret` folder:

    $ cd path/to/tweetharvest/lib/secret

Rename the file called `twitconfig.py.bak` to `twitconfig.py`:

    $  mv twitconfig.py.bak twitconfig.py

Edit this file in a text editor and insert your consumer key and consumer secret in between the quotation marks on lines 6 and 7. They look like this when you first open the file:

    CONSUMER_KEY = 'InsertYourConsumerKeyHere'
    CONSUMER_SECRET = 'InsertYourConsumerSecretHere'

Make sure you preserve the quotes when you past your tokens. The end result should look something like this:

    CONSUMER_KEY = 'Tte0jQJPFUph6hX66h8Rai6g5'
    CONSUMER_SECRET = 'XpQ2AvcEYhMkyXTwMkOT9tQAtddB7UusbHFon0BS5JeHkEliB0'

#### Check Authorization is Working

You now need to check that the authorization is working. Navigate back to the root folder and run the `auth.py` script:

    $ cd path/to/tweetharvest
    $ python auth.py

If all is working, you should get the following output:

    App is authorised, congratulations!

If you have made a mistake in the above process, you will get something like the following (with a printout of the detailed error received):

    Unable to authorise app. Full report follows.

Hopefully you will have been successful and now have authorized your harvester to collect statuses from Twitter. If there has been an error, the most likely issue is that the credentials were entered incorrectly or that a network connection failed. Try to troubleshoot and use the normal discussion fora to check on solutions. Consider [submitting an issue here](https://github.com/ggData/tweetharvest/issues) if you think this is a general problem or a bug in the program.

### Selection of hashtags to be monitored

We now come to the heart of the process. We have a MongoDB server running and ready to receive tweets. We have an app that has been authorized to collect statuses from the Twitter API. All we need is to select what we want to monitor. This is best illustrated by example. Let us imagine we are interested in monitoring expressions of two emotions and we decide to monitor two hashtags: `#happy` and `#sad`. We shall call our project `emotweets`. This is all we need to configure our app:

1. Create a file called `tags_emotweets.txt` in the tweetharvest root folder, beside `main.py`. (Note: for any project called `projectname`, our program expects to find a file called `tags_projectname.txt` in the root folder).
2. We insert each of the hashtags that we want to monitor on a separate line in this file. An example file is provided as a template. (In the example project, we insert the words `happy` and `sad` onto two lines and save the file).

This is all we need to run the `emotweets` harvest! In the case of this example, the `tags_emotweets.txt` configuration file is provided as a model for your own projects. There should be one such `tags_xxx.txt` file per project. Please also note that you can only monitor one project at a time (more on that later).

### Running a harvest session

It is assumed that you have MongoDB running in the background. If you have done this setup process in one session, it should still be running. If not, then go to the section 'Start the MongoDB Server' above and start it up...

Navigate to the root directory again and run the `main.py` script, giving it the project name as an argument:

    $ cd path/to/tweetharvest
    $ python main.py emotweets

If successful, you should now start getting outputs of this sort:

    sad -1
    happy -1
    100 / 100 #sad
    100 / 100 #happy
    100 / 100 #sad
    100 / 100 #happy
    99 / 100 #sad
    96 / 100 #happy

These lines appear with a delay of about 3 seconds between one and the other, thus ensuring that we stay within Twitter's rate-limiting policies. The lines tell us that:

- the program is working and actively collecting tweets
- the initial lines report the hashtags that we are monitoring and the id of the most recent tweet for that hashtag in our database. If there are no tweets yet, we get `-1`, as in this instance.
- every few seconds, our programme retrieves up to 100 tweets from Twitter for a given hashtag. It reports how many of these tweets are new in our database. The last line in our example output says that we retrieved 100 tweets with the hash `#happy` but only 96 of them were new.

### Stopping and Starting

At this stage the console reports that `tweetharvest` is merrily downloading emotional tweets for us. Eventually a number of things may happen:

- We may decide to stop the harvest. This can be done by pressing `Control-C` at any time and Python will exit the harvest. One reason we may want to stop is that we start to see that we are getting no fresh tweets for every set that we are downloading (for instance, we start to see `0 / 100 #happy` repeatedly in the output). It may be good practice to stop harvesting and return to it later. Generally Twitter will let us access the tweets from the past two weeks so we may want to run our harvest for a couple of hours every day and this will usually be sufficient for a complete collection.
- We may notice that the program has stopped with an error report. There is no effort to compensate for these in the program, as there are many errors possible (Twitter may temporarily be down, your network is temprarily down, etc). It is a design decision to allow these to crash the program, giving a natural break. The harvest can simply be restarted by hand at a convenient time.

## Kick-Starting Your Analysis

After a few hours, we will have accumulated an extensive collection of tweets in the Mongo database. They will be located inside a database called `tweets_db`, in a collection named `emotweets` (or whatever is our `projectname`). We can now analyze the data using any tools we prefer.

As an aid to kick-starting your analysis, an example IPython notebook (called `example.ipynb`) can be found in this repository and can also be viewed online.
