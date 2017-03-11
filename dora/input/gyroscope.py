import subprocess
import threading

stdout_result = 1
quat = [0 ** 4]
lock = threading.Lock()

def parse_line(line):
    words = line.split()
    if len(words) == 5:
        if words[0] == "quat":
            # Discard invalid data like:
            # -0.141235 -0.141235 -0.141235 -0.141235
            # 1.812500 0.000000 0.000000 0.011719
            if words[1] == words[2] == words[3] == words[4]:
                return
            if words[1] == 0 or words[2] == 0 or words[3] == 0 or words[4] == 0:
                return
            with lock:
                quat = [words[0], words[1], words[2], words[3]]


def stdout_thread(pipe):
    global stdout_result
    while True:
        out = pipe.stdout.readline()
        parse_line(out)
        stdout_result = pipe.poll()
        if out == '' and stdout_result is not None:
            break


def exec_command(command, cwd=None):
    if cwd is not None:
        print '[' + ' '.join(command) + '] in ' + cwd
    else:
        print '[' + ' '.join(command) + ']'
    p = subprocess.Popen(
        command, stdout=subprocess.PIPE, cwd=cwd
    )
    out_thread = threading.Thread(name='stdout_thread', target=stdout_thread, args=(p,))
    out_thread.start()
    out_thread.join()
    return stdout_result


class Gyroscope(object):

    alive = True

    def __init__(self):
        exec_command("demo_dmp", "../util")

    @property
    def quat(self):
        with self.lock:
            return quat
