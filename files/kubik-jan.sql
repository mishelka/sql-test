-- 1
select sum(count)
from (select count(*) as count from obec group by nazov having obec.count > 1) x;
-- 2
select nazov, count(nazov) as pocet_obci
from obec
group by nazov
having count(nazov) = (select max(count) from (select count(*) as count from obec group by nazov) ob)
limit 2;
-- 3
select kraj.nazov, count(*) as pocet_okresu
from kraj
         inner join okres on kraj.id = id_kraj
where kraj.nazov = 'Kosicky kraj'
group by kraj.nazov;
-- 4
select kraj.nazov, count(*) as pocet_obci
from kraj
         inner join okres on id_kraj = kraj.id
         inner join obec on id_okres = okres.id
where kraj.nazov = 'Kosicky kraj'
group by kraj.nazov;
-- 5
select nazov, muzi + zeny as populacia
from obec
         inner join populacia p on id = p.id_obec
where rok = 2012
  and muzi + zeny = (select max(muzi + zeny) from populacia where rok = 2012)
limit 1;
-- 6
select nazov, rok, muzi + zeny as populacia
from obec
         inner join populacia on id = populacia.id_obec
where rok = 2012
  and nazov = 'Sabinov';
-- 7
select rok, sum(zeny + muzi) as populacia
from populacia
group by rok
order by rok DESC;
-- 8
select obec.nazov, muzi + zeny as populacia
from okres
         inner join obec on okres.id = obec.id_okres
         inner join populacia p on obec.id = p.id_obec
where okres.nazov = 'Tvrdosin' and muzi + zeny = (select MIN(muzi + zeny) as populacia
                     from okres
                              inner join obec on okres.id = obec.id_okres
                              inner join populacia p on obec.id = p.id_obec
                     WHERE okres.nazov = 'Tvrdosin'
                       AND rok = 2012)
  AND rok = 2012
limit 2;
-- 9
select obec.nazov as population
from obec
         inner join populacia p on obec.id = p.id_obec
where muzi + zeny < 5000
  AND rok = 2010;
-- 10
select obec.nazov, ROUND(zeny::decimal / (muzi + zeny)::decimal, 4) as pomer_zen
from obec
         inner join populacia on obec.id = id_obec
where muzi + zeny > 5000
  AND rok = 2012
order by pomer_zen DESC
LIMIT 5;
-- 11
select kraj.nazov,
       sum(pocet_obci)    as pocet_obci,
       count(okres.nazov) as pocet_okresu,
       sum(populacia)     as populacia
from (select obec.id_okres, count(*) pocet_obci, sum(zeny + muzi) as populacia
      from kraj
               inner join okres on okres.id_kraj = kraj.id
               inner join obec on okres.id = obec.id_okres
               inner join populacia on obec.id = id_obec
      where rok = 2012
      group by obec.id_okres) as iopo
         inner join okres on id_okres = okres.id
         inner join kraj on id_kraj = kraj.id
group by kraj.nazov;
-- 13
select obec.nazov as population
from obec
         inner join populacia on obec.id = id_obec
where rok = 2012 and muzi + zeny < (select avg(muzi + zeny) from populacia where rok = 2012)