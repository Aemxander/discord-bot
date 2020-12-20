import os
import sys

import AlphaVantage
import DadJoke
import KEYS
import NASA
import OMBd
import RoboHash
import TheCatAPI
import TheDogAPI
import discord

# create connection to discord
client = discord.Client()


# event for when bot is logged in
@client.event
async def on_ready():
    # print message to console when bot logs in
    print('We have logged in as {0.user}'.format(client))


# event for when a message is sent
@client.event
async def on_message(message):
    # make message lowercase
    content = message.content.lower()
    # remove trailing space
    content.strip()

    # if message is from this bot
    if message.author == client.user:
        # return
        return

    # if first word is !admin
    if content.startswith('!admin'):
        # save message content
        adminMessage = content
        # split message content
        adminMessage = adminMessage.split()

        # if message is greater than one word
        if len(adminMessage) > 1:
            # if cat is second word in message
            if 'cat' in adminMessage[1]:
                # if votinghistory is third word in message
                if 'votinghistory' in adminMessage[2]:
                    # print cat voting history to console
                    TheCatAPI.GetVotingHistory()
                    # send success message
                    await message.channel.send('> ' +
                                               message.author.mention + " The cat voting history has been printed in the console!")
                    return
            # if dog is second word in message
            if 'dog' in adminMessage[1]:
                # if votinghistory is third word in message
                if 'votinghistory' in adminMessage[2]:
                    # print cat voting history to console
                    TheDogAPI.GetVotingHistory()
                    # send success message
                    await message.channel.send('> ' +
                                               message.author.mention + " The dog voting history has been printed in the console!")
                    return
            # if update is second word in message
            if 'update' in adminMessage[1]:
                # if listings is third word in message
                if 'listings' in adminMessage[2]:
                    # add reaction since command is slow
                    await message.add_reaction("🔪")
                    # update stock listings file
                    returnVal = AlphaVantage.UpdateListings()
                    await message.channel.send(returnVal)
                    return

    # if first word is !robot
    if content.startswith('!robot'):
        # save message content
        robotMessage = content
        # split message content
        robotMessage = robotMessage.split()

        # default parameters
        set = 'set1'
        background = None

        # check message for parameter updates
        if 'set1' in robotMessage:
            set = 'set1'
        if 'set2' in robotMessage:
            set = 'set2'
        if 'set3' in robotMessage:
            set = 'set3'
        if 'set4' in robotMessage:
            set = 'set4'
        if 'set5' in robotMessage:
            set = 'set5'
        if 'background1' in robotMessage:
            background = 'bg1'
        if 'background2' in robotMessage:
            background = 'bg2'

        # list of parameters
        nonHashItems = ['set1', 'set2', 'set3', 'set4', 'set5', 'background1', 'background2']

        # create hash value
        hashValue = ''
        # for each item in message
        for i in range(len(robotMessage)):
            # for each item after !robot
            if i > 0:
                # if item is not in nonHashItems
                if robotMessage[i] not in nonHashItems:
                    # add item to hash value
                    hashValue = hashValue + ' ' + str(robotMessage[i])
        # strip hash value
        hashValue = hashValue.strip()

        # try to get robot image
        try:
            if hashValue == '':
                robotFilename, returnMessage = RoboHash.GetRobot(None, set, background)

            if hashValue != '':
                robotFilename, returnMessage = RoboHash.GetRobot(hashValue, set, background)
        # if an error occurs
        except:
            await message.channel.send("> Sorry, an error occurred while getting the robot image!")

        # create discord file - sys.path[0] gets current directory path, os.path.join connects directory + imageName
        file = discord.File(os.path.join(sys.path[0], robotFilename), filename=robotFilename)
        # create discord embed
        embed = discord.Embed(colour=0x3498db)
        # set image to embed
        embed.set_image(url="attachment://" + robotFilename)
        # send embedded image message
        await message.channel.send(file=file, embed=embed, content=returnMessage)
        # delete image file
        DeleteImage(os.path.join(sys.path[0], robotFilename))
        return

    # if first word is !nasa
    if content.startswith('!nasa'):
        # save message content
        nasaMessage = content
        # split message content
        nasaMessage = nasaMessage.split()

        # if message is !nasa apod
        if len(nasaMessage) > 1 and nasaMessage[1] == 'apod':
            # if message is only !nasa apod
            if len(nasaMessage) == 2:
                # call PictureOfDay - returns filename of nasa image, title, and date
                nasaImageName, title, date = NASA.PictureOfDay(None)
                # if nasa links a youtube video
                if 'youtube' in nasaImageName:
                    # send embedded youtube link
                    await message.channel.send("> **" + str(title) + ': ' + str(date) + '**\n' + str(nasaImageName))
                    return
                # if invalid date
                if title == None and date == None:
                    # send error message
                    await message.channel.send('> ' + nasaImageName)
                    return
                # create discord file - sys.path[0] gets current directory path, os.path.join connects directory + imageName
                file = discord.File(os.path.join(sys.path[0], nasaImageName), filename=nasaImageName)
                # create discord embed
                embed = discord.Embed(colour=0x3498db)
                # set image to embed
                embed.set_image(url="attachment://" + nasaImageName)
                # send embedded image message
                await message.channel.send(file=file, embed=embed,
                                           content="> **" + str(title) + ': ' + str(date) + '**')
                # delete image file
                DeleteImage(os.path.join(sys.path[0], nasaImageName))
                return
            # if message is !nasa apod DATE
            if len(nasaMessage) == 3:
                # nasaDate
                nasaDate = str(nasaMessage[2]).strip('\"')
                nasaDate = nasaDate.strip("\'")
                # call PictureOfDay - returns filename of nasa image, title date
                nasaImageName, title, date = NASA.PictureOfDay(nasaDate)
                # if nasa links a youtube video
                if 'youtube' in nasaImageName:
                    # send embedded youtube link
                    await message.channel.send("> **" + str(title) + ': ' + str(date) + '**\n' + str(nasaImageName))
                    return
                # if invalid date
                if title == None and date == None:
                    # send error message
                    await message.channel.send('> ' + nasaImageName)
                    return
                # create discord file - sys.path[0] gets current directory path, os.path.join connects directory + imageName
                file = discord.File(os.path.join(sys.path[0], nasaImageName), filename=nasaImageName)
                # create discord embed
                embed = discord.Embed(colour=0x3498db)
                # set image to embed
                embed.set_image(url="attachment://" + nasaImageName)
                # send embedded image message
                await message.channel.send(file=file, embed=embed,
                                           content="> **" + str(title) + ': ' + str(date) + '**')
                # delete image file
                DeleteImage(os.path.join(sys.path[0], nasaImageName))
                return
        # if message is !nasa rover
        if len(nasaMessage) > 1 and nasaMessage[1] == 'rover':
            # if message is only !nasa rover
            if len(nasaMessage) == 2:
                # add reaction since command is slow
                await message.add_reaction("🔪")
                # call RoverImage - returns filename of nasa image, camera, date
                nasaImageName, camera, date = NASA.RoverImage(None)
                # if invalid date
                if camera == None and date == None:
                    # send error message
                    await message.channel.send('> ' + nasaImageName)
                    return
                # create discord file - sys.path[0] gets current directory path, os.path.join connects directory + imageName
                file = discord.File(os.path.join(sys.path[0], nasaImageName), filename=nasaImageName)
                # create discord embed
                embed = discord.Embed(colour=0x3498db)
                # set image to embed
                embed.set_image(url="attachment://" + nasaImageName)
                # send embedded image message
                await message.channel.send(file=file, embed=embed,
                                           content="> **Curiosity " + str(camera) + ': ' + str(date) + '**')
                # delete image file
                DeleteImage(os.path.join(sys.path[0], nasaImageName))
                return
            # if message is !nasa rover DATE
            if len(nasaMessage) == 3:
                # add reaction since command is slow
                await message.add_reaction("🔪")
                # nasaDate
                nasaDate = str(nasaMessage[2]).strip('\"')
                nasaDate = nasaDate.strip("\'")
                # call PictureOfDay - returns filename of nasa image, camera, date
                nasaImageName, camera, date = NASA.RoverImage(nasaDate)
                # if invalid date
                if camera == None and date == None:
                    # send error message
                    await message.channel.send('> ' + nasaImageName)
                    return
                # create discord file - sys.path[0] gets current directory path, os.path.join connects directory + imageName
                file = discord.File(os.path.join(sys.path[0], nasaImageName), filename=nasaImageName)
                # create discord embed
                embed = discord.Embed(colour=0x3498db)
                # set image to embed
                embed.set_image(url="attachment://" + nasaImageName)
                # send embedded image message
                await message.channel.send(file=file, embed=embed,
                                           content="> **Curiosity " + str(camera) + ': ' + str(date) + '**')
                # delete image file
                DeleteImage(os.path.join(sys.path[0], nasaImageName))
                return
        # if message is !nasa search
        if len(nasaMessage) > 1 and nasaMessage[1] == 'search':
            # if message is only !nasa search
            if len(nasaMessage) == 2:
                # call ImageSearch - returns filename of nasa image, title, description
                nasaImageName, title, date, description = NASA.ImageSearch(None)
                # if there are no results
                if title == None and date == None and description == None:
                    # send error message
                    await message.channel.send(nasaImageName)
                    return
                # create discord file - sys.path[0] gets current directory path, os.path.join connects directory + imageName
                file = discord.File(os.path.join(sys.path[0], nasaImageName), filename=nasaImageName)
                # create discord embed
                embed = discord.Embed(colour=0x3498db)
                # create embedFilename for embedding
                embedFilename = nasaImageName
                # remove ~ from filename so it will embed properly
                if '~' in nasaImageName:
                    # removes ~ from string
                    embedFilename = str(nasaImageName).replace('~', '')
                # set image to embed
                embed.set_image(url="attachment://" + embedFilename)
                # if description is not too long
                if len(description) < 400:
                    # send embedded image message
                    await message.channel.send(file=file, embed=embed,
                                               content="**" + str(title) + ': ' + str(date) + '**\n' + '> ' + str(
                                                   description))
                # if description is too long
                if len(description) >= 400:
                    # send embedded image message
                    await message.channel.send(file=file, embed=embed,
                                               content="**" + str(title) + ': ' + str(date) + '**')
                # delete image file
                DeleteImage(os.path.join(sys.path[0], nasaImageName))
                return
            # if message is !nasa search SEARCHTERM
            if len(nasaMessage) > 2:
                # create search string
                searchValue = ''
                # for each item in message
                for i in range(len(nasaMessage)):
                    # for each item after !joke
                    if i > 1:
                        # add item to search string
                        searchValue = searchValue + ' ' + str(nasaMessage[i])
                # strip search string
                searchValue = searchValue.strip()
                # call ImageSearch - returns filename of nasa image, title, description
                nasaImageName, title, date, description = NASA.ImageSearch(searchValue)
                # if there are no results
                if title == None and date == None and description == None:
                    # send error message
                    await message.channel.send(nasaImageName)
                    return
                # create discord file - sys.path[0] gets current directory path, os.path.join connects directory + imageName
                file = discord.File(os.path.join(sys.path[0], nasaImageName), filename=nasaImageName)
                # create discord embed
                embed = discord.Embed(colour=0x3498db)
                # create embedFilename for embedding
                embedFilename = nasaImageName
                # remove ~ from filename so it will embed properly
                if '~' in nasaImageName:
                    # removes ~ from string
                    embedFilename = str(nasaImageName).replace('~', '')
                # set image to embed
                embed.set_image(url="attachment://" + embedFilename)
                # if description is not too long
                if len(description) < 350:
                    # send embedded image message
                    await message.channel.send(file=file, embed=embed,
                                               content="**" + str(title) + ': ' + str(date) + '**\n' + '> ' + str(
                                                   description))
                # if description is too long
                if len(description) >= 350:
                    # send embedded image message
                    await message.channel.send(file=file, embed=embed,
                                               content="**" + str(title) + ': ' + str(date) + '**')
                # delete image file
                DeleteImage(os.path.join(sys.path[0], nasaImageName))
                return

    # if first word is !imbd
    if content.startswith('!imbd'):
        # save message content
        ombdMessage = content
        # split message content
        ombdMessage = ombdMessage.split()

        # if message is one word
        if len(ombdMessage) == 1:
            # send error message
            await message.channel.send('> You must enter a movie/show title to search for!')
            return

        # if message is more than 1 word
        if len(ombdMessage) > 1:
            # if message is !imbd search
            if ombdMessage[1] == 'search':
                # create search term
                searchValue = ''

                # for each word in message
                for i in range(len(ombdMessage)):
                    # for each word after 'search'
                    if i > 1:
                        # add term to searchValue
                        searchValue = searchValue + ' ' + str(ombdMessage[i])
                # strip searchValue
                searchValue = searchValue.strip()

                # get search results
                ombdData = OMBd.SearchTitle(searchValue)
                # print search results
                await message.channel.send(ombdData)
                return
            if ombdMessage[1] != 'search':
                # create title
                title = ''

                # for each word in message
                for i in range(len(ombdMessage)):
                    # for each word after '!imbd'
                    if i > 0:
                        # add term to searchValue
                        title = title + ' ' + str(ombdMessage[i])
                # strip searchValue
                title = title.strip()

                # get search results
                ombdData = OMBd.GetInformation(title)
                # print search results
                await message.channel.send(ombdData)
                return

    # if first word is !dadjoke
    if content.startswith('!joke'):
        # save message content
        jokeMessage = content
        # split message content
        jokeMessage = jokeMessage.split()

        # if message is one word
        if len(jokeMessage) == 1:
            # get dad joke
            jokeData = DadJoke.GetDadJoke()
            # send dad joke
            await message.channel.send(jokeData)
            return

        # if message is greater than one word
        if len(jokeMessage) > 1:
            # create search string
            searchValue = ''

            # for each item in message
            for i in range(len(jokeMessage)):
                # for each item after !joke
                if i > 0:
                    # add item to search string
                    searchValue = searchValue + ' ' + str(jokeMessage[i])

            # strip search string
            searchValue = searchValue.strip()
            # get dad joke based on search string
            jokeData = DadJoke.SearchDadJoke(searchValue)
            # send results message
            await message.channel.send(jokeData)
            return

    # if first word is !cat
    if content.startswith('!cat'):
        # save message content
        catMessage = content
        # split message content
        catMessage = catMessage.split()

        # make votedOnCat a global variable
        global votedOnCat

        # if message is one word
        if len(catMessage) == 1 or (('upvote' in catMessage) or ('downvote' in catMessage)) == False:
            # try to get image from cat API
            try:
                # make catImageID a global variable
                global catImageID
                # call CreateCatImage - returns filename of cat image, and cat image id
                catImageName, catImageID = TheCatAPI.CreateCatImage()
                # save catImageId into variable
                lastCatID = catImageID
                # create discord file - sys.path[0] gets current directory path, os.path.join connects directory + imageName
                file = discord.File(os.path.join(sys.path[0], catImageName), filename=catImageName)
                # create discord embed
                embed = discord.Embed(colour=0x3498db)
                # set image to embed
                embed.set_image(url="attachment://" + catImageName)
                # send embedded image message
                await message.channel.send(file=file, embed=embed, content="> **meow**")
                # delete image file
                DeleteImage(os.path.join(sys.path[0], catImageName))
                # set votedOnCat to 0
                votedOnCat = 0
                return
            # if an error occurs
            except:
                # send error message
                await message.channel.send(
                    '> ' + message.author.mention + " An error occurred while getting the cat image.")
                return

        # if message is greater than one word
        if len(catMessage) > 1:
            # if cat hasn't already been voted on
            if votedOnCat == 0:
                # if second word in message contains 'upvote'
                if 'upvote' in catMessage[1]:
                    # upvote cat image
                    TheCatAPI.VoteCatImage(catImageID, 1)
                    # send success message
                    await message.channel.send('> ' +
                                               message.author.mention + " Your upvote for the last cat image has been submitted!")
                    # set votedOnCat to 1
                    votedOnCat = 1
                    return
                # if second word in message contains 'downvote'
                if 'downvote' in catMessage[1]:
                    # downvote cat image
                    TheCatAPI.VoteCatImage(catImageID, 0)
                    # send success message
                    await message.channel.send('> ' +
                                               message.author.mention + " Your downvote for the last cat image has been submitted!")
                    # set votedOnCat to 1
                    votedOnCat = 1
                    return
            # if cat has already been voted on
            if votedOnCat == 1:
                # send error message
                await message.channel.send('> ' +
                                           message.author.mention + " This cat has already been voted on and cannot be voted on again!")
                return

    # if first word is !dog
    if content.startswith('!dog'):
        # save message content
        dogMessage = content
        # split message content
        dogMessage = dogMessage.split()

        # make votedOnDog a global variable
        global votedOnDog

        # if message is one word
        if len(dogMessage) == 1 or (('upvote' in dogMessage) or ('downvote' in dogMessage)) == False:
            # try to get image from dog API
            try:
                # make dogImageID a global variable
                global dogImageID
                # call CreateDogImage - returns filename of dog image, and dog image id
                dogImageName, dogImageID = TheDogAPI.CreateDogImage()
                # save dogImageId into variable
                lastDogID = dogImageID
                # create discord file - sys.path[0] gets current directory path, os.path.join connects directory + imageName
                file = discord.File(os.path.join(sys.path[0], dogImageName), filename=dogImageName)
                # create discord embed
                embed = discord.Embed(colour=0x3498db)
                # set image to embed
                embed.set_image(url="attachment://" + dogImageName)
                # send embedded image message
                await message.channel.send(file=file, embed=embed, content="> **woof**")
                # delete image file
                DeleteImage(os.path.join(sys.path[0], dogImageName))
                # set votedOnDog to 0
                votedOnDog = 0
                return
            # if an error occurs
            except:
                # send error message
                await message.channel.send('> ' +
                                           message.author.mention + " An error occurred while getting the dog image.")
                return

        # if message is greater than one word
        if len(dogMessage) > 1:
            # if dog hasn't already been voted on
            if votedOnDog == 0:
                # if second word in message contains 'upvote'
                if 'upvote' in dogMessage[1]:
                    # upvote dog image
                    TheDogAPI.VoteDogImage(dogImageID, 1)
                    # send success message
                    await message.channel.send('> ' +
                                               message.author.mention + " Your upvote for the last dog image has been submitted!")
                    # set votedOnDog to 1
                    votedOnDog = 1
                    return
                # if second word in message contains 'downvote'
                if 'downvote' in dogMessage[1]:
                    # downvote dog image
                    TheDogAPI.VoteDogImage(dogImageID, 0)
                    # send success message
                    await message.channel.send('> ' +
                                               message.author.mention + " Your downvote for the last dog image has been submitted!")
                    # set votedOnDog to 1
                    votedOnDog = 1
                    return
            # if dog has already been voted on
            if votedOnDog == 1:
                # send error message
                await message.channel.send('> ' +
                                           message.author.mention + " This dog has already been voted on and cannot be voted on again!")
                return

    # if first word is !stock
    if content.startswith('!stock'):
        stockMessage = content
        stockMessage = stockMessage.split()

        # if message contains search
        if 'search' in stockMessage[1]:
            # create search string
            searchValue = ''
            # for each item in message
            for i in range(len(stockMessage)):
                # for each item after !stock search
                if i > 1:
                    # add item to search string
                    searchValue = searchValue + ' ' + str(stockMessage[i])
            # strip search string
            searchValue = searchValue.strip()
            data = AlphaVantage.StockSearch(searchValue)
            await message.channel.send(data)
            return

        # if message doesn't contain search
        if 'search' not in stockMessage[1]:
            # add reaction since command is slow
            await message.add_reaction("🔪")
            # get stock name from message
            stockName = content
            stockName = stockName.split()
            stockName = stockName[1]

            # call StockCommandGetData - returns data, metadata
            data, metadata = StockCommandGetData(stockName)

            # if an error occured getting data
            if type(data) is int and type(metadata) is int:
                # if out of API calls
                if data == -2 and metadata == -2:
                    # send API calls error message
                    await message.channel.send("> I am out of stock API calls, please try again in a minute! :)")
                    return
                # if a different error occurs
                else:
                    # send default error message
                    await message.channel.send("> Sorry, there was no data for that stock ticker!")
                    return
            # if no errors occurred getting data
            else:
                # call command StockCommandGetChart - returns chartName
                chartName = StockCommandGetChart(data, metadata)

                # if an error occured getting chart
                if type(chartName) is int:
                    # send error message
                    await message.channel.send("> Sorry, an error occurred while getting the stock chart!")
                    return
                else:
                    # get stock information message
                    stockMessage = StockCommandGetInfo(data, metadata)
                    # create discord file - sys.path[0] gets current directory path, os.path.join connects directory + chartName
                    file = discord.File(os.path.join(sys.path[0], chartName), filename=chartName)
                    # create discord embed
                    embed = discord.Embed(colour=0x3498db)
                    # set image to embed
                    embed.set_image(url="attachment://" + chartName)
                    # send embedded image message
                    await message.channel.send(file=file, embed=embed, content=stockMessage)
                    pass
            # clear chart
            AlphaVantage.ClearChart()
            # delete chart - sys.path[0] gets current directory path, os.path.join connects directory + chartName
            DeleteImage(os.path.join(sys.path[0], chartName))
            # save stock data in text file
            StockCommandSaveData(data, metadata)
            # return from !stock
            return


