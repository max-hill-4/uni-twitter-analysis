import tweepy


# Authenticate with Twitter API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Create the API object
api = tweepy.API(auth)

def get_last_tweet(username):
    try:
        # Get the user's timeline
        tweets = api.user_timeline(screen_name=username, count=1, tweet_mode='extended')

        if not tweets:
            print(f"No tweets found for {username}")
            return

        # Extract and print the last tweet
        last_tweet = tweets[0]
        print(f"Last tweet by {username}:\n{last_tweet.full_text}")

    except tweepy.TweepError as e:
        print(f"Error: {e}")

# Replace 'username' with the Twitter handle of the user you want to fetch the last tweet for
get_last_tweet('username')