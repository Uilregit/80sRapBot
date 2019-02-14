import tweepy
import pronouncing as pn

def Main():
    consumer_key = "xxxxxxxxxxxxxxxxxxxxxxxxx"
    consumer_secret = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    access_token = "xxxxxxxxxxxxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    access_token_secret = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    
    auth = tweepy.OAuthHandler (consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    
    user = api.me()
    print (user.name)
    
    counter = 0
    
    for tweets in tweepy.Cursor(api.search, q = ",", lang = "en").items(1000):
        counter +=1
        
        words = BreakIntoWords(tweets.text)
        if len(words) > 1:
            if RhymeWithSay(words):
                if CountSyllables(words) in range (6,14):
                    print (tweets.text)
                    print ("###################################")
                    api.update_status("My name is RapBot and I'm here to say "+("https://twitter.com/"+tweets.user.screen_name+"/status/"+str(tweets.id)).replace(" ",""))
                    #tweets.retweet()
                else:
                    print (CountSyllables(words))
           
def RhymeWithSay (words):
    if words[len(words)-1].lower() in pn.rhymes("say"):
        return True
    return False
    
def CountSyllables (words):
    counter = 0
    for word in words:
        try:
            counter += pn.syllable_count(pn.phones_for_word(word.lower())[0])
        except IndexError:
            print ("*.*.*.*.*.*.*.*.*")
            print (word)
            print ("*.*.*.*.*.*.*.*.*")
            counter += len(word)//3
    return counter

def BreakIntoWords (sentence):
    if ("RT" in sentence):
        sentence = sentence[sentence.find(": ")+2:]
    if ("http" in sentence):
        sentence = sentence[:sentence.find("http")]
    words = sentence.split(" ")
    output = []
    for i in range(len(words)):
        if IsValidWord(words[i]):
            output += [FormateWord(words[i])]
    return output

def IsValidWord (word):
    numbers = ["1","2","3","4","5","6","7","8","9","0", "@", "#","http"]
    for num in numbers:
        if num in word:
            return False
    return True

def FormateWord (word):
    punctuation = [".",",","?","!","(",")",":",'''"''',"""'"""]
    for pun in punctuation:
        if pun in word:
            return word.replace(pun,"")
    return word