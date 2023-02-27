--1
select count(*)
from obec
where nazov in (select nazov
                from obec
                group by nazov
                having count(*) > 1);

--2
select *
from (select count(*) count, nazov
      from obec
      group by nazov) as subquery
where count =
      (select max(count)
       from (select count(*) count, nazov
             from obec
             group by nazov) as subquery);
--3
select count(*)
from okres o
         join kraj k on o.id_kraj = k.id
where k.nazov = 'Kosicky kraj';
--4
select count(*)
from obec o
         join okres o2 on o.id_okres = o2.id
         join kraj k on o2.id_kraj = k.id
where k.nazov = 'Kosicky kraj';

--5
select muzi + zeny populace, nazov
from populacia
         join obec o on o.id = populacia.id_obec
where muzi + zeny =
      (select max(total)
       from (select *, (muzi + zeny) total
             from populacia
             where rok = 2012) as sq);

--6
select sum(populace)
from (select (muzi + zeny) populace, *
      from populacia
               join obec o on o.id = populacia.id_obec
               join okres o2 on o.id_okres = o2.id
      where rok = 2012
        and o2.nazov = 'Sabinov') as sq;

--7
select sum(muzi + zeny) populace, rok
from populacia
group by rok
order by rok desc;


--8
select muzi + zeny populace, o.nazov
from populacia
         join obec o on o.id = populacia.id_obec
         join okres o2 on o2.id = o.id_okres
where muzi + zeny = (select min(populace)
                     from (select (zeny + muzi) populace
                           from populacia
                                    join obec o on populacia.id_obec = o.id
                                    join okres o2 on o.id_okres = o2.id
                           where o2.nazov = 'Tvrdosin'
                             and rok = 2011) sq)
  and o2.nazov = 'Tvrdosin'
  and rok = 2011;
--9
select o.nazov
from populacia
         join obec o on populacia.id_obec = o.id
where rok = 2010
  and muzi + zeny < 5000;

--10
select round(zeny::numeric / muzi::numeric, 4) pomer, nazov
from populacia
         join obec o on o.id = populacia.id_obec
where (muzi + zeny > 20000)
  and rok = 2012
order by pomer desc
limit 10;

--11
select k.nazov, sum(populacia.muzi + populacia.zeny), count(o.nazov) obce, count(distinct (o2.nazov)) okresy
from populacia
         join obec o on o.id = populacia.id_obec
         join okres o2 on o2.id = o.id_okres
         join kraj k on k.id = o2.id_kraj
where rok = 2012
group by k.nazov;

--12
select o.nazov,
       p12.muzi + p12.zeny                           populace12,
       p11.muzi + p11.zeny                           populace11,
       (p12.muzi + p12.zeny) - (p11.muzi + p11.zeny) prirustek
from populacia p12
         join populacia p11 on p11.rok = 2011 AND p12.muzi + p12.zeny < p11.muzi + p11.zeny
         join obec o on o.id = p11.id_obec AND o.id = p12.id_obec
where p12.rok = 2012
order by prirustek;

--13
select count(*)
from populacia
         join obec o on populacia.id_obec = o.id
where rok = 2012
  AND populacia.muzi + populacia.zeny < (select avg(muzi + zeny) populace
                                         from populacia
                                                  join obec o on o.id = populacia.id_obec
                                         where rok = 2012);


