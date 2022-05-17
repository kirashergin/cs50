# Messenger
#### Video Demo: https://youtu.be/VapKagkLRgM
#### Description:
Simple messenger with minimalistic design

My project is build by MVC architectular pattern.
I used all my gained knowledge to develop my own messenger.
The basic framework that I used is flask. In project's folder you can find:

-templates folder which contains all HTML files of my project. That's login.html (a page with simple form for singing in), regisrer.html(also a form with 3 inputs (email, password, confirmation)), index.html(main page where you can write and see all the messages. It's implemeted with a lot of JavaScript and Jinja), contacts.html(page where you can add, delete friends. Implementation details were taken from week 9 lecture (search using JSON and JavaScript)) and profile.html(If you want you can add or change some information about yourself) All JavaScript code is also included there (inside HTML files using script tag).

-app.py is a file written using flask. That's my backend server which handles user requests. I took 9 week problem set as a foundation to set up flask.

-messanger.db is a database which contains 3 tables: users (contains all information about users. There are some fields that are mandatory for filling out and some which can be filled out later, after signing up), friends (the table where all contact lists are stored by 2 foreign keys), messages (here all messages, receivers, senders, timestaps are stored).

-static folder where my css code is stored. Inside this folder you can also find static folder. All the pictures are situated there.

The majority of web pages are dinamically generated. It's implemented by jinja syntax as well as JavaScript.
For some buttons I used fetch function which allowed to send data without having page reloaded. All data received from server is in JSON format which is really convenient and uses less space.
I faced some problems during development. The main of them is to see new received messages page has to be reloaded. However, if I do so dialogue which was opened closes and I need to open it again which is not so userfriendly. Hope to fix that later
My messanger uses server stored cookies.
The majority of web pages styling is made by Bootstrap 5.1. I've found it more convenient than using only css.
I realized that it's not a good idea to combine JavaScript with Jinja because it's difficult to make this code work together properly.
During project development I also learned Git and GitHub which really helped me when I accidentally deleted all the files of my project.
Week 10 lectures helped me getting used to using VScode locally on my own machine. I used WSL extension to be able to use Linux commands.
Anyway, I still needed some help with flask configuration. That's really hard to make heads or tails of it. Hope all this nuances will be covered in CS50 Web Programming with Python and JavaScript course

Thank you, CS50 team!