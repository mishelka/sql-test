--1 - ktore nazvy sa opakuju - pocet obci

SELECT COUNT(*) FROM obec o
WHERE o.nazov IN
(SELECT ob.nazov FROM obec ob GROUP BY ob.nazov
HAVING COUNT(*) > 1);

-- 2 - ktory nazov sa opakuje najviac krat

SELECT o.nazov, COUNT(o.nazov) FROM obec o
WHERE o.nazov IN
(SELECT ob.nazov FROM obec ob
GROUP BY ob.nazov
HAVING COUNT(*) >1
)
group by o.nazov
order by count desc
limit 2;

-- 3 Kolko okresov je v kosickom kraji?

SELECT COUNT(*) FROM okres o INNER JOIN kraj k
ON o.id_kraj = k.id
WHERE k.nazov LIKE 'Kosicky kraj';

-- 4 kolko ma kosicky kraj obci?
SELECT COUNT(*) FROM obec ob
INNER JOIN okres ok
ON ob.id_okres = ok.id
INNER JOIN kraj k
ON ok.id_kraj = k.id
WHERE k.nazov LIKE 'Kosicky kraj';

-- 5 Ktora obec bola na slovensku najvacsia v 2012 - nazov a pocet obyv.
SELECT o.nazov, (p.muzi + p.zeny) AS pocet_obyvatelov
FROM obec o INNER JOIN populacia p
ON p.id_obec = o.id
WHERE p.rok = 2012
GROUP BY o.nazov, p.muzi, p.zeny
HAVING (p.muzi + p.zeny) =
	(SELECT MAX(p.muzi + p.zeny) FROM populacia p INNER JOIN obec o
	ON p.id_obec = o.id
	WHERE p.rok = 2012);
	
-- 6 Kolko obyvatelov mal okres Sabinov v 2012
SELECT (SUM(p.muzi) + SUM (p.zeny)) AS pocet_obyvatelov
FROM obec o INNER JOIN populacia p
ON p.id_obec = o.id
INNER JOIN okres ok
ON o.id_okres = ok.id
WHERE p.rok = 2012 AND ok.nazov LIKE 'Sabinov';

-- 7 Vymierame alebo rastieme na Slovensku? Trend vyvoja za rozne roky od najnovsich
SELECT rok, SUM(muzi) + SUM(zeny) as pocet_obyvatelov
FROM populacia
GROUP BY rok
ORDER BY rok desc;

-- 8 najmensia obec v okrese Tvrdosin v 2011
SELECT o.nazov, (p.muzi + p.zeny) AS pocet_obyvatelov
FROM obec o INNER JOIN populacia p
ON p.id_obec = o.id
INNER JOIN okres ok
ON ok.id = o.id_okres
WHERE p.rok = 2011 AND ok.nazov LIKE 'Tvrdosin'
GROUP BY o.nazov, p.muzi, p.zeny
HAVING (p.muzi + p.zeny) =
	(SELECT MIN(p.muzi + p.zeny) FROM populacia p INNER JOIN obec o
	ON p.id_obec = o.id
	 INNER JOIN okres ok
	ON ok.id = o.id_okres
	WHERE p.rok = 2011 AND ok.nazov LIKE 'Tvrdosin');

-- 9 Obce s poctom obyvatelov menej ako 5000 v r.2010

SELECT o.nazov, (p.muzi + p.zeny) AS pocet_obyvatelov
FROM obec o INNER JOIN populacia p
ON p.id_obec = o.id
WHERE p.rok = 2010
GROUP BY o.nazov, p.muzi, p.zeny
HAVING (p.muzi + p.zeny) < 5000;

-- 10 obce(10) s populaciou nad 20 000 ktore mali v r.2012 najvacsi pomer zien voci muzom - 
--od najvacsieho pomeru k najmensiemu, aj pomer zaokruhleny na 4 desatinne miesta

SELECT o.nazov, ROUND(p.zeny::numeric / p.muzi::numeric, 4) AS pomer
FROM obec o INNER JOIN populacia p
ON p.id_obec = o.id
WHERE p.rok = 2012
GROUP BY o.nazov, p.muzi, p.zeny
HAVING (p.zeny + p.muzi) > 20000
ORDER BY pomer desc
LIMIT 10;

-- 11 - rok 2012 pre kazdy kraj pocet obyv, obci, okresov
SELECT k.nazov, SUM(p.muzi) + SUM(p.zeny) AS obyvatelia, COUNT(ob.id) AS obce,
COUNT(ok.id) AS okresy
FROM kraj k, okres ok, obec ob, populacia p
WHERE k.id = ok.id_kraj AND ok.id = ob.id_okres AND ob.id = p.id_obec
AND p.rok = 2012
GROUP BY k.nazov;

-- 12 - Obce ktore maju klesajuci trend - t.j. rozdiel v populacii dvoch poslednych rokov 
--mensi ako 0 - ich nazov, pocet obyv v poslednom roku, pocet obyv v predch. roku a rozdiel. 
--Zoradit vzostupne

SELECT o.nazov, (p.muzi + p.zeny) AS pocet_obyvatelov_2012,
(pop.muzi + pop.zeny) AS pocet_obyvatelov_2011,
(p.muzi + p.zeny) - (pop.muzi + pop.zeny) AS rozdiel
FROM obec o INNER JOIN populacia p
ON p.id_obec = o.id
INNER JOIN populacia pop
ON pop.id_obec = o.id
WHERE p.rok = 2012 AND pop.rok = 2011
GROUP BY o.nazov, p.muzi, p.zeny, pop.zeny, pop.muzi
HAVING (p.muzi + p.zeny) - (pop.muzi + pop.zeny) < 0
ORDER BY rozdiel ASC;

-- 13 - pocet obci kde je pocet obyvatelov v roku 2012 nizsi ko priemer v danom roku

SELECT COUNT(*) FROM
(SELECT o.nazov, (p.muzi + p.zeny) AS pocet_obyvatelov FROM obec o INNER JOIN populacia p
ON p.id_obec = o.id
WHERE p.rok = 2012
GROUP BY o.nazov, p.muzi, p.zeny
HAVING (p.muzi + p.zeny) <
	(SELECT AVG(p.muzi + p.zeny) FROM populacia p INNER JOIN obec o
	ON p.id_obec = o.id
	WHERE p.rok = 2012)) as count;
