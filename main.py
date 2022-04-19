import threading
from queue import Queue
import time
import socket
import requests
import subprocess
import re 


print_lock = threading.Lock()

results = []
pattern =r"[a-zA-Z]+:([a-zA-Z]+(\.[a-zA-Z]+)+)"

target = []

def gethosts():
    f = open("urls.txt","r")
    for line in f.readlines():
        target.append(line.strip())
    f.close()

gethosts()

def portscan(url):
    process = subprocess.run("echo | timeout 3 openssl s_client -connect {}:443 | openssl x509 -noout -text | grep DNS".format(url),shell=True,capture_output=True)
    stdout_as_str = process.stdout.decode("utf-8")
    search_results = re.findall(pattern,stdout_as_str)

    for i in search_results:
        if i[0] == "sni.cloudflaressl.com":
            print("{}:{}".format(url,i[0]))

# The threader thread pulls an worker from the queue and processes it
def threader():
    while True:
        # gets an worker from the queue
        worker = q.get()

        # Run the example job with the avail worker in queue (thread)
        portscan(worker)

        # completed with the job
        q.task_done()



        

# Create the queue and threader 
q = Queue()

# how many threads are we going to allow for
for x in range(100):
     t = threading.Thread(target=threader)

     # classifying as a daemon, so they will die when the main dies
     t.daemon = True

     # begins, must come after daemon definition
     t.start()


start = time.time()

# 100 jobs assigned.
for worker in target:
    q.put(worker)

# wait until the thread terminates.
q.join()
