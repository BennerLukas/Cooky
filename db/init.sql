DROP TABLE IF EXISTS Pantry;
DROP TABLE IF EXISTS Rankings;
DROP TABLE IF EXISTS Recipe_Keywords;
DROP TABLE IF EXISTS Ingredients;

DROP TABLE IF EXISTS Recipes;
DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Items;


CREATE TABLE Users
(
    n_user_id  serial      NOT NULL,
    s_username varchar(32) NOT NULL,
    PRIMARY KEY (n_user_id)
);

CREATE TABLE Items
(
    n_item_id   serial      NOT NULL,
    s_item_name varchar(64) NOT NULL,
    PRIMARY KEY (n_item_id)
);


CREATE TABLE Recipes
(
    n_recipe_id    serial       NOT NULL,
    s_recipe_title varchar(128) NOT NULL,
    -- array_ingredients text[],
    s_directions   varchar(4096),
    s_link         varchar(128),
    s_source       varchar(128),
    array_NER      text[],
    PRIMARY KEY (n_recipe_id)
);

CREATE TABLE Recipe_Keywords
(
    n_keyword_id serial       NOT NULL,
    s_keyword    varchar(128) NOT NULL,
    n_recipe_id  int          NOT NULL,
    PRIMARY KEY (n_keyword_id),
    FOREIGN KEY (n_recipe_id) REFERENCES Recipes (n_recipe_id)
);

CREATE TABLE Ingredients
(
    n_ingredient_id serial NOT NULL,
    n_recipe_id     int    NOT NULL,
    n_item_id       int    NOT NULL,

    PRIMARY KEY (n_ingredient_id),
    FOREIGN KEY (n_recipe_id) REFERENCES Recipes (n_recipe_id),
    FOREIGN KEY (n_item_id) REFERENCES Items (n_item_id)
);

CREATE TABLE Pantry
(
    n_pantry_id       serial NOT NULL,
    n_user_id         int    NOT NULL,
    n_item_id         int    NOT NULL,
    s_unit_type       varchar(32), -- kg, l, mm, ...
    n_amount_in_stock int,
    ts_creation       timestamp DEFAULT CURRENT_TIMESTAMP,
    dt_expire_date    date,
    b_in_stock        boolean   default True,
    PRIMARY KEY (n_pantry_id),
    FOREIGN KEY (n_user_id) REFERENCES USERS (n_user_id),
    FOREIGN KEY (n_item_id) REFERENCES Items (n_item_id)
);

CREATE TABLE Rankings
(
    n_ranking_id    serial NOT NULL,
    n_user_id       int    NOT NULL,
    n_recipe_id     int    NOT NULL,
    n_ranking_value int DEFAULT NULL,
    PRIMARY KEY (n_ranking_id),
    FOREIGN KEY (n_user_id) REFERENCES USERS (n_user_id),
    FOREIGN KEY (n_recipe_id) REFERENCES recipes (n_recipe_id)

);