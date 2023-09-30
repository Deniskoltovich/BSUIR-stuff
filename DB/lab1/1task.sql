SELECT
    *
FROM
    teachers;

SELECT
    *
FROM
    student_groups
where
    specialization = 'ЭВМ';

SELECT
    personal_number,
    audit_number
FROM
    teacher_teaches_subjects_in_groups
where
    subject_code_number = '18П';

SELECT
    t.subject_code_number,
    s.name
FROM
    teacher_teaches_subjects_in_groups t
    JOIN subjects s ON t.subject_code_number = s.code_number
    JOIN teachers teach ON teach.personal_number = t.personal_number
WHERE
    teach.lastname = 'Костин';

SELECT
    group_code_number
FROM
    teacher_teaches_subjects_in_groups t
    JOIN teachers ON t.personal_number = teachers.personal_number
WHERE
    teachers.lastname = 'Фролов';

SELECT
    *
FROM
    subjects
WHERE
    specialization LIKE 'АСОИ';

SELECT
    DISTINCT teachers.*
from
    teacher_teaches_subjects_in_groups t
    JOIN teachers ON teachers.personal_number = t.personal_number
    JOIN subjects s ON s.code_number = t.subject_code_number
where
    s.specialization = 'АСОИ';

SELECT
    DISTINCT t.lastname
FROM
    teachers t
    JOIN teacher_teaches_subjects_in_groups ttsg ON ttsg.personal_number = t.personal_number
WHERE
    ttsg.audit_number = 210;

SELECT
    s.name AS subject_name,
    g.name AS group_name
FROM
    subjects s
    JOIN teacher_teaches_subjects_in_groups ttsg ON s.code_number = ttsg.subject_code_number
    JOIN student_groups g ON ttsg.group_code_number = g.code_number
WHERE
    ttsg.audit_number BETWEEN 100
    AND 200;

SELECT
    s1.code_number AS group1,
    s2.code_number AS group2
FROM
    student_groups s1
    JOIN student_groups s2 ON s1.specialization = s2.specialization
WHERE
    NOT s1.code_number = s2.code_number;

SELECT
    SUM(number_of_students) AS num_of_students
FROM
    student_groups
WHERE
    specialization = 'ЭВМ';

SELECT
    t.personal_number
FROM
    teachers t
    JOIN teacher_teaches_subjects_in_groups ttsg ON t.personal_number = ttsg.personal_number
    JOIN student_groups g ON g.code_number = ttsg.group_code_number
WHERE
    g.specialization = 'ЭВМ';

SELECT
    ttsg.subject_code_number
FROM
    teacher_teaches_subjects_in_groups ttsg
    JOIN student_groups s on s.code_number = ttsg.group_code_number
GROUP BY
    ttsg.subject_code_number
HAVING
    (
        SELECT
            COUNT(*)
        FROM
            student_groups
    ) = COUNT(s.code_number);

#14 SELECT DISTINCT t.lastname FROM teachers t
JOIN teacher_teaches_subjects_in_groups ttsg ON t.personal_number = ttsg.personal_number
WHERE
    ttsg.subject_code_number IN (
        SELECT
            subject_code_number
        FROM
            teacher_teaches_subjects_in_groups
        WHERE
            personal_number = (
                SELECT
                    DISTINCT personal_number
                FROM
                    teacher_teaches_subjects_in_groups
                WHERE
                    subject_code_number = '14П'
            )
    );

#15
SELECT
    s.*
from
    subjects s
    JOIN teacher_teaches_subjects_in_groups t on s.code_number = t.subject_code_number
WHERE
    t.personal_number != '221Л';

#16 
SELECT
    s.*
FROM
    subjects s
WHERE
    s.code_number NOT IN (
        SELECT
            t.subject_code_number
        FROM
            teacher_teaches_subjects_in_groups t
            JOIN student_groups g on g.code_number = t.group_code_number
        WHERE
            g.name = 'М-6'
    );

#17 
SELECT
    DISTINCT t.*