# get stock data
def StockCommandGetData(stockName):
    # try to get stock data
    try:
        # get stock data
        data, metadata = AlphaVantage.GetStock(stockName)
        # if data and metadata are integers
        if type(data) is int and type(metadata) is int:
            # return -1, -1
            return data, metadata
        # add simple moving averages to data
        data, metadata = AlphaVantage.SimpleMovingAverages(data, metadata)
        # return stock data, stock metadata
        return data, metadata
    # if an error occurs
    except Exception as e:
        # print error message
        print("An error occured in DiscordBot.StockCommandGetData")
        print(str(e))
        # type check parameters
        print('data: ' + str(type(data)))
        print('metadata: ' + str(type(metadata)))
        # return -1, -1
        return -1, -1


# get stock chart
def StockCommandGetChart(stockData, stockMetadata):
    # try to get stock chart
    try:
        # create chart
        chartName = AlphaVantage.CreateChart(stockData, stockMetadata)
        # return chartName
        return chartName
    # if an error occurs
    except:
        # print error message
        print("An error occured in DiscordBot.StockCommandGetChart")
        # return -1
        return -1


# save stock data to text file
def StockCommandSaveData(stockData, stockMetadata):
    # try to save data
    try:
        # save data
        AlphaVantage.SaveData(stockData, stockMetadata)
        return
    # if an error occurs
    except:
        # print error message
        print("An error occured in DiscordBot.StockCommandSaveData")
        return


