import requests
import json
import os


api_user = os.environ.get("APISIGHT")
api_secret = os.environ.get("APISECRETSIGHT")


def validateHateSpeechSight(inputText):
    data = {
        'text': inputText,
        'mode': 'standard',
        'lang': 'en,fr,it,es,de',
        'opt_countries': 'us,gb,fr,de,it,es',
        'api_user': api_user,
        'api_secret': api_secret
    }
    try:
        r = requests.post('https://api.sightengine.com/1.0/text/check.json', data=data)
        output = json.loads(r.text)
        return output
    except:
        return False


# https://sightengine.com/docs/text-moderation-guide
# https://sightengine.com/docs/reference?python#text-and-username-moderation