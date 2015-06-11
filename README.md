# tweetharvest

## Description

`tweetharvest` is a Python utility to monitor Twitter conversations around a small set of hashtags, and to store statuses (tweets) in that stream to a MongoDB database. The intended use case: monitoring discussions around a given event or campaign for later analysis using any tools that can access MongoDB.

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

### Install MongoDB and Start the Server

Download the appropriate [MongoDB installer](https://www.mongodb.org/downloads) for your system and follow the instructions to set it up on Linux (installation instructions vary by distro; see [the relevant download page](https://www.mongodb.org/downloads#linux-new)), [Windows](http://docs.mongodb.org/manual/tutorial/install-mongodb-on-windows/?_ga=1.167442750.1237211192.1434015304), or [Mac OSX](http://docs.mongodb.org/manual/tutorial/install-mongodb-on-os-x/?_ga=1.259119114.1237211192.1434015304).

In order to start storing statuses, we need to start up the MongoDB server:

    $ cd data
    $ mongod --dbpath .

MongoDB starts up the server, reserves disk space, and creates blank journal files, all ready to start receiving tweets for storage.

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

### Running a harvest session
