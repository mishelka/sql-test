--20 Obce, ktore sa opakuju
SELECT COUNT(*) FROM (
		SELECT nazov FROM obec
		GROUP BY nazov
		HAVING COUNT(*) > 1
) as obce;

--1b Najcastejsi nazov
SELECT nazov, count(nazov) as opakovanie FROM obec
GROUP BY nazov
ORDER BY opakovanie DESC
LIMIT 2;

--2 Okresy v kosickom kraji
SELECT okres.nazov FROM okres
INNER JOIN kraj ON okres.id_kraj = kraj.id
WHERE kraj.nazov = 'Kosicky kraj';

--3 Obce v kosickom kraji
SELECT obec.nazov FROM obec
INNER JOIN okres ON obec.id_okres = okres.id
INNER JOIN kraj ON okres.id_kraj = kraj.id
WHERE kraj.nazov = 'Kosicky kraj';

--4 Obec s najvyssou populaciou (podla scitania z roku 2012)
SELECT obec.nazov, SUM(zeny + muzi) as populacia FROM populacia p
FULL JOIN obec ON p.id_obec = obec.id
WHERE rok = 2012
GROUP BY obec.nazov
ORDER BY populacia DESC
LIMIT 1;

--5 Pocet obyvatelov okresu Sabinov (podla scitania z roku 2012)
SELECT SUM(males + females) FROM (
		SELECT SUM(muzi) as males, SUM(zeny) as females FROM populacia p
		FULL JOIN obec ON p.id_obec = obec.id
		FULL JOIN okres ON obec.id_okres = okres.id
		WHERE okres.nazov = 'Sabinov'
		AND rok = 2012
) as sb_pop;

-- (6 prvy pokus) Trend vyvoja populacie na Slovensku

--Zaujimavy, ale nefunkcny prvy pokus 			//DRUHY, USPESNY POKUS NIZSIE!

-- SELECT pop12, pop11, pop10, pop09 FROM (
-- 		SELECT SUM(men12 + women12) FROM (
-- 				SELECT SUM(muzi) as men12, SUM(zeny) as women12 FROM populacia
-- 				WHERE rok = 2012
-- 		SELECT SUM(men11 + women11) FROM (
-- 				SELECT SUM(muzi) as men11, SUM(zeny) as women11 FROM populacia
-- 				WHERE rok = 2011
-- 		) as pop11;

-- 		SELECT SUM(men10 + women10) FROM (
-- 				SELECT SUM(muzi) as men10, SUM(zeny) as women10 FROM populacia
-- 				WHERE rok = 2010
-- 		) as pop10;
--
-- 		SELECT SUM(men09 + women09) FROM (
-- 				SELECT SUM(muzi) as men09, SUM(zeny) as women09 FROM populacia
-- 				WHERE rok = 2009
-- 		) as pop09;
-- ) as trend;

--6 Trend vyvoja populacie na Slovensku // DRUHY, TERAZ UZ USPESNY POKUS

	SELECT rok, SUM(zeny) as zeny_spolu, SUM(muzi) as muzi_spolu, SUM(zeny + muzi) as dokopy FROM populacia
		WHERE rok = 2012
		GROUP BY rok
	UNION ALL
	SELECT rok, SUM(zeny) as zeny_spolu, SUM(muzi) as muzi_spolu, SUM(zeny + muzi) as dokopy FROM populacia
		WHERE rok = 2011
		GROUP BY rok
	UNION ALL
	SELECT rok, SUM(zeny) as zeny_spolu, SUM(muzi) as muzi_spolu, SUM(zeny + muzi) as dokopy FROM populacia
		WHERE rok = 2010
		GROUP BY rok
	UNION ALL
	SELECT rok, SUM(zeny) as zeny_spolu, SUM(muzi) as muzi_spolu, SUM(zeny + muzi) as dokopy FROM populacia
		WHERE rok = 2009
		GROUP BY rok;

--7 Najmensie obce v okrese Tvrdosin
SELECT obec.nazov, SUM(zeny + muzi) as obyvatelia FROM populacia p
INNER JOIN obec ON p.id_obec = obec.id
INNER JOIN okres ON obec.id_okres = okres.id
WHERE okres.nazov = 'Tvrdosin'
AND rok = 2011
GROUP BY obec.nazov
HAVING SUM(zeny + muzi) = 659; --Musim prist na elegantnejsie riesenie
	
--8 Obce s poctom obyvatelov pod 5000
SELECT obec.nazov, SUM(zeny + muzi) as obyvatelia FROM populacia p
INNER JOIN obec ON p.id_obec = obec.id
INNER JOIN okres ON obec.id_okres = okres.id
AND rok = 2010
GROUP BY obec.nazov
HAVING SUM(zeny + muzi) < 5000
ORDER BY obyvatelia DESC;

--9 Najvacsi pomer zien voci muzom
SELECT obec.nazov, zeny, muzi, SUM(zeny + muzi) as obyvatelia, CAST(zeny as FLOAT) / CAST(muzi as FLOAT) as pomer FROM populacia p
INNER JOIN obec ON p.id_obec = obec.id
WHERE rok = 2012
GROUP BY obec.nazov, zeny, muzi
HAVING SUM(zeny + muzi) > 20000
ORDER BY pomer DESC
LIMIT 10;

--10 Slovensko v 2012
SELECT k.nazov as kraj, COUNT(DISTINCT ob.id) as obce, COUNT(DISTINCT ok.id) as okresy, SUM(zeny + muzi) as obyvatelia FROM kraj k
INNER JOIN okres ok ON ok.id_kraj = k.id
INNER JOIN obec ob ON ob.id_okres = ok.id
INNER JOIN populacia p ON p.id_obec = ob.id
WHERE rok = 2012
GROUP BY k.nazov;

--11 Prirodzeny ubytok v obciach //NEDOKONCENE
SELECT nazov, SUM(zeny + muzi) as obyvatelia FROM populacia p
INNER JOIN obec ON p.id_obec = obec.id
GROUP BY nazov





