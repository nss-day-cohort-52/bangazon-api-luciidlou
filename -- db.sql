-- SQLite
CREATE VIEW PRODUCTS_MIN_1000 AS
SELECT
p.name as product_name,
p.price as product_price,
p.description as product_description,
p.quantity,
p.location,
c.name as category
FROM
bangazon_api_product as p
JOIN bangazon_api_category as c
ON p.category_id = c.id
WHERE p.price >= 1000
ORDER BY product_price


CREATE VIEW PRODUCTS_MAX_1000 AS
SELECT
p.name as product_name,
p.price as product_price,
p.description as product_description,
p.quantity,
p.location,
c.name as category
FROM
bangazon_api_product as p
JOIN bangazon_api_category as c
ON p.category_id = c.id
WHERE p.price <= 1000
ORDER BY product_price


SELECT
o.id as order_id,
u.first_name || " " || u.last_name as customer,
o.total,
o.payment_type.merchant_name as payment_type
FROM
bangazon_api_order as o
JOIN auth_user as u 
ON o.customer_id = u.id
