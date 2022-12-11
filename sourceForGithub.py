import praw
import spacy
import time
import matplotlib.pyplot as plot

parse = spacy.load("en_core_web_lg")

#I have removed my password, client_id, and client secret for privacy reasons. 
#In order to be run, this code needs to be given those values as strings in the fields below, along with the matching username.
#those values can be obtained after registering a new application with reddit.

reddit = praw.Reddit(

    client_id = "",
    client_secret = "",
    password = "",
    username = "17s-Alpha",
    user_agent = "Data Retreival tool for academic purposes by u/17s-Alpha" 

)

subreddit = reddit.subreddit("HollowKnight")
subreddit = reddit.subreddit("Breath_of_the_Wild")



count = 0
scount = 0

drecords = []

nrecords = []

frecords = []

def addRecord(new, records):
    for i in range(records.__len__()):
        if new[0] == records[i][0]:
            records[i] = (records[i][0], records[i][1] + new[1])
            return
    records.append(new)
        

def antAnalys(text):
    out = 0
    goodWords = ["hype", "anticipation", "release", "sequel"]

    
    words = parse(text)
    for word in words:
        for vword in goodWords:
            if parse.vocab[word.text].similarity(parse.vocab[vword]) > 0.8:
                out = 1
                break
    return out


def commentParseRecursive(cTree):


    for comments in cTree:
        score = antAnalys(comments.body) * comments.score
        daysAgo = int((time.time() -comments.created_utc)) // 86400
        if score != 0:
            addRecord((daysAgo, score), drecords)

        addRecord((daysAgo, comments.score), nrecords)
        commentParseRecursive(comments.replies)
    return 

c = 0

for post in subreddit.top(limit=100, time_filter = "month"):
    post.comments.replace_more(limit=0)
    commentParseRecursive(post.comments)
    c += 1
    print(c)

for data in drecords:
    for norm in nrecords:
        if data[0] == norm [0]:
            frecords.append((-data[0], data[1] / norm[1]))

frecords = sorted(frecords, key=lambda input: input[0], reverse= True)


x = []
y = []

for d in frecords:
    x.append(d[0])
    y.append(d[1])

plot.bar(x, y)
plot.show()

print("done")