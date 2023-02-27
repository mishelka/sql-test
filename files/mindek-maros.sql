--1
select count(*)
from (select o.nazov from obec o group by o.nazov having count(*) > 1) as correct;

--2

select nazov
from obec
group by nazov
having count(nazov) = (SELECT MAX(count)
                       FROM (SELECT o.nazov, COUNT(*) AS count
                             FROM obec o
                             GROUP BY o.nazov
                             HAVING COUNT(*) > 1) AS correct);

--3

select count(*) from okres o
join kraj k on k.id = o.id_kraj
where k.nazov like 'Kosicky kraj';

--4

select  count(*) from obec o
join okres o2 on o.id_okres = o2.id
join kraj k on k.id = o2.id_kraj
where k.nazov like 'Kosicky kraj';

--5

select o.nazov,p.muzi+p.zeny as pocet_obyvatelov from obec o
inner join populacia p on o.id = p.id_obec
where p.rok = 2012
and(p.muzi + p.zeny) = (select max(p.muzi+p.zeny)from populacia p where p.rok = 2012)
group by o.nazov, p.muzi+p.zeny;

--6
select (sum(p.muzi)+sum(p.zeny))as pocet_obyvatelov from populacia p
join obec o on o.id = p.id_obec
where o.nazov like 'Sabinov'
and p.rok = 2012;

--7
select p.rok,(sum(p.muzi)+sum(p.zeny))as pocet_obyvatelov from populacia p
group by p.rok
order by p.rok desc;

--8

select o.nazov, sum(p.muzi + p.zeny) from populacia p
join obec o on o.id = p.id_obec
join okres o2 on o2.id = o.id_okres
where o2.nazov like 'Tvrdosin' and p.rok = 2011
group by o.nazov
having sum(p.muzi +p.zeny) = (select min(count) from (select sum(p2.muzi+p2.zeny) as count from obec o3
    join okres o4 on o4.id = o3.id_okres
    join populacia p2 on o3.id = p2.id_obec
    where p2.rok = 2011 and o4.nazov like 'Tvrdosin'
    group by o3.nazov) as alias);

--9
select o.nazov from obec o
join populacia p on o.id = p.id_obec
where p.rok = 2010
group by o.nazov
having sum(p.muzi + p.zeny)<=5000;

--10
select o.nazov , ROUND(p.zeny::numeric/p.muzi::numeric,4) as pomer from obec o
join populacia p on o.id = p.id_obec
where p.rok = 2012
group by o.nazov, p.muzi,p.zeny
having sum(p.muzi+p.zeny)>20000
order by pomer desc
limit 10;

--11
select k.nazov as kraj, sum(p.muzi) + sum(p.zeny) as pocet_obyvatelov,count(o.id) as pocet_obci,count(distinct o2.id) as pocet_okresov
from obec o,populacia p,kraj k,okres o2
where k.id = o2.id_kraj and o2.id = o.id_okres and o.id = p.id_obec and p.rok = 2012
group by k.nazov;

--12
select o.nazov as nazov_obce ,(p.muzi + p.zeny) as pocet_obyvatelov2012,(p1.muzi + p1.zeny) as pocet_obyvatelov2011,(p.muzi+p.zeny)-(p1.muzi + p1.zeny) as rozdiel
from obec o
join populacia p on o.id = p.id_obec
join populacia p1 on o.id = p1.id_obec
where p.rok = 2012 and p1.rok = 2011
group by o.nazov, p.muzi,p.zeny,p1.muzi,p1.zeny
having (p.muzi+p.zeny)-(p1.muzi + p1.zeny)<0
order by rozdiel asc;

--13
select count(*) from (
select o.nazov,p.muzi + p.zeny as pocet_obyvatelov from obec o
join populacia p on o.id = p.id_obec
where p.rok = 2012
group by o.nazov, p.muzi, p.zeny
having (p.muzi+p.zeny)<(select avg(p.zeny+p.muzi)from populacia p
                                                 join obec o2 on o2.id = p.id_obec
                                                 where p.rok = 2012))as count

