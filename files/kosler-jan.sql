-- 1
SELECT sum(count)
FROM
   (SELECT obec.nazov, COUNT(*) as count
    FROM obec
    GROUP BY obec.nazov
    HAVING COUNT(*) > 1
   ) foo;

-- 2
SELECT nazev, pocet
FROM
   (SELECT obec.nazov as nazev, COUNT(*) as pocet
    FROM obec
    GROUP BY obec.nazov
    HAVING COUNT(*) > 1) foo
    WHERE pocet = (SELECT MAX(pocet)
                   FROM
                    (SELECT obec.nazov as nazev, COUNT(*) as pocet
                    FROM obec
                    GROUP BY obec.nazov
                    HAVING COUNT(*) > 1) foo
                   );

-- 3
SELECT COUNT(okres.id)
FROM okres
INNER JOIN kraj k on k.id = okres.id_kraj
WHERE k.nazov LIKE 'Kosicky kraj';

-- 4
SELECT COUNT(obec.id) FROM obec
INNER JOIN okres o on o.id = obec.id_okres
INNER JOIN kraj k on k.id = o.id_kraj
WHERE k.nazov LIKE 'Kosicky kraj';

-- 5
SELECT o.nazov, p.muzi + p.zeny as pocet_obyvatel
FROM populacia p
INNER JOIN obec o on o.id = p.id_obec
WHERE p.muzi + p.zeny = (
                  SELECT MAX(foo.pocet_obyvatel)
                  FROM (
                        SELECT o.nazov, p.muzi + p.zeny as pocet_obyvatel
                        FROM populacia p
                        INNER JOIN obec o on o.id = p.id_obec
                        WHERE rok = 2012
                        ) foo );

-- 6
SELECT SUM( p.muzi + p.zeny ) as pocet_obyvatel
FROM populacia p
INNER JOIN obec o on o.id = p.id_obec
INNER JOIN okres o2 on o2.id = o.id_okres
GROUP BY o2.nazov, rok
HAVING o2.nazov LIKE 'Sabinov' AND rok = 2012;

-- 7
SELECT foo.rok, pocet_obyvatel - LAG(pocet_obyvatel) OVER ( ORDER BY rok )
FROM
   (SELECT rok, SUM( p.muzi + p.zeny ) as pocet_obyvatel
    FROM populacia p
    GROUP BY rok
   ) foo
ORDER BY rok DESC ;

-- 8
SELECT o.nazov, p.muzi + p.zeny as pocet_obyvatel
FROM populacia p
INNER JOIN obec o on o.id = p.id_obec
INNER JOIN okres o2 on o2.id = o.id_okres
WHERE o2.nazov LIKE 'Tvrdosin'
  AND p.rok = 2011
  AND p.muzi + p.zeny = ( SELECT MIN(pocet_obyvatel) FROM
                            (
                                SELECT o2.nazov as okres, o.nazov as obec, p.muzi + p.zeny as pocet_obyvatel
                                FROM populacia p
                                INNER JOIN obec o on o.id = p.id_obec
                                INNER JOIN okres o2 on o2.id = o.id_okres
                                WHERE o2.nazov LIKE 'Tvrdosin'
                                    AND p.rok = 2011
                            ) foo
                       );

-- 9
SELECT o.nazov
FROM obec o
INNER JOIN populacia p on o.id = p.id_obec
WHERE rok = 2010 AND p.zeny + p.muzi < 5000;

-- 10
SELECT o.nazov, ROUND( p.zeny::numeric / p.muzi::numeric, 4 ) as pomer
FROM obec o
INNER JOIN populacia p on o.id = p.id_obec
WHERE p.zeny + p.muzi > 20000
  AND p.rok = 2012
ORDER BY pomer DESC
LIMIT 10;

-- 11
SELECT k.nazov,
       SUM(p.muzi + p.zeny) as pocet_obyvatel,
       COUNT( DISTINCT o) as pocet_obci,
       COUNT( DISTINCT o2) as pocet_okresu
FROM populacia p
INNER JOIN obec o on o.id = p.id_obec
INNER JOIN okres o2 on o2.id = o.id_okres
INNER JOIN kraj k on o2.id_kraj = k.id
WHERE p.rok = 2012
GROUP BY k.nazov;

-- 12
SELECT *
FROM
    (
SELECT nazov,
       LAG(pocet_obyvatel) OVER (PARTITION BY nazov ORDER BY rok) as pocet_minuly,
       pocet_obyvatel as pocet_tento,
       pocet_obyvatel - LAG(pocet_obyvatel) OVER (PARTITION BY nazov ORDER BY rok) as rozdil
FROM
    (
     SELECT o.nazov,
            p.rok,
            SUM(p.muzi + p.zeny) as pocet_obyvatel
     FROM populacia p
              INNER JOIN obec o on o.id = p.id_obec
     WHERE p.rok IN ( 2011, 2012 )
     GROUP BY o.nazov, p.rok
    ) foo
    ) foo2
    WHERE rozdil < 0
    ORDER BY rozdil;

-- 13
SELECT COUNT(o)
FROM obec o
INNER JOIN populacia p on o.id = p.id_obec
WHERE p.rok = 2012
    AND p.muzi + p.zeny < (
        SELECT AVG(p.muzi + p.zeny)
        FROM populacia p
        WHERE p.rok = 2012
    );