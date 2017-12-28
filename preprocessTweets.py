
import pandas as pd
import re
import string

from nltk import word_tokenize
import preprocessor as p
p.set_options(p.OPT.URL, p.OPT.EMOJI, p.OPT.NUMBER, p.OPT.SMILEY, p.OPT.MENTION)



regex = re.compile('[%s]' % re.escape(string.punctuation))
regexb=re.compile('b[\'\"]')

trainData = pd.read_csv('train.csv',sep=",")
testData = pd.read_csv('test.csv',sep=",")





for id, tweet in enumerate(trainData["Tweet"]):

    print id
    tweet = p.clean(tweet)
    tweet = tweet.lower()
    tweet = regexb.sub('', tweet)
    tweet = regex.sub('', tweet)
    tokens = filter(lambda token: token != '', word_tokenize(tweet))

    trainData["Tweet"][id] = " ".join(tokens)


for id, tweet in enumerate(testData["Tweet"]):


    print id
    tweet = p.clean(tweet)
    tweet = tweet.lower()
    tweet = regexb.sub('', tweet)
    tweet = regex.sub('', tweet)
    tokens = filter(lambda token: token != '', word_tokenize(tweet))

    trainData["Tweet"][id] = " ".join(tokens)

trainData.to_csv("clean_train.csv", sep=",", header = True)
testData.to_csv("clean_test.csv", sep=",", header = True)
