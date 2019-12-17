import json
import urllib.request
import ssl
import requests


def get_emotions(text, access_token):
    try:
        values = {
            'text': text,
        }

        host = 'https://aip.baidubce.com/rpc/2.0/nlp/v1/sentiment_classify?' + \
               'access_token=' + access_token \
               + '&charset=UTF-8' \
               + '&text=' + text

        response = requests.post(host, json=values).json()
        item_values = []
        items = response['items'][0]
        item_values.append(str(items['sentiment']))
        item_values.append(str(items['confidence']))
        item_values.append(str(items['positive_prob']))
        item_values.append(str(items['negative_prob']))

        return item_values
    except Exception as e:
        print(e)
        return []


def get_access_token():
    client_id = 'CwqN23lRUzBG8lEGjFrDLP4Y'
    client_secret = 'LlX7jAv8pGCz4bGYlDxDLKtoal8Udc1g'
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=' + client_id \
           + '&client_secret=' + client_secret
    request = urllib.request.Request(host)
    request.add_header('Content-Type', 'application/json; charset=UTF-8')
    response = urllib.request.urlopen(request)
    content = json.loads(response.read())
    access_token = content['access_token']
    return access_token


if __name__ == '__main__':
    ssl._create_default_https_context = ssl._create_unverified_context
    access_token = get_access_token()
    comment = '我们都没有错与对'
    ans = get_emotions(comment, access_token)
    print("正向情感可能性为{}".format(ans[2]))
    print("负向情感可能性为{}".format(ans[3]))
    if(ans[2]>ans[3]):
        print(comment, "这段文本的情绪是正向的")
    else:
        print(comment, "这段文本的情绪是负面的")