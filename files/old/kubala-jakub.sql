--20
SELECT COUNT(*)
FROM (
	SELECT nazov
	FROM obec
	GROUP BY nazov
	HAVING COUNT(*) > 1
) as ok;

--1b)
SELECT nazov, COUNT(*)
FROM obec
GROUP BY nazov
ORDER BY COUNT(*) DESC
LIMIT 2;
--Porubka
--Lucka

--2 
SELECT COUNT(*)
FROM kraj k, okres o
WHERE k.id = o.id_kraj
	AND k.nazov = 'Kosicky kraj';
--11

--3
SELECT COUNT(*)
FROM obec o, kraj k, okres ok
WHERE o.id_okres = ok.id
	AND ok.id_kraj = k.id
		AND k.nazov = 'Kosicky kraj';
		
--4
SELECT p.rok, o.nazov, p.muzi + p.zeny as celkovy_pocet
FROM obec o, populacia p
WHERE p.id_obec = o.id
	AND p.rok = 2012
ORDER BY celkovy_pocet DESC
LIMIT 1;

--5
SELECT SUM(p.muzi + p.zeny)
from populacia p, obec o, okres ok
WHERE p.id_obec = o.id
AND o.id_okres = ok.id
AND ok.nazov = 'Sabinov'
AND p.rok = 2012;

--6
SELECT p.rok, SUM(muzi + zeny) as celkovo
FROM populacia p
WHERE rok 
BETWEEN 2009 AND 2012
GROUP BY rok
ORDER BY rok DESC;

--7
SELECT o.nazov, p.muzi + p.zeny as pop, p.rok
FROM okres ok, populacia p, obec o
WHERE p.id_obec = o.id 
	AND o.id_okres = ok.id
	AND ok.nazov = 'Tvrdosin' AND p.rok = 2011
ORDER BY pop ASC
LIMIT 2;

--8
SELECT o.nazov, muzi + zeny as pop, rok
FROM obec o, populacia p
WHERE p.id_obec = o.id
	AND muzi + zeny < 5000 AND rok = 2010
ORDER BY pop ASC;
	
--9




--10


--11


--12
CREATE OR REPLACE VIEW priemer5
AS
SELECT ROUND(AVG(muzi + zeny)) as pop
FROM populacia
WHERE rok = 2012;


SELECT o.nazov, p.muzi + p.zeny as pocet, pop
FROM obec o, populacia p, priemer5
WHERE p.id_obec = o.id
AND p.muzi + p.zeny < pop
GROUP BY nazov, pop, pocet
ORDER BY pocet ASC