#! /usr/bin/env python

from Email import *
from Job import *
import subprocess
from os import listdir, walk
from os.path import isfile, join, getmtime
import re
import sys
from shutil import move
from collections import deque
import cPickle as pickle

PICKLE_PATH = "/opt/octoqueue/pickle/octoqueue.pickle"
QUEUE_PATH = "/data/GaussJobs/waiting_room"
INPUT_PATH = "/data/GaussJobs/inp"
OUTPUT_PATH = "/data/GaussJobs/out"

def isgaussianrunning():

    ps = subprocess.Popen("ps -eaf | grep g09", shell=True, stdout=subprocess.PIPE)
    output = ps.stdout.read()

    ps.stdout.close()
    ps.wait()

    rg = re.compile('(\\/)'+'(opt)'+'(\\/)'+'(g09)'+'(\\/)'+'(l)'+'(\\d+)'+'(\\.)'+'(exe)',
                    re.IGNORECASE | re.DOTALL)

    if not re.search(rg, output):
        return False
    else:
        return True

def generate_job(inp):
    # First convert to UNIX format
    ps = subprocess.Popen('dos2unix %s' %(QUEUE_PATH+inp), shell=True,stdout=subprocess.PIPE)
    ps.wait()

    inp_file = open(inp,'r')
    inp_file_info = inp_file.read().split('\n')[0]
    inp_file.close()


    # Initial comment in Gaussian input file looks like:
    # ! Name#E-mail
    info = inp_file_info.strip('!').strip(" ").split("#")

    return Job(uname=info[0], inp_name=inp, out_name=inp.split('.')[0]+".out", email=info[1])

def get_new_jobs(current_queue):

    dir_list = sorted(listdir(QUEUE_PATH), key=lambda x: getmtime(join(QUEUE_PATH, x)))
    new_queue = deque()

    if not dir_list:
        pass  # No files waiting to be run

    else:  # Now check each file in QUEUE_PATH to see if it's in the queue

        if current_queue:  # There's stuff in the queue to check

            for inp_file in dir_list:
                if inp_file in [f.inp_name for f in current_queue]:
                    continue
                else:
                    new_queue.append(generate_job(inp_file))

            new_queue = current_queue.extend(new_queue)

        else:  # Nothing in the queue, but stuff to add

            for inp_file in dir_list:
                new_queue.append(generate_job(inp_file))

    return new_queue


def main():

    # First check to see if pickled queue is available
    if isfile(PICKLE_PATH):
        current_queue = pickle.load(open(PICKLE_PATH, 'rb'))

        # Check to see if Gaussian is done with top job on queue
        if not isgaussianrunning():

            if current_queue:  # There's at least one item in the queue and it's done

                cur_job = current_queue.popleft()
                Email(dest=cur_job.email, job_json=cur_job.to_json(), status='end')

            else:  # Nothing in the queue, null
                pass

        else:  # Gaussian is still working
            sys.exit()

        # Now time to check if there's any new jobs to add to queue
        current_queue = get_new_jobs(current_queue)

    # Otherwise make a new queue
    else:
        current_queue = get_new_jobs(deque())

    if not current_queue:
        sys.exit() # Nothing to do

    else:  # Let's start the next process!
        cur_job = current_queue.popleft()
        current_queue.appendleft(cur_job)  # Put it back in

        input_path = join(INPUT_PATH, cur_job.inp_name)
        output_path = join(OUTPUT_PATH, cur_job.out_name)
        move(join(QUEUE_PATH, cur_job.inp_name), input_path)

        subprocess.Popen('g09 < %s > %s' %(input_path, output_path))
        Email(dest=cur_job.email, job_json=cur_job.to_json(), status='start')

    # Pickle the queue and quit
    pickle.dump(current_queue, open(PICKLE_PATH, 'wb'))
    sys.exit()

