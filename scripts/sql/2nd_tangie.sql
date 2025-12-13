SELECT DISTINCT
    u.id,
    u.cell,
    u.name,
    u.created_at,
    u.updated_at
FROM 
    users u
INNER JOIN 
    fruits f ON u.id = f.user_id
WHERE 
    f.template_id = '9a42b9e0-cc8f-4a1b-bbaa-75b9f08e5672'
    AND f.status = 'COMPLETED';