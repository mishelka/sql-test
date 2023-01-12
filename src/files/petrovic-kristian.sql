--20
select count(*)
from (
select nazov
from obec
group by nazov
	having count(nazov) > 1
	) as rovnake_nazvy

--1b

select nazov, COUNT(*)
from obec
group by nazov
order by count (*) desc


--2

select count (o.id_kraj)
from okres o, kraj k
where o.id_kraj = k.id
   AND k.nazov = 'Kosicky kraj'

--3

select count (*)
from obec o, kraj k, okres ok
where o.id_okres = ok.id
    and ok.id_kraj = k.id
	and k.nazov = 'Kosicky kraj';
   
--4
   
SELECT o.nazov, p.rok, p.muzi + p.zeny as celkovo
FROM obec o, populacia p
where p.id_obec = o.id
    AND p.rok = 2012
order by celkovo desc
limit 1

-- 5

select sum(muzi + zeny) as obyvatelia
from obec o
join populacia p on o.id = p.id_obec
join okres ok on ok.id = o.id_okres
where p.rok = 2012
and ok.nazov = 'Sabinov';

--6

select rok, sum(muzi + zeny) as celkovo
from populacia
where rok BETWEEN 2009 and 2012
group by rok
order by rok desc

--7

select o.nazov, min (p.muzi + p.zeny)
from okres ok
join obec o on o.id_okres = ok.id
join populacia p on p.id_obec = o.id
where ok.nazov = 'Tvrdosin'
AND p.rok = 2011
group by  o.nazov
order by min

--8

select o.nazov, (p.muzi + p.zeny) as celkovo
from obec o
join populacia p on p.id_obec = o.id
where rok = 2010
and (p.muzi + p.zeny) < 5000
order by celkovo desc

--9

select o.nazov, ROUND((zeny / muzi), 4) as pomer
from obec o
join populacia p on p.id_obec = o.id
where rok = 2012
group by nazov, zeny, muzi
having sum(zeny + muzi) > 20000
and zeny > muzi
order by pomer desc
limit 10
																		
--10

--11
select o.nazov, p.rok, (p.muzi + p.zeny) as celkovo
from obec o
join populacia p on p.id_obec = o.id
where rok BETWEEN 2011 and 2012
group by nazov, rok, celkovo
order by celkovo asc
--12

																