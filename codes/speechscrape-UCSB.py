#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 24 20:37:28 2019

@author: bartbonikowski
"""


import json
import requests
from bs4 import BeautifulSoup
import re
import os
import time
from collections import defaultdict
from datetime import date


#wkdir = '~/Users/bartbonikowski/Documents/Nationalism and Trump/Trump Scrape/'
root = 'https://www.presidency.ucsb.edu'

cand_dict = {1: {'first': 'Hillary', 'last': 'Clinton', 'title': 'Secretary', 'start': date(2015, 4, 12), 'end': date(2016, 11, 9)},
             2: {'first': 'Bernie', 'last': 'Sanders', 'title': 'Secretary', 'start': date(2015, 4, 30), 'end': date(2016, 7, 12)},
             3: {'first': 'Ted', 'last': 'Cruz', 'title': '', 'start': date(2015, 3, 23), 'end': date(2016, 5, 3)},
             4: {'first': 'Jeb', 'last': 'Bush', 'title': '', 'start': date(2015, 6, 15), 'end': date(2016, 2, 20)},
             5: {'first': 'John', 'last': 'Kasich', 'title': '', 'start': date(2015, 7, 21), 'end': date(2016, 5, 4)},
             6: {'first': 'Marco', 'last': 'Rubio', 'title': '', 'start': date(2015, 4, 13), 'end': date(2016, 3, 16)}}

for cand in range(1,7):  
    
    candidate = '/people/other/' + cand_dict[cand]['first'] + '-' + cand_dict[cand]['last'] + '?page='
    candidate_iter = 1
    
    speech_path = 'speeches_' + lower(cand_dict[cand]['last']) + '_ucsb'
    
    r = requests.get(root + candidate + str(candidate_iter))
    soup = BeautifulSoup(r.text, 'html.parser')
    
    fin = soup.find_all('a', title = 'Go to last page')
    
    max = int(re.findall(r'page=([0-9]+)', str(fin[0]))[0])
    
    metadata = defaultdict(list)
            
    for iter in range(candidate_iter, max + 1):
        
        print 'Page ' + str(iter)
    
        r = requests.get(root + candidate + str(iter))
        soup = BeautifulSoup(r.text, 'html.parser')

        titles_raw = soup.findAll(class_="views-field views-field-title")
        dates_raw = soup.findAll(class_="date-display-single")

        links = []
        for x in titles_raw:
            links.append(x.a['href'])
        titles = []
        for x in titles_raw:
            titles.append(x.a.contents[0])
        dates = []
        for x in dates_raw:
            date_raw = re.findall(r'content="([0-9]{4})-([0-9]{2})-([0-9]{2})', str(x))
            speechdate = date(int(date_raw[0][0]), int(date_raw[0][1]), int(date_raw[0][2]))
            dates.append(speechdate)

        assert len(links) == len(titles) == len(dates)
        
        lengthbefore = len(metadata)
        
        for i in range(len(metadata), len(metadata) + len(links)):
            metadata[i] = [links[i - lengthbefore], titles[i - lengthbefore], dates[i - lengthbefore]]
                    
    speechnum = 0
            
    for i in range(0, len(metadata) - 1):
        if metadata[i][2] >= cand_dict[cand]['start'] and metadata[i][2] <= cand_dict[cand]['end'] and re.findall('[Rr]emarks', metadata[i][1]):
            speechnum += 1
            print 'Speech number ' + str(speechnum)
            r = requests.get(root + metadata[i][0])
            soup = BeautifulSoup(r.text, 'html.parser')
            text_full = soup.findAll(class_='field-docs-content')[0].get_text()
    
    # DOUBLE CHECK IF THIS MAKES SENSE (AND CHECK IT FOR CRUZ ETC)
#            if re.findall(cand_dict[cand]['title'] + ' ' + cand_dict[cand]['last'] + ':([\s\S]+)', text_full):
#                text = re.findall(cand_dict[cand]['title'] + ' ' + cand_dict[cand]['last'] + ':([\s\S]+)', text_full)[0]
#            else:
            text = text_full
                
            filename = lower(cand_dict[cand]['last']) + '-speech-' + str(metadata[i][2]) + '-' + re.findall('[\w]+-[\w]+-[\w]+$', metadata[i][0])[0]
            try:
                os.mkdir(speech_path)
            except OSError:  
                pass
            with open(os.getcwd() + '/' + speech_path + '/' + filename + '.txt', 'w') as text_file:
                text_file.write(text.encode('utf8'))
                
        
#
#
#            # Grabbing LD-JSON header with speeech content
#            ldjson = soup.find('script', {'type':'application/ld+json'})
#            header = json.loads(ldjson.text, strict=False)
#            splen = len(header['articleBody'])
#            print(splen)
#        
#        # Tweaking URL suffix for use with file name later
#        filename = re.search(r'donald-(.*)', urlsuffix['url']).group(1)
#        
#        # Weeding out speeches that start with a note about automated transcription
#        match = re.search(r'\[', header['articleBody'])
#        if match:
#            if match.start() > 5:
#                try:  
#                    os.mkdir(speech_path)
#                except OSError:  
#                    pass
#                with open(os.getcwd() + '/' + speech_path + '/' + filename + '.txt', 'w') as text_file:
#                    text_file.write(header['articleBody'].encode('utf8'))
#            # Speeches that start with a note about automated transcription saved to a separate folder
#            else:
#                try:  
#                    os.mkdir(speech_path_aut)
#                except OSError:  
#                    pass
#                with open(os.getcwd() + '/' + speech_path_aut + '/' + filename + '.txt', 'w') as text_file:
#                    text_file.write(header['articleBody'].encode('utf8'))
#        else:
#            try:  
#                os.mkdir(speech_path)
#            except OSError:  
#                pass
#            with open(os.getcwd() + '/' + speech_path + '/' + filename + '.txt', 'w') as text_file:
#                text_file.write(header['articleBody'].encode('utf8'))
#            
##        time.sleep(3)
        