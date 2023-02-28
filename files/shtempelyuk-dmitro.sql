--1
select count(*)
from obec o
where (select count(*)
       from obec o_subq
       where o_subq.nazov = o.nazov) > 1;

--2
select o.nazov
from obec o
group by o.nazov
having count(*) = (select max(freq)
                   from (select count(*) as freq
                         from obec o
                         group by o.nazov) as freq_table);
--3
select count(*)
from oblast ob,
     kraj k,
     okres ok
where ob.id = k.id_oblast
  and k.id = ok.id_kraj
  and k.nazov = 'Kosicky kraj';

--4
select count(*)
from oblast ob,
     kraj k,
     okres ok,
     obec o
where ob.id = k.id_oblast
  and k.id = ok.id_kraj
  and o.id_okres = ok.id
  and k.nazov = 'Kosicky kraj';

--5
select o.nazov as obec
from obec o,
     populacia p
where o.id = p.id_obec
  and p.rok = '2012'
group by o.nazov
order by sum(p.muzi + p.zeny) desc
limit 1;

--6
select sum(p.muzi + p.zeny) as poc_os
from obec o,
     populacia p,
     okres ok
where ok.id = o.id_okres
  and o.id = p.id_obec
  and p.rok = '2012'
  and ok.nazov = 'Sabinov'
group by ok.nazov;

--7
select p.rok, sum(p.muzi + p.zeny) as poc_os
from populacia p
group by p.rok
order by p.rok;

--8
select o.nazov, sum(p.muzi + p.zeny) as poc_os
from obec o,
     populacia p,
     okres ok
where ok.id = o.id_okres
  and o.id = p.id_obec
  and p.rok = '2011'
  and ok.nazov = 'Tvrdosin'
group by o.nazov
order by poc_os
limit 2;

--9
select o.nazov
from obec o,
     populacia p
where o.id = p.id_obec
  and p.rok = '2010'
  and (p.muzi + p.zeny) < 5000
order by o.nazov;

--10
select o.nazov, round(cast(p.zeny as numeric) / cast(p.muzi AS numeric), 4) as pomer
from obec o,
     populacia p
where o.id = p.id_obec
  and p.rok = '2012'
  and (p.muzi + p.zeny) > 20000
  and p.zeny > p.muzi
order by pomer desc
limit 10;

--11
select k.nazov, sum(p.muzi + p.zeny) as celkem, count(o) as poc_obci, count(distinct ok) as poc_ok
from kraj k,
     okres ok,
     obec o,
     populacia p
where k.id = ok.id_kraj
  and ok.id = o.id_okres
  and o.id = p.id_obec
  and p.rok = '2012'
group by k.nazov
order by k.nazov;

--12
select o.nazov,
       p_act.muzi + p_act.zeny                                 as pop_act,
       p_last.muzi + p_last.zeny                               as pop_last,
       (p_act.muzi + p_act.zeny) - (p_last.muzi + p_last.zeny) as pop_diff
from obec o,
     populacia p_act,
     populacia p_last
where o.id = p_act.id_obec
  and o.id = p_last.id_obec
  and p_act.rok = '2012'
  and p_last.rok = '2011'
  and (p_act.muzi + p_act.zeny) < (p_last.muzi + p_last.zeny)
order by pop_diff;

--13
select count(o.id)
from obec o,
     populacia p_ob
where p_ob.id_obec = o.id
  and p_ob.rok = '2012'
  and (p_ob.muzi + p_ob.zeny) < (select avg(p_avg.muzi + p_avg.zeny)
                                 from populacia p_avg,
                                      okres ok,
                                      kraj k,
                                      oblast ob,
                                      obec o_avg
                                 where p_avg.id_obec = o_avg.id
                                   and o_avg.id_okres = ok.id
                                   and ok.id_kraj = k.id
                                   and k.id_oblast = ob.id
                                   and p_avg.rok = '2012');
