import requests
from bs4 import BeautifulSoup

async def get_tweet(tweet):

    r = requests.get("https://publish.twitter.com/oembed?url=%s" % tweet)
    print (r)
    return (r)
    #r = r.json()['html']

    #soup = BeautifulSoup(r, 'html.parser')
    #return (soup.find('blockquote').find('p').get_text(strip=True))

def get_users(query):
    """
    This function constructs a Twitter search link from the user's input,
    retrieves and displays each user from that link.
    """
    # Construct the Twitter search link
    url_start = ("https://publish.twitter.com/oembed?url=")
    url_end = "https://twitter.com/taylorswift13/status/1781171613058097619"
    #query = query.replace(" ", "%20")
    tweet_link = url_start + url_end
    r = requests.get(tweet_link)
    r = r.json()['html']
    soup = BeautifulSoup(r, 'html.parser')
    return (soup.find('blockquote').find('p').get_text(strip=True))


    # Find all user links in the search results
    #user_links = soup.find_all('a', class_='css-4rbku5 css-18t94o4 css-1dbjc4n r-1loqt21 r-1wbh5a2')

    #users = []
    #for link in user_links:
        # Extract the username from the user link
        #username = link['href'].split('/')[-1]
        #users.append(username)
    
    #return users

#user_input = input("Enter your search query: ")
#print(get_users(user_input))
#print (users)
#if users:
#    print("Users found:")
#    for user in users:
#        print(user)
#else:
#    print("No users found.")

# We would probably maybe have two gets, where one is ust for the embed code, 
# and the other for sentiment data! we would pass both ytohugh to jinja!