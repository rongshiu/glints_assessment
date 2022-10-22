-- to indicate state focusing more on “Hybrid” way of “Learning Modality” 
-- we will have to determine the ratio of operational schools in the state with "Hybrid" way of “Learning Modality” 
-- since the structure of ingestion is appending table, it is important to select with condition of latest created_at to avoid duplication
with cte as (
    select to_date("week", 'MM/DD/YYYY HH12:MI:SS AM/PM') as "week",
        state,
        learning_modality,
        sum(operational_schools) as operational_schools
    from public.source_table
    where created_at =(
            select max(created_at)
            from public.source_table
        )
    group by 1,
        2,
        3
),
get_hybrid_operational_schools as (
    select "week",
        state,
        operational_schools as hybrid_operational_schools
    from cte
    where learning_modality = 'Hybrid'
),
get_state_operational_schools as (
    select "week",
        state,
        sum(operational_schools) as state_operational_schools
    from cte
    group by 1,
        2
),
merged_cte as (
    select s.*,
        coalesce(h.hybrid_operational_schools, 0) as hybrid_operational_schools
    from get_state_operational_schools s
        left join get_hybrid_operational_schools h on s."week" = h."week"
        and s.state = h.state
)
select m.*,
    m.hybrid_operational_schools / m.state_operational_schools as ratio_of_hybrid_operational_schools
from merged_cte m
order by 5 desc,
    1 desc