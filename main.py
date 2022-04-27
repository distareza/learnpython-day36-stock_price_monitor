"""
    Learn how to monitor a stock price using python
    stock market api : https://www.alphavantage.co/
    news api : https://newsapi.org/

    Objectives :
    When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
    Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.
    to send a separate message with each article's title and description to your phone number.

    Format the message like this:

    TSLA: 🔺2%
    Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?.
    Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to
    file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st,
    near the height of the coronavirus market crash.

"""
import my_configuration
import requests
from twilio.rest import Client

STOCK_API = my_configuration.stock_api_key
NEWS_API = my_configuration.news_api_key
TWILIO_SID = my_configuration.twilio_sid
TWILIO_TOKEN = my_configuration.twilio_token

# pick a stock to monitor
# https://www.tradingview.com/symbols/NASDAQ-TSLA/
STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"


STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

## api doc : https://www.alphavantage.co/documentation/#daily
stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API
}
response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()["Time Series (Daily)"]
#print(data)

#Get yesterday's closing stock price. Hint: perform list comprehensions on Python dictionaries. e.g. [new_value for (key, value) in dictionary.items()]
data_list = [value for (key, value) in data.items()]
yesterday_closing_price = float(data_list[0]["4. close"])
print(f"Yesterday closing price : ${yesterday_closing_price:,.2f}")

#Get the day before yesterday's closing stock price
before_yesterday_closing_price = float(data_list[1]["4. close"])
print(f"Before yesterday closing price : ${before_yesterday_closing_price:,.2f}")

#Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20.
#Hint: https://www.w3schools.com/python/ref_func_abs.asp
difference = yesterday_closing_price - before_yesterday_closing_price
stock_movement = ""
if difference > 0:
    stock_movement = "🔺"
elif difference < 0:
    stock_movement = "🔻"
else:
    stock_movement = "="
positif_difference = abs(difference)
print(f"Difference price : ${positif_difference:,.2f}")

# Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.
percentage_difference = positif_difference/yesterday_closing_price*100
print(f"Percentage Difference : {percentage_difference:,.2f} %")

#If TODO4 percentage is greater than 5 then print "Get News".
if percentage_difference > 5:
    ##  api : https://newsapi.org/
    # Get the first 3 news pieces for the COMPANY_NAME.

    news_param = {
        "qInTitle" : COMPANY_NAME,
        "apiKey" : NEWS_API
    }

    # use the News API to get articles related to the COMPANY_NAME.
    news = requests.get(NEWS_ENDPOINT, params=news_param)
    articles = news.json()["articles"]

    #Use Python slice operator to create a list that contains the first 3 articles.
    # Hint: https://stackoverflow.com/questions/509211/understanding-slice-notation
    first_3_articles = articles[:3]

    # Create a new list of the first 3 article's headline and description using list comprehension.
    new_messages = [f"HeadLine: {article['title']}\nBrief: {article['description']}" for article in first_3_articles]

    # Use twilio.com/docs/sms/quickstart/python
    # to send a separate message with each article's title and description to your phone number.

    print()
    #client = Client(TWILIO_SID, TWILIO_TOKEN)
    for article in new_messages:
        # client.messages.create(
        #     body=article,
        #     from_="",
        #     to=""
        # )
        print(f"{COMPANY_NAME}: {stock_movement} {percentage_difference:,.2f}%")
        print(article)
        print()


# TODO 9. - Send each article as a separate message via Twilio.



