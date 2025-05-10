-- models/marts/fct_sales_summary.sql

with sales as (

    select * 
    from {{ ref('sales_model') }}

),

aggregated as (

    select
        category,
        count(*) as total_sales,
        sum(quantity) as total_quantity,
        sum(total_price) as total_revenue,
        avg(price) as avg_unit_price
    from sales
    group by category

)

select * from aggregated
