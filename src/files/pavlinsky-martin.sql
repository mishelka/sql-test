--20
SELECT nazov opakovanie_tab
FROM obec
GROUP BY nazov
having COUNT(*) > 1
order by opakovanie_tab DESC;

--1b
select nazov, count(nazov) as suma
from obec
group by nazov
order by suma desc;

--2.
select k.nazov, k.id, o.nazov, o.id
select count (o.id_kraj)
from okres o, kraj k
where k.id = o.id_kraj
and k.nazov like 'K%';

--3.
select count (ob.id) from obec as ob, okres as o, kraj as k
where ob.id_okres = o.id
and o.id_kraj = k.id
and k.nazov like 'K%';

--4.
obec, populacia
select o.nazov, (muzi + zeny) as obyvatelia
from obec o
join populacia p on p.id_obec = o.id
where rok = 2012
group by nazov, obyvatelia
order by obyvatelia desc;

--5.
select o.nazov, (muzi + zeny) as obyvatelia
from obec o
join populacia p on p.id_obec = o.id
where rok = 2012
and o.nazov like 'Sab%';

--6.
select rok, SUM(muzi + zeny) as vsetci_oby
from populacia
where rok between 2009 and 2012
group by rok
order by rok;

--7.
select o.nazov, SUM (muzi + zeny)
from populacia p, obec o, okres ok
where p.id_obec = o.id
and o.id_okres = ok.id
and ok.nazov like 'Tvrdosin'
and p.rok = 2011
group by o.nazov
order by SUM;

--8.
select o.nazov, rok, (muzi + zeny) as obyvatelia
from populacia p
join obec o on p.id_obec = o.id
where (muzi + zeny) < 5000
and rok = 2010
order by obyvatelia desc;

--9.Nedokoncene
select o.nazov muzi, zeny, SUM (muzi + zeny) as obyvatelia
from populacia p
join obec on p.id_obec = obec.id
having obyvatelia > 20000
group by o.nazov, muzi, zeny
and rok = 2012;

--10.
--11.
--12.



