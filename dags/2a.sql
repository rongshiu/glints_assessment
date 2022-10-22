-- since the structure of ingestion is appending table, it is important to select with condition of latest created_at to avoid duplication
with cte as (
    select to_date("week",'MM/DD/YYYY HH12:MI:SS AM/PM') as "week",
        district_name,
        student_count,
        rank() over (
            partition by "week"
            order by student_count desc
        ) as weekly_rank
    from public.source_table
    where student_count is not null
        and created_at =(
            select max(created_at)
            from public.source_table
        )
)
select *
from cte
where weekly_rank <= 5