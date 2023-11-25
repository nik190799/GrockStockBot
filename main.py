import os
import json
import tweepy
import requests
import openai
from newsdataapi import NewsDataApiClient
from yahoo_fin import stock_info
from datetime import datetime
from io import StringIO
import time
from pytrends.request import TrendReq
import math
import pyshorteners


news_api_key = os.environ.get('NEWS_DATA_IO_API_KEY')
api_key = os.environ.get("X_API_KEY")
api_secret = os.environ.get("X_API_SECRET")
bearer_token = os.environ.get("X_BEARER_TOKEN") 
access_token = os.environ.get("X_ACCESS_TOKEN") 
access_token_secret = os.environ.get("X_ACCESS_TOKEN_SECRET")

news_id_file = "C:/Users/16823/Documents/X/GrokStockBot/GrockStockBot/used_news_id.txt"

auth = tweepy.OAuthHandler(api_key, api_secret)
auth.set_access_token(access_token, access_token_secret)
api1 = tweepy.API(auth, wait_on_rate_limit=True)

news_id = set()

def dallEMemeImage(prompt, save_path):
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    api_url = 'https://api.openai.com/v1/images/generations'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {OPENAI_API_KEY}'
    }
    modify_blocker = "I NEED to test how the tool works with extremely simple prompts. DO NOT add any detail, just use it AS-IS: "
    description = "Don't include more than 4-5 words/ texts in the image Just few important words are fine. this is meme text generated from news. Create a meme out of it."
    data = {
        "model": "dall-e-3",
        "prompt": f"{modify_blocker} {prompt} {description}",
        "n": 1,
        "size": "1024x1024"
    }
    response = requests.post(api_url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        result = response.json()
        image_url = result['data'][0]['url']
        image_response = requests.get(image_url)
        if image_response.status_code == 200:
            with open(save_path, 'wb') as f:
                f.write(image_response.content)
            print(f"Image downloaded and saved at {save_path}")
        else:
            print("Error downloading image:", image_response.status_code, image_response.text)
    else:
        print("Error:", response.status_code, response.text)


def tweet(api, text: str, image_path: str):
    global api1
    media_id = api1.media_upload(image_path).media_id_string
    if(media_id):
        api.create_tweet(text=text, media_ids=[media_id])

def xApi():
    client = tweepy.Client(
        bearer_token,
        api_key,
        api_secret,
        access_token,
        access_token_secret,
        wait_on_rate_limit=True,
    )
    return client

def newsApi(trending_topic: str):
    global news_id

    api = NewsDataApiClient(apikey = news_api_key)
    response = api.news_api(q = trending_topic, language='en')
    results = sorted(response["results"], key=lambda x: x["pubDate"], reverse = True)
    news_text = results[0]["content"]
    news_link = results[0]["link"]

    if checkAndAddId(results[0]["article_id"]):
        print(" NewsId added...")
    else:
        return "", ""

    print("News: " + news_text)
    return gptModifyer(news_text), news_link

def gptModifyer(news_text: str):
    messages = ""
    path = "C:/Users/16823/Documents/X/GrokStockBot/GrockStockBot/memePrompt.json"

    if os.path.exists(path):
        with open(path, 'r') as f:
            messages = json.load(f)

    response = openai.ChatCompletion.create(model="gpt-4",messages = messages + [{"role": "user", "content": news_text}]).choices[0].message.content
    print("Memed news: " + response)

    return response

def getStockDataText(tickers_list):
    stock_text = ""
    for ticker in tickers_list:
        try:
            quote_table = stock_info.get_data(ticker)

            current_price = float("{:.2f}".format(stock_info.get_live_price(ticker)))
            previous_close = float("{:.2f}".format(quote_table['close'].iloc[-1]))

            if math.isnan(current_price) or math.isnan(previous_close):
                continue

            print(current_price, previous_close)

            # Calculate the percentage change
            calculation = float("{:.2f}".format(((current_price - previous_close) / previous_close) * 100))
            percentage_change = ""

            if calculation > 0:
                percentage_change = "   📈 " + str(calculation) + "%"
            elif calculation < 0:
                percentage_change = "   📉 " + str(calculation) + "%"

            stock_text += "$"+ ticker + " " + str(current_price) + str(percentage_change) + "\n"
        except Exception as e:
            print(e)
    print(stock_text)
    return stock_text

def formatTweet(meme_text, shortend_link):
    tweet = meme_text.split('***')[0] + '\n\n' + getStockDataText(meme_text.split('***')[1].split(',')) + '\n\n' + "Sauce: "+ shortend_link
    return tweet

def shortenurl(url):
    s = pyshorteners.Shortener()
    return str(s.tinyurl.short(url))

def getTopTrendingTopics():
    # Create pytrends object
    pytrends = TrendReq(hl='en-US', tz=360)
    # Get Google Hot Trends data
    trending_searches_df = pytrends.trending_searches(pn='united_states')
    return trending_searches_df[0]

# Saving used newsIds
def addIdToFile(news_id_file, article_id):
    with open(news_id_file, 'a') as file:
        file.write(str(article_id) + '\n')

def readIdsFromFile(news_id_file):
    try:
        with open(news_id_file, 'r') as file:
            return set(str(line.strip()) for line in file.readlines())
    except FileNotFoundError:
        return set()

def checkAndAddId(article_id):
    global news_id_file
    news_ids = readIdsFromFile(news_id_file)

    if article_id not in news_ids:
        addIdToFile(news_id_file, article_id)
        return True
    else:
        return False
    
def startMachine():
    try:
        topics = getTopTrendingTopics()
        for topic in topics:
            current_time = datetime.now().strftime("%Y%m%d%H%M%S")
            meme_text, news_link = newsApi(topic)
            if meme_text != "":
                save_path = f"C:/Users/16823/Documents/X/memes/{current_time}.jpg"
                dallEMemeImage(meme_text, save_path)
                tweet(xApi(), formatTweet(meme_text, shortenurl(news_link)), save_path)
                time.sleep(300)
    except Exception as e:
        time.sleep(120)
        startMachine()


if __name__ == '__main__':
    startMachine()