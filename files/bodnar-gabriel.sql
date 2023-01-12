-- 20 Nazvy obci v tabulke obe sa opakuju, pretoze na Slovensku existuju obce, ktore maju rovnaky nazov. Zistite:
--a - kolko je takych obci . 
--	  Odpoved: Je ich 100.

SELECT o.nazov, COUNT(*)
FROM obec o
GROUP BY o.nazov
HAVING COUNT(*) > 1
ORDER BY COUNT DESC;

-- 1b - odpoved na otazku je Porubka a Lucka, obe 4x.

-- 2. Kolko okresov sa nachadza v kosickom kraji?

select count(*)
from okres
where id_kraj = 8; 

-- odpoved je 11 okresov.

--3 A koľko má košický kraj obcí?
-- Pri tvorbe dopytu vám môže pomôcť informácia, že trenčiansky kraj má spolu 276 obcí.

select count(*)
from obec o
where o.id_okres between 801 and 811;

-- Odpoved je 461, pretoze 11 Kosickych okresov je v tabulke Obec oznacenych trojcislim zacinajucim 801 a konciacim 811

--4 najdi obec s najvacsim poctom obyvatelov v rokoch 2009 - 2012

select o.nazov, p.zeny + p.muzi as pocet_obyvatelov
from populacia p
inner join obec o on o.id = p.id_obec
where p.zeny = (select max(zeny) from populacia p)
and p.muzi = (select max(muzi) from populacia p)
and p.rok between 2009 and 2012;


-- Bratislava - Petrzalka - 112545 pocet obyvatelov

-- 5 Koľko obyvateľov mal okres Sabinov v roku 2012? 
-- Pri tvorbe dopytu vám môže pomôcť informácia, 
-- že okres Dolný Kubín mal v roku 2010 39553 obyvateľov.

select sum(p.muzi + p.zeny)
from obec o
inner join populacia p on p.id_obec=o.id
inner join okres ok on o.id_okres=ok.id
where ok.nazov like 'Sabinov'
and p.rok = 2012;

-- Odpoved je 58450 obyvatelov

-- 6 Ako sme na tom na Slovensku? Vymierame alebo rastieme? 
--   Zobrazte trend vývoja populácie za jednotlivé roky 
--   a výsledok zobrazte od najnovších informácií po najstaršie.


select p.rok, sum(p.muzi + p.zeny) as populacia
from populacia p
where p.rok between 2009 and 2012
group by p.rok
order by p.rok desc;

-- 7 Zistite, ktorá obec alebo obce boli najmenšie v okrese Tvrdošín v roku 2011.
-- Pri tvorbe dopytu vám môže pomôcť informácia, že v okrese Ružomberok 
-- to bola v roku 2012 obec Potok s počtom obyvateľov 107.

select o.nazov, min(p.zeny + p.muzi) as pocet_obyvatelov
from populacia p
inner join obec o on p.id_obec = o.id
inner join okres ok on o.id_okres=ok.id
where ok.nazov like 'Tvrdosin'
and p.rok = 2011
group by o.nazov
order by pocet_obyvatelov asc;

-- Odpoved je Stefanov nad Oravou , a taktiez Cimhova , obe po 659 obyvatelov.

--8 Zistite všetky obce (ich názvy), 
-- ktoré mali v roku 2010 počet obyvateľov do 5000. 
-- Pri tvorbe dopytu vám môže pomôcť informácia, že v roku 2009 bolo týchto obcí o 1 viac ako v roku 2010.

select p.rok, o.nazov, (p.zeny + p.muzi) as pocet_obyvatelov
from populacia p
inner join obec o on p.id_obec = o.id
inner join okres ok on o.id_okres=ok.id
where p.zeny + p.muzi < 5000
and p.rok = 2010
order by pocet_obyvatelov desc;

-- Pocet tychto obci sa rovna 1774

-- 9 Zistite 10 obcí s populáciou nad 20000, 
-- ktoré mali v roku 2012 najväčší pomer žien voči mužom (viac žien v obci ako mužov). 
-- Týchto 10 obcí vypíšte v poradí od najväčšieho pomeru po najmenší.
-- Vo výsledku okrem názvu obce vypíšte aj pomer zaokrúhlený na 4 desatinné miesta. 
-- Pri tvorbe dopytu vám môže pomôcť informácia, že v roku 2011 bol tento pomer pre obec Košice  - Juh 1,1673.

select o.nazov, p.zeny, p.muzi, round(p.zeny / p.muzi, 2) as pomer
from populacia p
inner join obec o on p.id_obec = o.id
inner join okres ok on o.id_okres=ok.id
where p.muzi + p.zeny > 20000
and p.zeny > p.muzi
and p.rok = 2012
order by (p.zeny > p.muzi) desc
LIMIT 10;

--max. co som dokazal spravit, nad moje sily, neviem zadat vypocet pomeru.

-- 10 Vypíšte sumárne informácie o stave Slovenska v roku 2012 v podobe tabuľky,
-- ktorá bude obsahovať pre každý kraj informácie o počte obyvateľov, o počte obcí a počte okresov. 

select o.nazov as obec, ok.nazov as okres, k.nazov as kraj, p.zeny + p.muzi as pocet_obyvatelov
from populacia p
inner join obec o on p.id_obec = o.id
inner join okres ok on o.id_okres=ok.id
inner join kraj k on k.id=ok.id_kraj
where p.rok = '2012';

-- iba v stadiu pokusu


--12 Zistite počet obcí, ktorých počet obyvateľov v roku 2012 je nižší, ako bol slovenský priemer v danom roku.

SELECT COUNT(id_obec)
FROM populacia p
WHERE (p.zeny + p.muzi) < (SELECT ROUND(AVG(p2.zeny + p2.muzi), 2)
FROM populacia p2
WHERE p.rok = 2012);






 



