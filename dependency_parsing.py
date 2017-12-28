
import pandas as pd
from nltk.parse.malt import MaltParser
mp = MaltParser('maltparser-1.8.1', 'engmalt.linear-1.7.mco')





train_triplets_list = []
test_triplets_list = []


dependency_triplets = {}
dependency_triplet_id = 0


def generateTriplets(tweet, mode):


    global dependency_triplet_id
    triplets = []
    parsed_sent = mp.parse_one(tweet.split())
    for triple in parsed_sent.triples():

        """

          triple format : ((u'shot', u'NN'), u'nsubj', (u'I', u'PRP'))
              Extract dependency triples of the form:
              ((head word, head tag), rel, (dep word, dep tag))

          Convert to form: (word, head, label/relation)

        """


        head, label, word = triple

        head = head[0]
        word = word[0]

        triplet = (word, head, label)

        if mode == "train":
            train_triplets_list.append(triplet)
            if triplet not in dependency_triplets.keys() :
                dependency_triplets[triplet] = dependency_triplet_id
                dependency_triplet_id = dependency_triplet_id + 1
        else:
            test_triplets_list.append(triplet)










def getFeatureList(mode, trainData, testData):

    """
        get all the necessary features
    """

    if mode == 'train':
        tweets = trainData["Tweet"]
    else:
        tweets = testData["Tweet"]

    keys = dependency_triplets.keys()
    feature_length = len(keys)

    features = []
    for id,tweet in enumerate(tweets.values):


        temp_list = [0] * feature_length


        if mode == "train":
            tweet_triplets = train_triplets_list[id]
            target = trainData["Target"][id]
            sentiment = trainData["Sentiment"][id]
            stance = trainData["Stance"][id]

        else:
            tweet_triplets = test_triplets_list[id]
            target = testData["Target"][id]
            sentiment = testData["Sentiment"][id]
            stance  = testData["Stance"][id]

        if stance == "AGAINST":
            stance = -1
        elif stance == "FAVOR":
            stance = 1
        else:
            stance = 0


        if sentiment == "neg":
            sentiment = -1
        elif sentiment == "pos":
            sentiment = 1
        else:
            sentiment = 0

        if target == "Hillary Clinton":
            target = 5
        elif target == "Legalization of Abortion":
            target = 4
        elif target == "Atheism":
            target = 3
        elif target == "Climate Change is a Real Concern":
            target = 2
        elif target == "Feminist Movement":
            target = 1
        else:
            target =0

        for triplet in tweet_triplets:
            if trilpet in keys:
                temp_list[dependency_triplets[triplet]] = 1


        temp_list.append(target)
        temp_list.append(sentiment)
        temp_list.append(stance)
        features.append(temp_list)
    print len(features), len(features[0])
    return features





def writeFeatureList(trainData, testData, dependency_triplets):

    train_features = getFeatureList(trainData, testData, mode = "train")
    test_features = getFeatureList( trainData, testData, mode = "test",)
    train_df = pd.DataFrame(train_features)
    test_df = pd.DataFrame(test_features)
    train_df.to_csv('timbl_triplets_train.csv',index=False,header=False)
    test_df.to_csv('timbl_triplets_test.csv', index=False, header=False)






trainData = pd.read_csv('test.csv',sep=",")
testData = pd.read_csv('test.csv',sep=",",)


# dictionary of triplets :: global

for tweet in trainData["Tweet"]:

    #preprocess(tweet)
    generateTriplets(tweet, mode="train")

for tweet in testData["Tweet"]:

    generateTriplets(tweet, mode="test")



    #print dependency_triplets.keys()
    #print dependency_triplets
print len(dependency_triplets.keys())



# Generate Features
writeFeatureList(trainData, testData, dependency_triplets)
