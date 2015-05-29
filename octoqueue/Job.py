__author__ = 'nate'
import time
from random import choice
import json

class Job(object):

    # Potential variables needed for Job:
    # 1) Username
    # 2) Gaussian input file name / path
    # 3) Gaussian output file name / path
    # 4) Time & Date for input file submission
    # 5) E-mail address

    DEFAULT_IN_PATH = '/data/GaussJobs/inp/'
    DEFAULT_OUT_PATH = '/data/GaussJobs/out/'

    noun_list = ['Wolf', 'Johnson', 'Rabi', 'Peter', 'SteelBeams', 'Frog', 'Zombie', 'Insomniac', 'Jackrabbit',
                 'Mario', 'Luigi','Cabbage','Sashimi','Dongle','Pitbull','JustinBieber']
    adjec_list = ['Mad', 'Inquisitive', 'Big', 'Melted', 'Stylish', 'Scientific', 'Bored', 'Terrifying', 'Adiabatic',
                  'Coherent', 'Incoherent', 'Stimulated', 'Perturbative', 'Classy','Symmetric','Quantum','Classical']
    gerund_list = ['Dancing', 'Sleeping', 'Laughing', 'Stinking', 'Loving', 'Running', 'Dying', 'Fermenting', 'Cooking',
                   'Calculating', 'Partying', 'Celebrating', 'Crying']

    def genInpName(self):
        timestamp = str(time.time()).replace('.','_')
        return choice(self.adjec_list)+choice(self.gerund_list)+choice(self.noun_list)+'_'+timestamp+'.inp'

    def genOutName(self, inp_name):
        return inp_name.split('.')[0]+'.out'

    def __str__(self):
        return "Username:       %s \n" \
        "E-mail:         %s \n" \
        "Input File:     %s \n" \
        "Output File:    %s \n" \
        "Time Started:   %s \n" %(self.uname,self.email,self.inp_name,self.out_name, self.epoch_time)

    def to_json(self):
        return json.dumps(self.__dict__)

    def __init__(self, uname=None, inp_name=None, out_name=None, email=None, in_path=None, out_path=None,
                 **kwargs):

        self.uname = uname if uname is not None and isinstance(uname,basestring)\
            else 'defaultUser'

        self.inp_name = inp_name if inp_name is not None and isinstance(inp_name,basestring)\
            else self.genInpName()

        self.out_name = out_name if out_name is not None and isinstance(out_name,basestring)\
            else self.genOutName(self.inp_name)

        self.email = email if email is not None and isinstance(email,basestring)\
            else 'noAddress@ayylmao.ca'

        self.in_path = in_path if in_path is not None and isinstance(in_path,basestring)\
            else self.DEFAULT_IN_PATH

        self.out_path = out_path if out_path is not None and isinstance(out_path,basestring)\
            else self.DEFAULT_OUT_PATH

        self.epoch_time = str(time.strftime('%l:%M%p %Z on %b %d, %Y'))
