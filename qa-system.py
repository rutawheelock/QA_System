#!/usr/bin/python

"""
CS 5761 PA 5 "Question Answering System"
Author: Ruta Wheelock
Date: 12/06/2017

Description:
This program answers simple Who, What, When and Where
factual questions using Wikipedia as a source.
A user can enter a question and the program
will generate and display an answer. 
In cases when the answer can't be found, the program 
will output "Sorry, I can't answer that."

To run the program, execute:
$./qa-system.py log_file.txt
The second argument is a name of a log file
where the program records user questions, performed queries,
and retrieved results.

To exit the program type 'exit' in a prompt.

Algorithm:
The program parses user input and determines a search term.
The search term is used to get a Wikipedia page.
For each question type regular expressions are used
to find a matching fragment in Wikipedia extract.
If a match is found, the search term is combined with
the match and displayed to the output.
If there is no match, the program will inform the user
that the question can't be answered.

Example:
% ./qa-system.py log_file.txt

*** This is a QA system by Ruta Wheelock.
 It will try to answer questions that start with Who, What, When or Where.
 Enter "exit" to close the program.
=?> What is gravity?
=> Answer: Gravity is a natural phenomenon by which all things with mass are brought toward (or gravitate toward) one another.
=?> Who was Tecumseh?
=> Answer: Tecumseh was a Native American Shawnee warrior and chief.
=?> When was Latvia established?
=> Answer: Latvia was established on 18 November 1918.
=?> Where is Taj Mahal?
=> Answer: Taj Mahal is on the south bank of the Yamuna river in the Indian city of Agra.
=?> When was the Great Fire of Rome?
=> Sorry, I can't answer that.
=?> exit
Have a great day!

"""

import sys
import wptools
import re
import unicodedata


def main():

    # If a user does not provide enough arguments, display message and exit with 1
    if (len(sys.argv) < 2 ):
        print "Please provide log file as a second command line argument."
        exit(1)

    # Open a log file
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
        log_file.write("\nQuestion: {}\n".format(question))
        if str(question) == "exit":
            break

        # Default answer if the lookup fails
        reply = "=> Sorry, I can't answer that."

        word_list = str(question).split()
        # Strip the question mark
        word_list[-1] = word_list[-1].strip('?')
        
        first_word = word_list[0].lower()
        # validate if the question starts with allowed keywords
        if first_word not in allowed_questions:
            reply = "=> The question has to start with Who, What, When or Where."
            print reply
            log_file.write("Reply:\n {}\n".format(reply))
            continue
        

        # Processing Questions with is/was/are/were as a second word
        if word_list[1] in ['is', 'was', 'are', 'were']:        

            # Retrieve search term, remove determiner.
            # Search term is the questions without first two words
            # and without determiner if it's a third word.
            if word_list[2] in ['a', 'an', 'the']:
                subject = ' '.join(word_list[3:])
            else:
                subject = ' '.join(word_list[2:])

            # For 'when' questions,
            # Save the second and the last word from the question.
            # 'When' questions are expected to be in form:
            # When {was/were} something {established/born etc.}?
            if first_word == 'when':
                subject = ' '.join(subject.split()[:-1])
                verb1 = word_list[1]
                verb2 = word_list[-1]

            log_file.write("Search term: {}\n".format(subject))
                
            try:
                # Retrieve Wikipedia page with the same title as the subject
                page = wptools.page(subject, silent=True).get_query(show=False)
                # Get the extract of Wikipedia page and split in paragraphs
                extract = page.data['extract'].split('</p>')

                # Clean up the extract text
                for i, paragraph in enumerate(extract):
                    # Convert unicode to a string
                    extract[i] = unicodedata.normalize('NFKD', paragraph).encode('ascii', 'ignore')
                    # Remove html tags
                    extract[i] = re.sub(r'<.*?>','', extract[i])

                first_paragraph = extract[0]              
                whole_extract = ' '.join(extract)
                log_file.write("Retrieved extract:\n{}\n".format(whole_extract))


                #----------------------------------
                # Processing WHO and WHAT questions
                
                if first_word == 'who' or first_word == 'what':
                    # Compile regular expression which looks for a pattern:
                    # (is|are|was|were) followed by (a|an|the) and everything after that
                    # until . or , is encountered.
                    Who_What_RE = re.compile(r'(?P<answer>\b(is|are|was|were)\b \b(a|an|the)\b .*?(?=[,.]\s))',
                                         re.IGNORECASE)
                    
                    log_file.write("Processing '{}' question:\n".format(first_word))
                    # Look for the pattern in the first paragraph of extract
                    findings = Who_What_RE.search(first_paragraph)
                    # Save the matched fragment of text
                    answer = findings.group('answer')
                    log_file.write("Retrieved answer: {}\n".format(answer))
                    # Create reply
                    reply = "=> Answer: {0} {1}.".format(subject.title(), answer)

                #---------------------------
                # Processing WHERE questions
                
                elif first_word == 'where':
                    # Compile regular expression which looks for a pattern:
                    # (on|in|located) followed by (the|a|an|in) and everything after that
                    # until . or , is encountered.
                    # Example matches: /located in Duluth/, /in a city of Duluth/
                    Where_RE = re.compile(r'(?P<answer>\b(on|in|located)\b \b(the|a|an|in)\b .*?(?=[,.]\s))',
                                      re.IGNORECASE)
                    log_file.write("Processing '{}' question:\n".format(first_word))
                    findings = Where_RE.search(first_paragraph)
                    answer = findings.group('answer')
                    log_file.write("Retrieved answer: {}\n".format(answer))
                    reply = "=> Answer: {0} {1} {2}.".format(subject.title(), word_list[1], answer)

                #--------------------------
                # Processing WHEN questions
                else:
                    # Compile regular expressions that look for patterns:

                    # (verb2) optional (on) followed by two digits, a word, optional (, or .) followed by four digits
                    # Example matches: /born 10 January 1200/ /founded on 2 February, 1999/
                    When_RE_dd_Month_dddd = re.compile(r'(?P<answer>{} (\bon\b)?\s?\d\d? \b(\w+)\b[,.]? \d\d\d\d)'.format(verb2), re.IGNORECASE)

                    # (verb2) followed by (in) and four digits
                    # Example match: /completed in 2000/
                    When_RE_dddd = re.compile(r'(?P<answer>{} (\bin\b) \d\d\d\d)'.format(verb2), re.IGNORECASE)

                    log_file.write("Processing 'when' question:\n")

                    # Look for the pattern in the extract
                    # Try dd_Month_ddd pattern first
                    findings = When_RE_dd_Month_dddd.search(whole_extract)
                    # If the previous pattern did not match, try dddd
                    if not findings:
                        findings = When_RE_dddd.search(whole_extract)
                        
                    answer = findings.group('answer')
                    log_file.write("Retrieved answer: {}\n".format(answer))
                    reply = "=> Answer: {0} {1} {2}.".format(subject.title(), verb1, answer)

                    
                print reply
                log_file.write("Reply: \n{}\n".format(reply))

            # If the Wikipedia lookup fails or nothing matches,
            # print default reply
            except (AttributeError, LookupError):
                print reply
                log_file.write("Reply: \n{}\n".format(reply))
                continue


        # If the second word in the question is not is, are, was, were
        # print default reply
        else:
            print reply
            log_file.write("Reply: \n{}\n".format(reply))


    print "Have a great day!"
    # Close the log file
    log_file.close()



if __name__ == "__main__":
    main()
