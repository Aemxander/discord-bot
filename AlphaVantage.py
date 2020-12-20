import os.path
import sys

import KEYS
import matplotlib.pyplot as plt
import pandas
import requests
from alpha_vantage.timeseries import TimeSeries

# alpha vantage api key
apiKey = KEYS.GetAlphaVantageKey()

# show all rows/columns from DataFrame
pandas.set_option('display.max_rows', None)
pandas.set_option('display.max_columns', None)


# function for getting stock data
def GetStock(stockName):
    # initiate alpha vantage timeseries api
    ts = TimeSeries(key=apiKey, output_format='pandas')
    # try to get stock data
    try:
        # get stock data
        data, metadata = ts.get_intraday(symbol=stockName, interval="60min", outputsize="full")
        # return stock data
        return data, metadata
    # if a ValueError occurs
    except ValueError as error:
        # save error as a string
        error_string = str(error)
        # if out of API calls
        if error_string.__contains__("Our standard API call frequency is 5 calls per minute and 500 calls per day."):
            # return -2, -2
            return -2, -2
        # if it is a different error
        else:
            # return -1, -1
            return -1, -1
    # if an error occurs
    except:
        # return -1, -1
        return -1, -1


# add simple moving averages to DataFrame
def SimpleMovingAverages(stockData, stockMetadata):
    # convert parameter to DataFrame
    stockData = pandas.DataFrame(stockData)

    # create deep copy of stockData
    duplicate = stockData.copy(deep=True)
    # sort duplicate by ascending date
    duplicate = duplicate.sort_values(by='date', ascending=True)

    # get 50 SMA from close using duplicate (ascending order by date)
    stockData['6. sma50'] = duplicate['4. close'].rolling(window=50).mean().shift(1)
    # get 200 SMA from close using deplicate(ascending order by date)
    stockData['7. sma200'] = duplicate['4. close'].rolling(window=200).mean().shift(1)

    # return data, metadata
    return stockData, stockMetadata


# create image from stock data
def CreateChart(stockData, stockMetadata):
    # try to create chart
    try:
        # create image name
        imageName = "StockChart.png"
        # plot data
        stockData['4. close'].plot(label='Closing Price', color='black', alpha=0.7, lw=1.15)
        stockData['6. sma50'].plot(label='MA 50', color='teal', alpha=0.7, lw=1)
        stockData['7. sma200'].plot(label='MA 200', color='orange', alpha=0.7, lw=1)
        # add plot legend
        plt.legend(loc="best")
        # add horizontal line
        plt.axhline(y=stockData['4. close'][0], color="black", linestyle=":", alpha=0.7, lw=0.75)
        # set plot title
        plt.title(
            "Stock: " + stockMetadata["2. Symbol"].upper() + " - " + "Timeframe: " + stockMetadata[
                "4. Interval"].upper())
        # print x length
        leftX, rightX = plt.xlim()
        plt.text(x=rightX + 1, y=stockData['4. close'][0], s=str(stockData['4. close'][0]), color='black')
        # save plot as image
        plt.savefig(imageName)
        # return path to chart
        return imageName
    # if an error occurs
    except:
        # print error message
        print("An error occurred in AlphaVantage.CreateChart")
        return


# clears and saves the plot
def ClearChart():
    # clear plot
    plt.clf()
    # close plot
    plt.close()
    # return
    return


# save data to pardir + AlphaVantageData folder
def SaveData(stockData, stockMetadata):
    # create directory name
    directory = os.pardir
    directory += "\\"
    directory += "AlphaVantageData"
    directory += "\\"
    # if directory does not exist
    if not os.path.isdir(directory):
        # create directory
        os.mkdir(directory)

    # create file name
    fileName = stockMetadata["2. Symbol"].upper() + "-" + stockMetadata["4. Interval"].upper()

    # boolean for file existing
    exists = True
    # integer to increment
    integer = 1
    # unique file name
    uniqueFileName = ""

    # until file doesn't exist
    while exists == True:
        # if file with fileName doesn't exist
        if os.path.isfile(directory + fileName + "-" + str(integer) + ".txt") == False:
            # save file name
            uniqueFileName = directory + fileName + "-" + str(integer) + ".txt"
            # set exists to false
            exists = False
            # leave loop
            pass
        # if file exists
        else:
            # increment integer
            integer += 1

    # try to write data to a file
    try:
        # open/create a text file called uniqueFileName
        datafile = open(uniqueFileName, "w+")
        # write stock data to file
        datafile.write(str(stockData) + "\n")
        datafile.write(str(stockMetadata))
        # close file
        datafile.close()
        return
    # if an error occurs
    except:
        # print error message
        print("An error occured in AlphaVantage.SaveData")
        return


# search stocks
def StockSearch(searchQuery):
    # try to search for stock
    try:
        # initiate timeseries alpha vantage api
        ts = TimeSeries(key=apiKey, output_format='json')

        # get data from search query
        data = ts.get_symbol_search(searchQuery)
        # take the first item from data
        data = data[0]

        # create list for search results
        searchResults = []

        # for each item in data
        for item in data:
            # add item ticker and item name to the search results
            searchResults.append([item['1. symbol'], item['2. name']])

        # sort results based on stock ticker
        searchResults = sorted(searchResults, key=lambda x: x[0])

        # if search results are empty
        if searchResults == []:
            # return error message
            return '> Sorry, there were no results for this search term!'

        # create string for filtered search results
        filteredSearchResults = '**Search Results** \n'

        # for each item in search results
        for item in searchResults:
            # open text file of listings
            with open('StockListings.txt', 'r') as file:
                # read each line from file
                for line in file:
                    # check if line contains stock ticker + '|'
                    if (str(item[0]) + '|') in line:
                        # if line contains stock ticker + '|' add to result string
                        filteredSearchResults += '> ' + str(item[0]) + ' - ' + str(item[1]) + '\n'
                        break
                # close file
                file.close()

        # return search results string
        return filteredSearchResults
    # if an error occurs
    except:
        # print error message
        print('An error occurred in AlphaVantage.StockSearch')
        # return error string
        return '> Sorry, an error occurred while getting the search results!'


# update stock listings file
def UpdateListings():
    # try to update stocks w/ deleting current file
    try:
        # delete current stock listing file
        os.remove(os.path.join(sys.path[0], 'StockListings.txt'))

        # get nasdaq listed stocks
        r = requests.get('http://ftp.nasdaqtrader.com/dynamic/SymDir/nasdaqlisted.txt')
        nasdaqListed = r.text

        # get other exchange listed stocks
        r = requests.get('http://ftp.nasdaqtrader.com/dynamic/SymDir/otherlisted.txt')
        otherListed = r.text

        # open/create a text file called uniqueFileName
        datafile = open('StockListings.txt', "w+")

        # write stock data to file
        datafile.write(str(nasdaqListed) + str('\n') + str(otherListed))
        return '> The stock listings have been updated!'
    # try to update stocks w/o deleting current file
    except:
        # get nasdaq listed stocks
        r = requests.get('http://ftp.nasdaqtrader.com/dynamic/SymDir/nasdaqlisted.txt')
        nasdaqListed = r.text

        # get other exchange listed stocks
        r = requests.get('http://ftp.nasdaqtrader.com/dynamic/SymDir/otherlisted.txt')
        otherListed = r.text

        # open/create a text file called uniqueFileName
        datafile = open('StockListings.txt', "w+")

        # write stock data to file
        datafile.write(str(nasdaqListed) + str('\n') + str(otherListed))
        return '> The stock listings have been updated!'
