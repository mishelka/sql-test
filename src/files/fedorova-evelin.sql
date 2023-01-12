-- 20
SELECT obec.nazov
FROM obec
GROUP BY nazov
HAVING COUNT (*) > 1;

-- 1b
SELECT nazov, COUNT(nazov) as mnozstvo
FROM obec
GROUP BY nazov
ORDER BY mnozstvo DESC;

-- 2
SELECT
	o.id_kraj,
	o.nazov,
	k.id, k.nazov
FROM okres o, kraj k
WHERE o.id_kraj = k.id
AND k.nazov LIKE 'Kosic%' ;

-- 3
SELECT COUNT(*)
FROM obec o
WHERE o.id_okres BETWEEN 801 AND 811;

-- 4
SELECT o.nazov, (po.muzi + po.zeny) as obyvatelia
FROM obec o
JOIN populacia po on o.id = po.id_obec
WHERE po.rok BETWEEN 2009 AND 2012
ORDER BY obyvatelia DESC
LIMIT 1;

-- 5
SELECT
	SUM (muzi + zeny) as obyvatelia
FROM obec o
JOIN okres k on k.id = o.id_okres
JOIN populacia po on o.id = po.id_obec
WHERE po.rok = 2012
AND k.nazov LIKE 'Sabin%'
GROUP BY k.nazov;

-- 6
SELECT SUM (muzi + zeny) FROM populacia
WHERE rok BETWEEN 2009 AND 2012
GROUP BY rok
ORDER BY rok DESC;

-- 7
SELECT o.nazov, SUM (po.muzi + po.zeny )
FROM okres k
JOIN obec o ON o.id_okres = k.id
JOIN populacia po ON po.id_obec = o.id
WHERE k.nazov LIKE 'Tvrdosin'
	AND po.rok = 2011
GROUP BY o.nazov
ORDER BY SUM;

-- 8
SELECT o.nazov, po.muzi + po.zeny AS pocet
FROM obec o
JOIN populacia po ON po.id_obec = o.id
WHERE rok = 2010
AND (muzi + zeny) < 5000;

-- 9
SELECT o.nazov,
	SUM(muzi + zeny) as Obyvatelia
FROM populacia p
JOIN obec o ON p.id_obec = o.id
WHERE rok = 2012
GROUP BY o.nazov,zeny, muzi
HAVING SUM(muzi + zeny) > 20000
AND zeny > muzi
ORDER BY obyvatelia DESC
LIMIT 10;

-- 10


-- 11


-- 12


