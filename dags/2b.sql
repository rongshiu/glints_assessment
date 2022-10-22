-- since the structure of ingestion is appending table, it is important to select with condition of latest created_at to avoid duplication
select to_date("week", 'MM/DD/YYYY HH12:MI:SS AM/PM') as "week",
    district_name,
    learning_modality
from public.source_table
where created_at =(
        select max(created_at)
        from public.source_table
    )