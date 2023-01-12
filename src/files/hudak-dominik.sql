--20 obci maju rovnaky nazov
SELECT COUNT(*) AS pocet, nazov
FROM obec
GROUP BY nazov
HAVING COUNT(*) > 1;

--1b-- Lucka a Porubka
SELECT COUNT(*) as pocet, nazov
FROM obec
GROUP BY nazov
ORDER BY pocet DESC
LIMIT 1;

--2-- 11 okresov
SELECT COUNT (o.id_kraj)
FROM okres o, kraj k
WHERE o.id_kraj = k.id
AND k.nazov LIKE 'Kosicky%';

--3--
SELECT COUNT (ob.id_okres)
FROM obec ob, okres o, kraj k
WHERE ob.id_okres = o.id
	AND o.id_kraj = k.id
	AND k.nazov LIKE 'Kos%';
	
--4--
SELECT ob.nazov, p.rok, p.muzi + p.zeny as pocet_obyvatelov
FROM obec ob, populacia p
WHERE ob.id = p.id_obec
AND p.rok = 2012
ORDER BY pocet_obyvatelov DESC
LIMIT 1;

--5---58450--
SELECT SUM(p.muzi + p.zeny) as pocet_obyvatelov_sab_2012
FROM obec ob, populacia p, okres ok
WHERE ob.id = p.id_obec
AND ok.id = ob.id_okres
AND p.rok = 2012
AND ok.nazov LIKE 'Sabinov';

--6--
SELECT rok, SUM(muzi + zeny) as celkova_populacia
FROM populacia
WHERE rok BETWEEN 2009 AND 2012
GROUP BY rok
ORDER BY rok DESC;

--7--Su dve, preto limit 2--
SELECT ob.nazov, SUM(muzi + zeny) as celkova_populacia
FROM populacia p, obec ob, okres ok
WHERE p.id_obec = ob.id
AND ob.id_okres = ok.id
AND ok.nazov = 'Tvrdosin'
AND p.rok = 2011
GROUP BY ob.nazov
ORDER BY celkova_populacia
LIMIT 2;

--8--
SELECT ob.nazov, muzi + zeny as celkova_populacia, rok
FROM obec ob, populacia p
WHERE muzi + zeny <= 5000
AND rok = 2010
AND ob.id = p.id_obec
ORDER BY celkova_populacia;

--9--
SELECT ob.nazov, rok, zeny, muzi, CAST(zeny AS FLOAT) / CAST(muzi AS FLOAT) as pomer 
--Skusal som to aj cez ROUND ale pisalo mi to ze funkcia neexistuje a nevedel som preco--
FROM populacia p, obec ob
WHERE p.id_obec = ob.id
GROUP BY ob.nazov, zeny, muzi, rok
HAVING SUM(zeny + muzi) > 20000
AND zeny > muzi
AND rok = 2012
ORDER BY pomer DESC
LIMIT 10;

--10--Nevedel som


--11--Nevedel som


--12--Nevedel som ako overit tie obce s tym priemerom, mam iba priemer za ten rok 2012 
SELECT rok, ROUND(AVG(muzi + zeny)) AS priemerna_celkova_populacia
FROM populacia p, obec ob
WHERE rok = 2012
AND p.id_obec = ob.id
--AND muzi + zeny < priemerna_celkova_populacia
GROUP BY rok;



















