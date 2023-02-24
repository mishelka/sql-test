-- 2.(11 okresov)
select okres.nazov, kraj.nazov
from okres
inner join kraj on okres.id_kraj = kraj.id
where kraj.nazov = 'Kosicky kraj';



-- 3.(461 obci)
select obec.nazov, okres.nazov
from obec
inner join okres on obec.id_okres = okres.id
where okres.id between 801 and 811


-- 4.(Bratislava-Petrzalka, pocet obyvatelov je 105468)
select obec.nazov, (muzi + zeny) as Obyvatelia
from obec
inner join populacia on populacia.id_obec = obec.id
where rok = 2012
order by obyvatelia desc


-- 1b.(Lucka a Porubka, 4x)
select nazov, count(nazov) as Pocet
from obec
group by nazov
order by pocet desc


-- 20.(pocet obci je 100)
select count (*)
from (select nazov
	  from obec
	  group by nazov
	  having count (*) > 1)
	  as ok;

-- 5.(pocet obyvatelov je 58450)
select sum(muzi + zeny) as obyvatelia
from obec
join populacia on obec.id = populacia.id_obec
join okres on okres.id = obec.id_okres
where populacia.rok = 2012	and okres.nazov = 'Sabinov'

-- 7.(Najmensia pocet obyvatelov ma obec STEFANOV NAD ORAVOU)
select	obec.nazov, (muzi + zeny) as obyvatelia, okres.nazov, populacia.rok
from obec
inner join populacia on populacia.id_obec = obec.id
inner join okres on okres.id = obec.id_okres
where okres.nazov = 'Tvrdosin' and populacia.rok = 2011
order by obyvatelia asc

-- 8.
select obec.nazov,(muzi + zeny) as obyvatelia
from obec
join populacia on populacia.id_obec = obec.id
where (muzi + zeny) < 5001 and populacia.rok = 2010
order by (muzi + zeny) desc

-- 9.
select obec.nazov, zeny, muzi, populacia.rok, (zeny + muzi) as obyvatelia, cast (zeny as float) / cast (muzi as float) as pomer
from obec
inner join populacia on populacia.id_obec = obec.id
where populacia.rok = 2012 and (muzi + zeny) > 20000
order by pomer desc
limit  10

-- 6.(Vymierame)
select rok, sum(muzi + zeny) as obyvatelia
from populacia
where rok between 2009 and 2012
group by rok
order by rok