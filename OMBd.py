import json

import KEYS
import requests

# get contact info
apiKey = KEYS.GetOmbdKey()
# create url
url = 'http://www.omdbapi.com/' + '?apikey=' + str(apiKey)
# create header
headers = {'Accept': 'application/json'}


# get information of a movie/series title
def GetInformation(title):
    # make title a string
    title = str(title)

    # add title to parameters
    body = {
        't': title,
        'plot': 'short'
    }

    # request information from api
    r = requests.get(url, headers=headers, params=body)

    # if no movies/shows were found
    if r.text.__contains__('Movie not found!'):
        # return no movies/shows message
        return "> Sorry, there were no movies/shows for that term!"

    # convert string to dictionary
    data = json.loads(r.text)

    # title information string
    results = ''

    # add title, year, type
    results += '**' + str(data['Title']) + ' - ' + str(data['Type']).capitalize() + ' (' + str(
        data['Year']) + ')**' + '\n'
    # add genre
    results += '> ' + str(data['Genre']) + '\n'
    # add plot
    results += '> ' + str(data['Plot']) + '\n'
    # add link
    results += '> <https://www.imdb.com/title/' + str(data['imdbID']) + '/>'

    # return results string
    return results


# ombd search
def SearchTitle(searchTerm):
    # make searchTerm a string
    searchTerm = str(searchTerm)

    # add searchTerm to parameters
    body = {
        's': searchTerm,
    }

    # request information from api
    r = requests.get(url, headers=headers, params=body)

    # get response text
    data = r.text
    # get start index of string
    start = r.text.find('[') + 1
    # get end index of string
    end = r.text.find(']')
    # split string to only keep whats inside the brackets
    data = data[start:end]

    # if there are too many results
    if data.__contains__("Too many results."):
        # return too many results message
        return "> Sorry, there were too many movies/shows for that term!"

    # if no movies/shows were found
    if data.__contains__('Movie not found!'):
        # return no movies/shows message
        return "> Sorry, there were no movies/shows for that term!"

    # if data contains },
    if data.__contains__('},'):
        # split the multiple
        data = data.split('},')

    # if data is a list
    if type(data) == list:
        # search results string
        searchResults = '**Results** \n'
        # for each item in data
        for i in range(len(data)):
            # if not the last item
            if i < len(data) - 1:
                # add closing curly bracket
                data[i] += '}'
            # convert every item to dictionary
            data[i] = json.loads(data[i])
            # add information to searchResults
            searchResults += '> ' + str(data[i]['Title']) + ' - ' + str(
                data[i]['Type']).capitalize() + ' (' + str(data[i]['Year']) + ')' + '\n'
        # return searchResults string
        return searchResults

    # if data is a string
    if type(data) == str:
        # convert string to dictionary
        data = json.loads(data)
        # return movie message from dictionary
        return '**Result** \n' + '> ' + str(data['Title']) + ' (' + str(data['Year']) + ') - ' + str(
            data['Type']).capitalize()
