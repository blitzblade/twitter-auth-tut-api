from flask import Flask, request
from flask_cors import CORS, cross_origin
from twitter_script import consumer_key, consumer_secret
import tweepy
import json


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/api/auth_twitter', methods = ["POST"])
@cross_origin()
def authorize_twitter():

    body = request.get_json()
    print(request.json)
    callback_url = body.get("callback_url")
    print(callback_url)
    
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback_url)

    try:
        redirect_url = auth.get_authorization_url()
        return json.dumps({"message":"success", "redirect_url": redirect_url })
    except tweepy.TweepError as ex:
        print(ex)
        return json.dumps({"message":"Failed to get request token", "redirect_url": None})


@app.route('/api/twitter_auth_callback', methods=["GET"])
@cross_origin()
def twitter_callback():
    try:
        oauth_token = request.args.get('oauth_token')
        oauth_verifier = request.args.get('oauth_verifier')
        # print("hello")
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

        auth.request_token = { "oauth_token": oauth_token, "oauth_token_secret": oauth_verifier }
        auth.get_access_token(oauth_verifier)
        api = tweepy.API(auth)
        print(api)
        user = api.me()
        username = user.screen_name
        user_id = user.id
        return json.dumps({"message":"success", "user_id": user_id, "username": username, "access_token": auth.access_token, "access_token_secret": auth.access_token_secret})
    except Exception as ex:
        print(ex)
        return json.dumps({"message":"Failed to get tokens"}), 500

@app.route('/')
def home():
    return "API is Alive and Well!"


if __name__ == '__main__':
    app.secret_key = "AUTH_KWESI_SECRET"
    app.run()