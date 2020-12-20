import datetime
import json
import random

import KEYS
import requests

# get api key
apiKey = KEYS.GetNASAKey()


# get nasa picture of the day
def PictureOfDay(pictureDate):
    # api url
    url = 'https://api.nasa.gov/planetary/apod'

    # create header
    headers = {'Accept': 'application/json'}

    # if no date is given
    if pictureDate is None:
        # create body
        body = {
            'api_key': apiKey
        }

        # api call to get image information
        r = requests.request(method="GET", url=url, headers=headers, params=body)

        # if image is a youtube video
        if r.text.__contains__('youtube'):
            # get api results as a dictionary
            data = json.loads(r.text)
            # get url from results
            imageUrl = data['url']
            # split by slash
            imageUrl = imageUrl.split('/')
            # create embed youtube link getting video id from imageUrl
            videoLink = 'https://www.youtube.com/watch?v=' + imageUrl[-1][
                                                             :imageUrl[-1].index('?')] + '&feature=emb_title'
            # return embed youtube link, title, and date
            return videoLink, data['title'], data['date']

        # get api results as a dictionary
        data = json.loads(r.text)
        # get url from results
        imageUrl = data['url']
        # get filename from url
        imageFilename = imageUrl.split('/')[-1]
        # get image data from imageUrl
        r = requests.get(imageUrl, allow_redirects=True)
        # write image data to imageFilename
        open(imageFilename, 'wb').write(r.content)

        # return imageFilename, title, and date
        return imageFilename, data['title'], data['date']

    # if a date is given
    if pictureDate is not None:
        # try to get picture from given date
        try:
            # create body
            body = {
                'api_key': apiKey,
                'date': str(pictureDate)
            }

            # api call for picture information
            r = requests.request(method="GET", url=url, headers=headers, params=body)

            # if response contains []
            if r.text.__contains__('[]'):
                # return error message
                return 'Sorry, that date is invalid - valid dates are between June 16, 1995 and the current date!', None, None

            # if image is a youtube video
            if r.text.__contains__('youtube'):
                # get api results as a dictionary
                data = json.loads(r.text)
                # get url from results
                imageUrl = data['url']
                # split by slash
                imageUrl = imageUrl.split('/')
                # create embed youtube link getting video id from imageUrl
                videoLink = 'https://www.youtube.com/watch?v=' + imageUrl[-1][
                                                                 :imageUrl[-1].index('?')] + '&feature=emb_title'
                # return embed youtube link, title, and date
                return videoLink, data['title'], data['date']

            # get api results as a dictionary
            data = json.loads(r.text)
            # get url from results
            imageUrl = data['url']
            # get filename from url
            imageFilename = imageUrl.split('/')[-1]
            # get image data from imageUrl
            r = requests.get(imageUrl, allow_redirects=True)
            # write image data to imageFilename
            open(imageFilename, 'wb').write(r.content)

            # return imageFilename, title, and date
            return imageFilename, data['title'], data['date']
        # if an error occurs
        except:
            # return error message
            return 'Sorry, that date is invalid - valid dates are between June 16, 1995 and the current date!', None, None


# get nasa rover images
def RoverImage(pictureDate):
    # api url
    url = 'https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos'

    # create header
    headers = {'Accept': 'application/json'}

    # if no date is given
    if pictureDate is None:
        # start and end dates
        startDate = datetime.date(2012, 8, 6)
        endDate = datetime.date.today()
        # date difference
        difference = endDate - startDate
        daysDifference = difference.days
        # random number of days
        randomDays = random.randrange(daysDifference)
        # random date
        randomDate = startDate + datetime.timedelta(days=randomDays)

        # create body
        body = {
            'api_key': apiKey,
            'earth_date': randomDate,
        }

        # try to get data 100 times
        for i in range(100):
            # api call for picture information
            r = requests.request(method="GET", url=url, headers=headers, params=body)

            # if r.text has image sources
            if r.text.__contains__('[]') == False:
                # break for loop
                break

    # if a date is given
    if pictureDate is not None:
        # try to get picture from given date
        try:
            # create body
            body = {
                'api_key': apiKey,
                'earth_date': str(pictureDate),
            }

            # api call for picture information
            r = requests.request(method="GET", url=url, headers=headers, params=body)
        except:
            # return error message
            return 'Sorry, that date is invalid - valid dates are between August 6, 2012 and 7 days prior to the current date!', None, None

        # if message contains []
        if r.text.__contains__('[]'):
            return 'Sorry, that date is invalid - valid dates are between August 6, 2012 and 7 days prior to the current date!', None, None

    # get response text
    data = r.text
    # get start index of string
    start = r.text.find('[') + 1
    # get end index of string
    end = r.text.find(']')
    # split string to only keep whats inside the brackets
    data = data[start:end]

    # if data contains }},
    if data.__contains__('}},'):
        # split the multiple
        data = data.split('}},')
    # if data doesn't contain }},
    else:
        # split by }}
        data = data.split('}}')

    # if data is a list
    if type(data) == list:
        # for each item in data
        for i in range(len(data)):
            # if not the last item
            if i < len(data) - 1:
                # add double closing curly brackets
                data[i] += '}}'
            # convert every item to dictionary
            data[i] = json.loads(data[i])

    # create random integer
    randomInt = random.randint(0, len(data) - 1)
    # get random url from results
    imageUrl = str(data[randomInt]['img_src'])
    # get filename from url
    imageFilename = imageUrl.split('/')[-1]

    # get image data from imageUrl
    r = requests.get(imageUrl)
    # write image data to imageFilename
    open(imageFilename, 'wb').write(r.content)

    # return imageFilename
    return imageFilename, data[randomInt]['camera']['full_name'], data[randomInt]['earth_date']


#search images from nasa api
def ImageSearch(searchQuery):
    # api url
    url = 'https://images-api.nasa.gov/search'

    # create header
    headers = {'Accept': 'application/json'}

    #query with no search term
    if searchQuery == None:
        body = {
            'media_type': 'image',
            'description_508': 'a',
            'page': 1
        }
    #query with passed search term
    if searchQuery != None:
        body = {
            'q': str(searchQuery),
            'media_type': 'image',
            'page': 1
        }

    # api call for picture information
    r = requests.request(method="GET", url=url, headers=headers, params=body)

    #if response contains []
    if r.text.__contains__('[]'):
        return '> Sorry, there were no images for that search term!', None, None, None

    # get response text
    data = r.text
    # get start index of string
    data = json.loads(data)

    # pick a random image from items
    imageInfo = random.choice(data['collection']['items'])

    # get url from results
    imageUrl = imageInfo['links'][0]['href']
    # get filename from url
    imageFilename = imageUrl.split('/')[-1]

    # get image data from imageUrl
    r = requests.get(imageUrl)
    # write image data to imageFilename
    open(imageFilename, 'wb').write(r.content)

    #get image creation date
    imageDate = imageInfo['data'][0]['date_created']
    imageDate = imageDate[:str(imageDate).find('T')]

    # if there is a short description
    if 'description_508' in imageInfo['data'][0]:
        # return filename, title, date, short description
        return imageFilename, imageInfo['data'][0]['title'], imageDate, imageInfo['data'][0]['description_508']
    # if there is not a short description
    if 'description_508' not in imageInfo['data'][0]:
        # return filename, title, date, long description
        return imageFilename, imageInfo['data'][0]['title'], imageDate, imageInfo['data'][0]['description']
