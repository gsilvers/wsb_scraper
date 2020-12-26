
'''
    Hi u/TiltedOneTrick 
    I've added some code changes but also some comments to help explain why 
    overall this code is really good and these changes are just things to learn
    for your next project. Please give a shout if you need anything or have q's

    Things I've Changed and Why
    1 - You have some inconsistancies and issues with your namings nothing big but for 
        example you have client_id which is snake case but files which is not 
        there are guides for python like https://www.python.org/dev/peps/pep-0008/
        but in general just stick with the same fully through your code if you're 
        uncertain always go with word_word in python for functions and variables
        if you are to the point of making classes and instances then you use some
        CapitolCase.
    2 - Some of your variable names you say like _list or _dict. This is good to do
        if you make your own custom class but you don't need to say its a dict or list 
    3 - Not sure if this is just because or what but you have these three ticker files 
        list1,2,3 you seem to be just reading them so i renamed the file and made it one
    4 - You are on the right path putting get_tickers as its own function 
        I am guessing you picked that up front. That is good but once you have your code
        working you should "re-factor" and see if you can clean up your code to do the
        same thing but more clearly or faster this is a huge part of coding if you
        take it up as a job I am refactoring your code to break things into a few more functions
        function 1 : get_ticker
'''

import praw
import re
import pandas as pd
import config


def get_tickers():
    reddit = praw.Reddit(
        client_id= config.api_id,
        client_secret= config.api_secret,
        user_agent="WSB Scraping",
    )
    to_buy = []
    to_sell = []
    prev = open("prev.txt", "w+")
    prev_tickers = prev.readlines()
    prev_tickers = [x.strip() for x in prev_tickers]
    weekly_tickers = {}
    regex_pattern = r'\b([A-Z]+)\b'
    phrases = {}
    tickers = {}
    files = ["list1.csv", "list2.csv", "list3.csv"]
    for file in files:
        tl = pd.read_csv(file, skiprows=0, skip_blank_lines=True)
        tl = tl[tl.columns[0]].tolist()
        for ticker in tl:
            tickers[ticker] = 1
    black_list = ["A", "I", "DD", "WSB", "YOLO", "RH"]
    for submission in reddit.subreddit("wallstreetbets").top("week"):
        strings = [submission.title]
        submission.comments.replace_more(limit=0)
        for comment in submission.comments.list():
            strings.append(comment.body)
        for s in strings:
            for phrase in re.findall(regex_pattern, s):
                if phrase not in black_list:
                    if tickers.get(phrase) == 1:
                        if weekly_tickers.get(phrase) is None:
                            weekly_tickers[phrase] = 1
                        else:
                            weekly_tickers[phrase] += 1
    top_tickers = sorted(weekly_tickers, key=weekly_tickers.get, reverse=True)[:5]
    for new in top_tickers:
        if new not in prev_tickers:
            to_buy.append(new+'\n')
    for old in prev_tickers:
        if old not in top_tickers:
            to_sell.append(old+'\n')

    prev.writelines(top_tickers)
    prev.close()
    return to_buy, to_sell


def main():
    to_buy, to_sell = get_tickers()
    buy = open("toBuy.txt", "w")
    sell = open("toSell.txt", "w")
    buy.writelines(to_buy)
    sell.writelines(to_sell)
    buy.close()
    sell.close()


if __name__ == '__main__':
    main()
