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
        

        # Processing WHO and WHAT questions
        if first_word == 'who' or first_word == 'what':

            # Question is of type: 'Who/what is/was somebody/something?'
            if word_list[1] == 'is' or word_list[1] == 'was':        
                subject = ' '.join(word_list[2:])

                try:
                    page = wptools.page(subject).get_query(show=False)
                    answer = page.data['description']
                    reply = "=> Answer: {0} {1} {2}.".format(subject, word_list[1], answer)
                    print reply
                except LookupError:
                    print "Sorry, I can't answer that."
                    continue

                try:
                    page = wptools.page(subject).get_query(show=False)
                    extract = page.data['extract'].split('</p>')

                    findAnswerRE = re.compile(r'.*(?P<answer>\b(is|are|was|were)\b \b(a|an|the)\b (\w+\s*)+)[,.].*', re.IGNORECASE)
                    findings = findAnswerRE.match(extract[0])
                    answer = findings.group('answer')
                    reply = "=> Answer: {0} {1}.".format(subject, answer)
                    print reply
                    
                except LookupError, AttributeError:
                    print "Sorry, I can't answer that."
                    continue

    # Close the log file
    log_file.close()



if __name__ == "__main__":
    main()
