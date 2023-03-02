-- 1
SELECT COUNT(pocet) AS pocet_opakujucich_sa_nazvov
FROM (
    SELECT Count(nazov) AS pocet
    FROM obec
    GROUP BY nazov
    HAVING COUNT(nazov)>1
     ) AS duplikaty;
-- 2
SELECT nazov
FROM obec
GROUP BY nazov
HAVING COUNT(nazov) = (
    SELECT MAX(najviac_pouzite_nazvy)
    FROM (
        SELECT COUNT(nazov) AS najviac_pouzite_nazvy
        FROM obec
        GROUP BY nazov
         ) AS max
    );
-- 3
SELECT COUNT(*) AS pocet_okresov_KE
FROM kraj
JOIN okres ON kraj.id = okres.id_kraj
WHERE kraj.nazov LIKE 'Kosicky kraj';
-- 4
SELECT COUNT(*) AS pocet_obci_KE
FROM kraj
JOIN okres ON kraj.id = okres.id_kraj
JOIN obec ON okres.id = obec.id_okres
WHERE kraj.nazov LIKE 'Kosicky kraj';
-- 5
SELECT nazov, SUM(muzi+zeny) AS pocet_obyvatelov
FROM obec
JOIN populacia ON obec.id = populacia.id_obec
WHERE populacia.rok = 2012
GROUP by nazov
HAVING SUM(muzi+zeny) = (
    SELECT MAX(najvacsia_obec)
    FROM (
        SELECT SUM(muzi+zeny) AS najvacsia_obec
        FROM obec
        JOIN populacia ON obec.id = populacia.id_obec
        WHERE populacia.rok = 2012
        GROUP by nazov
         ) AS max
    );
-- 6
SELECT SUM(muzi+zeny) AS pocet_obyvatelov
FROM okres
JOIN obec ON okres.id = obec.id_okres
JOIN populacia ON obec.id = populacia.id_obec
WHERE okres.nazov LIKE 'Sabinov'
AND populacia.rok = 2012;
-- 7
SELECT rok, SUM(muzi + zeny) AS pocet_obyvatelov,
       SUM(muzi + zeny) - LAG(SUM(muzi + zeny)) OVER (ORDER BY rok) AS trend
FROM populacia
GROUP BY rok
ORDER BY rok DESC;
-- 8
SELECT obec.nazov, SUM(muzi+zeny) AS najmensi_pocet
FROM obec
JOIN okres ON obec.id_okres = okres.id
JOIN populacia ON obec.id = populacia.id_obec
WHERE rok = 2011
AND okres.nazov LIKE 'Tvrdosin'
GROUP BY obec.nazov
HAVING SUM(muzi+zeny) = (
    SELECT MIN(min_pocet_obyvatelov)
    FROM (
        SELECT SUM(muzi+zeny) AS min_pocet_obyvatelov
        FROM obec
        JOIN okres ON obec.id_okres = okres.id
        JOIN populacia ON obec.id = populacia.id_obec
        WHERE rok = 2011
        AND okres.nazov LIKE 'Tvrdosin'
        GROUP BY obec.nazov
         ) AS min
    );
-- 9
SELECT nazov
FROM obec
JOIN populacia ON obec.id = populacia.id_obec
WHERE rok = 2010
GROUP BY nazov
HAVING SUM(muzi+zeny)<=5000;
-- 10
SELECT nazov, ROUND(SUM(zeny)/CAST(SUM(muzi) AS DECIMAL(18,4)),4) AS pomer
FROM obec
JOIN populacia ON obec.id = populacia.id_obec
WHERE rok = 2012
AND zeny != 0
GROUP BY nazov
HAVING SUM(muzi+zeny)>20000
ORDER BY ROUND(SUM(zeny)/CAST(SUM(muzi) AS DECIMAL(18,4)),4) DESC
LIMIT 10;
-- 11

CREATE VIEW stav_SK_2012 AS
SELECT kraj.nazov, SUM(muzi+zeny) AS pocet_obyvatelov, COUNT(obec.id) AS pocet_obci,
       COUNT(DISTINCT okres.id) AS pocet_okresov
FROM kraj
JOIN okres ON kraj.id = okres.id_kraj
JOIN obec ON okres.id = obec.id_okres
JOIN populacia ON obec.id = populacia.id_obec
WHERE rok = 2012
GROUP BY kraj.nazov;

select * from stav_SK_2012;

-- 12
SELECT obec.nazov, SUM(p2012.muzi+p2012.zeny) AS posledny_rok, SUM(p2011.muzi+p2011.zeny) AS predosly_rok,
       SUM(p2012.muzi+p2012.zeny) - SUM(p2011.muzi+p2011.zeny) AS rozdiel
FROM obec
JOIN populacia p2012 ON obec.id = p2012.id_obec AND p2012.rok = 2012
JOIN populacia p2011 ON obec.id = p2011.id_obec AND p2011.rok = 2011
GROUP BY obec.nazov
ORDER BY rozdiel;
-- 13
SELECT COUNT(*) AS pocet_obci
FROM (
    SELECT obec.id, SUM(muzi+zeny) AS pocet_obyvatelov
    FROM obec
    JOIN populacia ON obec.id = populacia.id_obec
    WHERE rok = 2012
    GROUP BY obec.id
    HAVING SUM(muzi+zeny) < (
        SELECT AVG(muzi+zeny)
        FROM populacia
        WHERE rok = 2012
    )
) AS vnorene;


























