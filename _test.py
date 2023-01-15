import os
import re
import subprocess
import psycopg2

path = os.path.join('.', 'files')
os.chdir(path)


def cleandb():
    # FNULL = open(os.devnull, 'w')  # use this if you want to suppress output to stdout from the subprocess
    # subprocess.call('cleandb.bat', shell=False, stdout=FNULL, stderr=FNULL)
    subprocess.call(['sh', 'cleandb.sh'], check=True, capture_output=True)
    print('Cleaning database successful...')


def readsqlscript(_filepath, _file):
    print('\treading: {}'.format(_filepath))

    with open(_file, 'r', encoding='utf8') as f:
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
        _tasks = {}
        linenum = -1
        currenttask = ''

        for l in filelines:
            if isinstance(l, int):
                if linenum != -1:
                    t = currenttask.strip()
                    if t:
                        if linenum == 20:
                            _tasks[1.1] = t
                        elif linenum == 1:
                            _tasks[1.2] = t
                        else:
                            _tasks[linenum] = t
                linenum = l
                currenttask = ''
                continue
            currenttask = currenttask + ' ' + l

        # store the last task
        t = currenttask.strip()
        if t: _tasks[linenum] = t

        f.close()
        _tasks = dict(sorted(_tasks.items()))
        return _tasks


def printtasks(_tasks):
    print('solved tasks: ', len(_tasks))
    for key, value in _tasks.items():
        print(key, '. ', value)


def dbconn():
    _conn = psycopg2.connect(
        host='localhost',
        dbname='obce',
        user='starosta',
        password='p4ssw0rd',
        port=5432
    )
    return _conn


