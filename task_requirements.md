# Code Challenge

Please implement the challenge below with the technology of your choosing,

something you feel confident in and that is suiting for the objective.

 


 

## Web-Service

Develop a Web service with following functionality, in summary:
1. file upload
2. one random line
3. one random line backwards
4. 20 longest lines of one file
5. longest 100 lines

### file upload

Upload a text file and store it.
 

### one random line

Return one random line of a previously uploaded file via http as

`text/plain`, `application/json` or `application/xml` depending

on the request accept header. All three headers must be supported.

 

If the request is `application/*` please include following details in the

response:

 

* line number

* file name

* the letter which occurs most often in this line
 

### one random line backwards

Return the requested line backwards


### 20 longest lines of one file

Return the 20 longest lines of one file uploaded


### longest 100 lines

Return the 100 longest lines of all files uploaded
