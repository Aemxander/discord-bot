import json

import KEYS
import requests

# get api key
apiKey = KEYS.GetCatKey()
# API key authentication
headers = {'X-API-KEY': apiKey}


# gets cat image from API
def CreateCatImage():
    # API search url
    url = 'https://api.thecatapi.com/v1/images/search'

    # API call parameters
    body = {
        "size": "large",
        "limit": 1,
        "mime_types": "gif"
    }

    # request an image from API
    r = requests.request(method="GET", url=url, headers=headers, params=body)

    # get response content as text
    dataString = r.text
    # remove open and closing bracket
    dataString = dataString[1:-1]
    # convert data from string to dictionary
    dataDictionary = json.loads(dataString)

    # get url from dataDictionary
    imageUrl = dataDictionary['url']
    # get id from dataDictionary
    imageID = dataDictionary['id']

    # get filename from imageUrl
    imageFilename = imageUrl.split('/')[-1]

    # get image data from imageUrl
    r = requests.get(imageUrl, allow_redirects=True)

    # write image data to imageFilename
    open(imageFilename, 'wb').write(r.content)

    # return imageFilename, imageID
    return imageFilename, imageID


# post vote for cat image to API
def VoteCatImage(imageID, voteValue):
    # API votes url
    url = 'https://api.thecatapi.com/v1/votes'

    # if downvoting - set parameters
    if voteValue == 0:
        body = {
            'image_id': imageID,
            "value": 0,
        }

    # if upvoting - set parameters
    if voteValue == 1:
        body = {
            "image_id": imageID,
            "value": 1,
        }

    # post a vote to API
    requests.request(method="POST", url=url, headers=headers, json=body)
    return


# get voting history from the API
def GetVotingHistory():
    # API votes url
    url = 'https://api.thecatapi.com/v1/votes'

    # request voting history from API
    r = requests.request(method="GET", url=url, headers=headers)

    # remove brackets from response
    votingHistory = r.text[1:-1]
    # split response by closing curly bracket
    votingHistory = votingHistory.split('}')

    # for each vote in votingHistory
    for i in votingHistory:
        # print vote along with closing curly bracket
        print(i + '}')
    return
