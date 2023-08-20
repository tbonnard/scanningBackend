import requests
import json
import os

publicKey = os.environ.get("PUBLICKEYFUKAI")
api = os.environ.get("APIFUKAI")

def validateHateSpeech(inputText):
    url = f'https://fuk.ai/detect-hatespeech/?input={inputText}'

    headers = {'Authorization': api}
    try:
        response = requests.get(url,  headers=headers)
        result = json.loads(response.text)
        # print(response.content)
        return result
    except:
        return False


# https://fuk.ai/docs/
  # {
  #           "success": true,
  #           "result": {
  #               "probability": 76.0,
  #               "hatespeech_indexes": [
  #                   [
  #                       0,
  #                       80
  #                   ],
  #                   [
  #                       145,
  #                       178
  #                   ]
  #               ]
  #           }
  #       }