-- 1
SELECT count(DISTINCT o1.nazov)
FROM obec o1
WHERE (
    SELECT count(*)
    FROM obec o2
    WHERE o1.nazov = o2.nazov
) > 1;

-- 2
SELECT nazov
FROM obec
GROUP BY nazov
ORDER BY count(nazov) DESC
LIMIT 2;

-- 3
SELECT count(id) as pocetOkresov
FROM okres
WHERE id_kraj = (
    SELECT k.id
    FROM kraj k
    WHERE k.nazov like 'Kosicky kraj'
);

-- 4
SELECT count(obec.id) as pocetObci
FROM obec
JOIN okres o on obec.id_okres = o.id
JOIN kraj k on o.id_kraj = k.id
WHERE k.nazov = 'Kosicky kraj';

-- 5
SELECT o.nazov, sum(p.muzi + p.zeny) as pocetObyvatel
FROM obec o
JOIN populacia p on o.id = p.id_obec
WHERE p.rok = 2009 or p.rok = 2010 or p.rok = 2011 or p.rok = 2012
GROUP BY o.nazov
ORDER BY pocetObyvatel DESC
LIMIT 1;

-- 6
SELECT okres.nazov, sum(p.muzi + p.zeny) as pocetObyvatel
FROM okres
JOIN obec o on okres.id = o.id_okres
JOIN populacia p on o.id = p.id_obec
WHERE p.rok = 2012 and okres.nazov LIKE 'Sabinov'
GROUP BY okres.nazov;

-- 7
SELECT rok, sum(muzi + zeny) as obyvatel
FROM populacia
GROUP BY rok
ORDER BY rok DESC;

-- 8
SELECT obec.nazov as obec, sum(p.muzi + p.zeny) as obyvatel
FROM obec
JOIN okres o on obec.id_okres = o.id
JOIN populacia p on obec.id = p.id_obec
WHERE o.nazov LIKE 'Tvrdosin' AND p.rok = 2011
GROUP BY obec.nazov
ORDER BY obyvatel
LIMIT 2;

-- 9
SELECT obec.nazov
FROM obec
JOIN populacia p on obec.id = p.id_obec
WHERE p.rok = 2010 and p.muzi + p.zeny < 5000
ORDER BY obec.nazov;

-- 10
SELECT obec.nazov,
       round(p.zeny::DECIMAL / p.muzi::DECIMAL, 4) as pomer
FROM obec
JOIN populacia p on obec.id = p.id_obec
WHERE p.zeny > p.muzi and p.rok = 2012
GROUP BY obec.nazov, pomer
HAVING sum(p.muzi + p.zeny) > 20000
ORDER BY pomer DESC
LIMIT 10;

-- 11
SELECT kraj.nazov as kraj,
       count(DISTINCT o.id) as okresov,
       count(DISTINCT o2.id) as obci,
       sum(p.muzi + p.zeny) as obyvatelov
FROM kraj
JOIN okres o on kraj.id = o.id_kraj
JOIN obec o2 on o.id = o2.id_okres
JOIN populacia p on o2.id = p.id_obec
WHERE p.rok = 2012
GROUP BY kraj.nazov
ORDER BY obyvatelov DESC;

-- 12
SELECT o.nazov,
       pop2012.muzi + pop2012.zeny
           as obyvatelov2012,
       pop2011.muzi + pop2011.zeny
           as obyvatelov2011,
       (pop2011.muzi + pop2011.zeny) - (pop2012.muzi + pop2012.zeny)
           as pokles

FROM obec o
INNER JOIN populacia pop2011 on o.id = pop2011.id_obec
INNER JOIN populacia pop2012 on o.id = pop2012.id_obec

WHERE pop2011.rok = 2011 and pop2012.rok = 2012 and
      (pop2012.muzi + pop2012.zeny) - (pop2011.muzi + pop2011.zeny) < 0
GROUP BY o.nazov, pop2011.muzi, pop2011.zeny, pop2012.muzi, pop2012.zeny
ORDER BY pokles;

-- 13