FROM
    teachers t
    JOIN teacher_teaches_subjects_in_groups ttsg ON ttsg.personal_number = t.personal_number
WHERE
    t.job_title = 'Доцент'
    AND (
        ttsg.group_code_number = '3Г'
        OR ttsg.group_code_number = '8Г'
    );

#18 
SELECT
    ttsg.subject_code_number,
    ttsg.personal_number,
    ttsg.group_code_number
FROM
    teacher_teaches_subjects_in_groups ttsg
    JOIN teachers t ON t.personal_number = ttsg.personal_number
WHERE
    t.specialization LIKE 'АСОИ%'
    AND t.department = 'ЭВМ';

#19 
SELECT
    g.code_number
FROM
    teacher_teaches_subjects_in_groups ttsg
    JOIN teachers t ON t.personal_number = ttsg.personal_number
    JOIN student_groups g on g.code_number = ttsg.group_code_number
WHERE
    LOCATE(g.specialization, t.specialization);

#20 
SELECT
    DISTINCT ttsg.personal_number
FROM
    teacher_teaches_subjects_in_groups ttsg
    JOIN subjects s ON s.code_number = ttsg.subject_code_number
    JOIN teachers t on t.personal_number = ttsg.personal_number
    JOIN student_groups g ON g.code_number = ttsg.group_code_number
WHERE
    LOCATE('ЭВМ', t.specialization)
    AND s.specialization = g.specialization;

#21 
SELECT
    DISTINCT g.specialization
FROM
    student_groups g
    JOIN teacher_teaches_subjects_in_groups ttsg on ttsg.group_code_number = g.code_number
    JOIN teachers t on t.personal_number = ttsg.personal_number
WHERE
    t.department = 'АСУ';

#22 
SELECT
    ttsg.subject_code_number
FROM
    teacher_teaches_subjects_in_groups ttsg
    JOIN student_groups g ON ttsg.group_code_number = g.code_number
WHERE
    g.name = 'АС-8';

#23 
SELECT DISTINCT ttsg.group_code_number
FROM teacher_teaches_subjects_in_groups ttsg
WHERE ttsg.subject_code_number IN (
    SELECT subject_code_number
    FROM teacher_teaches_subjects_in_groups
    WHERE group_code_number = '3Г'
)
GROUP BY ttsg.group_code_number
HAVING COUNT(DISTINCT ttsg.subject_code_number) = (
    SELECT COUNT(DISTINCT subject_code_number)
    FROM teacher_teaches_subjects_in_groups
    WHERE group_code_number = '3Г'
);


#24 
SELECT
    DISTINCT sg.code_number
FROM
    student_groups sg
WHERE
    sg.code_number NOT IN (
        SELECT
            DISTINCT ttsg.group_code_number
        FROM
            teacher_teaches_subjects_in_groups ttsg
        WHERE
            ttsg.subject_code_number IN (
                SELECT
                    DISTINCT ttsg.subject_code_number
                FROM
                    teacher_teaches_subjects_in_groups ttsg
                WHERE
                    ttsg.group_code_number IN (
                        SELECT
                            DISTINCT sg2.code_number
                        FROM
                            student_groups sg2
                        WHERE
                            sg2.name = 'АС-8'
                    )
            )
    );

#25 
SELECT
    DISTINCT sg.code_number
FROM
    student_groups sg
WHERE
    sg.code_number NOT IN (
        SELECT
            DISTINCT ttsg.group_code_number
        FROM
            teacher_teaches_subjects_in_groups ttsg
        WHERE
            ttsg.personal_number = '430Л'
    );

#26
SELECT
    DISTINCT ttsg.personal_number
FROM
    teacher_teaches_subjects_in_groups ttsg
    JOIN student_groups sg ON ttsg.group_code_number = sg.code_number
WHERE
    sg.name = 'Э-15'
    AND ttsg.personal_number NOT IN (
        SELECT
            ttsg_inner.personal_number
        FROM
            teacher_teaches_subjects_in_groups ttsg_inner
        WHERE
            ttsg_inner.subject_code_number = '12П'
    );


