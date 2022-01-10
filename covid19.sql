drop view if exists cube cascade;

create or replace view destatis6_view as 
    SELECT destatis6.zeit as year, replace(destatis6."3_auspraegung_code", 'MONAT'::text, ''::text)::int as month, to_date(concat(destatis6.zeit, replace(destatis6."3_auspraegung_code", 'MONAT'::text, ''::text)), '%YYYYMM'::text) AS "time",     (replace(destatis6.bev002__gestorbene__anzahl, '...'::text, '0'::text))::integer AS value    FROM destatis6;

create or replace view destatis6_moments as 
    SELECT month, min(value) as minimum, avg(value)::int as average, max(value) as maximum from destatis6_view where year > 2000 and year < 2021 group by month ; 

create or replace view destatis6_daterange as 
    select extract(MONTH from time)::int as month ,*  from (SELECT * FROM generate_series('2019-01-01'::timestamp, '2022-03-04', '1 week') as time) as foo ;  

create or replace view destatis6_moments_fused as 
    select m.*, dr.time from destatis6_moments m inner JOIN destatis6_daterange dr on m.month=dr.month;
    

drop table if exists facts;

create table facts as SELECT * FROM generate_series('1950-01-01'::timestamp, '2025-01-01', '1 day') as time ;  

create or replace view cube as select f.*, m.minimum, m.maximum, m.average, v.value as deaths, rki.value as covid_deaths from facts f 
    left outer join destatis6_moments_fused m on f.time=m.time
    left outer join destatis6_view v on f.time=v.time
    left outer join rki_covid_deaths_view rki on f.time=rki.timestamp

