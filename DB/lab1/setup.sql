CREATE TABLE teachers  ( 
     id INT NOT NULL AUTO_INCREMENT,
     personal_number VARCHAR(16) UNIQUE NOT NULL,
     lastname VARCHAR(64) NOT NULL, 
     job_title VARCHAR(64) NOT NULL, 
     department VARCHAR(16) NOT NULL, 
     specialization VARCHAR(64) NOT NULL, 
     home_phone VARCHAR(16) NOT NULL, 
     PRIMARY KEY (id) );


INSERT INTO teachers (personal_number, lastname, job_title, department, specialization, home_phone)
    VALUES ('221Л', 'Фролов', 'Доцент', 'ЭВМ', 'АСОИ, ЭМВ', '487'),
     ('222Л', 'Костин', 'Доцент', 'ЭВМ', 'ЭМВ', '543'),
     ('225Л', 'Бойко', 'Профессор', 'АСУ', 'АСОИ ЭМВ', '112'),
     ('430Л', 'Глазов', 'Ассистент', 'ТФ', 'СД', '421'),
     ('110Л', 'Петров', 'Ассистент', 'Экономики', 'Международная экономика', '324');


CREATE TABLE subjects (
     id INT NOT NULL AUTO_INCREMENT,
     code_number VARCHAR(16) NOT NULL UNIQUE,
     name VARCHAR(64) NOT NULL,
     hours INT NOT NULL,
     specialization VARCHAR(64) NOT NULL,
     semester INT NOT NULL,
     PRIMARY KEY (id)
);

INSERT INTO subjects ( code_number, name, hours, specialization, semester ) VALUES
     ('12П', 'Мини ЭВМ', 36, 'ЭВМ', 1),
     ('14П', 'ПЭВМ', 72, 'ЭВМ', 2),
     ('17П', 'СУБД ПК', 48, 'АСОИ', 4),
     ('18П', 'ВКСС', 52, 'АСОИ', 6),
     ('34П', 'Физика', 30, 'СД', 6),
     ('22П', 'Аудит', 24, 'Бухучета', 3);


CREATE TABLE student_groups (
     id INT NOT NULL AUTO_INCREMENT,
     code_number VARCHAR(16) NOT NULL UNIQUE, 
     name VARCHAR(64) NOT NULL, 
     number_of_students INT NOT NULL, 
     specialization VARCHAR(64) NOT NULL, 
     headman_lastname VARCHAR(64) NOT NULL,
     PRIMARY KEY (id)
     );


INSERT INTO student_groups ( code_number, name, number_of_students, specialization, headman_lastname ) VALUES
     ('8Г', 'Э-12', 18, 'ЭВМ', 'Иванова'),
     ('7Г', 'Э-15', 22, 'ЭВМ', 'Сеткин'),
     ('4Г', 'АС-9', 24, 'АСОИ', 'Балабанов'),
     ('3Г', 'АС-8', 20, 'АСОИ', 'Чижов'),
     ('17Г', 'С-14', 29, 'СД', 'Амросов'),
     ('12Г', 'М-6', 16, 'Международная экономика', 'Трубин'),
     ('10Г', 'Б-4', 21, 'Бухучет', 'Зязюткин');



CREATE TABLE teacher_teaches_subjects_in_groups (
     id INT NOT NULL AUTO_INCREMENT,
     group_code_number VARCHAR(16) NOT NULL, 
     subject_code_number VARCHAR(16) NOT NULL, 
     personal_number VARCHAR(64) NOT NULL, 
     audit_number INT NOT NULL, 
     PRIMARY KEY (id)
     );

INSERT INTO teacher_teaches_subjects_in_groups ( group_code_number, subject_code_number, personal_number, audit_number ) VALUES
     ('8Г', '12П', '222Л', 112),
     ('8Г', '14П', '221Л', 220),
     ('8Г', '17П', '222Л', 112),
     ('7Г', '14П', '221Л', 220),
     ('7Г', '17П', '222Л', 241),
     ('7Г', '18П', '225Л', 210),
     ('4Г', '12П', '222Л', 112),
     ('4Г', '18П', '225Л', 210),
     ('3Г', '12П', '222Л', 112),
     ('3Г', '17П', '221Л', 241),
     ('3Г', '18П', '225Л', 210),
     ('17Г', '12П', '222Л', 112),
     ('17Г', '22П', '110Л', 220),
     ('17Г', '34П', '430Л', 118),
     ('12Г', '12П', '222Л', 112),
     ('12Г', '22П', '110Л', 210),
     ('10Г', '12П', '222Л', 210),
     ('10Г', '22П', '110Л', 210);





