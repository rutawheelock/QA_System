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

# Helper functions

# Check if the question starts with Who, What, When or Where
def valid_input(some_input):
    word_list = str(some_input).lower().split()
    allowed_questions = ['who', 'what', 'when', 'where']
    
    if word_list[0] in allowed_questions:
        return True
    else:
        return False



def main():

    # If the user does not provide enough arguments, display message and exit with 1
    if (len(sys.argv) < 2 ):
        print "Please provide log file as a second command line argument."
        exit(1)

    # Save the log file name
    log_file = str(sys.argv[1])
    print "Log file name: %s" % log_file


    print "\n*** This is a QA system by Ruta Wheelock."
    print " It will try to answer questions that start with Who, What, When or Where."
    print " Enter \"exit\" to close the program."

    while True:
        question = raw_input("=?> ")
        if str(question) == "exit":
            break

        if not valid_input(question):
            print "=> The question has to start with Who, What, When or Where"
        else:
            word_list = str(question).lower().split()

            print word_list
            #Strip the question mark
            subject = " ".join(word_list[2:])
            print subject
            pages = wptools.page(subject)
            print pages.get()




if __name__ == "__main__":
    main()
