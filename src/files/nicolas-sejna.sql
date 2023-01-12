-- 20
-- Nazvy niektorých obcí v tabulke obec sa opakuju, pretoze na Slovensku existuju obce, ktore maju rovnaky nazov. Zistite:
-- kolko je takych obci (1 dopyt)
SELECT COUNT (*)
FROM (
	SELECT nazov
	FROM obec
	GROUP BY nazov
	HAVING COUNT (id) > 1)
as duplicates;

-- 1b
-- Porubka
SELECT COUNT(*) as pocet_opakovani, nazov
FROM obec
GROUP BY nazov
HAVING COUNT(*) > 1
ORDER BY pocet_opakovani DESC
LIMIT 1;

-- 2
-- Kolko okresov sa nachadza v kosickom kraji?
SELECT COUNT (o.id_kraj)
-- SELECT o.nazov, o.id_kraj, k.id, k.nazov
FROM okres o, kraj k
WHERE o.id_kraj = k.id
	AND k.nazov LIKE 'Kos%';
	
-- 3
-- A kolko ma kosicky kraj obci? Pri tvorbe dopytu vam moze pomoct informacia, ze trenciansky kraj ma spolu 276 obci.
-- Kosicky kraj ma 461 obci
SELECT COUNT (ob.id)
-- SELECT ob.id, ob.nazov, ob.id_okres, o.id, o.id_kraj, k.id
FROM obec ob, okres o, kraj k
WHERE ob.id_okres = o.id
AND o.id_kraj = k.id
	AND k.nazov LIKE 'Kos%';


-- 4
-- Zistite, ktora obec (mesto) bola na Slovensku najvacsia v roku 2012. 
-- Pri tvorbe dopytu vam moze pomoct informacia, ze tato obec (mesto) bola najvacsia na Slovensku v rokoch 2009-2012,
-- avsak ma v populacii klesajucu tendenciu. Vo vysledku vypiste jej nazov a pocet obyvatelov.
-- Bratislava - Petrzalka 105 468
SELECT p.rok, p.id_obec, p.muzi + p.zeny as pocet_ob, o.id, o.nazov
FROM populacia p, obec o
WHERE p.id_obec = o.id
	AND p.rok = 2012
	ORDER BY pocet_ob desc
	LIMIT 1;
	
-- 5
--Kolko obyvatelov mal okres Sabinov v roku 2012? 
--Pri tvorbe dopytu vam moze pomoct informacia, ze okres Dolny Kubin mal v roku 2010 39553 obyvatelov.
-- Odpoved 58450
SELECT SUM (p.muzi + p.zeny)
from populacia p, obec ob, okres o
WHERE p.id_obec = ob.id
AND ob.id_okres = o.id
AND o.nazov LIKE 'Sabinov'
AND p.rok = 2012;

-- 6
--Ako sme na tom na Slovensku? Vymierame alebo rastieme? 
--Zobrazte trend vývoja populácie za jednotlivé roky a výsledok zobrazte od najnovších informácií po najstaršie.

SELECT p.rok, SUM(p.muzi + p.zeny) as pocet_obyvatelov
FROM populacia p
WHERE p.rok BETWEEN 2009 AND 2012
GROUP BY p.rok
ORDER BY p.rok desc;

-- 7
-- Zistite, ktora obec alebo obce boli najmensie v okrese Tvrdosin v roku 2011. 
-- Pri tvorbe dopytu vam moze pomoct informacia, 
-- ze v okrese Ruzomberok to bola v roku 2012 obec Potok s poctom obyvatelov 107.
-- Najmensie su 2 obce, Stefanov nad Oravou a Cimhova s 659 obyvatelmi

SELECT SUM (p.muzi + p.zeny) as pocet_obyv, ob.nazov
from populacia p, obec ob, okres o
WHERE p.id_obec = ob.id
AND ob.id_okres = o.id
AND o.nazov LIKE 'Tvrd%'
AND p.rok = 2011
GROUP BY ob.nazov
ORDER BY pocet_obyv
LIMIT 2;

-- 8
--Zistite vsetky obce (ich nazvy), ktore mali v roku 2010 pocet obyvatelov do 5000. 
--Pri tvorbe dopytu vam moze pomoct informacia, ze v roku 2009 bolo tychto obci o 1 viac ako v roku 2010

SELECT p.muzi + p.zeny as pocet_obyvatelov, ob.nazov
FROM populacia p, obec ob
WHERE p.id_obec = ob.id
AND p.muzi + p.zeny < 5000
AND rok = 2010
ORDER BY pocet_obyvatelov;

-- 9
--Zistite 10 obci s populaciou nad 20000,
--ktore mali v roku 2012 najvacsi pomer zien voci muzom (viac zien v obci ako muzov). 
--Tychto 10 obci vypiste v poradi od najvacsieho pomeru po najmensi. 
--Vo vysledku okrem nazvu obce vypiste aj pomer zaokruhleny na 4 desatinne miesta. 
--Pri tvorbe dopytu vam moze pomoct informacia, ze v roku 2011 bol tento pomer pre obec Kosice  - Juh 1,1673.

-- viem ze ::numeric sme nemali ale uz som bol zufaly a google pomohol

SELECT ROUND(p.zeny/p.muzi::numeric,4) as pomer, p.muzi + p.zeny as pocet_obyv, p.muzi, p.zeny, p.rok,
		o.nazov
from populacia p, obec o
where p.id_obec = o.id
	and p.muzi + p.zeny > 20000
	and p.rok = 2012
ORDER BY pomer desc
Limit 10;

-- 10
--Vypiste sumarne informacie o stave Slovenska v roku 2012 v podobe tabulky, 
--ktora bude obsahovat pre kazdy kraj informacie o pocte obyvatelov, o pocte obci a pocte okresov. 

SELECT SUM(p.muzi + p.zeny) as pocet_obyvatelov, COUNT(DISTINCT ob.id) as pocet_obci, 
		COUNT(DISTINCT o.id) as pocet_okresov, k.nazov
FROM populacia p, kraj k, okres o, obec ob
WHERE p.id_obec = ob.id
	AND ob.id_okres = o.id
	AND o.id_kraj = k.id
GROUP BY k.nazov;

-- 11
--To, ci vymierame alebo rastieme, sme uz zistovali. Ale ktore obce su na tom naozaj zle? 
--Kde by sa nad touto otazkou mali naozaj zamysliet? 
--Zobrazte obce, ktore maju klesajuci trend (rozdiel v populacii dvoch poslednych rokov je mensi ako 0) - 
--vypiste ich nazov, pocet obyvatelov v poslednom roku, .
--pocet obyvatelov v predchadzajucom roku a rozdiel v populacii posledneho oproti predchadzajucemu roku. 
--Zoznam utriedte vzostupne podla tohto rozdielu od obci s najmensi prirastkom obyvatelov po najvacsi.

SELECT p.muzi + p.zeny as pocet_obyv, p.rok, ob.nazov 
from populacia p, obec ob
where p.id_obec = ob.id;

-- nic mi nenapada pri ulohe c. 11

--  12
--Zistite pocet obci, ktorych pocet obyvatelov v roku 2012 je nizsi, ako bol slovensky priemer v danom roku.

CREATE OR REPLACE VIEW priemer
AS
SELECT ROUND (AVG(muzi+zeny)) as populacia_sr
from populacia
WHERE rok = 2012;

SELECT nazov, p.muzi + p.zeny as pocet_ob, populacia_sr, obec.id
FROM obec, populacia p, priemer
WHERE p.id_obec = obec.id
AND p.muzi + p.zeny < populacia_sr

	  



