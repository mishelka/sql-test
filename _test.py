import os
import re
import subprocess
import psycopg2

path = os.path.join('.', 'files')
os.chdir(path)


def cleandb():
    # FNULL = open(os.devnull, 'w')  # use this if you want to suppress output to stdout from the subprocess
    # subprocess.call('cleandb.bat', shell=False, stdout=FNULL, stderr=FNULL)
    subprocess.call(['sh', 'cleandb.sh'], shell=True)#, stdout=FNULL, stderr=FNULL)
    print('Cleaning database successful...')


def readsqlscript(filepath, file):

    print('reading: {}'.format(filepath))

    with open(file, 'r', encoding='utf8') as f:
        filelines = (line.strip() for line in f)  # All lines including the blank ones
        filelines = list(line for line in filelines if line)  # Non-blank lines

        for i in range(0, len(filelines)):
            line = filelines[i]
            if line.startswith('--'):
                m = re.match(r'--\s*(\d+)[^\n]*', line)
                if m:
                    filelines[i] = int(m.group(1))
                else:
                    filelines[i] = ''

        filelines = list(line for line in filelines if line)  # Non-blank lines
        tasks = {}
        linenum = -1
        currenttask = ''

        for l in filelines:
            if isinstance(l, int):
                if linenum != -1:
                    t = currenttask.strip()
                    if t: tasks[linenum] = t
                linenum = l
                currenttask = ''
                continue
            currenttask = currenttask + ' ' + l

        # store the last task
        t = currenttask.strip()
        if t: tasks[linenum] = t

        f.close()
        return tasks


def printtasks(tasks):
    print('solved tasks: ', len(tasks))
    for key, value in tasks.items():
        print(key, '. ', value)


def dbconn():
    conn = psycopg2.connect(
        host='localhost',
        dbname='obce',
        user='postgres',
        password='postgres',
        port=5432
    )


print('Cleaning database...')
# cleandb()

print('Parsing results...')
results = {}

for file in os.listdir():
    if file.endswith('.sql'):
        filepath = os.path.join(path, file)
        tasks = readsqlscript(filepath, file)
        title = file.replace('.sql', '')
        results[title] = tasks
        # printtasks(tasks)

# print(results)

print('Connecting to database')
dbconn()

print('Running tests')
for r in results:
    break