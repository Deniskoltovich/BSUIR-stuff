CREATE TABLE suppliers  ( 
     id INT NOT NULL AUTO_INCREMENT,
     name VARCHAR(16) NOT NULL,
     status INT NOT NULL, 
     city VARCHAR(64),
     PRIMARY KEY (id) );


INSERT INTO suppliers (name, status, city)
    VALUES ('Петров', 20, 'Москва'),
     ('Синицин', 10, 'Таллин'),
     ( 'Федоров', 30, 'Таллин'),
     ( 'Чаянов', 20, 'Минск'),
     ( 'Крюков', 30, 'Киев');


CREATE TABLE details (
     id INT NOT NULL AUTO_INCREMENT,
     name VARCHAR(64) NOT NULL,
     color VARCHAR(64) NOT NULL,
     size INT NOT NULL,
     city VARCHAR(64) NOT NULL,
     PRIMARY KEY (id)
);

INSERT INTO details (name,color, size, city) VALUES
     ('Болт', 'Красный', 12, 'Москва'),
     ('Гайка', 'Зеленая', 17, 'Минск'),
     ('Диск', 'Черный', 17, 'Вильнюс'),
     ('Диск', 'Черный', 14, 'Москва'),
     ('Корпус', 'Красный', 12, 'Минск'),
     ('Крышкин', 'Красный', 19, 'Москва');

CREATE TABLE projects (
     id INT NOT NULL AUTO_INCREMENT,
     name VARCHAR(64) NOT NULL,
     city VARCHAR(64) NOT NULL,
     PRIMARY KEY (id)
);

INSERT INTO projects (name,city) VALUES
     ('ИПР1', 'Минск'),
     ('ИПР2', 'Таллин'),
     ('ИПР3', 'Псков'),
     ('ИПР4', 'Псков'),
     ('ИПР4', 'Москва'),
     ('ИПР6', 'Саратов'),
     ('ИПР7', 'Москва');


CREATE TABLE num_of_ditails_per_project (
     id INT NOT NULL AUTO_INCREMENT,
     supplier_id INT, 
     detail_id INT, 
     project_id INT, 
     s INT,
     PRIMARY KEY (id),
     FOREIGN KEY (supplier_id) REFERENCES suppliers (id) ON DELETE CASCADE,
     FOREIGN KEY (detail_id) REFERENCES details (id) ON DELETE CASCADE,
     FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE
     );

INSERT INTO num_of_ditails_per_project ( supplier_id, detail_id, project_id, s ) VALUES
     (1, 1, 1, 200),
     (1, 1, 2, 700),
     (2, 3, 1, 400),
     (2, 2, 2, 200),
     (2, 3, 3, 200),
     (2, 3, 4, 500),
     (2, 3, 5, 600),
     (2, 3, 6, 400),
     (2, 3, 7, 800),
     (2, 5, 2, 100),
     (3, 3, 1, 200),
     (3, 4, 2, 500),
     (4, 6, 3, 300),
     (4, 6, 7, 300),
     (5, 2, 2, 200),
     (5, 2, 4, 100),
     (5, 5, 5, 500),
     (5, 5, 7, 100),
     (5, 6, 2, 200),
     (5, 1, 2, 100),
     (5, 3, 4, 200),
     (5, 4, 4, 800),
     (5, 5, 4, 400),
     (5, 6, 4, 500);
     







