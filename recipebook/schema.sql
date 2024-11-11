CREATE TABLE user (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL
);


CREATE TABLE recipe (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    ingredients TEXT NOT NULL,
    steps TEXT NOT NULL,
    category VARCHAR(50) NOT NULL,
    image_path VARCHAR(255) NULL,
    FOREIGN KEY (user_id) REFERENCES user(user_id)
);