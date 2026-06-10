SELECT
    target_currency,
    rate_at::date AS rate_date,
    rate,
    LAG(rate) OVER (PARTITION BY target_currency ORDER BY rate_at) AS prev_rate,
    ROUND(((rate - LAG(rate) OVER (PARTITION BY target_currency ORDER BY rate_at))
           / NULLIF(LAG(rate) OVER (PARTITION BY target_currency ORDER BY rate_at), 0) * 100)::numeric, 4)
        AS pct_change
FROM {{ ref('stg_exchange_rates') }}
WHERE base_currency = 'USD'
ORDER BY target_currency, rate_date
