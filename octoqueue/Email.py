__author__ = 'nate'
import re
import json
import time

import smtplib
import email.MIMEMultipart
import email.MIMEText

from random import choice
import subprocess

class Email(object):



    @staticmethod
    def prettifyit(input_json):

        json_dict = json.loads(input_json)

        out = "%20s\t%s\r\n%20s\t%20s\r\n%20s\t%20s\r\n%20s\t%20s\r\n" \
              "%20s\t%20s" %('Username:', json_dict['uname'], 'E-mail:', json_dict['email'],
                             'Input File Name:', json_dict['inp_name'],
                             'Output File Name:', json_dict['out_name'],
                             'Time Started:', json_dict['initial_time'])
        return out


    def send(self, status='start'):

        # --------------- Create message ------------------

        msg = email.MIMEMultipart.MIMEMultipart()
        current_time = time.strftime('%a, %d %b %Y %H:%M:%S', time.localtime())
        msg['From'] = self.EMAIL_DAEMON_ADDR
        msg['To'] = ','.join([self.dest])
        msg['Subject'] = 'octowolf Gaussian Job Update'

        if status == 'start':
            msg['Subject'] += '-- init'

        if status == 'end':
            msg['Subject'] += '-- finish'

        body = 'Hello! This is an automated message from the Octowolf mail daemon, sent at %s. \n\n' \
                %current_time

        if status == 'start':
            body += 'This message is to inform you that your Gaussian 09 job has been initialized. Below is the' \
                    ' relevant information regarding your job:\n\n'
        if status == 'end':
            body += 'This message is to inform you that your Gaussian 09 job has been completed. Below is the' \
                    ' relevant information regarding your job:\n\n'

        body += self.content

        if status == 'end':
            body += "\n%20s\t%20s\n" %('Time Ended:',current_time)

        list_o_cows = "apt bud-frogs bunny calvin cheese cock cower daemon default dragon " \
            "dragon-and-cow duck elephant" \
            "elephant-in-snake eyes flaming-sheep ghostbusters gnu " \
            "head-in hellokitty kiss kitty koala kosh luke-koala mech-and-cow meow milk moofasa moose " \
            "mutilated pony pony-smaller ren sheep skeleton snowman stegosaurus stimpy suse " \
            "three-eyes turkey turtle tux unipony unipony-smaller vader vader-koala".split()

        cmd = 'cowsay -f %s \"Thanks for using Octowolf!\"' % choice(list_o_cows)
        goodbye_cow = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True).communicate()[0]

        body += '\n\n %s' % goodbye_cow


        msg.attach(email.MIMEText.MIMEText(body))

        # NEW FEATURE TO ADD HERE:
        # Add attachment of Gaussian input/output file?!!?! Is possible! See:
        # http://www.jayrambhia.com/blog/send-emails-using-python/

        # ------------- Initialize SMTP server handshake ---------------

        server = smtplib.SMTP()
        server.connect('smtp.gmail.com', port=587)
        server.ehlo()
        server.starttls()
        server.login(self.EMAIL_DAEMON_ADDR, self.EMAIL_DAEMON_PASS)

        # ------------ Send e-mail -----------------------

        server.sendmail(self.EMAIL_DAEMON_ADDR, [self.dest], msg.as_string())
        server.quit()


    @staticmethod
    def checkaddressvalidity(addr):
        if not re.match("(^[a-zA-Z0-9_.+-]+@[a-z A-Z0-9-]+\.[a-zA-Z0-9-.]+$)", addr):
            return False
        else:
            return True

    def __init__(self, dest, job_json=None, status='start'):

        self.EMAIL_DAEMON_ADDR = 'octowolf.daemon@gmail.com'
        self.EMAIL_DAEMON_PASS = 'secret'

        if self.checkaddressvalidity(dest):
            self.dest = dest
        else:
            self.dest = None
            raise ValueError('Not a valid e-mail address')

        self.content = self.prettifyit(job_json)

        if status == 'start':
            self.send()
        if status == 'end':
            self.send(status='end')

