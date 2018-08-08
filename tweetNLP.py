import numpy as np
import csv

def readSentimentList(file_name):
    ifile = open(file_name, 'r')
    happy_log_probs = {}
    sad_log_probs = {}
    ifile.readline() #Ignore title row
    
    for line in ifile:
        tokens = line[:-1].split(',')
        happy_log_probs[tokens[0]] = float(tokens[1])
        sad_log_probs[tokens[0]] = float(tokens[2])
    
    return happy_log_probs, sad_log_probs

def classifySentiment(words, happy_log_probs, sad_log_probs):
    # Get the log-probability of each word under each sentiment
    happy_probs = [happy_log_probs[word] for word in words if word in happy_log_probs]
    sad_probs = [sad_log_probs[word] for word in words if word in sad_log_probs]
    
    # Sum all the log-probabilities for each sentiment to get a log-probability for the whole tweet
    tweet_happy_log_prob = np.sum(happy_probs)
    tweet_sad_log_prob = np.sum(sad_probs)
    
    # Calculate the probability of the tweet belonging to each sentiment
    prob_happy = np.reciprocal(np.exp(tweet_sad_log_prob - tweet_happy_log_prob) + 1)
    prob_sad = 1 - prob_happy
    
    return prob_happy, prob_sad

def main():
    # We load in the list of words and their log probabilities
    happy_log_probs, sad_log_probs = readSentimentList('twitter_sentiment_list.csv')
    sentimentAnalysisResult=[]
    counter=0
    with  open('tweet.csv','rb') as csvfile:
        
        with open('tweetWithSemantics.csv', 'wb') as fp:
            #a = csv.writer(fp)
            a = csv.writer(fp, delimiter='|',quotechar='"')
            spamreader = csv.reader(csvfile, delimiter='|',quotechar='"')
            tweet1=[]
            result=[]

            for row in spamreader:
                
                sentence=row[2].decode('utf-8')
                print (sentence)
                tweet1=sentence.split()
                #print(tweet1)
                #Calculate the probabilities that the tweets are happy or sad
                tweet1_happy_prob, tweet1_sad_prob = classifySentiment(tweet1, happy_log_probs, sad_log_probs)
                #print "The probability that tweet1 (", tweet1, ") is happy is ", tweet1_happy_prob, "and the probability that it is sad is ", tweet1_sad_prob
                if tweet1_happy_prob>0.5:
                    emotionIndex=1
                elif tweet1_happy_prob==0.5:
                    emotionIndex=0
                else:
                    emotionIndex=-1
                #emotionIndex=(float(tweet1_happy_prob)-0.5)*20
                print "the emotion index is : %d "%emotionIndex
                sentimentAnalysisResult.append(emotionIndex)
                a.writerow([str(row[0]),str(row[1]),str(sentence.encode('utf-8')),str(row[3]), int(emotionIndex)])
                counter=counter+1
if __name__ == '__main__':
    main()
