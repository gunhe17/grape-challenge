SELECT 
    u.id,
    u.cell,
    u.name,
    u.created_at,
    COUNT(m.id) as mission_count
FROM 
    users u
INNER JOIN 
    missions m ON u.id = m.user_id
GROUP BY 
    u.id, u.cell, u.name, u.created_at
ORDER BY 
    mission_count DESC;