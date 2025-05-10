with sales as (

    select * from {{ ref('sales_model') }}

),

aggregated as (

    select
        date_trunc('day', timestamp) as sale_date,
        sum(total_price) as total_sales,
        count(*) as total_transactions,
        sum(quantity) as total_units_sold

    from sales
    group by 1

)

select * from aggregated
