from twitter.api import TwitterHTTPError

try:
    from lib.secret.twitconfig import T
    if T.domain == 'api.twitter.com':
        print 'App is authorised, congratulations!'
except TwitterHTTPError, e:
    print 'Unable to authorise app. Full report follows:\n\n'
    print e
