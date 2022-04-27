import configparser

config = configparser.RawConfigParser()
config.read(filenames="../config.properties")

stock_api_key = config.get("alphavantage.co", "stock-api-key")
news_api_key = config.get("newsapi.org", "news-api-key")

twilio_sid = config.get("twilio.com", "twilio.api.sid")
twilio_token = config.get("twilio.com", "twilio.api.token")