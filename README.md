# Question Answering System
Developed as an assignment for University of Minnesota Duluth course Intro to Natural Language Processing.  
Author: Ruta Wheelock  
Date: 12/06/2017  

## Description
This program answers simple Who, What, When and Where
factual questions using Wikipedia as a source.  
A user can enter a question and the program
will generate and display an answer.  
In cases when the answer can't be found, the program 
will output "Sorry, I can't answer that."  
To run the program, execute:
```
$./qa-system.py log_file.txt
```
The second argument is a name of a log file
where the program records user questions, performed queries,
and retrieved results.  
To exit the program type '**exit**' in a prompt.

## Algorithm
The program parses user input and determines a search term.
The search term is used to get a Wikipedia page.
For each question type regular expressions are used
to find a matching fragment in Wikipedia extract.
If a match is found, the search term is combined with
the match and displayed to the output.
If there is no match, the program will inform the user
that the question can't be answered.

## Example
```
% ./qa-system.py log_file.txt
*** This is a QA system by Ruta Wheelock.
 It will try to answer questions that start with Who, What, When or Where.
 Enter "exit" to close the program.
=?> What is gravity?
=> Answer: Gravity is a natural phenomenon by which all things with mass are  brought toward (or gravitate toward) one another.
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
```
