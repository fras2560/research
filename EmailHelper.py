"""
-------------------------------------------------------
[program name]
[program description]
-------------------------------------------------------
Author:  Dallas Fraser
ID:      110242560
Email:   fras2560@mylaurier.ca
Version: 2014-11-11
-------------------------------------------------------
"""
import smtplib
from config import PASSWORD, USER
def send_email(message, to):
    fromaddr = USER
    toaddrs  = [to]
    username = USER
    password = PASSWORD
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(username,password)
    server.sendmail(fromaddr, toaddrs, message)
    server.quit()

import unittest
class Tester(unittest.TestCase):
    def setUp(self):
        #called when starting test
        pass

    def tearDown(self):
        #called when done test
        pass

    def testSendEmail(self):
        send_email("Hey Test", "dallas.j.fraser.laurier@gmail.com")
