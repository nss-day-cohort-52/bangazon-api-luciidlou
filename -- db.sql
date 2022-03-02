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
ON p.category_id- = c.id
WHERE p.price <= 1000
ORDER BY product_price


CREATE VIEW COMPLETED_ORDERS AS
SELECT
o.id as order_id,
u.first_name || " " || u.last_name as customer,
SUM(p.price) as order_total,
pt.merchant_name as payment_type
FROM
bangazon_api_order as o
JOIN 
auth_user as u,
bangazon_api_orderproduct as op,
bangazon_api_product as p,
bangazon_api_paymenttype as pt
ON o.user_id = u.id
AND o.id = op.order_id
AND op.product_id = p.id
AND o.payment_type_id = pt.id
WHERE o.payment_type_id IS NOT NULL
GROUP BY o.id

CREATE VIEW INCOMPLETE_ORDERS AS
SELECT
o.id as order_id,
u.first_name || " " || u.last_name as customer,
SUM(p.price) as order_total,
o.created_on
FROM
bangazon_api_order as o
JOIN 
auth_user as u,
bangazon_api_orderproduct as op,
bangazon_api_product as p
ON o.user_id = u.id
AND o.id = op.order_id
AND op.product_id = p.id
WHERE o.completed_on ISNULL
GROUP BY o.id

CREATE VIEW FAV_SELLERS AS
SELECT
u.id as user_id,
u.first_name || " " || u.last_name as customer,
s.id as store_id,
s.name as store
FROM
bangazon_api_store as s
JOIN 
bangazon_api_favorite as f,
auth_user as u
ON s.id = f.store_id
AND f.customer_id = u.id
