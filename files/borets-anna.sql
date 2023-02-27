-- 1
SELECT count(*) AS count
FROM (SELECT count(*)
      FROM obec
      GROUP BY nazov
      HAVING count(*) > 1) AS duplicit;

-- 2
SELECT nazov
FROM (SELECT nazov, rank() over (order by count(*) desc) as najcastejsi_nazov_obce
      FROM obec
      GROUP BY nazov) foo
WHERE najcastejsi_nazov_obce = 1;

-- 3
SELECT count(*) as okresy_pocet
FROM okres
         JOIN kraj k on okres.id_kraj = k.id
WHERE k.nazov LIKE 'Kosicky%';

-- 4
SELECT count(*) as obce_pocet
FROM obec
         JOIN okres o on obec.id_okres = o.id
         JOIN kraj k on o.id_kraj = k.id
WHERE k.nazov LIKE 'Kosicky%';

-- 5
SELECT nazov, max(muzi + zeny) as pocet_obyvatelov
FROM (SELECT o.nazov, rank() over (order by MAX(muzi + zeny) desc) as pocet_obyvatelov
      FROM populacia
               JOIN obec o on o.id = populacia.id_obec
      WHERE populacia.rok = 2012
      GROUP BY o.nazov) as foo,
     populacia
WHERE pocet_obyvatelov = 1
  AND rok = 2012
GROUP BY nazov, pocet_obyvatelov;

-- 6
SELECT o2.nazov, sum(muzi + zeny) AS pocet_obyvatelov
FROM populacia
         JOIN obec o on o.id = populacia.id_obec
         JOIN okres o2 on o2.id = o.id_okres
WHERE o2.nazov = 'Sabinov'
  AND populacia.rok = 2012
GROUP BY o2.nazov;

-- 7
SELECT rok, sum(muzi + zeny) as pocet_obyvatelov, rank() over (order by sum(muzi + zeny) desc) as max_population
FROM populacia
GROUP BY rok
ORDER BY rok desc;

-- 8
SELECT nazov, foo.pocet_obyvatelov
FROM (SELECT o.nazov, rank() over (order by min(muzi + zeny) asc) as rank, min(muzi + zeny) as pocet_obyvatelov
      FROM populacia
               JOIN obec o on o.id = populacia.id_obec
               JOIN okres o2 on o.id_okres = o2.id
      WHERE populacia.rok = 2011
        AND o2.nazov = 'Tvrdosin'
      GROUP BY o.nazov) as foo,
     populacia
WHERE rank = 1
  AND rok = 2011
GROUP BY nazov, foo.pocet_obyvatelov;

-- 9
SELECT nazov
FROM obec
JOIN populacia p on obec.id = p.id_obec
WHERE (p.muzi + p.zeny)<5000 AND p.rok = 2010;


-- 10
SELECT nazov, round(1.0 * zeny/muzi,4) as pomer_zeny_muzi
FROM obec
JOIN populacia p on obec.id = p.id_obec
WHERE (p.muzi + p.zeny)>20000 AND rok = 2012
ORDER BY pomer_zeny_muzi desc
LIMIT 10;


-- 11 with view
CREATE VIEW okresy
    AS (SELECT k.nazov, count(*) as okresy_pocet
FROM okres
         JOIN kraj k on okres.id_kraj = k.id
GROUP BY k.nazov);

SELECT kraj.nazov, sum(p.muzi + p.zeny) as population,count(o2.id) as obce_pocet,okresy_pocet
    FROM kraj
         JOIN okres o on kraj.id = o.id_kraj
         JOIN obec o2 on o.id = o2.id_okres
         JOIN populacia p on o2.id = p.id_obec
    JOIN okresy o3 on kraj.nazov = o3.nazov
     WHERE p.rok = 2012
GROUP BY kraj.nazov, okresy_pocet
ORDER BY kraj.nazov;

-- 12
WITH pocet_2012
         AS (SELECT o.nazov, sum(muzi + zeny) as pocet_obyvatelov_2012
             FROM populacia
                      JOIN obec o on o.id = populacia.id_obec
             WHERE rok = 2012
             GROUP BY o.nazov),
     pocet_2011
         AS (SELECT o.nazov, sum(muzi + zeny) as pocet_obyvatelov_2011
             FROM populacia
                      JOIN obec o on o.id = populacia.id_obec
             WHERE rok = 2011
             GROUP BY o.nazov)

SELECT pocet_2012.nazov, pocet_obyvatelov_2011, pocet_obyvatelov_2012, (pocet_obyvatelov_2012 - pocet_obyvatelov_2011) as rozdiel
FROM pocet_2011
         join pocet_2012 on pocet_2011.nazov = pocet_2012.nazov
WHERE (pocet_obyvatelov_2012 - pocet_obyvatelov_2011)<0
ORDER BY rozdiel;


-- 13
SELECT count(*) as obce_pocet_obyv_menej_priemeru
FROM obec
JOIN populacia p on obec.id = p.id_obec
WHERE p.rok = 2012
AND (p.muzi + p.zeny) < (
SELECT AVG(populacia.muzi + populacia.zeny)
FROM populacia WHERE populacia.rok = 2012);





