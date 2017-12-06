#!/usr/bin/python

"""
CS 5761 PA 5 "Question Answering System"
Author: Ruta Wheelock
Date: 12/06/2017

Description:

To run the program, execute:

Algorithm:

Example:

"""

import sys
import wptools
import re


def clean_text(list_text):
    for i, line in enumerate(list_text):
        # Remove non-Ascii characters
        list_text[i] = re.sub(r'[^\x00-\x7F]+','', line)
        # Remove tags
        list_text[i] = re.sub(r'<.*?>','', line)
        list_text[i] = re.sub(r'{.*?}','', line)
        list_text[i] = re.sub(r'[.*?]','', line)

    return list_text


def main():

    # If the user does not provide enough arguments, display message and exit with 1
    if (len(sys.argv) < 2 ):
        print "Please provide log file as a second command line argument."
        exit(1)

    # Open the log file
    log_file_name = str(sys.argv[1])
    log_file = open(log_file_name, 'w')

    print "\n*** This is a QA system by Ruta Wheelock."
    print " It will try to answer questions that start with Who, What, When or Where."
    print " Enter \"exit\" to close the program."

    # List of allowed question types
    allowed_questions = ['who', 'what', 'when', 'where']

    # Keep reading in questions and finding answers until user types 'exit'
    while True:
        question = raw_input("=?> ")
        if str(question) == "exit":
            break

        word_list = str(question).split()
        # Strip the question mark
        word_list[-1] = word_list[-1].strip('?')
        first_word = word_list[0].lower()
        
        # validate if the question starts with allowed keywords
        if first_word not in allowed_questions:
            print "=> The question has to start with Who, What, When or Where."
            continue
        

        # Processing Queations with is/was/are/were as a second word
        if word_list[1] in ['is', 'was', 'are', 'were']:        

            # Retrieve search term, remove determiner
            if word_list[2] in ['a', 'an', 'the']:
                subject = ' '.join(word_list[3:])
            else:
                subject = ' '.join(word_list[2:])

            verb1 = ''
            verb2 = ''
            
            if first_word == 'when':
                subject = ' '.join(subject.split()[:-1])
                verb1 = word_list[1]
                verb2 = word_list[-1]

                
            print subject
                
            try:
                page = wptools.page(subject, silent=True).get_query(show=False)
                extract = page.data['extract'].split('</p>')

                for i, paragraph in enumerate(extract):
                    # Remove non-Ascii characters
                    extract[i] = re.sub(r'[^\x00-\x7F]+','', paragraph)
                    # Remove html tags
                    extract[i] = re.sub(r'<.*?>','', paragraph)

                first_paragraph = extract[0]              
                whole_extract = ' '.join(extract)

                # Regular expressions
                Who_What_RE = re.compile(r'(?P<answer>\b(is|are|was|were)\b \b(a|an|the)\b .*?(?=[,.]\s))',
                                         re.IGNORECASE)
                Where_RE = re.compile(r'(?P<answer>\b(on|in|located)\b \b(the|a|an|in)\b .*?(?=[,.]\s))',
                                      re.IGNORECASE)
                When_RE = re.compile(r'{} {} (?P<answer>\b(on|in)\b .*?(?=[,.]\s))'.format(verb1, verb2),
                                     re.IGNORECASE)
                # Search for pattern /{born} on 10 January, 1200/ /{founded} 2 February 1999/
                When_RE_dd_Month_dddd = re.compile(r'(?P<answer>{} (\bon\b)?\s?\d\d? \b(\w+)\b[,.]? \d\d\d\d)'.format(verb2), re.IGNORECASE)

                # Search for patterns /{completed} in 2000/
                When_RE_dddd = re.compile(r'(?P<answer>{} (\bin\b) \d\d\d\d)'.format(verb2), re.IGNORECASE)

                
                reply = "=> Sorry, I can't aswer that."
                
                # Processing WHO and WHAT questions
                if first_word == 'who' or first_word == 'what':
                    findings = Who_What_RE.search(first_paragraph)
                    answer = findings.group('answer')
                    reply = "=> Answer: {0} {1}.".format(subject.title(), answer)

                # Processing WHERE questions
                elif first_word == 'where':
                    findings = Where_RE.search(first_paragraph)
                    answer = findings.group('answer')
                    reply = "=> Answer: {0} {1} {2}.".format(subject.title(), word_list[1], answer)

                # Processing WHEN questions
                else:

                    # Try dd_Month_ddd pattern first
                    findings = When_RE_dd_Month_dddd.search(whole_extract)
                    # If the previous pattern did not match, try dddd
                    if not findings:
                        findings = When_RE_dddd.search(whole_extract)
                        
                    answer = findings.group('answer')                     
                    reply = "=> Answer: {0} {1} {2}.".format(subject.title(), verb1, answer)

                    
                print reply
                    
            except (AttributeError, LookupError):
                print "=> Sorry, I can't answer that."
                continue


        # If the second word in the question is not is, are, was, were
        else:
            print "=> Sorry, I can't answer that."

    # Close the log file
    log_file.close()



if __name__ == "__main__":
    main()
