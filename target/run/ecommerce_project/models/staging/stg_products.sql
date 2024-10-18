
  create view "d9snqvovhsjpqs"."public"."stg_products__dbt_tmp"
    
    
  as (
    WITH raw_products AS (
    SELECT
        product_id,
        product_name,
        category,
        price
    FROM "d9snqvovhsjpqs"."public"."products"
)
SELECT
    product_id,
    product_name,
    category,
    price::decimal AS price
FROM raw_products
  );