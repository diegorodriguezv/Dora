import os
import subprocess


def check_ping_error(hostname):
    response = False
    FNULL = open(os.devnull, 'w')
    if os.name == "nt":
        response = subprocess.call(["ping", "-n", "1", hostname], stdout=FNULL)
    if os.name == "posix":
        response = subprocess.call(["ping", "-c", "1", hostname], stdout=FNULL)
    return response
