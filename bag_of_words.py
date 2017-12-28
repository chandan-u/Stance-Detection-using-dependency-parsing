import nltk
#nltk.download('averaged_perceptron_tagger')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import ngrams

import pandas as pd



class Features:
    def __init__(self):
        self.train_features=[]


        # readfile
        self.trainData = pd.read_csv('clean_train.csv',sep=",")
        self.testData = pd.read_csv('clean_test.csv',sep=",",)




        # getBagOfWords
        self.getPOSBagOfWords()
        #self.getAllBagOfWords()

        # getCharcterNgrams
        # self.getCharcterNgrams()

        # Generate Features
        self.writeFeatureList()



    def preprocessing(self, tweet):


        tokens = filter(lambda word: word not in stop_words, tweet.split())

        return " ".join(tokens)





    def getPOSBagOfWords(self):
        """
           generate bag of words from the train set (unigrams nly)
        """

        tweets =self.trainData["Tweet"]

        for tweet in tweets.values:
            #tweet = self.preprocessing(tweet)
            pos_tag=nltk.pos_tag(tweet.split())
            for token, pos_tag in pos_tag:
                if pos_tag.startswith("NN") or pos_tag.startswith("JJ") or pos_tag.startswith("VB"):
                #| value.startswith("JJR") | value.startswith("JJS") | value.startswith("NNS") | value.startswith("NNP") | value.startswith("NNPS") | value.startswith("VBD")| value.startswith("VBG") | value.startswith("VBN") | value.startswith("VBP") | value.startswith("VBZ"):
                    # print token
                    if token not in self.train_features:
                        self.train_features.append(token)


    def getAllBagOfWords(self):
        """
           generate bag of words from the train set (unigrams nly)
        """

        tweets =self.trainData["Tweet"]


        for tweet in tweets.values:

            tweet = self.preprocessing(tweet)
            pos_tag=nltk.pos_tag(tweet.split())
            for token, pos_tag in pos_tag:
                if pos_tag.startswith("NN") or pos_tag.startswith("JJ") or pos_tag.startswith("VB"):
                #| value.startswith("JJR") | value.startswith("JJS") | value.startswith("NNS") | value.startswith("NNP") | value.startswith("NNPS") | value.startswith("VBD")| value.startswith("VBG") | value.startswith("VBN") | value.startswith("VBP") | value.startswith("VBZ"):
                    # print token
                    if token not in self.train_features:
                        self.train_features.append(token)


    def getMPQALexicon(self, sc_path = './subjectivity_clues_hltemnlp05/subjclueslen1-HLTEMNLP05.tff'):

        """
            Extract MPQA words and polarities from the lexicon
            return: mpqa_dictionary
        """

        mpqa_dict = {}
        # print sc_path
        fo = open(str(sc_path), 'r')
        for c in fo:
            c = str(c)
            key, value = c.strip().split(" ")[-1].split("=")
            if value == "negitive":
                mpqa_dict[key] = 0
            elif value == "positive":
                mpqa_dict[key] = 1
            else:
                mpqa_dict[key] = 0
        fo.close()

        return mpqa_dict


    def getCharcterNgrams(self, len=7):

        """
            generate character ngrams of lenght len
            return: list of list of ngrams of len n

        """

        for tweet in trainData[tweets].values:

            ngrams = [tweet[i:i+n] for i in range(len(tweet)-n+1)]

            for ngram in ngrams:
                if ngram not in self.train_features:
                    self.features.append(ngram)




    def getFeatureList(self,mode):

        """
            get all the necessary features
        """

        if mode == 'train':
            tweets = self.trainData["Tweet"]

        else:
            tweets = self.testData["Tweet"]

        # get mpqa lexicon dictionary
        #mpqa_dict = self.getMPQALexicon()

        features = []
        for id,tweet in enumerate(tweets.values):


            temp_list = [0] * len(self.train_features)
            tokens = tweet.split()



            for index, token in enumerate(self.train_features):
                if token in tweet:
                    #if token in mpqa_dict.keys():
                    #temp_list[index] = mpqa_dict[train_features[index]]
                    #else:
                    #    temp_list[index] = 0
                    temp_list[index] =  1

            if mode == "train":
                target = self.trainData["Target"][id]
                sentiment = self.trainData["Sentiment"][id]
                stance = self.trainData["Stance"][id]

            else:
                target = self.testData["Target"][id]
                sentiment = self.testData["Sentiment"][id]
                stance  = self.testData["Stance"][id]

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




            temp_list.append(target)
            temp_list.append(sentiment)
            temp_list.append(stance)
            features.append(temp_list)
        print len(features), len(features[0])
        return features





    def writeFeatureList(self):

        train_df = pd.DataFrame(self.getFeatureList(mode = "train"))
        test_df = pd.DataFrame(self.getFeatureList(mode = "test"))
        print train_df.head(3)
        train_df.to_csv('timbl_pos_train_1.csv',index=False,header=False)
        test_df.to_csv('timbl_pos_test_1.csv', index=False, header=False)





if __name__ == '__main__':
    Features()
