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
task12cities = ['Prievidza', 'Bratislava - Petrzalka', 'Humenne', 'Presov', 'Martin', 'Nitra', 'Kosice - Dargovskych hrdinov', 'Ruzomberok', 'Nove Zamky', 'Topolcany', 'Banska Bystrica', 'Spisska Nova Ves', 'Banovce nad Bebravou', 'Bardejov', 'Sala', 'Kosice - Sidlisko KVP', 'Povazska Bystrica', 'Kosice - Juh', 'Zvolen', 'Michalovce', 'Levice', 'Trnava', 'Partizanske', 'Zlate Moravce', 'Zilina', 'Cadca', 'Galanta', 'Brezno', 'Piestany', 'Kosice - Stare Mesto', 'Kosice - Sidlisko Tahanovce', 'Dubnica nad Vahom', 'Svidnik', 'Nove Mesto nad Vahom', 'Snina', 'Velky Krtis', 'Sturovo', 'Lucenec', 'Rimavska Sobota', 'Hlohovec', 'Puchov', 'Kosice - Sever', 'Myjava', 'Nova Dubnica', 'Dolny Kubin', 'Turcianske Teplice', 'Kosice - Zapad', 'Handlova', 'Sladkovicovo', 'Ziar nad Hronom', 'Kezmarok', 'Vranov nad Toplou', 'Kysucke Nove Mesto', 'Kosice - Nad jazerom', 'Banska Stiavnica', 'Liptovsky Mikulas', 'Sered', 'Holic', 'Revuca', 'Vrbove', 'Hnusta', 'Horne Srnie', 'Pliesovce', 'Vrable', 'Stara Tura', 'Likavka', 'Krasno nad Kysucou', 'Surany', 'Plesivec', 'Turzovka', 'Stropkov', 'Pohorela', 'Sliac', 'Tisovec', 'Cierna nad Tisou', 'Svodin', 'Imel', 'Vinica', 'Cinobana', 'Liptovske Revuce', 'Nitrianske Pravno', 'Medzilaborce', 'Chynorany', 'Tekovske Luzany', 'Henckovce', 'Klokocov', 'Vychodna', 'Savol', 'Zavadka nad Hronom', 'Bytca', 'Pukanec', 'Turany', 'Kremnica', 'Pribylina', 'Gabcikovo', 'Trstene pri Hornade', 'Topolniky', 'Cejkov', 'Sobrance', 'Zemianska Olca', 'Krupina', 'Tlmace', 'Helcmanovce', 'Male Trakany', 'Velke Rovne', 'Viglas', 'Zavar', 'Valaska', 'Ostry Grun', 'Belusa', 'Poprad', 'Hronovce', 'Abraham', 'Gelnica', 'Velke Orviste', 'Klenovec', 'Kokava nad Rimavicou', 'Zlatna na Ostrove', 'Hontianske Nemce', 'Nyrovce', 'Zarnovica', 'Hronec', 'Udavske', 'Tornala', 'Korna', 'Cata', 'Hozelec', 'Hronske Klacany', 'Smolnik', 'Velka Maca', 'Hurbanovo', 'Kolta', 'Chtelnica', 'Zlatno', 'Helpa', 'Horne Saliby', 'Jablonov nad Turnou', 'Paca', 'Slavosovce', 'Strekov', 'Preselany', 'Vlcany', 'Novaky', 'Dudince', 'Ondrejovce', 'Dolne Vestenice', 'Rakovec nad Ondavou', 'Semsa', 'Tovarne', 'Kvakovce', 'Kamenica', 'Gbely', 'Janova Lehota', 'Hlinik nad Hronom', 'Korytarky', 'Cierny Balog', 'Liptovske Sliace', 'Kamenec pod Vtacnikom', 'Zeliezovce', 'Santovka', 'Cajkov', 'Cerenany', 'Velky Cetin', 'Kralov Brod', 'Caka', 'Predajna', 'Rapovce', 'Zavada', 'Michal na Ostrove', 'Horne Hamre', 'Vyhne', 'Jeskova Ves', 'Patas', 'Mana', 'Vysoke Tatry', 'Brusno', 'Patince', 'Male Borove', 'Lipovnik', 'Hniezdne', 'Spissky Hrusov', 'Velky Folkmar', 'Lazany', 'Dlhe nad Cirochou', 'Horna Marikova', 'Donovaly', 'Velke Kapusany', 'Pobedim', 'Poniky', 'Lok', 'Sumiac', 'Makov', 'Hrustin', 'Harmanec', 'Brezova pod Bradlom', 'Velke Dravce', 'Kamienka', 'Besenov', 'Stakcin', 'Slivnik', 'Trstice', 'Spisske Vlachy', 'Velke Ludince', 'Valaliky', 'Bezovce', 'Sarovce', 'Sahy', 'Strazne', 'Drnava', 'Pribeta', 'Pozba', 'Surovce', 'Obid', 'Breza', 'Valaska Bela', 'Nemecka', 'Dolna Marikova', 'Kolacno', 'Liptovska Luzna', 'Parchovany', 'Puste Ulany', 'Zemplinske Hradiste', 'Cilizska Radvan', 'Lehnice', 'Hradiste pod Vratnom', 'Nova Bosaca', 'Udica', 'Kmetovo', 'Zemne', 'Chrabrany', 'Topolcianky', 'Rudinska', 'Lubochna', 'Bravacovo', 'Detva', 'Ozdin', 'Zacharovce', 'Balog nad Iplom', 'Tekovska Breznica', 'Hazlin', 'Orlov', 'Zahor', 'Sirk', 'Neslusa', 'Cierna', 'Vcelince', 'Hronsky Benadik', 'Sirnik', 'Tomasovce', 'Lubina', 'Dacov', 'Bojnice', 'Matovske Vojkovce', 'Batka', 'Nova Bana', 'Neded', 'Travnica', 'Lontov', 'Nemcice', 'Kukucinov', 'Jedlove Kostolany', 'Stara Kremnicka', 'Kosihovce', 'Ipelsky Sokolec', 'Vycapy - Opatovce', 'Jasova', 'Zakopcie', 'Temes', 'Leopoldov', 'Ulic', 'Plave Vozokany', 'Bosaca', 'Ladzany', 'Velke Dvorany', 'Pastovce', 'Sikenica', 'Dolna Tizina', 'Bela', 'Male Straciny', 'Svinna', 'Lovca', 'Ohrady', 'Hazin', 'Tusice', 'Hrabovec nad Laborcom', 'Nitrianske Rudno', 'Koromla', 'Slovenske Nove Mesto', 'Modrany', 'Stredne Plachtince', 'Bardonovo', 'Horna', 'Voznica', 'Prasice', 'Sambron', 'Svatuse', 'Sivetice', 'Ratkovske Bystre', 'Dolna Krupa', 'Velke Pole', 'Horne Zahorany', 'Rykyncice', 'Detvianska Huta', 'Kosihy nad Iplom', 'Bacuch', 'Sebedin - Becov', 'Luc na Ostrove', 'Hatalov', 'Slovinky', 'Velky Blh', 'Namestovo', 'Vazec', 'Dobsina', 'Lubovec', 'Dlha Ves', 'Sasa', 'Stary Tekov', 'Michalok', 'Ulicske Krive', 'Nova Bystrica', 'Velky Kliz', 'Lela', 'Inacovce', 'Ptruksa', 'Brusnica', 'Vojka', 'Buc', 'Brodske', 'Sklene Teplice', 'Ochtina', 'Kralova nad Vahom', 'Celovce', 'Zaskov', 'Kralovany', 'Smolinske', 'Tisinec', 'Ardanovce', 'Radvan nad Laborcom', 'Moravsky Svaty Jan', 'Kuty', 'Okruhle', 'Liptovska Porubka', 'Calovec', 'Chanava', 'Kopcany', 'Malatiny', 'Podhradie', 'Jelsava', 'Potor', 'Nizna Olsava', 'Oponice', 'Hertnik', 'Visnov', 'Dolne Srnie', 'Kravany nad Dunajom', 'Muran', 'Demjata', 'Samudovce', 'Mojzesovo', 'Silica', 'Mlynarovce', 'Kusin', 'Lipovce', 'Mernik', 'Zbince', 'Mokrance', 'Pavlova', 'Hrabovka', 'Norovce', 'Radosina', 'Sulovce', 'Velky Lapas', 'Praznovce', 'Skycov', 'Hradiste', 'Velke Krstenany', 'Staskov', 'Demanovska Dolina', 'Jalovec', 'Liptovska Sielnica', 'Zemianske Kostolany', 'Koprivnica', 'Rajec', 'Durkova', 'Molca', 'Bela nad Cirochou', 'Malachov', 'Slavnica', 'Pitelova', 'Sudovce', 'Trencianske Teplice', 'Remetske Hamre', 'Siatorska Bukovinka', 'Pecenice', 'Trnie', 'Okruzna', 'Stranska', 'Rusky Hrabovec', 'Vadovce', 'Hrasne', 'Beloveza', 'Hornany', 'Gbelany', 'Prosiek', 'Semerovo', 'Borka', 'Jasenove', 'Martin nad Zitavou', 'Kocin - Lancar', 'Hudcovce', 'Mytna', 'Stiavnicke Bane', 'Varechovce', 'Ladmovce', 'Nova Polianka', 'Zelezna Breznica', 'Kalniste', 'Coltovo', 'Botany', 'Podhajska', 'Pribelce', 'Sucany', 'Lipove', 'Toporec', 'Dolne Plachtince', 'Mytne Ludany', 'Divin', 'Habura', 'Slovenska Ves', 'Cermany', 'Polany', 'Dubovica', 'Hrinova', 'Vrbova nad Vahom', 'Velke Revistia', 'Petrovce', 'Sabinov', 'Kalna nad Hronom', 'Pohronska Polhora', 'Tuchyna', 'Choca', 'Kosice - Dzungla', 'Krasna Luka', 'Stankovany', 'Neporadza', 'Horna Ves', 'Mnisek nad Popradom', 'Velke Slemence', 'Gerlachov', 'Stvrtok na Ostrove', 'Terany', 'Pastina Zavada', 'Mojtin', 'Brezolupy', 'Sasa', 'Jastraba', 'Biel', 'Bara', 'Vricko', 'Zabokreky', 'Dedinka', 'Bodza', 'Merasice', 'Vysne Valice', 'Myto pod Dumbierom', 'Narad', 'Strba', 'Odorin', 'Lazy pod Makytou', 'Kamenny Most', 'Resov', 'Podhorod', 'Tuzina', 'Vysna Rybnica', 'Vrsatske Podhradie', 'Horne Obdokovce', 'Petrovce', 'Domanovce', 'Vinohrady nad Vahom', 'Podhorie', 'Podkylava', 'Uzovsky Salgov', 'Dolny Hricov', 'Brezov', 'Kliestina', 'Magnezitovce', 'Kamienka', 'Salka', 'Nova Ves nad Zitavou', 'Skrabske', 'Hrochot', 'Vojcice', 'Krizovany nad Dudvahom', 'Stitnik', 'Dlha nad Kysucou', 'Radosovce', 'Sobotiste', 'Male Kozmalovce', 'Ruban', 'Poluvsie', 'Panicke Dravce', 'Tuhar', 'Banov', 'Dolny Ohaj', 'Polina', 'Nova Dedina', 'Cierna Voda', 'Cierne Klacany', 'Brehy', 'Panovce', 'Sneznica', 'Resica', 'Liestany', 'Malas', 'Holiare', 'Lutina', 'Jalovec', 'Nechvalova  Polianka', 'Hronska Breznica', 'Lukacovce', 'Lubela', 'Dvorec', 'Partizanska Lupca', 'Lubisa', 'Zboj', 'Brhlovce', 'Jablon', 'Blatna na Ostrove', 'Jastrabie pri Michalovciach', 'Bracovce', 'Vysna Boca', 'Radoma', 'Hronska Dubrava', 'Pichne', 'Aleksince', 'Giglovce', 'Granc - Petrovce', 'Jacovce', 'Jablonica', 'Cavoj', 'Vernar', 'Zdiar', 'Matiasovce', 'Novy Salas', 'Gemerska Panica', 'Rudlov', 'Hazin nad Cirochou', 'Olsovany', 'Kriva', 'Luhyna', 'Makovce', 'Ohradzany', 'Zelovce', 'Smrecany', 'Radava', 'Vlachy', 'Pohranice', 'Nova Vieska', 'Olsavka', 'Losonec', 'Stebnik', 'Smilno', 'Busince', 'Puste Sady', 'Podbiel', 'Vitanova', 'Hrabicov', 'Kobyly', 'Hricovske Podhradie', 'Rumince', 'Ipelske Ulany', 'Povraznik', 'Tura', 'Kubanovo', 'Dolna Lehota', 'Ladce', 'Koseca', 'Horna Poruba', 'Podkrivan', 'Stara Huta', 'Opatovska Nova Ves', 'Baskovce', 'Jestice', 'Tehla', 'Horna Zdana', 'Litava', 'Budina', 'Radobica', 'Halic', 'Komarovce', 'Dulovce', 'Olka', 'Stara Voda', 'Selice', 'Korytne', 'Volica', 'Cabov', 'Velke Trakany', 'Dvorniky', 'Stare', 'Budkovce', 'Trenc', 'Martinova', 'Mala Lehota', 'Hrachoviste', 'Kruzna', 'Bystra', 'Kalnica', 'Cabiny', 'Velky Meder', 'Luboriecka', 'Nizny Slavkov', 'Rimavske Zaluzany', 'Nana', 'Celadince', 'Kremnicke Bane', 'Srobarova', 'Ket', 'Domaniky', 'Zlate', 'Sutovce', 'Gocaltovo', 'Ockov', 'Sulin', 'Brehov', 'Povazany', 'Bielovce', 'Valkovce', 'Papradno', 'Zombor', 'Zaskalie', 'Medovarce', 'Hrachovo', 'Cerhov', 'Modra nad Cirochou', 'Trnavka', 'Visnove', 'Puste Pole', 'Mlynica', 'Buzitka', 'Sterusy', 'Dojc', 'Rastislavice', 'Lipovnik', 'Hran', 'Dedinky', 'Tusicka Nova Ves', 'Stretava', 'Malatina', 'Velka Lehota', 'Rudnianska Lehota', 'Cernina', 'Bodzianske Luky', 'Velke Zlievce', 'Mikusovce', 'Zbudza', 'Male Uherce', 'Velke Raskovce', 'Haligovce', 'Chrtany', 'Chmelova', 'Harhaj', 'Nezbudska Lucka', 'Svaty Anton', 'Badan', 'Banska Bela', 'Turie', 'Vidina', 'Dolne Oresany', 'Stara Basta', 'Nove Sady', 'Livovska Huta', 'Marhan', 'Slovenske Pravno', 'Kolare', 'Rudno', 'Hnilec', 'Sintava', 'Kostolec', 'Jasenovo', 'Horny Pial', 'Dolny Pial', 'Ladomirov', 'Slatvina', 'Dubnik', 'Plavec', 'Plavnica', 'Plechotice', 'Motesice', 'Krusinec', 'Okolicna na Ostrove', 'Mala nad Hronom', 'Horny Lieskov', 'Hubina', 'Dvorniky - Vcelare', 'Matovce', 'Vagrinec', 'Vysny Komarnik', 'Juskova Vola', 'Ondavske Matiasovce', 'Krivosud - Bodovka', 'Margecany', 'Svedlar', 'Haniska', 'Svrbice', 'Dolna Poruba', 'Kostolany pod Tribecom', 'Nevidzany', 'Ton', 'Kvasov', 'Velke Vozokany', 'Novosad', 'Maly Hores', 'Zubak', 'Visolaje', 'Haluzice', 'Chotin', 'Lipnik', 'Turcianske Jaseno', 'Vojkovce', 'Turik', 'Malacky', 'Svosov', 'Horne Semerovce', 'Iliasovce', 'Krasnany', 'Suja', 'Priepasne', 'Kosariska', 'Spania Dolina', 'Mociar', 'Polomka', 'Dulov', 'Horny Tisovnik', 'Horne Mladonice', 'Kozi Vrbovok', 'Zemiansky Vrbovok', 'Hradiste', 'Raztocno', 'Visnove', 'Gemersky Sad', 'Muranska Lehota', 'Muranska Zdychava', 'Hajnacka', 'Vyskovce nad Iplom', 'Zbrojniky', 'Velky Hores', 'Dolinka', 'Obeckov', 'Sirakov', 'Rakovnica', 'Nevolne', 'Buclovany', 'Kovacova', 'Mikulasova', 'Porubka', 'Rovne', 'Slovenske Krive', 'Tajna', 'Bohunovo', 'Cerveny Klastor', 'Holumnica', 'Vojka nad Dunajom', 'Kurimany', 'Olsavica', 'Spisske Podhradie', 'Roskovce', 'Sukov', 'Brestov', 'Hrabkov', 'Velky Slivnik', 'Podbranc', 'Osadne', 'Circ', 'Suche Brezovo', 'Driencany', 'Velky Lom', 'Ciz', 'Slatina nad Bebravou', 'Vlckovce', 'Revucka Lehota', 'Stary Hradok', 'Otrocok', 'Michal nad Zitavou', 'Rybnik', 'Dubakovo', 'Velka Ves', 'Ruzina', 'Cierna Lehota', 'Sec', 'Jelsovec', 'Bucany', 'Bartosova Lehotka', 'Stvrtok', 'Lisov', 'Halacovce', 'Medvedov', 'Cekovce', 'Radosovce', 'Meliata', 'Bolesov', 'Lucky', 'Raztoka', 'Lom nad Rimavicou', 'Bogliarka', 'Chvojnica', 'Turecka', 'Jablonka', 'Jalova', 'Plavecke Podhradie', 'Motycky', 'Polianka', 'Beckov', 'Nesvady', 'Regetovka', 'Cremosne', 'Stebnicka Huta', 'Mlynky', 'Sarisske Cierne', 'Backa', 'Sutovo', 'Gemerska Horka', 'Zavazna Poruba', 'Veterna Poruba', 'Vavrisovo', 'Stara Lehota', 'Liptovske Matiasovce', 'Hybe', 'Bobrovnik', 'Legnava', 'Kozuchov', 'Diviaky nad Nitricou', 'Ruska Poruba', 'Runina', 'Nadlice', 'Lomne', 'Nedanovce', 'Klubina', 'Brodzany', 'Jablonove', 'Jasenica', 'Zlatno', 'Velcice', 'Dubrava', 'Biskupova', 'Ludovitova', 'Lucka', 'Urmince', 'Kamenin', 'Dolne Kockovce', 'Ulany nad Zitavou', 'Certizne', 'Dolne Trhoviste', 'Kalinov', 'Prakovce', 'Zalobin', 'Smrdaky', 'Secovska Polianka', 'Lesne', 'Fulianka', 'Obrucne', 'Matiaska', 'Sena', 'Vysna Jedlova', 'Pusovce', 'Stefanovce', 'Bajerovce', 'Skaros', 'Jakovany', 'Vojtovce', 'Uzovce', 'Horna Strehova', 'Rimavske Brezovo', 'Vlachovo', 'Nova Basta', 'Lenka', 'Male Zlievce', 'Kraskovo', 'Hontianske Trstany', 'Slizke', 'Kralova Lehota', 'Jamnik', 'Holcikovce', 'Dukovce', 'Mosurov', 'Mrazovce', 'Konska', 'Katov', 'Radola', 'Vysne Ladickovce', 'Nedasovce', 'Kralovsky Chlmec', 'Mikova', 'Brdarka', 'Pakostov', 'Chrastince', 'Istebne', 'Ruska Kajna', 'Rovne', 'Proc', 'Salov', 'Sopkovce', 'Sedlice', 'Hnojne', 'Ipelske Predmostie', 'Lubotin', 'Mestecko', 'Nevidzany', 'Vydrna', 'Duplin', 'Cervena Voda', 'Vysoka', 'Sula', 'Cerveny Hradok', 'Vislava', 'Stos', 'Brutovce', 'Krnca', 'Bunkovce', 'Turcok', 'Benadikovce', 'Bojna', 'Nitrica', 'Levkuska', 'Lesnica', 'Trencianske Jastrabie', 'Smigovec', 'Horna Krupa', 'Vieska', 'Susany', 'Velusovce', 'Priekopa', 'Velke Chlievany', 'Breznicka', 'Podskalie', 'Ratka', 'Bajany', 'Praha', 'Polanovce', 'Lipovany', 'Kalonda', 'Bukova', 'Vyskovce', 'Studenec', 'Torysky', 'Padan', 'Suche', 'Binovce', 'Kapusianske Klacany', 'Jalsovik', 'Ihrac', 'Poloma', 'Zalaba', 'Rakytnik', 'Gemerske Michalovce', 'Tasula', 'Celkova Lehota', 'Kosicky Klecenov', 'Olsinkov', 'Dubravka', 'Latky', 'Prochot', 'Sasinkovo', 'Izkovce', 'Lucka', 'Sedmerovec', 'Rohovce', 'Krasnohorska Dlha Luka', 'Becherov', 'Pocuvadlo', 'Starina', 'Kozelnik', 'Hrabova Roztoka', 'Podolinec', 'Nemce', 'Cigel', 'Valice', 'Trakovice', 'Lucnica nad Zitavou', 'Tekoldany', 'Girovce', 'Bodina', 'Lysica', 'Kecovo', 'Ina', 'Dlhe Pole', 'Krize', 'Kucin', 'Cicmany', 'Hrhov', 'Zabiedovo', 'Lukavica', 'Babie', 'Solnik', 'Vecelkov', 'Vlaca', 'Vavrinec', 'Honce', 'Budis', 'Vesele', 'Teply Vrch', 'Husina', 'Sasova', 'Bajc', 'Rafajovce', 'Polny Kesov', 'Strkovec', 'Risnovce', 'Borsa', 'Opina', 'Medzianky', 'Spanie Pole', 'Tupa', 'Janovik', 'Pavlova Ves', 'Babin', 'Martovce', 'Mudronovo', 'Lednica', 'Virt', 'Bajka', 'Plastovce', 'Poruba', 'Mala Causa', 'Melek', 'Cab', 'Dolne Lefantovce', 'Bruty', 'Cernik', 'Lipova', 'Pocarova', 'Slopna', 'Dlha nad Vahom', 'Obyce', 'Vlky', 'Vieska nad Zitavou', 'Krasno', 'Radostka', 'Pribis', 'Bukovina', 'Liptovska Kokava', 'Liptovsky Trnovec', 'Nizna Boca', 'Svaty Kriz', 'Folkusova', 'Brestovec', 'Cachtice', 'Valaska Dubova', 'Abramova', 'Haj', 'Ivancina', 'Kamenna Poruba', 'Kotrcina Lucka', 'Hiadel', 'Beluj', 'Ilija', 'Krivoklat', 'Cerveny Kamen', 'Devicie', 'Chuda Lehota', 'Horny Badin', 'Dubnicka', 'Bolkovce', 'Filakovo', 'Lovinobana', 'Nitra nad Iplom', 'Nove Hony', 'Zlatniky', 'Vysocany', 'Kalinovo', 'Kuchyna', 'Hrnciarske Zaluzany', 'Utekac', 'Ploske', 'Sisov', 'Ziar', 'Muranska Huta', 'Slatinka nad Bebravou', 'Dubovec', 'Gemerske Dechtare', 'Hubovo', 'Kociha', 'Krokava', 'Kyjatice', 'Ratkovska Lehota', 'Ratkovska Sucha', 'Studena', 'Vysny Skalnik', 'Riecka', 'Dolne Lovcice', 'Senne', 'Budca', 'Horne Oresany', 'Klak', 'Dolna Ves', 'Unin', 'Hrabovec', 'Janovce', 'Jedlinka', 'Krive', 'Vysna Polianka', 'Vysny Tvarozec', 'Letnicie', 'Zubne', 'Pritulany', 'Mala Frankova', 'Beharovce', 'Vysny Slavkov', 'Klcov', 'Nizne Repase', 'Dubovce', 'Svetlice', 'Valentovce', 'Zbojne', 'Lucina', 'Nemcovce', 'Sucha Dolina', 'Nova Sedlica', 'Parihuzovce', 'Ubla', 'Chmelnica', 'Kremna', 'Litmanova', 'Stranany', 'Velka Lesna', 'Vysne Ruzbachy', 'Breznicka', 'Gribov', 'Jakusovce', 'Potoky', 'Staskovce', 'Tokajik', 'Velkrop', 'Dobroslava', 'Krajne Cierno', 'Nizna Pisana', 'Nizny Komarnik', 'Sobos', 'Majerovce', 'Ruska Vola', 'Stefanovce', 'Vysny Zipov', 'Benkovce', 'Henclova', 'Pastuchov', 'Bojnicky', 'Poproc', 'Salgocka', 'Jovsa', 'Sliepkovce', 'Vysoka nad Uhom', 'Besa', 'Cierne Pole', 'Ruska', 'Petrovo', 'Okoc', 'Stratena', 'Mierovo', 'Fekisovce', 'Ruska Bystra', 'Vysne Nemecke', 'Hincovce', 'Kolinovce', 'Klin nad Bodrogom', 'Stanca', 'Baka', 'Bac', 'Zadiel', 'Zelmanovce', 'Micakovce', 'Kobylnice', 'Vladica', 'Turany nad Ondavou', 'Borsky Mikulas', 'Mala Polana', 'Korunkova', 'Havaj', 'Bystra', 'Pokryvac', 'Ruska Vola nad Popradom', 'Hranicne', 'Bodiky', 'Klizska Nema', 'Hajtovka', 'Ruska Volova', 'Olsov', 'Hanigovce', 'Ondrasovce', 'Brezany', 'Stiavnik', 'Tatranska Javorina', 'Kravany', 'Sulov - Hradna', 'Hvozdnica', 'Repejov', 'Cabalovce', 'Pavlany', 'Vlkovce', 'Male Vozokany', 'Stara Lesna', 'Osturna', 'Chropov', 'Hradisko', 'Jasenov', 'Rohoznik', 'Kosarovce', 'Zavadka', 'Vysny Hrusov', 'Vitazovce', 'Turcovce', 'Nizne Ladickovce', 'Baskovce', 'Adidovce', 'Trocany', 'Rokytov', 'Livov', 'Lipova', 'Komarov', 'Hervartov', 'Abrahamovce', 'Prietrzka', 'Radimov', 'Kunesov', 'Kopernica', 'Dolna Trnavka', 'Horne Chlebany', 'Dvorany nad Nitrou', 'Ocova', 'Vrbovka', 'Silicka Brezova', 'Mula', 'Plevnik - Drienove', 'Klenany', 'Potok', 'Lehota nad Rimavicou', 'Male Hoste', 'Vrchtepla', 'Mokra Luka', 'Male Lednice', 'Prihradzany', 'Chonkovce', 'Nandraz', 'Krcava', 'Hrlica', 'Trebichava', 'Uhorske', 'Dobroc', 'Komjatice', 'Lackov', 'Drienovo', 'Pochabany', 'Somotor', 'Drabsko', 'Opatovce', 'Podkonice', 'Sklene', 'Chlaba', 'Moskovec', 'Kalamenova', 'Kanianka', 'Borcova', 'Bodorova', 'Potok', 'Lucky', 'Kostolne Kracany', 'Hubova', 'Teplicka', 'Lokca', 'Velka Trna', 'Jesenske', 'Male Ludince', 'Modrova', 'Turciansky Dur', 'Nova Lehota', 'Ratkovo', 'Karlova', 'Liptovsky Peter', 'Brezina', 'Bysta', 'Velke Borove', 'Liptovska Anna', 'Ochodnica', 'Dolne Semerovce', 'Dvorianky', 'Lopusne Pazite', 'Dolny Vadicov', 'Topolnica', 'Uhorna', 'Kysak', 'Detrik', 'Mudrovce', 'Vysny Kazimir', 'Radvanovce', 'Petrovce', 'Petkovce', 'Bziny', 'Jasenovce', 'Vysna Pisana', 'Mestisko', 'Sedliacka Dubova', 'Krajna Porubka', 'Krajna Polana', 'Havranec', 'Vysny Caj', 'Zarnov', 'Zdana', 'Cigla']
task12population2011 = [48866, 105763, 34921, 91638, 57300, 78875, 27424, 28364, 39585, 27124, 79775, 37948, 19503, 33625, 23440, 25223, 41153, 23461, 43311, 39989, 34649, 66219, 24006, 12286, 81515, 24921, 15147, 21827, 28267, 20598, 23264, 25229, 11602, 20360, 20701, 12853, 10851, 28508, 24549, 22661, 18213, 20348, 12267, 11469, 19554, 6679, 40695, 17738, 5465, 19862, 16843, 23225, 15652, 25679, 10387, 31928, 16214, 11218, 12815, 6212, 7749, 2849, 2312, 8983, 9338, 3086, 6905, 10155, 2383, 7772, 10905, 2332, 5095, 4309, 3861, 2574, 2046, 1853, 2398, 1627, 3193, 6781, 2743, 2913, 476, 2365, 2201, 571, 2457, 11313, 1984, 4389, 5571, 1376, 5343, 1541, 3054, 1183, 5992, 2444, 8035, 3813, 1488, 1148, 3891, 1697, 2245, 3900, 551, 5855, 52791, 1480, 1061, 6232, 1082, 3304, 3026, 2421, 1547, 565, 6476, 1217, 1242, 7474, 2140, 1071, 824, 1462, 1129, 2617, 7740, 1402, 2585, 490, 2777, 3225, 809, 631, 1959, 2071, 1480, 3330, 4283, 1474, 466, 2595, 1086, 804, 1036, 431, 1853, 5218, 936, 2974, 965, 5234, 3791, 1840, 7166, 768, 1018, 1706, 1609, 1153, 786, 1354, 979, 517, 920, 623, 1270, 517, 824, 2103, 4222, 2140, 504, 167, 510, 1468, 1261, 943, 1618, 2048, 654, 231, 9371, 1199, 1591, 1012, 1334, 1813, 3180, 881, 5109, 683, 556, 1682, 2474, 799, 3794, 3627, 1556, 4228, 996, 1658, 7607, 649, 704, 2964, 503, 2280, 1178, 1582, 2226, 1845, 1438, 886, 2898, 1942, 1683, 1162, 1206, 2551, 675, 1126, 2178, 910, 2287, 756, 2766, 971, 1062, 718, 15062, 367, 419, 845, 1250, 1175, 691, 666, 1170, 3181, 485, 813, 1217, 625, 1385, 1406, 766, 4939, 628, 956, 7556, 3298, 1121, 705, 982, 628, 930, 1109, 605, 859, 2153, 1210, 1808, 251, 4164, 932, 865, 1397, 311, 702, 530, 653, 1298, 375, 148, 1592, 691, 1173, 466, 713, 565, 1937, 473, 1085, 1455, 653, 774, 384, 670, 2027, 413, 838, 399, 388, 2297, 411, 138, 311, 720, 467, 1007, 381, 749, 766, 1902, 1212, 7945, 2374, 5696, 506, 581, 960, 1434, 318, 270, 2828, 918, 364, 751, 508, 416, 517, 1172, 2360, 444, 544, 1701, 443, 1633, 454, 958, 392, 225, 581, 2131, 4090, 651, 1151, 1194, 707, 2591, 204, 665, 3235, 842, 415, 869, 1042, 247, 980, 747, 1253, 1091, 640, 1344, 566, 224, 350, 520, 605, 985, 1370, 249, 429, 324, 2017, 487, 1127, 976, 1033, 1027, 633, 2771, 278, 595, 604, 1677, 687, 5874, 256, 357, 3377, 1063, 848, 675, 222, 4161, 621, 314, 128, 432, 465, 351, 324, 781, 458, 812, 439, 1226, 196, 1447, 528, 605, 517, 524, 424, 1185, 822, 182, 334, 83, 551, 556, 485, 1263, 1065, 576, 4673, 157, 1861, 610, 994, 2070, 463, 1864, 386, 528, 1504, 7802, 556, 543, 222, 12715, 2043, 1765, 780, 506, 668, 725, 1216, 283, 714, 670, 606, 1034, 1771, 668, 225, 505, 509, 194, 554, 1463, 321, 466, 1174, 765, 381, 423, 303, 526, 651, 3602, 961, 1290, 1054, 324, 388, 1214, 366, 246, 1542, 247, 939, 1574, 365, 235, 610, 1551, 396, 347, 460, 1387, 1047, 1333, 796, 1502, 2179, 1833, 1550, 628, 426, 1498, 389, 962, 591, 755, 378, 3709, 1603, 129, 1549, 1401, 1087, 1073, 591, 1002, 346, 1244, 493, 476, 468, 310, 103, 269, 480, 1129, 425, 1225, 834, 367, 314, 431, 878, 294, 963, 101, 458, 417, 582, 1667, 150, 596, 1768, 2256, 528, 598, 1375, 798, 212, 664, 664, 692, 603, 802, 326, 188, 652, 1333, 624, 793, 597, 1076, 736, 234, 527, 313, 714, 1470, 599, 1275, 1301, 589, 858, 374, 382, 299, 149, 229, 291, 786, 2617, 2519, 1069, 599, 333, 718, 256, 178, 531, 554, 774, 263, 521, 1688, 386, 1800, 311, 226, 2870, 101, 317, 407, 1420, 2081, 792, 1510, 482, 226, 930, 734, 487, 194, 1046, 387, 8869, 154, 817, 335, 1184, 444, 263, 501, 663, 191, 758, 414, 253, 471, 366, 620, 1291, 231, 232, 2528, 146, 185, 257, 874, 811, 1013, 464, 178, 230, 455, 534, 514, 1272, 895, 325, 1601, 289, 562, 651, 836, 1191, 738, 592, 201, 495, 281, 540, 705, 326, 676, 152, 401, 273, 400, 1231, 213, 1240, 1960, 1857, 1263, 328, 1288, 52, 969, 960, 275, 222, 446, 1774, 237, 155, 281, 958, 315, 329, 1698, 1841, 1625, 797, 799, 280, 1534, 392, 374, 493, 439, 133, 129, 76, 338, 828, 323, 1963, 2085, 1443, 209, 807, 373, 595, 799, 669, 492, 1013, 1115, 880, 897, 66, 1390, 488, 361, 429, 226, 17066, 823, 612, 982, 1436, 310, 371, 444, 193, 172, 3047, 933, 215, 175, 179, 102, 248, 1247, 69, 287, 201, 257, 1196, 675, 501, 1037, 483, 498, 215, 606, 429, 215, 72, 139, 229, 460, 134, 273, 290, 232, 876, 458, 379, 291, 4075, 192, 134, 447, 693, 339, 614, 186, 1249, 113, 245, 209, 666, 450, 1263, 326, 192, 308, 671, 1413, 96, 460, 874, 131, 390, 311, 2279, 397, 349, 251, 353, 563, 444, 1804, 211, 1545, 215, 288, 293, 134, 373, 151, 475, 81, 686, 114, 380, 1353, 5060, 28, 94, 254, 571, 310, 654, 526, 1343, 1231, 373, 662, 233, 298, 1509, 131, 121, 214, 1769, 251, 81, 633, 272, 644, 546, 805, 864, 1053, 224, 822, 342, 223, 256, 123, 1413, 1504, 1233, 1547, 371, 652, 290, 3380, 817, 701, 2740, 447, 389, 39, 270, 2114, 202, 536, 212, 307, 1102, 347, 113, 530, 183, 559, 864, 526, 191, 283, 153, 328, 212, 603, 469, 440, 262, 183, 91, 216, 601, 1449, 217, 433, 7685, 155, 75, 473, 239, 1356, 114, 497, 449, 382, 114, 1051, 234, 632, 1372, 521, 305, 350, 484, 489, 135, 76, 420, 221, 734, 199, 1343, 362, 273, 230, 2010, 1240, 251, 515, 1200, 93, 494, 426, 446, 509, 297, 487, 787, 128, 333, 487, 88, 184, 262, 216, 665, 140, 492, 359, 863, 402, 676, 889, 202, 562, 948, 189, 312, 99, 205, 136, 275, 34, 684, 581, 595, 877, 108, 193, 426, 1193, 729, 276, 101, 46, 185, 63, 3271, 1164, 1224, 324, 1479, 892, 148, 68, 497, 825, 374, 206, 1955, 78, 319, 167, 1138, 812, 383, 247, 39, 255, 232, 62, 380, 210, 1189, 295, 538, 154, 1249, 193, 628, 380, 2085, 1213, 200, 296, 86, 590, 269, 254, 1418, 689, 126, 978, 289, 332, 1631, 1263, 668, 453, 783, 529, 623, 1019, 1565, 139, 485, 872, 1507, 428, 467, 516, 840, 453, 118, 966, 568, 158, 800, 139, 467, 4010, 795, 203, 464, 99, 1829, 431, 517, 128, 339, 255, 711, 304, 203, 180, 114, 640, 10801, 2168, 346, 185, 671, 125, 2231, 1672, 872, 1027, 79, 484, 157, 201, 203, 558, 456, 140, 220, 31, 86, 61, 52, 279, 153, 231, 752, 223, 1275, 1904, 237, 249, 1221, 513, 433, 87, 220, 111, 118, 513, 360, 64, 189, 178, 298, 612, 186, 649, 116, 43, 177, 165, 471, 195, 286, 32, 805, 959, 109, 641, 195, 466, 1396, 134, 207, 48, 92, 255, 115, 221, 34, 80, 87, 186, 149, 448, 84, 116, 1205, 540, 103, 999, 1345, 2761, 441, 820, 747, 807, 368, 302, 611, 107, 3672, 134, 454, 308, 114, 247, 239, 580, 211, 424, 1118, 562, 170, 335, 146, 98, 61, 398, 3936, 113, 82, 408, 33, 176, 98, 193, 283, 505, 78, 111, 394, 133, 60, 158, 4069, 228, 885, 932, 1181, 148, 360, 56, 477, 291, 1009, 330, 380, 100, 1186, 39, 622, 538, 479, 322, 313, 349, 428, 202, 310, 556, 87, 84, 426, 496, 369, 489, 583, 248, 423, 344, 358, 762, 2611, 360, 166, 327, 1591, 293, 49, 278, 434, 259, 528, 509, 87, 566, 287, 419, 85, 43, 558, 644, 4286, 105, 114, 247, 1561, 207, 410, 867, 768, 700, 65, 84, 4126, 128, 243, 108, 1832, 1272, 1069, 1168, 2290, 454, 45, 181, 522, 170, 207, 174, 107, 1376, 706, 159, 61, 93, 1947, 541, 601, 462, 468, 815, 145, 1426, 56, 73, 199, 212, 435, 149, 556, 221, 77, 468, 516, 54, 209, 14, 304, 415, 1372, 108]
task12population2012 = [48519, 105468, 34634, 91352, 57023, 78607, 27166, 28145, 39373, 26916, 79583, 37767, 19323, 33451, 23268, 25052, 40982, 23293, 43148, 39833, 34500, 66073, 23860, 12150, 81382, 24791, 15021, 21703, 28149, 20483, 23149, 25116, 11492, 20250, 20596, 12756, 10755, 28413, 24454, 22570, 18127, 20265, 12185, 11387, 19472, 6598, 40615, 17664, 5392, 19789, 16774, 23157, 15584, 25619, 10330, 31873, 16161, 11169, 12766, 6164, 7701, 2804, 2267, 8941, 9296, 3045, 6864, 10115, 2343, 7733, 10866, 2293, 5056, 4270, 3824, 2538, 2010, 1817, 2362, 1593, 3159, 6747, 2711, 2881, 445, 2335, 2171, 541, 2427, 11284, 1955, 4360, 5542, 1347, 5314, 1512, 3026, 1155, 5964, 2416, 8007, 3785, 1460, 1120, 3863, 1670, 2218, 3873, 524, 5828, 52765, 1454, 1035, 6206, 1056, 3278, 3000, 2395, 1522, 540, 6451, 1192, 1217, 7450, 2116, 1047, 800, 1438, 1105, 2593, 7717, 1379, 2563, 468, 2755, 3203, 787, 609, 1937, 2050, 1459, 3309, 4262, 1453, 445, 2575, 1066, 784, 1016, 411, 1833, 5198, 916, 2954, 945, 5214, 3771, 1820, 7146, 748, 998, 1687, 1590, 1134, 767, 1335, 960, 498, 901, 604, 1251, 498, 805, 2084, 4203, 2121, 485, 148, 492, 1450, 1243, 925, 1600, 2030, 636, 213, 9353, 1181, 1573, 994, 1316, 1796, 3163, 864, 5092, 666, 539, 1665, 2457, 782, 3777, 3610, 1539, 4211, 979, 1642, 7591, 633, 688, 2948, 487, 2264, 1162, 1566, 2210, 1829, 1422, 870, 2882, 1926, 1667, 1147, 1191, 2536, 660, 1111, 2163, 895, 2272, 741, 2751, 956, 1047, 703, 15047, 352, 404, 830, 1235, 1160, 676, 651, 1156, 3167, 471, 799, 1203, 611, 1371, 1392, 752, 4925, 614, 942, 7542, 3284, 1107, 691, 968, 614, 916, 1095, 591, 845, 2139, 1196, 1794, 237, 4151, 919, 852, 1384, 298, 689, 517, 640, 1285, 362, 135, 1579, 678, 1160, 453, 700, 552, 1924, 460, 1072, 1442, 640, 761, 371, 657, 2015, 401, 826, 387, 376, 2285, 399, 126, 299, 708, 455, 995, 369, 737, 754, 1890, 1200, 7933, 2362, 5684, 494, 569, 948, 1422, 306, 258, 2816, 906, 352, 739, 496, 404, 505, 1160, 2348, 433, 533, 1690, 432, 1622, 443, 947, 381, 214, 570, 2120, 4079, 640, 1140, 1183, 696, 2580, 193, 654, 3224, 831, 404, 858, 1031, 236, 969, 736, 1242, 1080, 630, 1334, 556, 214, 340, 510, 595, 975, 1360, 239, 419, 314, 2007, 477, 1117, 966, 1023, 1017, 623, 2761, 268, 585, 594, 1667, 677, 5864, 246, 347, 3367, 1053, 838, 665, 212, 4151, 611, 304, 118, 422, 456, 342, 315, 772, 449, 803, 430, 1217, 187, 1438, 519, 596, 508, 515, 415, 1176, 813, 173, 325, 74, 542, 547, 476, 1254, 1056, 567, 4664, 148, 1852, 601, 985, 2061, 454, 1855, 377, 519, 1495, 7793, 547, 534, 213, 12706, 2034, 1756, 771, 497, 659, 716, 1207, 274, 705, 661, 597, 1025, 1762, 659, 216, 496, 500, 185, 546, 1455, 313, 458, 1166, 757, 373, 415, 295, 518, 643, 3594, 953, 1282, 1046, 316, 380, 1206, 358, 238, 1534, 239, 931, 1566, 357, 227, 602, 1543, 388, 339, 452, 1379, 1039, 1325, 788, 1494, 2171, 1825, 1542, 620, 418, 1490, 381, 954, 583, 747, 370, 3701, 1595, 121, 1541, 1393, 1079, 1065, 583, 994, 338, 1236, 485, 468, 460, 302, 95, 261, 472, 1121, 417, 1217, 826, 359, 306, 423, 870, 286, 955, 93, 450, 409, 574, 1659, 143, 589, 1761, 2249, 521, 591, 1368, 791, 205, 657, 657, 685, 596, 795, 319, 181, 645, 1326, 617, 786, 590, 1069, 729, 227, 520, 306, 707, 1463, 592, 1268, 1294, 582, 851, 367, 375, 292, 142, 222, 284, 779, 2610, 2512, 1062, 592, 326, 711, 249, 171, 524, 547, 767, 256, 514, 1681, 379, 1793, 304, 219, 2863, 94, 310, 400, 1414, 2075, 786, 1504, 476, 220, 924, 728, 481, 188, 1040, 381, 8863, 148, 811, 329, 1178, 438, 257, 495, 657, 185, 752, 408, 247, 465, 360, 614, 1285, 225, 226, 2522, 140, 179, 251, 868, 805, 1007, 458, 172, 224, 449, 528, 508, 1266, 889, 319, 1595, 283, 556, 645, 830, 1185, 732, 586, 195, 489, 275, 534, 699, 320, 670, 146, 395, 267, 394, 1225, 207, 1234, 1954, 1851, 1257, 322, 1282, 46, 963, 954, 269, 216, 440, 1768, 231, 149, 275, 952, 309, 323, 1693, 1836, 1620, 792, 794, 275, 1529, 387, 369, 488, 434, 128, 124, 71, 333, 823, 318, 1958, 2080, 1438, 204, 802, 368, 590, 794, 664, 487, 1008, 1110, 875, 892, 61, 1385, 483, 356, 424, 221, 17061, 818, 607, 977, 1431, 305, 366, 439, 188, 167, 3042, 928, 210, 170, 174, 97, 243, 1242, 64, 282, 196, 252, 1191, 670, 496, 1032, 478, 493, 210, 601, 424, 210, 67, 134, 224, 455, 129, 268, 285, 227, 871, 453, 374, 286, 4070, 187, 129, 442, 688, 334, 609, 181, 1244, 109, 241, 205, 662, 446, 1259, 322, 188, 304, 667, 1409, 92, 456, 870, 127, 386, 307, 2275, 393, 345, 247, 349, 559, 440, 1800, 207, 1541, 211, 284, 289, 130, 369, 147, 471, 77, 682, 110, 376, 1349, 5056, 24, 90, 250, 567, 306, 650, 522, 1339, 1227, 369, 658, 229, 294, 1505, 127, 117, 210, 1765, 247, 77, 629, 268, 640, 542, 801, 860, 1049, 220, 818, 338, 219, 252, 119, 1409, 1500, 1229, 1543, 367, 648, 286, 3376, 813, 697, 2736, 443, 385, 35, 266, 2110, 198, 532, 208, 303, 1098, 343, 109, 526, 179, 555, 860, 522, 187, 279, 149, 324, 209, 600, 466, 437, 259, 180, 88, 213, 598, 1446, 214, 430, 7682, 152, 72, 470, 236, 1353, 111, 494, 446, 379, 111, 1048, 231, 629, 1369, 518, 302, 347, 481, 486, 132, 73, 417, 218, 731, 196, 1340, 359, 270, 227, 2007, 1237, 248, 512, 1197, 90, 491, 423, 443, 506, 294, 484, 784, 125, 330, 484, 85, 181, 259, 213, 662, 137, 489, 356, 860, 399, 673, 886, 199, 559, 945, 186, 309, 96, 202, 133, 272, 31, 681, 578, 592, 874, 105, 190, 423, 1190, 726, 273, 98, 43, 182, 60, 3268, 1161, 1221, 321, 1476, 889, 145, 65, 494, 822, 371, 203, 1952, 75, 316, 164, 1135, 809, 380, 244, 36, 252, 229, 59, 377, 207, 1186, 292, 535, 151, 1246, 190, 625, 377, 2082, 1210, 197, 293, 83, 587, 266, 251, 1416, 687, 124, 976, 287, 330, 1629, 1261, 666, 451, 781, 527, 621, 1017, 1563, 137, 483, 870, 1505, 426, 465, 514, 838, 451, 116, 964, 566, 156, 798, 137, 465, 4008, 793, 201, 462, 97, 1827, 429, 515, 126, 337, 253, 709, 302, 201, 178, 112, 638, 10799, 2166, 344, 183, 669, 123, 2229, 1670, 870, 1025, 77, 482, 155, 199, 201, 556, 454, 138, 218, 29, 84, 59, 50, 277, 151, 229, 750, 221, 1273, 1902, 235, 247, 1219, 511, 431, 85, 218, 109, 116, 511, 358, 62, 187, 176, 296, 610, 184, 647, 114, 41, 175, 163, 469, 193, 284, 30, 803, 957, 107, 639, 193, 464, 1394, 132, 205, 46, 90, 253, 113, 219, 32, 78, 85, 184, 147, 446, 82, 114, 1203, 538, 101, 997, 1343, 2759, 439, 818, 745, 805, 366, 300, 609, 105, 3670, 132, 452, 306, 112, 245, 237, 578, 209, 422, 1116, 560, 169, 334, 145, 97, 60, 397, 3935, 112, 81, 407, 32, 175, 97, 192, 282, 504, 77, 110, 393, 132, 59, 157, 4068, 227, 884, 931, 1180, 147, 359, 55, 476, 290, 1008, 329, 379, 99, 1185, 38, 621, 537, 478, 321, 312, 348, 427, 201, 309, 555, 86, 83, 425, 495, 368, 488, 582, 247, 422, 343, 357, 761, 2610, 359, 165, 326, 1590, 292, 48, 277, 433, 258, 527, 508, 86, 565, 286, 418, 84, 42, 557, 643, 4285, 104, 113, 246, 1560, 206, 409, 866, 767, 699, 64, 83, 4125, 127, 242, 107, 1831, 1271, 1068, 1167, 2289, 453, 44, 180, 521, 169, 206, 173, 106, 1375, 705, 158, 60, 92, 1946, 540, 600, 461, 467, 814, 144, 1425, 55, 72, 198, 211, 434, 148, 555, 220, 76, 467, 515, 53, 208, 13, 303, 414, 1371, 107]
task12diff = [347, 295, 287, 286, 277, 268, 258, 219, 212, 208, 192, 181, 180, 174, 172, 171, 171, 168, 163, 156, 149, 146, 146, 136, 133, 130, 126, 124, 118, 115, 115, 113, 110, 110, 105, 97, 96, 95, 95, 91, 86, 83, 82, 82, 82, 81, 80, 74, 73, 73, 69, 68, 68, 60, 57, 55, 53, 49, 49, 48, 48, 45, 45, 42, 42, 41, 41, 40, 40, 39, 39, 39, 39, 39, 37, 36, 36, 36, 36, 34, 34, 34, 32, 32, 31, 30, 30, 30, 30, 29, 29, 29, 29, 29, 29, 29, 28, 28, 28, 28, 28, 28, 28, 28, 28, 27, 27, 27, 27, 27, 26, 26, 26, 26, 26, 26, 26, 26, 25, 25, 25, 25, 25, 24, 24, 24, 24, 24, 24, 24, 23, 23, 22, 22, 22, 22, 22, 22, 22, 21, 21, 21, 21, 21, 21, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]


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
                    if t and len(t) > 0:
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
        # vysledok je 217 (resp. ak si pochopil/a ze jedinecne nazvy, tak 100)
        record = dbcursor.fetchall()
        if len(record) == 100 or len(record) == 217:
            print(f'\t record all length: {len(record)}')
            return 2
        if len(record) == 1:
            print(f'\t result one: {record}')
            for col in record[0]:
                if col == 100 or col == 217: return 3
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
        if len(record) != 1307: return 0

        foundcities, foundpopulation2011, foundpopulation2012, founddiff, issorted = 0, 0, 0, 0, True
        index = 0

        print(f'>>> {len(task12population2011)},  {len(task12population2012)}, {len(task12cities)}, {len(task12diff)}')

        for line in record:
            for col in line:
                if col in task12cities:
                    foundcities += 1
                    if col != task12cities[index]:
                        issorted = False
                    break
            for col in line:
                if col in task12population2012:
                    foundpopulation2011 += 1
                    break
            for col in line:
                if col in task12population2011:
                    foundpopulation2012 += 1
                    break
            for col in line:
                for diff in task12diff:
                    if diff == col or -diff == col:
                        founddiff += 1
                        break
                else:
                    continue
                break
            index += 1
        print(f'sorted: {"true" if issorted else "false"}, cities: {foundcities}, 2012: {foundpopulation2012}, 2011: {foundpopulation2011}, diff: {founddiff}')
        points = 5
        if not issorted: points -= 1
        if foundcities != 1307: points -= 1
        if foundpopulation2012 != 1307: points -= 1
        if foundpopulation2011 != 1307: points -= 1
        if founddiff != 1307: points -= 1
        return points
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
