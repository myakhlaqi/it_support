#! /usr/bin/env python3

from genericpath import isfile
import os
import requests

def extract_feedback(logfile):
    review_items={}
    file=open(logfile, "r")

    title,name,date,feedback =[ line.strip() for line in file.readlines()]
    #print(title,name,date,feedback)
    review_items[title]=[name,date,feedback]
    return review_items

#print(gen_error_report("./test.txt"))

def get_txt_files(path):
    files=[item for item in os.listdir(path) if os.path.isfile(item) and item.endswith(".txt")]
    return files
def gen_feedback_dic(path):
    feedbcak_dic={}
    for f in get_txt_files(path):
        x=extract_feedback(f)
        feedbcak_dic.update(x)
    return feedbcak_dic

def post_to_webservice(url,feedbacks):
    x = requests.post(url, feedbacks)
    print(x.text)
    
feedback_data=gen_feedback_dic("./")
print(feedback_data)
#post_to_webservice("",feedback_data)
print("web service successfully updated!")


    
    