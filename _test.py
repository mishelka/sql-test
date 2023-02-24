import os
import re
import subprocess
import psycopg2
import sys

from _decimal import Decimal


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


path = os.path.join('.', 'files')
os.chdir(path)

task7results = {2012: 5410836, 2011: 5404322, 2010: 5435273, 2009: 5424925}
task10results = {
            'Bratislava - Ruzinov': 1.2103,
            'Bratislava - Nove Mesto': 1.1989,
            'Kosice - Juh': 1.163,
            'Bratislava - Dubravka': 1.1628,
            'Bratislava - Karlova Ves': 1.152,
            'Kosice - Stare Mesto': 1.1437,
            'Lucenec': 1.1432,
            'Kosice - Sever': 1.1343,
            'Bratislava - Podunajske Biskupice': 1.1301,
            'Piestany': 1.1269
        }
task11names = ['Banskobystricky kraj', 'Bratislavsky kraj', 'Kosicky kraj', 'Nitriansky kraj', 'Presovsky kraj', 'Trenciansky kraj', 'Trnavsky kraj', 'Zilinsky kraj']
task11population = [658490, 612682, 794025, 688400, 817382, 593159, 556577, 690121]
task11cities = [516, 89, 461, 354, 665, 276, 251, 315]
task11regions = [13, 8, 11, 7, 13, 9, 7, 11]


def cleandb():
    # FNULL = open(os.devnull, 'w')  # use this if you want to suppress output to stdout from the subprocess
    # subprocess.call('cleandb.bat', shell=False, stdout=FNULL, stderr=FNULL)
    subprocess.call(['sh', 'cleandb.sh'], check=True, capture_output=True)
    print('Cleaning database successful...')


def readsqlscript(_filepath, _file):
    print(f'\treading: {_filepath}')

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
                    _tasks[linenum] = t
                linenum = l
                currenttask = ''
                continue
            currenttask = currenttask + ' ' + l

        # store the last task
        t = currenttask.strip()
        if t and len(t) > 0:
            _tasks[linenum] = t

        f.close()
        _tasks = dict(sorted(_tasks.items()))
        return _tasks


