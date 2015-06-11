# -*- coding: utf-8 -*-

import os
import sys
from time import sleep
import logging

from pymongo import MongoClient
from delorean import parse

from lib.secret.twitconfig import T  # hide access keys


# provide project name as a command line argument
# use lowercase ascii-only no-spaces 
# (the program does not check for these yet -- so take care)
try:
    PROJECT = sys.argv[1]
except:
    raise KeyError('No project name provided.')

# put hashtags in a text file called tags_<PROJECT>.txt next to this script

SIGINT_RCVD = False  # Converted to True when Ctrl-C is pressed

CLIENT = MongoClient('localhost', 27017)
DB = CLIENT.tweets_db
TWEETS = DB[PROJECT]

TAGS_FILE = os.path.join('tags_{}.txt'.format(PROJECT))
LOG_FILE = os.path.join('logs', 'log_{}.txt'.format(PROJECT))

TAG_DICT = {}


def get_tweets(query, count=100, max_id=-1):
    if max_id != -1:
        retriever = T.search.tweets(q=query,
                                    count=count,
                                    max_id=max_id)
    else:
        # on first call, only send count, to get oldest tweets for query
        retriever = T.search.tweets(q=query,
                                    count=count)

    statuses = retriever[u'statuses']
    # sleep_int = get_sleep_interval()
    sleep(2.3)  # comply with API level rate-limiting: 450 calls in every 15 min window
    if len(statuses) > 0:
        msg = 'Query: {}. Loaded {} statuses from id {} to id {}.'
        msg = msg.format(query,
                         len(statuses),
                         statuses[0]['id'],
                         statuses[-1]['id'])
        logging.info(msg)
        new_max = insert_tweets(statuses, query)
        return new_max
    else:
        logging.info('No tweets for hashtag: {}.'.format(query))
        return False


def make_hash_field(hashtags):
    tag_list = []
    for item in hashtags:
        tag_lc = item['text'].lower()
        tag_list.append(tag_lc)
    return tag_list


def insert_tweets(tweets, query):
    # TODO clean up the logic re the max_id -- the current tweet_id is not
    # necessarily the max id for all hastags being monitored! We need to keep
    # separate max_id for each tag...

    max_id = -1
    results = []
    feedback = ''
    for tweet in tweets:
        tweet['_id'] = tweet['id']
        max_id = int(tweet['_id'])
        tweet.pop('id', None)  # delete the old id key
        tweet['hashtags'] = make_hash_field(tweet['entities']['hashtags'])
        tweet['created_at'] = parse(tweet['created_at']).datetime
        tweet['user']['created_at'] = parse(tweet['user']['created_at']).datetime
        try:
            result = TWEETS.update({'_id': tweet['_id']}, tweet, upsert=True)
            # print '{} inserted with tags {}'.format(result, tweet['hashtags'])
            results.append(result)
        except:
            logging.info('ERROR in updating document id: {}.'.format(tweet['_id']))
    feedback = ['+' for result in results if not result['updatedExisting']]
    feedback = '{:3} / {:3} {}'.format(len(feedback), len(tweets), query)
    print feedback
    return max_id


def get_tags(fyle):
    with open(fyle, 'rb') as f:
        lines = f.readlines()
    hash_tags = [ln.strip()
                 for ln in lines
                 if not ln.startswith('#') and ln.strip()]
    return hash_tags


def process_tags(sigint):
    # NOTE that hashtags in tag_dict have no leading # sign but this is needed for Twitter API queries
    # foreach item in the queue get max id and
    # send a call to get_tweets, go to next in the queue, cycle
    queue = TAG_DICT.keys()
    try:
        while not sigint:
            tag = queue.pop(0)
            # query = tag
            query = '#' + tag
            maxid = TAG_DICT[tag]
            # print '{}: Getting query {} from maxid {} in queue {}'.format(cycles, query, maxid, str(queue))
            maxid = get_tweets(query, max_id=maxid)
            if maxid:
                TAG_DICT[tag] = maxid
            queue.append(tag)
    except KeyboardInterrupt:
        sigint = True
        logging.info('SIGINT received. Capture terminated by user.')


def get_latest_id(spec):
    """Find the first and last document given a spec dict"""
    try:
        # latest = TWEETS.find_one(spec)
        # latest = TWEETS.find(spec).sort([('_id', -1)]).limit(1).next()
        latest = TWEETS.find(spec).sort([('_id', -1)]).limit(1).next()
        latest = latest['_id']
    except:
        latest = -1
    return latest


def main():
    tags = get_tags(TAGS_FILE)

    for tag in tags:
        doc_max_id = get_latest_id(spec={'hashtags': tag})
        if doc_max_id:
            TAG_DICT[tag] = doc_max_id
        else:
            TAG_DICT[tag] = 0

    for k, v in TAG_DICT.iteritems():
        print k, v

    logging.basicConfig(filename=LOG_FILE,
                        level=logging.DEBUG,
                        format='%(asctime)s %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p')
    logging.info('Started loading tweets.')
    process_tags(sigint=SIGINT_RCVD)


if __name__ == '__main__':
    main()
