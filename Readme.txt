For installation
1) Install Django in your system
2) During installation, you should have given a workspace path (something like C:/.../django/)
3) Extract the contents of the websearch.zip folder in a folder names websearch
4) Place the folder inside folder named django (or wherever the workspace path points)
5) Our entire backend  resides inside django/websearch/relfeedback/src
6) Our html code is at websearch/relfeedback/templates/relfeedback/index.html
7) Our Controller code is at websearch/relfeedback/views.py

To run the program
1) You will need to place all original files in django/websearch/relfeedback/src/originalFiles/
2) You need to open file parseHTML.py and update the path to point to originalFiles in your local directory(It points to mine)
3) Run the file (You can run this python file from PyCharm as well. No UI needed)
4) The parsedFiles will be generated in django/websearch/refeedback/src/parsedFiles
6) Create your local copy of mapping.txt file. This is only used for displaying files on UI. You can run mapping.py from PyCharm(Update paths in mapping.py)

7) Once the preprocessing is done, you can bring up the search engine. You can open the file stopliststemmer.py and check the last line for a function call to createIndex() method. Comment this method if you do not want index generation, uncomment it if you want to generate the index. 
Ideally this method only needs to run when we add new crawled files to the system.
8) Update all file paths in stopliststemmer.py to reflect paths in your system. you will need to update them in all the 3 methods
9) Similarly, update paths in file queryProcessing.py(they make use of mapping.txt and rev_mapping.txt from etc folder)
10) Check all files for updating the paths.

11) To run your web search engine, you need to navigate to websearch folder using command prompt
12) Type python manage.py runserver
13) In your browser you will need to type http://localhost:port/search
(default port is 8000)