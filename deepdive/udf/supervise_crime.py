#!/usr/bin/env python
# coding=utf-8
from deepdive import *
import re
from collections import namedtuple
from util.processer import *
import os, sys
import divlaw
import handle_string

# CrimeLabel = namedtuple('CrimeLabel', 'p_id, label, type')


@tsv_extractor
@returns(lambda
				 mention_id="text",
				 label="int",
				 rule_id="text",
		 : [])
# heuristic rules for finding positive/negative examples of spouse relationship mentions
def supervise(
		mention_id="text",
		mention_text = "text",
		mention_begin_index="int", 
		mention_end_index="int",
		doc_id="text", 
		position = "text",
		sentence_index="int", 
		sentence_text="text",
		tokens="text[]", 
		pos_tags="text[]"
):
	APP_HOME = os.environ['APP_HOME']
	kw_non_crime = map(lambda word: word.strip(), open(APP_HOME + "/udf/dicts/kw_non_crime.txt", 'r').readlines())
	kw_crime = map(lambda word: word.strip(), open(APP_HOME + "/udf/dicts/kw_crime.txt", 'r').readlines())

	# Non crime signals on the left of candidate mention
	NON_CRIME_SIGNALS_LEFT = frozenset(kw_non_crime)
	# crime signals on the left of candidate mention
	CRIME_SIGNALS_LEFT = frozenset(kw_crime)

	WINDOW_SIZE = 10
	MAX_PHRASE_LENGTH = 5
	num_tokens = len(tokens)

	# Get all subsequences of left sentence with WINDOW_SIZE = 10
	low_tokens = map(lambda token: token.lower(), tokens)
	left_window = get_left_window(mention_begin_index, low_tokens, WINDOW_SIZE)
	# right_window = get_right_window(p_end, low_tokens, WINDOW_SIZE)
	phrases_in_sentence_left = list(get_all_phrases_in_sentence(left_window, MAX_PHRASE_LENGTH))

	# Get candiate mention text
	crime_in_content = " ".join(low_tokens[mention_begin_index:mention_end_index + 1])


	
	# Negative rules
	# Rule 1: On the left of mention, contains some keywords that appears in kw_non_legal_penalty

	if len(NON_CRIME_SIGNALS_LEFT.intersection(phrases_in_sentence_left)) > 0:
		yield [
			mention_id,
			-1, 
			"neg:non_crime_signals_left"
		]

	# Rule 2: The sentence that contains mention is in is too short
	if num_tokens < 10:
		yield [
			mention_id,
			-1,
			"neg:sentence_too_short"
		]

	if len(mention_text) < 10:
		yield [
			mention_id,
			-1,
			"neg:crime_mention_too_short"
		]
	# Positive rules
	# Ruile 1: on the left of mention, containing some keywords that appears in kw_legal_penalty :
	if len(CRIME_SIGNALS_LEFT.intersection(phrases_in_sentence_left)) > 0:
		yield [
			mention_id,
			1, 
			"pos:crime_signals_left"
		]
	if len(CRIME_SIGNALS_LEFT.intersection(crime_in_content)) > 0:
                yield [
                        mention_id,
                        1,
                        "pos:crime_signals_in_content"
                ]
