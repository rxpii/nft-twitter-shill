import os
import time
import tweepy
from random import randint
from dotenv import load_dotenv

CHECK_DELAY = 30 * 60
REPLY_DELAY = 60
REPLY_VARIANCE_DELAY = 30
RATE_LIMIT_DELAY = 60 * 60
MIN_RETWEETS = 20
COUNT = 30

def relevant_stat(stat):
    if stat.retweet_count < MIN_RETWEETS: return False
    return True

def form_reply(message, user):
    return "@{} {}".format(user.screen_name, message)

def check_timeline(api, shill_msg, since_id):
    new_stats = api.home_timeline(count=COUNT, since_id=since_id, exclude_replies=True)
    new_since_id = since_id

    reply_count = 0
    for stat in new_stats:
        new_since_id = max(new_since_id, stat.id)
        if not relevant_stat(stat): continue

        # generate mesage and post
        reply = form_reply(shill_msg, stat.user)
        try:
            api.update_status(status=reply, in_reply_to_status_id=stat.id)
            print("Replied to tweet with {} retweets, {} likes".format(stat.retweet_count, stat.favorite_count))
        except Exception as e:
            print(e)
            print("Error occured with reply, skipping to next")

        # sleep for a bit to avoid violating TOS
        delay_until_next_reply = REPLY_DELAY + randint(0, REPLY_VARIANCE_DELAY)
        print("Waiting {}s until next reply".format(delay_until_next_reply))
        time.sleep(delay_until_next_reply)

        reply_count += 1

    print("Parsed {} tweets, replied to {}".format(len(new_stats), reply_count))

    return new_since_id

def create_api():
    load_dotenv()

    API_KEY = os.getenv('API_KEY')
    API_KEY_SECRET = os.getenv('API_KEY_SECRET')
    BEARER_TOKEN = os.getenv('BEARER_TOKEN')
    ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
    ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

    auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    # create API object
    api = tweepy.API(auth)

    return api

def main():
    api = create_api()
    #shill_msg = "Super mysterious project that only the smartest can get it, no clue what it's all about yet but it'll probably be big https://discord.gg/Y9n5qhga" 
    shill_msg = "This is going to be bigger than 0N1 Force. Whitelisting happening now https://discord.gg/rHnxyjQv" 
    
    #shill_msg = "Polar bears NFT. Whitlisting now, CLOSING IN 6HRS https://discord.gg/3pvSv4ep" 
    since_id = 1
    while True:
        try:
            since_id = check_timeline(api, shill_msg, since_id)
            print("Waiting...")
            time.sleep(CHECK_DELAY)
        except Exception as e:
            # in case we hit the rate limiter
            print(e)
            print("Hit rate limit, sleeping for {}s".format(RATE_LIMIT_DELAY))
            time.sleep(RATE_LIMIT_DELAY)

if __name__ == '__main__':
    main()
