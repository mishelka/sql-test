--20
SELECT COUNT(nazov) FROM obec
group by nazov
having count(nazov) > 1;
-- 100

--1b
SELECT COUNT(*) as pocet, nazov
FROM obec
GROUP BY nazov
HAVING COUNT(*) > 1
order by pocet desc
limit 1;


--2.Koľko okresov sa nachádza v košickom kraji?

select okres.nazov, okres.id_kraj, kraj.id, kraj.nazov
from okres, kraj
where okres.id_kraj = kraj.id
and kraj.nazov like 'Kos%';

--3.
select count (obec.id)
from obec, okres, kraj
where obec.id_okres = okres.id
and okres.id_kraj = kraj.id
and kraj.nazov like 'Kos%';

--4.
SELECT o.nazov, (muzi + zeny) as obyvatelia
from obec o
inner join populacia p on p.id_obec = o.id
where rok = 2012
group by o.nazov, obyvatelia
order by obyvatelia desc
limit 1;

-- 5.
select sum (p.muzi + p.zeny)
from populacia p
inner join obec ob on  p.id_obec = ob.id
inner join okres o on ob.id_okres = o.id
where o.nazov like 'Sab%'
and p.rok = 2012;

-- 6.
SELECT rok, SUM(muzi + zeny) as populaciaSR
from populacia
where rok between 2009 and 2012
group by rok
order by rok;

-- 7.
select sum (p.muzi + p.zeny), ob.nazov
from populacia p, obec ob, okres ok
where p.id_obec = ob.id
and ob.id_okres = ok.id
and ok.nazov like 'Tvr%'
and p.rok = 2011
group by ob.nazov
order by sum
limit 5;

-- 8.
select o.nazov, (p.muzi + p.zeny) as populacia
from obec o
inner join populacia p on p.id_obec = o.id
where rok = 2010 and (p.muzi + p.zeny) <= 5000;

-- 9.
select o.nazov, zeny, muzi, SUM(zeny + muzi) as pocet_obyvatelov, CAST (zeny as FLOAT) / CAST (muzi as FLOAT) as ZENY_MUZI
FROM populacia p
inner join obec o on p.id_obec = o.id
where rok = 2012
group by o.nazov, zeny, muzi
having sum(zeny + muzi) > 20000
and zeny > muzi 
order by ZENY_MUZI desc
limit 10;

-- ked chcem dat do slectu ROUND(pomer, 4) tak round mi vobec neberie ako prikaz

-- 10.

-- 11.

-- 12.