# get stock info from stock data
def StockCommandGetInfo(stockData, stockMetadata):
    # try to get stock information
    try:
        # get stock ticker
        stockTicker = str(stockMetadata['2. Symbol'])
        stockTicker = stockTicker.upper()
        # get timeframe
        stockTimeframe = str(stockMetadata['4. Interval'])
        stockTimeframe = stockTimeframe.upper()
        # get stock prices
        lastPrice = stockData['4. close'][0]
        sma50Price = stockData['6. sma50'][0]
        sma200Price = stockData['7. sma200'][0]
        # variables for percent differences
        sma50Difference = 0
        sma200Difference = 0

        # calculate sma50 percent difference
        if sma50Price != 0:
            sma50Difference = ((lastPrice / sma50Price) - 1) * 100
        # calculate sma200 percent difference
        if sma200Price != 0:
            sma200Difference = ((lastPrice / sma200Price) - 1) * 100

        # format and convert prices to strings
        lastPrice = "{:.2f}".format(lastPrice)
        lastPrice = str(lastPrice)
        sma50Price = "{:.2f}".format(sma50Price)
        sma50Price = str(sma50Price)
        sma200Price = "{:.2f}".format(sma200Price)
        sma200Price = str(sma200Price)

        # add stock ticker and timeframe to message
        messageString = '**Stock: ' + stockTicker + ' - Timeframe: ' + stockTimeframe + '**\n'
        # add sma50 difference to message
        if sma50Difference >= 0:
            messageString += '> Currently ' + "{:.2f}".format(
                abs(sma50Difference)) + '% above 50-period moving average \n'
        if sma50Difference < 0:
            messageString += '> Currently ' + "{:.2f}".format(
                abs(sma50Difference)) + '% below 50-period moving average \n'
        # add sma200 difference to message
        if sma200Difference >= 0:
            messageString += '> Currently ' + "{:.2f}".format(
                abs(sma200Difference)) + '% above 200-period moving average \n'
        if sma200Difference < 0:
            messageString += '> Currently ' + "{:.2f}".format(
                abs(sma200Difference)) + '% below 200-period moving average \n'

        # return message
        return messageString
    # if an error occurs
    except:
        # print error message
        print("An error occured in DiscordBot.StockCommandGetInfo")
        # return empty message
        return ' '


# clear matplotlib plot
def ClearStockChart():
    # try to clear chart
    try:
        # clear chart
        AlphaVantage.ClearChart()
        return
    # if an error occurs
    except:
        # print error message
        print("An error occured in DiscordBot.ClearStockChart")
        return


# delete image file
def DeleteImage(imagePath):
    # try to delete file
    try:
        # delete file
        os.remove(imagePath)
        return
    # if an error occurs
    except:
        # print error message
        print("An error occured in DiscordBot.DeleteImage")
        return


# get login key
loginKey = KEYS.GetDiscordLoginToken()
# run bot using login token
client.run(loginKey)
