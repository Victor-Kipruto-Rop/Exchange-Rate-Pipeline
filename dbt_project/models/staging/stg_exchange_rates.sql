SELECT
    base_currency,
    target_currency,
    rate,
    rate_date::timestamp AS rate_at,
    loaded_at
FROM raw_exchange_rates
WHERE rate > 0