def checktask(_task, dbcursor):
    record = ''
    if _task == 1.1:
        # 1a kolko je takych obci
        # vysledok je 100
        record = dbcursor.fetchone()
        print('\t record one: ', record)
        if record[0] == 100: return 3
        record = dbcursor.fetchall()
        print('\t record all length: ', len(record))
        if len(record) == 100: return 2
    elif _task == 1.2:
        # 1b ktorý názov obce je použitý najviac.
        # Odpoveď: Porubka, Lucka (4)
        record = dbcursor.fetchall()
        print('\t record all length: ', len(record))
        por, luc = False, False
        for c in record:
            if c == 'Porubka': por = True
            if c == 'Lucka': luc = True
        if len(record) == 2 and por and luc: return 3
        if (por and not luc) or (not por and luc): return 2
        if len(record) > 2 or (not luc and not por): return 0
    elif _task == 2:
        # Koľko okresov sa nachádza v košickom kraji?
        # Odpoveď: 11
        record = dbcursor.fetchone()
        print('\t record one: ', record)
        if record[0] == 11: return 3
        record = dbcursor.fetchall()
        print('\t record all length: ', len(record))
        if len(record) == 11: return 2
    elif _task== 3:
        # A koľko má košický kraj obcí? Pri tvorbe dopytu vám môže pomôcť informácia, že Trenčiansky kraj má spolu 276 obcí.
        # Odpoveď: 461
        record = dbcursor.fetchone()
        if record[0] == 461: return 3
        print('\t record one: ', record)
        record = dbcursor.fetchall()
        if len(record) == 461: return 2
        print('\t record all length: ', len(record))
    elif _task == 4:
        # Zistite, ktorá obec (mesto) bola na Slovensku najväčšia v roku 2012.
        # Pri tvorbe dopytu vám môže pomôcť informácia, že táto obec (mesto) bola najväčšia na Slovensku v rokoch 2009-2012,
        # avšak má v populácii klesajúcu tendenciu. Vo výsledku vypíšte jej názov a počet obyvateľov.
        # Odpoveď: Bratislava - Petržalka, 105468
        record = dbcursor.fetchone()
        print('\t record one: ', record)
        ba = False
        num = False
        for c in record:
            if c == 'Bratislava - Petržalka':
                ba = True
            if c == 105468:
                num = True
        if ba & num: return 3
        if ba: return 1.5
        if num: return 1.5
    elif _task == 5:
        # Koľko obyvateľov mal okres Sabinov v roku 2012? Pri tvorbe dopytu vám môže pomôcť informácia, že okres Dolný Kubín mal v roku 2010 39553 obyvateľov.
        # Odpoveď: 58450
        record = dbcursor.fetchone()
        print('\t record one: ', record)
        for r in record:
            if record[r] == 58450: return 3
    elif _task == 6:
        # Ako sme na tom na Slovensku? Vymierame alebo rastieme?
        # Zobrazte trend vývoja populácie za jednotlivé roky a výsledok zobrazte od najnovších informácií po najstaršie.
        # ?
        # record = dbcursor.fetchall()
        print('\t record all: ', record)
        print('\t>>>>>>task 6 does not have a test yet')
    elif _task == 7:
        # Zistite, ktorá obec bola najmenšia v okrese Tvrdošín v roku 2011.
        # Pri tvorbe dopytu vám môže pomôcť informácia,
        # že v okrese Ružomberok to bola v roku 2012 obec
        # Potok s počtom obyvateľov 107.
        # Odpoveď: Štefanov nad Oravou a Čimhová (659)
        record = dbcursor.fetchall()
        print('\t record all length: ', len(record))
        stefanov = False
        cimhova = False
        num = False
        if len(record) == 2:
            for r in record:
                for c in r:
                    if c == 'Štefanov nad Oravou':
                        stefanov = True
                    if c == 'Čimhová':
                        cimhova = True
                    if c == 659:
                        num = True
            if cimhova & stefanov & num: return 3
            if stefanov or cimhova or num: return 1.5
        return 0
    elif _task == 8:
        # Zistite všetky obce, ktoré mali v roku 2010 počet obyvateľov do 5000.
        # Pri tvorbe dopytu vám môže pomôcť informácia, že v roku 2009 bolo týchto obcí o
        # 1 viac ako v roku 2009.
        # Odpoveď: obcí je spolu 2774
        record = dbcursor.fetchall()
        print('\t record all length', len(record))
        if len(record) == 2774: return 3
    elif _task == 9:
        # Zistite 10 obcí s populáciou nad 20000, ktoré mali v roku 2012 najväčší pomer žien voči mužom (viac žien v obci ako mužov). Týchto 10 obcí vypíšte v poradí od najväčšieho pomeru po najmenší. Vo výsledku okrem názvu obce vypíšte aj pomer zaokrúhlený na 4 desatinné miesta. Pri tvorbe dopytu vám môže pomôcť informácia,
        # že v roku 2011 bol tento pomer pre obec Košice  - Juh 1,1673.
        record = dbcursor.fetchall()
        print('\t record all length: ', len(record))
        if len(record) != 10: return 0
    elif _task == 10:
        # Vypíšte sumárne informácie o stave Slovenska v roku 2012 v podobe tabuľky, ktorá bude obsahovať
        # pre každý kraj informácie o počte obyvateľov, o počte obcí a počte okresov.
        # ?
        record = dbcursor.fetchall()
        print('\t record all (test visually I guess): ', record)
        print(record)
    elif _task == 11:
        # To, že či vymierame alebo rastieme, sme už zisťovali.
        # Ale ktoré obce sú na tom naozaj zle?
        # Kde by sa nad touto otázkou mali naozaj zamyslieť?
        # Zobrazte obce, ktoré majú klesajúci trend (rozdiel v populácii dvoch
        # posledných rokov je menší ako 0) - vypíšte ich názov, počet obyvateľov
        # v poslednom roku, počet obyvateľov v predchádzajúcom roku a rozdiel
        # v populácii posledného oproti predchádzajúcemu roku. Zoznam utrieďte
        # vzostupne podľa tohto rozdielu od obcí s najmenším prírastkom obyvateľov
        # po najväčší.
        # Odpoveď: obcí je 1307
        record = dbcursor.fetchall()
        print('\t record all length: ', len(record))
        if len(record) == 1307: return 3
    elif _task == 12:
        # Zistite počet obcí, ktorých počet obyvateľov v roku 2012 je nižší,
        # ako bol slovenský priemer v danom roku.
        # Odpoveď: obcí je 2433
        record = dbcursor.fetchone()
        print('\t record one: ', record)
        if record[0] == 2433: return 3
        record = dbcursor.fetchall()
        print('\t record all length: ', len(record))
        if len(record) == 2433: return 2
    else:
        print('!!!UNKNOWN TASK')
    print('\t\t\t>>>> ', record)
    return 0


# print('Cleaning database...')
# cleandb()

print('Parsing results...')
results = {}

for file in sorted(os.listdir()):
    if file.endswith('.sql'):
        filepath = os.path.join(path, file)
        tasks = readsqlscript(filepath, file)
        title = file.replace('.sql', '')
        results[title] = tasks
        # printtasks(tasks)

# print(results)

print('Connecting to database')
conn = dbconn()
cur = conn.cursor()
print('\tConnected to db obce')

print('Running tests')
for result in results:
    print('#########', result, '#########')
    for task in results[result]:
        if conn is None:
            conn = dbconn()
            cur = conn.cursor()
        try:
            print('\t>>>> Task ', task)
            cur.execute(results[result][task])
            res = checktask(task, cur)
            if res == 0:
                print('\t<<<<< FAIL')
            else:
                print('\t<<<<<', task, 'SUCCESS (', str(res) + 'b', ')')
        except Exception as error:
            print('\t<<<<<', task, 'ERROR EXECUTING', error)
            cur.close()
            conn.close()
            conn = None

cur.close()
conn.close()
