SELECT 
    e.name AS employee_name,
    (p.salary * c.tax_percentage) / 100 AS tax_amount
FROM 
    employees e
JOIN 
    positions p ON e.position_id = p.id
JOIN 
    contracts c ON e.contract_id = c.id
WHERE 
    p.salary < 50000;
