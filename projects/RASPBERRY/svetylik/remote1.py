import subprocess

p = subprocess.Popen('irw', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
while (True):
    line = p.stdout.readline()
    if "KEY_RIGHT" in line:
        print(line)
