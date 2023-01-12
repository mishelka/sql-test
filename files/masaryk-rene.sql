--20
SELECT COUNT (*)
FROM (
	SELECT nazov
	FROM obec
	GROUP BY nazov
	HAVING COUNT (*) > 1
) AS Total

--1b
SELECT COUNT(*) as total, nazov
FROM obec
GROUP BY nazov
ORDER BY total DESC
LIMIT 1

--2.uloha
SELECT  COUNT (o.nazov)
FROM okres o, kraj k
WHERE o.id_kraj = k.id
AND k.nazov LIKE 'Kosicky%'


--3.uloha
SELECT COUNT  (ob.id)
FROM obec ob, okres o, kraj k
WHERE ob.id_okres = o.id
AND o.id_kraj = k.id
AND k.nazov LIKE 'Kos%'

--4.uloha
SELECT p.rok , p. id_obec, p.muzi + p.zeny AS Celkovypocet_ob, o.id, o.nazov
FROM populacia p , obec o
WHERE p.id_obec = o.id
AND p.rok = 2012
ORDER BY Celkovypocet_ob DESC
LIMIT 1;

-- 5.uloha
SELECT SUM (p.muzi + p.zeny) AS Sabinovpocetobyvatelov
FROM populacia p, obec ob, okres o
WHERE p.id_obec = ob.id
AND ob.id_okres = o.id
AND o.nazov LIKE 'Sabinov'
AND p.rok = 2012

--6.uloha
SELECT rok, SUM (muzi + zeny) Populacia
FROM populacia
WHERE rok BETWEEN 2009 AND 2012
GROUP BY rok
ORDER BY rok DESC

--7.uloha
SELECT ob.nazov, SUM (pop.muzi + pop.zeny) AS Populacia
FROM okres o
JOIN obec ob ON ob.id_okres = o.id
JOIN populacia pop ON pop.id_obec = ob.id
WHERE o.nazov LIKE 'Tvrdosin'
GROUP BY ob.nazov
ORDER BY Populacia
LIMIT 2

--8.Uloha
SELECT ob.nazov,  muzi+zeny AS Populacia
FROM obec ob
JOIN populacia po on po.id_obec = ob.id
WHERE rok = 2010
AND (muzi + zeny) < 5000
ORDER BY Populacia DESC

--9.uloha
SELECT obec.nazov, zeny, muzi, SUM(zeny+muzi) as Populacia, CAST(zeny as FLOAT) / CAST(muzi as FLOAT) as pomer FROM populacia p
INNER JOIN obec ON p.id_obec = obec.id
WHERE rok = 2012
GROUP BY obec.nazov, zeny, muzi
HAVING SUM(zeny + muzi) > 20000
ORDER BY pomer DESC
LIMIT 10;
--Funkciu CAST som si vyhladal na internete

--10.uloha 