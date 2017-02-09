import pandas as pd
from python.twitter_authentication import authenticate_twitter


def scrape_tweets(SEARCHTERM, n):
    """
    Input: a search term and a number of tweets to grab
    Output: a pandas dataframe of the tweet text and other parameters
    """
    twitter_api = authenticate_twitter()
    data_types = ['id', 'text', 'retweet_count']
    
    tweets_dict = {}
    tweets_dict['id'] = []
    tweets_dict['text'] = []
    tweets_dict['retweet_count'] = []
      
    # initial search without max_id parameter
    search = twitter_api.search.tweets(q=SEARCHTERM, count=100)
    results = list(search.values())
    
    for data in data_types:
        for i in range(100):
            tweets_dict[data].append(results[0][i][data])
        
    # now repeat the request to get rest of results,
    # setting max_id to the lowest id - 1 (to avoid duplicate tweets)
    for i in range(n // 100 - 1):
        print('Getting tweets', (i+1)*100, 'to', (i+2)*100)
        search = twitter_api.search.tweets(q=SEARCHTERM, 
                                           count=100, 
                                           max_id=str(min(tweets_dict['id'])-1))
        results = list(search.values())

        for data in data_types:
            for i in range(100):
                tweets_dict[data].append(results[0][i][data])
    
    # convert to a pandas dataframe and return
    return pd.DataFrame(tweets_dict)


def scrape_tweets_improved(SEARCHTERM, n):
    """
    Input: a search term and a number of tweets to grab
    Output: a pandas dataframe of the tweet text and other parameters
    This removes the O(n) min() operation and hopefully speeds up the code
    """
    twitter_api = authenticate_twitter()
    data_types = ['id', 'text', 'retweet_count']
    
    tweets_dict = {}
    tweets_dict['id'] = []
    tweets_dict['text'] = []
    tweets_dict['retweet_count'] = []
    max_id = 999999999999999
        
    for i in range(n // 100):
        print('Getting tweets', i*100, 'to', i*100)

        search = twitter_api.search.tweets(q=SEARCHTERM, 
                                           count=100, 
                                           max_id=str(max_id - 1))
        results = list(search.values())

        for data in data_types:
            for i in range(100):
                if data == 'id' and results[0][i][data] < max_id:
                    max_id = results[0][i][data]
                tweets_dict[data].append(results[0][i][data])
    
    # convert to a pandas dataframe and return
    return pd.DataFrame(tweets_dict)


if __name__ == "__main__":
    pass
    