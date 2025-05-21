{{
    config(
        materialized='incremental',
        on_schema_change='fail',
        tags=['fact', 'reviews'],
        description="Fact table containing reviews data."
    )
}}
WITH src_reviews AS (
    SELECT
        *
    FROM {{ ref('src_reviews') }}
)
SELECT * FROM src_reviews
WHERE review_text IS NOT NULL
AND review_text != ''
{% if is_incremental() %}
    AND review_date > (SELECT MAX(review_date) FROM {{ this }})
{% endif %}