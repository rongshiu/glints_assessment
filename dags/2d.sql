-- create base cte limiting data size to oct data
-- since the structure of ingestion is appending table, it is important to select with condition of latest created_at to avoid duplication
with oct_data as (
select to_date("week",'MM/DD/YYYY HH12:MI:SS AM/PM') as "week",
    district_name,
    student_count
from public.source_table
where created_at =(
        select max(created_at)
        from public.source_table
    )
and to_date("week",'MM/DD/YYYY HH12:MI:SS AM/PM')>='2022-10-01'
and to_date("week",'MM/DD/YYYY HH12:MI:SS AM/PM')<'2022-11-01'),

-- get first week of oct and last week of oct
get_relevant_date as (
select min("week") as first_week_of_oct,
max("week") as last_week_of_oct 
from oct_data),

get_initial_week_cte as (
select district_name, student_count as initial_student_count
from oct_data
where "week"=(select first_week_of_oct from get_relevant_date)),

get_final_week_cte as (
select district_name, student_count as final_student_count
from oct_data
where "week"=(select last_week_of_oct from get_relevant_date)),

-- full outer join will keep records where first week of oct of last week of oct data is missing
merged_cte as (
select coalesce(i.district_name,f.district_name),
i.initial_student_count,
f.final_student_count
from get_initial_week_cte i
full join get_final_week_cte f on f.district_name=i.district_name)

select m.*,final_student_count-initial_student_count as growth from merged_cte m
order by 4 desc