-- 1
WITH multypleNameCount as (
SELECT count(*) multyCount FROM obec
group by nazov
)
SELECT count(*) FROM multypleNameCount WHERE multyCount > 1;
-- 2
SELECT nazov FROM obec
group by nazov
HAVING count(*) = (
    WITH multypleNameCount as (
    SELECT count(*) multyCount FROM obec
    group by nazov
    )
    SELECT MAX(multyCount) FROM multypleNameCount
    );
-- 3
SELECT count(*) FROM okres
JOIN kraj k on k.id = okres.id_kraj
WHERE k.nazov = 'Kosicky kraj';
-- 4
SELECT count(*) from obec
JOIN okres o on o.id = obec.id_okres
JOIN kraj k on k.id = o.id_kraj
WHERE k.nazov = 'Kosicky kraj';
-- 5
SELECT obec.nazov population FROM obec
JOIN populacia p on obec.id = p.id_obec
WHERE p.rok = '2012'
GROUP BY obec.nazov, (p.muzi+p.muzi)
HAVING (p.muzi+p.muzi) = (
    SELECT Max(population) FROM (
    SELECT (p.muzi+p.muzi) population FROM obec
    JOIN populacia p on obec.id = p.id_obec
    WHERE p.rok = '2012'
    ) maxPopulation
);
-- 6
SELECT sum(populacia.zeny+populacia.muzi) FROM populacia
JOIN obec o on o.id = populacia.id_obec
JOIN okres o2 on o2.id = o.id_okres
WHERE rok = '2012'
AND o2.nazov = 'Sabinov'
group by o2.id;
-- 7
SELECT rok, sum(muzi+populacia.zeny)populacia FROM populacia
GROUP BY rok
ORDER BY rok DESC;
-- 8
SELECT obec.nazov, sum(p.muzi + p.zeny) population FROM obec
JOIN populacia p on obec.id = p.id_obec
JOIN okres o on o.id = obec.id_okres
WHERE o.nazov = 'Tvrdosin'
and p.rok = '2011'
GROUP BY obec.id
HAVING sum(p.muzi + p.zeny) = (
    SELECT MIN(population) min FROM (
    SELECT sum(p.muzi + p.zeny) population FROM obec
    JOIN populacia p on obec.id = p.id_obec
    JOIN okres o on o.id = obec.id_okres
    WHERE o.nazov = 'Tvrdosin'
    and p.rok = '2011'
    GROUP BY obec.id
    ) minPopulation
);
-- 9
SELECT obec.nazov population FROM obec
JOIN populacia p on obec.id = p.id_obec
and p.rok = '2010'
where (p.muzi + p.zeny) < 5000;
-- 10
SELECT obec.nazov, ROUND((p.zeny::decimal / p.muzi::decimal),4) pomer_zien from obec
join populacia p on obec.id = p.id_obec
WHERE (p.zeny + p.muzi) > 20000 AND p.zeny > p.muzi
AND p.rok = '2012'
ORDER BY pomer_zien DESC
LIMIT 10;
-- 11
SELECT
    k.nazov,
    sum(p.zeny + p.muzi) populacia,
    count(distinct obec.id) obce,
    count(distinct o.id) okresy
FROM obec
JOIN okres o on o.id = obec.id_okres
JOIN kraj k on k.id = o.id_kraj
JOIN populacia p on obec.id = p.id_obec
WHERE p.rok = '2012'
GROUP BY k.id;
-- 12
WITH p2011 AS (SELECT populacia.id_obec id, (muzi+zeny) populacia FROM populacia WHERE rok = '2011'),
     p2012 AS (SELECT populacia.id_obec id,(muzi+zeny) populacia FROM populacia WHERE rok = '2012')
SELECT obec.nazov, p2012.populacia p2012, p2011.populacia p2009, (p2012.populacia-p2011.populacia) rozdiel  from obec
JOIN p2011 ON p2011.id = obec.id
JOIN p2012 ON p2012.id = obec.id
WHERE (p2012.populacia-p2011.populacia) < 0
ORDER BY rozdiel;
-- 13
SELECT count(*) FROM obec
JOIN populacia p on obec.id = p.id_obec
WHERE p.rok = '2012'
AND (p.muzi+p.zeny) < (
    SELECT avg(p.zeny+p.muzi) populacia FROM populacia p WHERE rok = '2012'
);