def printtasks(_tasks):
    print(f'solved tasks: {len(_tasks)}')
    for key, value in _tasks.items():
        print(f'{key}. {value}')


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
    if _task == 1:
        # 1a kolko je takych obci
        # vysledok je 100
        record = dbcursor.fetchall()
        if len(record) == 100:
            print(f'\t record all length: {len(record)}')
            return 2
        if len(record) == 1:
            print(f'\t result one: {record}')
            for col in record[0]:
                if col == 100: return 3
    elif _task == 2:
        # 1b ktorý názov obce je použitý najviac.
        # Odpoveď: Porubka, Lucka (4)
        record = dbcursor.fetchall()
        print(f'\t record all length: {len(record)}')

        por, luc = False, False
        for line in record:
            for col in line:
                if col == 'Porubka': por = True
                if col == 'Lucka': luc = True
        if len(record) > 2 and por and luc: return 1
        if por and luc: return 3
        if (por and not luc) or (not por and luc): return 2
    elif _task == 3:
        # Koľko okresov sa nachádza v košickom kraji?
        # Odpoveď: 11
        record = dbcursor.fetchall()
        if len(record) == 11:
            print(f'\t record all length: {len(record)}')
            return 2
        if len(record) == 1:
            print(f'\t record one: {record[0]}')
            for col in record[0]:
                print(col)
                if col == 11: return 3
    elif _task == 4:
        # A koľko má košický kraj obcí? Pri tvorbe dopytu vám môže pomôcť informácia, že Trenčiansky kraj má spolu 276 obcí.
        # Odpoveď: 461
        record = dbcursor.fetchall()
        if len(record) == 461:
            print(f'\t record length: {len(record)}')
            return 1.5
        if len(record) == 1:
            print(f'\t record one: {record[0]}')
            for col in record[0]:
                print(col)
                if col == 461: return 3
    elif _task == 5:
        # Zistite, ktorá obec (mesto) bola na Slovensku najväčšia v roku 2012.
        # Pri tvorbe dopytu vám môže pomôcť informácia, že táto obec (mesto) bola najväčšia na Slovensku v rokoch 2009-2012,
        # avšak má v populácii klesajúcu tendenciu. Vo výsledku vypíšte jej názov a počet obyvateľov.
        # Odpoveď: Bratislava - Petržalka, 105468
        record = dbcursor.fetchone()
        print(f'\t record one: {record}')
        ba = False
        num = False
        for col in record:
            if col == 'Bratislava - Petrzalka':
                ba = True
            if col == 105468:
                num = True
        if ba and num: return 3
        if ba: return 1.5
        if num: return 1.5
    elif _task == 6:
        # Koľko obyvateľov mal okres Sabinov v roku 2012? Pri tvorbe dopytu vám môže pomôcť informácia, že okres Dolný Kubín mal v roku 2010 39553 obyvateľov.
        # Odpoveď: 58450
        record = dbcursor.fetchall()
        if len(record) == 58450:
            print(f'\t record length: {len(record)}')
            return 1.5
        if len(record) == 1:
            print(f'\t record: {record[0]}')
            for col in record[0]:
                print(col)
                if col == 58450:
                    return 3
    elif _task == 7:
        # Ako sme na tom na Slovensku? Vymierame alebo rastieme?
        # Zobrazte trend vývoja populácie za jednotlivé roky a výsledok zobrazte od najnovších informácií po najstaršie.
        # ?
        record = dbcursor.fetchall()
        foundyears, foundvalues, lineindex, issorted = 0, 0, 0, True
        print(record)
        if len(record) != 4: return 0

        for line in record:
            for col in line:
                if col in task7results.keys():
                    foundyears += 1
                    if list(task7results.keys())[lineindex] != col:
                        issorted = False
                    break
            lineindex += 1
        lineindex = 0
        for line in record:
            for col in line:
                if col in list(task7results.values()):
                    foundvalues += 1
                    if foundyears == 0 and list(task7results.values())[lineindex] != col:
                        issorted = False
                    break
            lineindex += 1
        print(f'found names: {foundyears}, values: {foundvalues}')
        points = 3
        if not issorted: points -= 0.5
        if foundyears == 4 and foundvalues == 4: return points
        if foundyears == 4: return points / 2
        if foundvalues == 4: return points / 2
    elif _task == 8:
        # Zistite, ktorá obec bola najmenšia v okrese Tvrdošín v roku 2011.
        # Pri tvorbe dopytu vám môže pomôcť informácia,
        # že v okrese Ružomberok to bola v roku 2012 obec
        # Potok s počtom obyvateľov 107.
        # Odpoveď: Štefanov nad Oravou a Čimhová (659)
        record = dbcursor.fetchall()
        print(f'\t record all length: {len(record)}')
        stefanov = False
        cimhova = False
        num = False

        print(f'\t record: {record}')
        for line in record:
            for col in line:
                if col == 'Stefanov nad Oravou':
                    stefanov = True
                if col == 'Cimhova':
                    cimhova = True
                if col == Decimal(659) or col == 659:
                    num = True
                    print('>>>>> 659:', num)

        if cimhova and stefanov and len(record) == 2: return 3
        if (stefanov or cimhova) and len(record) == 2: return 1.5
        if len(record) > 2: return 1
    elif _task == 9:
        # Zistite všetky obce, ktoré mali v roku 2010 počet obyvateľov do 5000.
        # Pri tvorbe dopytu vám môže pomôcť informácia, že v roku 2009 bolo týchto obcí o
        # 1 viac ako v roku 2009.
        # Odpoveď: obcí je spolu 2774
        record = dbcursor.fetchall()
        print(f'\t record all length {len(record)}')
        if len(record) == 2774: return 3
    elif _task == 10:
        # Zistite 10 obcí s populáciou nad 20000, ktoré mali v roku 2012 najväčší pomer žien voči mužom (viac žien v obci ako mužov). Týchto 10 obcí vypíšte v poradí od najväčšieho pomeru po najmenší. Vo výsledku okrem názvu obce vypíšte aj pomer zaokrúhlený na 4 desatinné miesta. Pri tvorbe dopytu vám môže pomôcť informácia,
        # že v roku 2011 bol tento pomer pre obec Košice  - Juh 1,1673.
        record = dbcursor.fetchall()

        if len(record) != 10: return 0

        namesfound, valuesfound = 0, 0
        for line in record:
            for col in line:
                if col in task10results.keys():
                    namesfound += 1
                    break
        for line in record:
            for col in line:
                if isinstance(col, Decimal) and float(col) in task10results.values():
                    valuesfound += 1
                    break
        print(f'found names: {namesfound}, values: {valuesfound}')
        if namesfound == 10 and valuesfound == 10: return 3
        if namesfound == 10: return 1
        if valuesfound == 10: return 2
    elif _task == 11:
        # Vypíšte sumárne informácie o stave Slovenska v roku 2012 v podobe tabuľky,
        # ktorá bude obsahovať
        # pre každý kraj informácie o počte obyvateľov, o počte obcí a počte okresov.

        record = dbcursor.fetchall()
        if len(record) != 8: return 0

        foundnames, foundpopulation, foundcities, foundregions, issorted = 0, 0, 0, 0, True
        index = 0

        for line in record:
            for col in line:
                if col in task11names:
                    foundnames += 1
                    if col != task11names[index]:
                        issorted = False
                    break
            for col in line:
                if col in task11population:
                    foundpopulation += 1
                    break
            for col in line:
                if col in task11cities:
                    foundcities += 1
                    break
            for col in line:
                if col in task11regions:
                    foundregions += 1
                    break
            index += 1
        points = 5
        if not issorted: points -= 1
        if foundnames != 8: points -= 1
        if foundpopulation != 8: points -= 1
        if foundcities != 8: points -= 1
        if foundregions != 8: points -= 1
        return points
    elif _task == 12:
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
        print(f'\t record all length: {len(record)}')
        if len(record) == 1307: return 5
    elif _task == 13:
        # Zistite počet obcí, ktorých počet obyvateľov v roku 2012 je nižší,
        # ako bol slovenský priemer v danom roku.
        # Odpoveď: obcí je 2433
        record = dbcursor.fetchone()
        print(f'\t record one: {record}')
        if record[0] == 2433: return 3
        if record[0] == 2435: return 1.5
        record = dbcursor.fetchall()
        print(f'\t record all length: {len(record)}')
        if len(record) == 2432: return 2
        if len(record) == 2434: return 1
    else:
        print('!!!UNKNOWN TASK')
    return 0


