import json
import random

import KEYS
import requests

# get contact info
contactInfo = KEYS.GetJokeContactInfo()
# request header
headers = {'Accept': 'application/json', 'User-Agent': contactInfo}


# get a random dad joke
def GetDadJoke():
    # api request for joke
    r = requests.get('https://icanhazdadjoke.com/', headers=headers)

    # convert response text to dictionary
    data = json.loads(r.text)

    # return joke from dictionary
    return '> ' + data['joke']


# search dad jokes by search term
def SearchDadJoke(searchValue):
    # set search value to the passed parameter
    body = {'term': searchValue}

    # api request for joke based on search term
    r = requests.get('https://icanhazdadjoke.com/search', headers=headers, params=body)

    # [] means there are no jokes
    if not r.text.__contains__('[]'):
        # get response text
        data = r.text
        # get start index of string
        start = r.text.find('[') + 1
        # get end index of string
        end = r.text.find(']')
        # split string to only keep whats inside the brackets
        data = data[start:end]

        # if data contains },
        if data.__contains__('},'):
            # split the multiple
            data = data.split('},')

        # if data is a list
        if type(data) == list:
            # for each item in data
            for i in range(len(data)):
                # if not the last item
                if i < len(data) - 1:
                    # add closing curly bracket
                    data[i] += '}'
                # convert every item to dictionary
                data[i] = json.loads(data[i])
            # return random joke from list of dictionaries
            return '> ' + data[random.randint(0, len(data) - 1)]['joke']

        # if data is a string
        if type(data) == str:
            # convert string to dictionary
            data = json.loads(data)
            # return joke from the dictionary
            return '> ' + data['joke']
    # if response contains [] return no jokes
    else:
        return "> Sorry, there were no jokes for that search term!"
