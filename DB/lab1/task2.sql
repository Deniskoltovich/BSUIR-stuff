вар10

#23
SELECT DISTINCT supplier_id
FROM num_of_ditails_per_project
WHERE detail_id IN (
    SELECT DISTINCT detail_id
    FROM num_of_ditails_per_project
    WHERE supplier_id IN (
        SELECT DISTINCT supplier_id
        FROM num_of_ditails_per_project
        WHERE detail_id IN (
            SELECT DISTINCT detail_id
            FROM details
            WHERE color = 'Красный'
        )
    )
);


#20
SELECT DISTINCT details.color
FROM num_of_ditails_per_project
 JOIN details ON num_of_ditails_per_project.detail_id = details.id
WHERE num_of_ditails_per_project.supplier_id = 1;

#28
SELECT DISTINCT p.id
FROM projects p
WHERE NOT EXISTS (
  SELECT *
  FROM num_of_ditails_per_project nd
  JOIN suppliers s ON nd.supplier_id = s.id
  JOIN details d ON nd.detail_id = d.id
  WHERE nd.project_id = p.id AND d.color = 'Красный' AND s.city = 'Лондон'
); 
SELECT DISTINCT d1.color, d2.city FROM details d1 CROSS JOIN details d2;
#6
SELECT s.id AS supplier_id, d.id AS detail_id, p.id AS project_id
FROM num_of_ditails_per_project AS ndpp
 JOIN suppliers s ON ndpp.supplier_id = s.id
 JOIN details d ON ndpp.detail_id = d.id
 JOIN projects p ON ndpp.project_id = p.id
WHERE s.city = d.city AND s.city = p.city;
#10
SELECT ndpp.detail_id AS detail_id
FROM num_of_ditails_per_project AS ndpp
 JOIN suppliers AS s ON ndpp.supplier_id = s.id
 JOIN projects AS p ON ndpp.project_id = p.id
WHERE s.city = 'Лондон' AND p.city = 'Лондон';
#14
SELECT DISTINCT a.detail_id AS detail_id1, b.detail_id AS detail_id2
FROM num_of_ditails_per_project AS a
JOIN num_of_ditails_per_project AS b ON a.supplier_id = b.supplier_id
WHERE a.detail_id < b.detail_id;

#34
SELECT DISTINCT d.id
FROM details d
JOIN num_of_ditails_per_project np ON d.id = np.detail_id
JOIN suppliers s ON np.supplier_id = s.id
JOIN projects p ON np.project_id = p.id
WHERE s.city = 'Лондон' OR p.city = 'Лондон';

#19
SELECT DISTINCT projects.name
FROM num_of_ditails_per_project
JOIN projects ON num_of_ditails_per_project.project_id = projects.id
WHERE num_of_ditails_per_project.supplier_id = 1;

#35
SELECT s.id AS supplier_id, d.id AS detail_id
FROM suppliers s
CROSS JOIN details d
WHERE (s.id, d.id) NOT IN (
    SELECT supplier_id, detail_id
    FROM num_of_ditails_per_project
);

