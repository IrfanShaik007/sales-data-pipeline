
-- models/staging/stg_sales.sql

with source as (

    select * 
    from {{ source('raw_sales', 'raw_sales_data') }}

),

renamed as (

    select
        sale_id,
        product_id,
        product_name,
        category,
        price,
        quantity,
        total_price,
        timestamp

    from source

)

select * from renamed

