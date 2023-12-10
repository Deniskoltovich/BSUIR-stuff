CREATE TABLE Animals (
    ID SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    bio_type_id INT,
    age INT,
    cage INT,
    is_danger BOOLEAN NOT NULL DEFAULT FALSE,
    areal_id INT,
    FOREIGN KEY (bio_type_id) REFERENCES BioTypes(ID),
    FOREIGN KEY (areal_id) REFERENCES Areal(ID)
);

CREATE TABLE BioTypes (
    ID SERIAL PRIMARY KEY,
    type VARCHAR(255) NOT NULL
);

CREATE TABLE Areal (
    ID SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    image_link VARCHAR(255) NOT NUll
);


INSERT INTO BioTypes (type) VALUES 
    ('Млекопитающее'),
    ('Птица'),
    ('Рептилия');

INSERT INTO Areal (name, image_link) VALUES 
    ('Африка', 'link_to_africa_image.jpg'),
    ('Австралия', 'link_to_australia_image.jpg'),
    ('Южная Америка', 'link_to_south_america_image.jpg');

INSERT INTO Animals (name, bio_type_id, age, cage, type_id, is_danger, areal_id) VALUES
    ('Лев', 1, 5, 1, 1, TRUE, 1),
    ('Орел', 2, 3, 2, 2, FALSE, 2),
    ('Крокодил', 3, 8, 3, 1, TRUE, 3);


select * from Animals a 
    join BioTypes bt on bt.id = a.bio_type_id
    join Areal ar on ar.id = a.areal_id;