# print('Cleaning database...')
# cleandb()

print(f'{bcolors.WARNING}Parsing results...{bcolors.ENDC}')
results = {}

for file in sorted(os.listdir()):
    if file.endswith('.sql'):
        filepath = os.path.join(path, file)
        tasks = readsqlscript(filepath, file)
        title = file.replace('.sql', '')
        results[title] = tasks
        # printtasks(tasks)

# print(results)

print(f'{bcolors.WARNING}Connecting to database{bcolors.ENDC}')
conn = dbconn()
cur = conn.cursor()
print('\tConnected to db obce')

print(f'{bcolors.FAIL}Missing tasks{bcolors.ENDC}')
for result in results:
    sys.stdout.write('\t' + result + ': ')
    keys = results[result].keys()
    for i in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]:
        if not (i in keys):
            sys.stdout.write(str(i) + ', ')
    print()

print(f'\n{bcolors.WARNING}Running tests{bcolors.ENDC}\n')
for result in results:
    print(f'{bcolors.HEADER}{bcolors.BOLD}######### {result} #########{bcolors.ENDC}')
    total = 0
    for task in results[result]:
        if conn is None:
            conn = dbconn()
            cur = conn.cursor()
        try:
            print(f'{bcolors.BOLD}Task {task}{bcolors.ENDC}')
            query = results[result][task]
            cur.execute(query)
            res = checktask(task, cur)
            if ((task == 2 or task == 5 or task == 8)
                    and ('LIMIT' in query.upper())):
                res = 2
            if res == 0:
                print(f'\tRESULT: {bcolors.FAIL}FAIL{bcolors.ENDC}')
            else:
                print(f'\tRESULT: {bcolors.OKGREEN}{str(res)}b{bcolors.ENDC}')
            total += res
        except Exception as error:
            print(f'{bcolors.FAIL}\tTASK {task} RESULT: ERROR EXECUTING: {error}{bcolors.ENDC}')
            cur.close()
            conn.close()
            conn = None
    print(f'{bcolors.OKGREEN}TOTAL: {bcolors.BOLD}{total}b{bcolors.ENDC}')

if cur: cur.close()
if conn: conn.close()
