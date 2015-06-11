# README

## Description

`tweetharvest` is a Python utility to monitor Twitter conversations around a small set of hashtags, and to store statuses (tweets) in that stream to a MongoDB database. The intended use case: monitoring discussions around a given event or campaign for later analysis using any tools that can access MongoDB. An example is given of simple analysis using an IPython notebook.

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

### Installation of Python Packages

### Creation of a Twitter App

### Authorisation of the App

### Selection of hashtags to be monitored

### Running a harvest session
