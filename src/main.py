import time
import tweepy
from random import randint
from config import Config
from util import log_err, log_out


def relevant_stat(stat, config):
    return stat.retweet_count >= config.MIN_RETWEETS


def form_reply(message, user):
    return "@{} {}".format(user.screen_name, message)


def check_timeline(api, shill_msg, since_id, config):
    new_stats = api.home_timeline(count=config.FETCH_COUNT,
                                  since_id=since_id, exclude_replies=True)
    new_since_id = since_id

    reply_count = 0
    for stat in new_stats:
        new_since_id = max(new_since_id, stat.id)
        if not relevant_stat(stat, config):
            continue

        # generate mesage and post
        reply = form_reply(shill_msg, stat.user)
        try:
            api.update_status(status=reply, in_reply_to_status_id=stat.id)
            log_out("INFO", "Replied to tweet with {} retweets, {} likes"
                    .format(stat.retweet_count, stat.favorite_count))
        except Exception as e:
            log_out("INFO", "Error occured with reply, skipping to next")
            log_err(e)
            log_err("Error occured with reply, skipping to next")

        # sleep for a bit to avoid violating TOS
        delay_until_next_reply = \
            config.REPLY_DELAY + randint(0, config.REPLY_VARIANCE_DELAY)
        log_out("INFO",
                "Waiting {}s until next reply".format(delay_until_next_reply))
        time.sleep(delay_until_next_reply)

        reply_count += 1

    log_out("INFO",
            "Parsed {} tweets, replied to {}".format(len(new_stats), reply_count))

    return new_since_id


def create_api(config):
    auth = tweepy.OAuthHandler(config.API_KEY, config.API_KEY_SECRET)
    auth.set_access_token(config.ACCESS_TOKEN, config.ACCESS_TOKEN_SECRET)

    # create API object
    api = tweepy.API(auth)

    return api


def main():
    config = Config()
    api = create_api(config)
    log_out("INFO", "App loaded for {}".format(config.API_KEY))

    #shill_msg = "Super mysterious project that only the smartest can get it, no clue what it's all about yet but it'll probably be big https://discord.gg/Y9n5qhga" 
    
    since_id = 1
    while True:
        try:
            config.update_msg()
            since_id = check_timeline(api, config.SHILL_MSG, since_id, config)
            log_out("INFO",
                    "Finished batch, sleeping for a while ({}s)..."
                    .format(config.CHECK_DELAY))
            time.sleep(config.CHECK_DELAY)
        except Exception as e:
            # in case we hit the rate limiter
            log_err(e)
            time.sleep(config.RATE_LIMIT_DELAY)


if __name__ == '__main__':
    main()
