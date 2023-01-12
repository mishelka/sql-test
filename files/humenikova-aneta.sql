-- 20
SELECT COUNT (*) pocet_duplikatov
FROM (
SELECT nazov FROM obec
GROUP BY nazov
HAVING COUNT (*) > 1 )
AS pocet_duplikatov;


-- 1b)
SELECT nazov, count(nazov) FROM obec
GROUP BY nazov
HAVING COUNT(nazov) > 1
ORDER BY COUNT(nazov) desc LIMIT 2;

-- 2
SELECT count (o.id)
FROM okres o, kraj k
WHERE  o.id_kraj = k.id
AND k.nazov like 'Kos%'

-- 3
SELECT count(ob.nazov)
FROM obec ob, okres ok, kraj kr
WHERE ob.id_okres = ok.id
AND ok.id_kraj = kr.id
AND kr.nazov like 'Kos%'

-- 4
 SELECT ob.nazov , (muzi + zeny) as pocet_obyvatelov
 FROM obec ob
 JOIN populacia pop on pop.id_obec = ob.id
 WHERE rok = 2012
 GROUP BY ob.nazov, pocet_obyvatelov
 ORDER BY pocet_obyvatelov DESC LIMIT 1   -- 4

-- 5
SELECT SUM(muzi + zeny) as pocet_obyvatelov
FROM obec ob
JOIN populacia pop ON ob.id = pop.id_obec
JOIN okres ok ON ok.id = ob.id_okres
WHERE pop.rok = 2012
AND ok.nazov like 'Sab%'  -- 5

--6
SELECT rok , SUM (muzi + zeny) AS populacia
FROM populacia
WHERE rok BETWEEN 2009 AND 2012
GROUP BY rok
ORDER BY rok DESC -- 6

-- 7
SELECT ob.nazov, MIN (pop.muzi + pop.zeny)
FROM okres ok
JOIN obec ob ON ob.id_okres = ok.id
JOIN populacia pop ON pop.id_obec = ob.id
WHERE ok.nazov like 'Tvrdosin'
AND pop.rok = 2011
GROUP BY ob.nazov
ORDER BY MIN  -- 7

-- 8
SELECT ob.nazov, muzi + zeny AS pocet_obyvatelov
FROM obec ob
JOIN populacia pop ON pop.id_obec = ob.id
WHERE rok = 2010
AND (muzi + zeny) < 5000 -- 8

--ZVYSOK SOM BOHUZIAL NEVEDELA


