#!/usr/bin/env python
# -*- coding:utf8 -*-

from deepdive import *
import re
import handle_string
import divlaw
import time
import sys

@tsv_extractor
@returns(lambda
    doc_id = "text",
    position = "text",
    modify_doc_id = "text"  
    :[])
def extract(
    doc_id =  "text",
    position = "text", 
    modify_title = "text",
    released_date = "text",
    doc_id_resources = "text[]",
    doc_title_resources = "text[]",
    doc_symbol_resources = "text[]",
    type_doc = "text[]",
    released_date_resources ="text[]" 
    ):
    
    released_date_temp = None
    if released_date:
	try:
            released_date_temp = time.strptime(released_date, "%Y-%m-%d")
	except:
	    print >>sys.stderr, doc_id,position,released_date
	    return
    pattern = re.compile(r"[0-9]+(/[0-9]+)*((/|-)[A-ZĐƯ]+[0-9]*)+")
    m = pattern.match(modify_title)
    if (m is not None):
        symbol = m.group(0)
        symbol = handle_string.toLowerCase(symbol)
        available = False
        for i in range(0,len(doc_symbol_resources)):
	    try:
                released_date_temp2 = time.strptime(released_date_resources[i], "%Y-%m-%d")
	    except:
		print >>sys.stderr, doc_id,position,released_date_resources[i]
		continue
            if handle_string.toLowerCase(doc_symbol_resources[i]) == symbol and (released_date_temp2 == released_date_temp or released_date is None):
                available = True
                yield [
                    doc_id,
                    position,
                    doc_id_resources[i],
                ]
		return
        if not available :
            yield [
                doc_id,
                position,
                "NA",
            ]
	    return
    else :
        available = False
        tempReal = handle_string.to_unicode(modify_title)
        tempReal = handle_string.toLowerCase(tempReal)
        for i in range(0,len(doc_title_resources)):
            temp = type_doc[i] + " " + doc_title_resources[i]
            tempU = handle_string.to_unicode(temp)
            tempU = handle_string.toLowerCase(tempU)
	    try:
            	released_date_temp2 = time.strptime(released_date_resources[i], "%Y-%m-%d")
            except:
                print >>sys.stderr, doc_id,position,released_date_resources[i]
            if tempU.strip() == tempReal.strip() and (released_date_temp2 == released_date_temp or released_date is None):
                available == True
                yield [
                    doc_id,
                    position,
                    doc_id_resources[i]
                ]
		return
                break
        if available == False :
            yield [
                doc_id,
                position,
                "NA"
            ]


