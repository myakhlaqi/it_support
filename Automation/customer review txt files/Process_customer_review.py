#! /usr/bin/env python3

import json
import os
import requests

def extract_feedback(logfile):
    review_items = {}
    file = open(logfile, "r")

    title, name, date, feedback = [line.strip() for line in file.readlines()]
    #print(title,name,date,feedback)
    review_items["title"] = title
    review_items["name"] = name
    review_items["date"] = date
    review_items["feedback"] = feedback
    return review_items

def get_txt_files(path):
    #    files=[os.path.join(path,item) for item in os.listdir(path) if os.path.isfile(item) and item.endswith(".txt")]
    files = [
        os.path.join(path, item) for item in os.listdir(path)
        if item.endswith(".txt")
    ]
    return files


def gen_feedback_dic(path):
    feedback_dic = []
    for f in get_txt_files(path):
        x = extract_feedback(f)
        feedback_dic.append(x)
        #print(extract_feedback(f))
        post_to_webservice("http://104.198.221.153/feedback/",x)
    return feedback_dic

def post_to_webservice(url, feedbacks):
    #headers =  {"Content-Type":"application/json"}
    response = requests.post(url, json=feedbacks)
    if (response.status_code == 201):
        print("Submitted!")
    print("inside post:", response.status_code)
    #print("json:", response.json)

path = "./"
print(get_txt_files(path))

print(extract_feedback("./020.txt"))

gen_feedback_dic(path)
#print(feedback_data)
