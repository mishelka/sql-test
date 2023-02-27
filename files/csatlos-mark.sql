-- 1 uloha

SELECT COUNT(DISTINCT nazov)
FROM obec
WHERE nazov IN (
  SELECT nazov
  FROM obec
  GROUP BY nazov
  HAVING COUNT(*) > 1
);

-- 2 uloha
SELECT obec.nazov, COUNT(*)
FROM obec
GROUP BY obec.nazov
HAVING COUNT(*) = (
  SELECT MAX(count)
  FROM (
    SELECT COUNT(*) AS count
    FROM obec
    GROUP BY nazov
  ) AS subquery
);

-- 3 uloha
SELECT COUNT(*) as pocet_okresov_kosice
FROM okres o
JOIN kraj k ON o.id_kraj = k.id
WHERE k.nazov = 'Kosicky kraj';

-- 4 uloha
SELECT COUNT(o.id) AS pocet_obci
FROM kraj k
JOIN okres ok ON k.id = ok.id_kraj
JOIN obec o ON ok.id = o.id_okres
WHERE k.nazov = 'Kosicky kraj';
-- 5 uloha

SELECT o.nazov AS obec, p.muzi + p.zeny AS pocet_obyvatelov
FROM obec o
JOIN populacia p ON o.id = p.id_obec
WHERE p.rok = 2012
AND p.muzi + p.zeny = (
    SELECT MAX(p2.muzi + p2.zeny)
    FROM populacia p2
    WHERE p2.rok = 2012
);

-- 6 uloha
SELECT SUM(p.muzi + p.zeny) AS celkovo
FROM populacia p
JOIN obec o ON o.id = p.id_obec
JOIN okres ok ON ok.id = o.id_okres
WHERE ok.nazov = 'Sabinov' AND p.rok = 2012;
-- 7 uloha
SELECT rok, SUM(muzi + zeny) AS celkova_populacia
FROM populacia
GROUP BY rok
ORDER BY rok DESC;
-- 8 uloha
SELECT o.nazov, p.muzi + p.zeny AS "Pocet obyvatelov"
FROM populacia p
INNER JOIN obec o ON p.id_obec = o.id
INNER JOIN okres ok ON o.id_okres = ok.id
WHERE ok.nazov = 'Tvrdosin' AND p.rok = 2011 AND (p.muzi + p.zeny) = (
  SELECT MIN(muzi + zeny)
  FROM populacia p2
  INNER JOIN obec o2 ON p2.id_obec = o2.id
  INNER JOIN okres ok2 ON o2.id_okres = ok2.id
  WHERE ok2.nazov = 'Tvrdosin' AND p2.rok = 2011
)
ORDER BY o.nazov ASC;
-- 9 uloha
SELECT o.nazov
    FROM obec o
    JOIN populacia p ON o.id = p.id_obec
    WHERE p.rok = 2010 AND p.muzi + p.zeny <= 5000;
-- 10 uloha
SELECT obec.nazov, ROUND(populacia.zeny::numeric/populacia.muzi::numeric, 4) AS pomer
FROM obec
JOIN populacia ON obec.id = populacia.id_obec
WHERE populacia.rok = 2012
AND populacia.zeny > populacia.muzi
AND (populacia.muzi + populacia.zeny) > 20000
ORDER BY pomer DESC
LIMIT 10;
-- 11 uloha
SELECT k.nazov AS kraj,
       SUM(pt.muzi + pt.zeny) AS pocet_obyvatelov,
       COUNT(ob.nazov) AS pocet_obci,
       COUNT(o.nazov) AS pocet_okresov
FROM kraj k
 JOIN okres o ON k.id = o.id_kraj
 JOIN obec ob on o.id = ob.id_okres
 JOIN populacia pt ON ob.id = pt.id_obec AND pt.rok = 2012
GROUP BY k.nazov
ORDER BY k.nazov;
-- 12 uloha
SELECT obec.nazov,
       pop2012.zeny + pop2012.muzi AS pocet_obyvatelov_2012,
       pop2011.zeny + pop2011.muzi AS pocet_obyvatelov_2011,
       (pop2012.zeny + pop2012.muzi) - (pop2011.zeny + pop2011.muzi) AS rozdiel
FROM obec
JOIN (
  SELECT id_obec, muzi, zeny FROM populacia WHERE rok = 2012
) AS pop2012 ON obec.id = pop2012.id_obec
JOIN (
  SELECT id_obec, muzi, zeny FROM populacia WHERE rok = 2011
) AS pop2011 ON obec.id = pop2011.id_obec
WHERE (pop2012.zeny + pop2012.muzi) - (pop2011.zeny + pop2011.muzi) > 0
ORDER BY rozdiel;
-- 13 uloha
SELECT COUNT(*) AS pocet_obci
FROM (
  SELECT id_obec, SUM(muzi) + SUM(zeny) AS pocet_obyvatelov
  FROM populacia
  WHERE rok = 2012
  GROUP BY id_obec
  HAVING SUM(muzi) + SUM(zeny) < (
    SELECT AVG(pocet_obyvatelov)
    FROM (
      SELECT id_obec, SUM(muzi) + SUM(zeny) AS pocet_obyvatelov
      FROM populacia
      WHERE rok = 2012
      GROUP BY id_obec
    ) AS subquery
  )
) AS subquery2;





