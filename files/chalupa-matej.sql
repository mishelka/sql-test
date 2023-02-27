--1 - Počítám VŠECHNY obce, které mají duplicitní název
SELECT count(id)
FROM obec o
WHERE (SELECT count(nazov)
       FROM obec o2
       WHERE o.nazov = o2.nazov
       GROUP BY nazov) > 1;

--2
CREATE OR REPLACE VIEW names_counted AS
SELECT nazov, count(nazov)
FROM obec
GROUP BY nazov;

SELECT nazov
FROM names_counted nc
WHERE (SELECT max(count) FROM names_counted) = nc.count;

--3
SELECT count(o.nazov)
FROM okres o
         join kraj k on k.id = o.id_kraj
WHERE k.nazov = 'Kosicky kraj';

--4
SELECT count(o.nazov)
FROM obec o
         join okres o2 on o2.id = o.id_okres
         join kraj k on k.id = o2.id_kraj
WHERE k.nazov = 'Kosicky kraj';

--5
SELECT o.nazov, (p.muzi + p.zeny) as populace
FROM populacia p
         join obec o on o.id = p.id_obec
WHERE (p.muzi + p.zeny) = (SELECT max(muzi + zeny)
                           from populacia
                           where rok = 2012);

--6
SELECT SUM(p.muzi + p.zeny)
FROM populacia p
         join obec o on o.id = p.id_obec
         join okres o2 on o2.id = o.id_okres
WHERE p.rok = 2012
  AND o2.nazov = 'Sabinov';

--7
SELECT p.rok,
       sum(p.muzi + p.zeny)
--            - (SELECT sum(p2.muzi + p2.zeny)
--                                FROM populacia p2
--                                WHERE p2.rok = p.rok - 1)
           as trend
FROM populacia p
GROUP BY p.rok
ORDER BY p.rok desc;

--8
SELECT o.nazov, (p.muzi + p.zeny) as populace
FROM populacia p
         join obec o on o.id = p.id_obec
         join okres o2 on o2.id = o.id_okres
WHERE p.rok = 2011
  AND o2.nazov = 'Tvrdosin'
  AND (p.muzi + p.zeny) = (SELECT min(muzi + zeny)
                           FROM populacia
                                    join obec o3 on o3.id = populacia.id_obec
                                    join okres o4 on o4.id = o3.id_okres
                           WHERE rok = 2011
                             AND o4.nazov = 'Tvrdosin');

--9
SELECT o.nazov
FROM obec o
         join populacia p on o.id = p.id_obec
WHERE (p.muzi + p.zeny) < 5000
  AND p.rok = 2010;

--10
SELECT o.nazov, round(p.zeny * 1.0 / p.muzi, 4) as pomer
FROM populacia p
         join obec o on o.id = p.id_obec
WHERE (p.muzi + p.zeny) > 20000
  AND p.rok = 2012
ORDER BY pomer DESC
limit 10;

--11
SELECT k.nazov, sum(p.zeny + p.muzi) as obyvatele, count(DISTINCT o2.id) as obce, count(DISTINCT o.id) as okresy
FROM kraj k
         join okres o on k.id = o.id_kraj
         join obec o2 on o.id = o2.id_okres
         join populacia p on o2.id = p.id_obec
WHERE p.rok = 2012
GROUP BY k.nazov;

--12
SELECT o.nazov,
       (p.muzi + p.zeny)                         as obyvatele_2011,
       (p2.muzi + p2.zeny)                       as obyvatele_2012,
       (p2.muzi + p2.zeny) - ((p.muzi + p.zeny)) as rozdil
FROM populacia p
         join obec o on o.id = p.id_obec
         join populacia p2 on o.id = p2.id_obec
WHERE p.rok = 2011
  AND p2.rok = 2012
  AND (p.muzi + p.zeny) > (p2.muzi + p2.zeny)
ORDER BY rozdil ASC;

--13
SELECT count(p.muzi + p.zeny)
from populacia p
WHERE p.rok = 2012
  AND (p.muzi + p.zeny) < (SELECT avg(muzi + zeny)
                           FROM populacia
                           WHERE populacia.rok = 2012)
