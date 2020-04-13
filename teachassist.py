from bs4 import BeautifulSoup
from datetime import date
import requests                     #imports
import smtplib, ssl

receiver_email = ''#receiver email
sender_email = ''#sender sender_email
password = ''#password of email you want to end
message = """\
Subject: Hi there

Enter your message here.

This message is sent from python. Hi!"""
port = 465  # For SSL


#a, c, e  OR b, d, f
a = ''#'put username here'
b = ''#'optional other username'
c = ''#'password1'
d = ''#'password2'
e = 'https://ta.yrdsb.ca/live/students/listReports.php?student_id='#id link here
f = 'https://ta.yrdsb.ca/live/students/listReports.php?student_id='#id link here
USERNAME = a
PASSWORD = c
login_url = 'https://ta.yrdsb.ca/yrdsb/index.php'
url = e

session_requests = requests.session()   #requests a session


payload = {'username': USERNAME, 'password': PASSWORD, }      #sets up the payload

result = session_requests.post(login_url, data = payload, headers = dict(referer=login_url))     #actually getting the data

result = session_requests.get(url, headers=dict(referer=url))
content = BeautifulSoup(result.content, 'html.parser')      #using BeautifulSoup to get the html

#print(content)

cols = []
marks = []            #variables
counter1 = 0

divs = content.find_all('div')
divs = divs[3]
tables = divs.find('table')        #getting elements of the html
rows = tables.find_all('tr')

for row in rows:
    cols.append(row.find_all('td'))

cols.pop(0) #empty first column

# for x in range(len(cols)):
#      print(cols[x])
#      print ('\n')

marks = []
for x in range (len(cols)):
    if 'current mark' in str(cols[x]):
        string = str(cols[x]);
        index = string.find('current mark')
        #print(index)
        #print(len(string))
        #print(string[index+15])
        marks.append(float(string[index+15:len(string)-12]))          #actually getting the mark here : have to parse it manually since there are many numbers in the html
    else:
        marks.append(float('0')) #storing everything as a float in the marks and oldMarks lists

# for x in range (len(marks)):
#     print(marks[x])

#------------------------------part where we read and write to file

today = date.today()
date = today.strftime("%b-%d-%Y")       #date
f1 = 'myMarks.txt'
f2 = 'myMarks2.txt'                  #creating two files; one for each account
old = []
if USERNAME == a:
    file = open(f1, 'r')
    content = file.readlines()
else:
    file = open(f2, 'r')
    content = file.readlines()

for x in range(len(marks)):
    old.append(content[len(content)-(x+1)])

old.reverse()
# for x in range(len(old)):
#     print(old[x])
oldMarks = []
for x in range(len(old)):
    string = old[x]
    index = string.find(':')
    oldMarks.append(string[index+3:])
    oldMarks[x] = float(oldMarks[x].rstrip())

# for x in range(len(oldMarks)):
#     print(oldMarks[x])

changed = False
for x in range(len(marks)):
    if marks[x] != oldMarks[x]:           #seeing if the marks have changed
        changed = True

if changed:            #if the marks have changed

    print('Changed!')
    if USERNAME == a:
        file = open('myMarks.txt', 'a+')
    else:   #for alternate account
        file = open('myMarks2.txt', 'a+')
        #print('2')
    file.write('\n')
    file.write(date+'\n')                   #writing to a file
    for x in range (len(marks)):
        file.write('Class ' + str(x+1) + ':  ' + str(marks[x]))
        file.write('\n')
    message = " change message here to the mark if you want to!"


    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:    #part that actually sends the email
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)


else:
    print('Not Changed')  #not changed



file.close()       #finished writing to the file
