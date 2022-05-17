#!/usr/bin/env python3 

import re
import operator

def gen_error_report( logfile):
    error_dic={}
    file=open(logfile, "r")

    for line in file.readlines():
        #print(line)
        match=re.search(r"(ERROR )([\w ]*)", line)
        if match:
            key=match.group(2)
            if key in error_dic:
                error_dic[key]+=1 
            else: 
                error_dic[key]=1 
    file.close()
    return error_dic


def gen_usr_report(logFile):
    user_dic={}
    file=open(logFile, "r")
    info_pattern="(INFO )([\w ]*) (\[#\d*\]) .([.a-zA-Z]+)."
    error_pattern=r"(ERROR )([\w|' ]*) .([.a-zA-Z]+)."

    for line in file.readlines():
#
        info_result=re.search(info_pattern,line)
        error_result= re. search(error_pattern,line)
        if info_result:
            key=info_result.group(4)
            if key in user_dic:
                user_dic[key][0]+=1
            else:
                user_dic[key]=[1,0]
        elif error_result:
            key=error_result.group(3)
            if key in user_dic:
                user_dic[key][1]+=1
            else:
                user_dic[key]=[0,1]

    file.close()
    return user_dic

def print_error(dic):
    max_len_msg= max([len(item[0]) for item in dic])
    for key in dic:
        print("{0:<{2:d}} {1:<10}".format(key[0],key[ 1] , max_len_msg ))

def print_user(dic):
    for item in dic:
        print("{0:<10}\t({1:<5},{2:>5})".format(item[0],item[1][0],item[1][1]))

def save_to_file(file_name,my_list,header):
    file=open(file_name,"w")
    file.write(header+"\n")
    for item in my_list:
        if isinstance(item[1], list):
            file.write("{0},{1},{2}\n".format(item[0],item[1][0],item[1][1]))
        elif isinstance(item[1],int):
            file.write("{0},{1}\n".format(item[0],item[1]))
    file.close()
msg_dic=gen_error_report("./syslog.log")
user_dic=gen_usr_report("./syslog.log")
#print_error(sorted(msg_dic.items(),key = lambda x: x[1], reverse=True))
save_to_file("./error_message.csv",sorted(msg_dic.items(),key = lambda x: x[1], reverse=True),"Error,Count")
save_to_file("./user_statistics.csv",sorted(user_dic.items()),"Username,INFO,ERROR")
