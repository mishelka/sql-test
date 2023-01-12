-- 20.Názvy niektorých obcí v tabuľke obec sa opakujú, pretože na Slovensku existujú obce, ktoré majú rovnaký názov. Zistite:
-- a)koľko je takých obcí (1 dopyt) (100)
-- b)ktorý názov obce je použitý najviac (1 dopyt) (Porubka, Lucka)
select count(*)
from (
	select nazov
	from obec
    group by nazov
    having count(*) > 1
	) as ok;


--1b
select nazov, count(*)
from obec
group by nazov
order by count(*) desc;

-- 2.Koľko okresov sa nachádza v košickom kraji?
select count(o.id_kraj) as pocet_okresov
from okres o, kraj k
where o.id_kraj = k.id
and k.nazov like 'Kosicky %';


-- 3.A koľko má košický kraj obcí? Pri tvorbe dopytu vám môže pomôcť informácia, že trenčiansky kraj má spolu 276 obcí. (461)
select count(oc.id) as pocet_obci
from obec oc, kraj k, okres ok
where oc.id_okres = ok.id and ok.id_kraj = k.id and k.id = 8;


-- 4.Zistite, ktorá obec (mesto) bola na Slovensku najväčšia v roku 2012. 
-- Pri tvorbe dopytu vám môže pomôcť informácia, že táto obec (mesto) bola najväčšia na Slovensku v rokoch 2009-2012, 
-- avšak má v populácii klesajúcu tendenciu. Vo výsledku vypíšte jej názov a počet obyvateľov. (Bratislava -Petrzalka - 105468)
select oc.nazov, (pop.muzi + pop.zeny) as pocet_obyvatelov
from obec oc
inner join populacia pop on oc.id = pop.id_obec
where pop.rok = 2012
order by pocet_obyvatelov desc
limit 1;

-- 5.Koľko obyvateľov mal okres Sabinov v roku 2012? (58450)
-- Pri tvorbe dopytu vám môže pomôcť informácia, že okres Dolný Kubín mal v roku 2010 39553 obyvateľov.
select sum(pop.muzi + pop.zeny) as pocet_obyvatelov
from obec oc
inner join populacia pop on oc.id = pop.id_obec
inner join okres ok on ok.id = oc.id_okres
where pop.rok = 2012 and ok.nazov like 'Sabinov';


-- 6.Ako sme na tom na Slovensku? Vymierame alebo rastieme? (oproti roku 2011 v najnovsom roku 2012 rastieme, oproti rokom 2009 a 2010 vymierame)
-- Zobrazte trend vývoja populácie za jednotlivé roky a výsledok zobrazte od najnovších informácií po najstaršie.
select pop.rok, sum(pop.muzi + pop.zeny) as pocet_obyvatelov
from populacia pop
inner join obec oc on oc.id = pop.id_obec
group by pop.rok
order by pop.rok desc;


-- 7.Zistite, ktorá obec alebo obce boli najmenšie v okrese Tvrdošín v roku 2011. 
-- Pri tvorbe dopytu vám môže pomôcť informácia, že v okrese Ružomberok to bola v roku 2012 obec Potok s počtom obyvateľov 107.	
select oc.nazov, (pop.muzi + pop.zeny) as pocet_obyvatelov
from obec oc
inner join populacia pop on oc.id = pop.id_obec
inner join okres ok on ok.id = oc.id_okres
where ok.nazov like 'Tvrdosin' and pop.rok = 2011
order by pocet_obyvatelov asc
limit 10;
	
		

-- 8.Zistite všetky obce (ich názvy), ktoré mali v roku 2010 počet obyvateľov do 5000. (2774)
-- Pri tvorbe dopytu vám môže pomôcť informácia, že v roku 2009 bolo týchto obcí o 1 viac ako v roku 2010.
select oc.nazov, (pop.muzi + pop.zeny) as pocet_obyvatelov
from obec oc
inner join populacia pop on oc.id = pop.id_obec
where pop.rok = 2010 and (pop.muzi + pop.zeny) <= 5000;


-- 9.Zistite 10 obcí s populáciou nad 20000, ktoré mali v roku 2012 najväčší pomer žien voči mužom (viac žien v obci ako mužov). 
-- Týchto 10 obcí vypíšte v poradí od najväčšieho pomeru po najmenší. 
-- Vo výsledku okrem názvu obce vypíšte aj pomer zaokrúhlený na 4 desatinné miesta. 
-- Pri tvorbe dopytu vám môže pomôcť informácia, že v roku 2011 bol tento pomer pre obec Košice  - Juh 1,1673.
select oc.nazov, pop.muzi, pop.zeny, 
sum(muzi + zeny) as celkova_populacia, 
round(cast(cast(zeny as float) / cast(muzi as float) as numeric), 4) as pomer
from populacia pop
join obec oc on pop.id_obec = oc.id
where pop.rok = 2012
group by oc.nazov, zeny, muzi
having sum(muzi + zeny) > 20000
order by pomer desc
limit 10;


-- 10.Vypíšte sumárne informácie o stave Slovenska v roku 2012 v podobe tabuľky, 
-- ktorá bude obsahovať pre každý kraj informácie o počte obyvateľov, o počte obcí a počte okresov. 
select k.nazov as kraj, sum(pop.muzi + pop.zeny) as pocet_obyvatelov, count(distinct oc.id) as pocet_obci, 
count(distinct ok.id) as pocet_okresov
from populacia pop, obec oc, okres ok
join obec oc on pop.id_obec = oc.id
join okres ok on oc.id_okres = ok.id
join kraj k on ok.id_kraj = k.id
where pop.rok = 2012
group by k.nazov;


-- 11.To, či vymierame alebo rastieme, sme už zisťovali. Ale ktoré obce sú na tom naozaj zle? 
-- Kde by sa nad touto otázkou mali naozaj zamyslieť? 
-- Zobrazte obce, ktoré majú klesajúci trend (rozdiel v populácii dvoch posledných rokov je menší ako 0) 
-- vypíšte ich názov, počet obyvateľov v poslednom roku, počet obyvateľov v predchádzajúcom roku a
-- rozdiel v populácii posledného oproti predchádzajúcemu roku. 
-- Zoznam utrieďte vzostupne podľa tohto rozdielu od obcí s najmenším prírastkom obyvateľov po najväčší.
select o.name, p1.(pop.muzi + pop.zeny) as (pop.muzi + pop.zeny)_2012, 
p2.(pop.muzi + pop.zeny) as (pop.muzi + pop.zeny)_2011, 
p1.(pop.muzi + pop.zeny) - p2.(pop.muzi + pop.zeny) as (pop.muzi + pop.zeny)_diff
from obec oc
join populacia pop p1 on oc.id = p1.id_obec and p1.rok = (select max(2012) from populacia where id_obec = oc.id)
join populacia pop p2 on oc.id = p2.id_obec and p2.rok = (select max(2011) from populacia where id_obec = oc.id and rok < (select max(2011) from populacia pop where id_obec = oc.id))
where p1.(pop.muzi + pop.zeny) - p2.(pop.muzi + pop.zeny) < 0
order by populacia pop_diff asc;
	
-- 12.Zistite počet obcí, ktorých počet obyvateľov v roku 2012 je nižší, ako bol slovenský priemer v danom roku.
select count(*) as pocet_obci
from obec oc
join populacia pop on oc.id = pop.id_obec
where pop.rok = 2012 and (pop.muzi + pop.zeny) < (select avg(pop.muzi + pop.zeny) from (pop.muzi + pop.zeny) where pop.rok = 2012);

