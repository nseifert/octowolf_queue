__author__ = 'nate'
import re

class Email(object):

    def decodeIt(self, input_json):
        # This function should process a json output from Job and turn it into an e-mail string
        pass

    def checkAddressValidity(self, addr):
        if not re.match("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", addr):
            return False
        else:
            return True

    def __init__(self, dest, job_json=None):

        if self.checkAddressValidity(dest):
            self.dest = dest
            print 'It worked!'
        else:
            self.dest = None
            raise ValueError('Not a valid e-mail address')

        self.job_data = self.decodeIt(job_json)
