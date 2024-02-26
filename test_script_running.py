import psutil
import os

def is_running(script):
    for q in psutil.process_iter():
        print(f'psutil.process_iter(): {q}')
        if q.name().startswith('python'):
            if len(q.cmdline())>1 and script in q.cmdline()[1] and q.pid !=os.getpid():
                print("'{}' Process is already running".format(script))
                return True

    return False


if not is_running("scripts/fetch.py"):
    n = input("What is Your Name? ")
    print ("Hello " + n)