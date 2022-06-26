ALTER TABLE recipes ADD PRIMARY KEY (n_recipe_id);
ALTER TABLE Items ADD PRIMARY KEY (n_item_id);

ALTER TABLE Ingredients ADD FOREIGN KEY (n_recipe_id) REFERENCES Recipes (n_recipe_id);
-- ALTER TABLE Ingredients ADD FOREIGN KEY (n_item_id) REFERENCES Items (n_item_id);
ALTER TABLE Ingredients ADD PRIMARY KEY (n_ingredient_id);

CREATE TABLE Users
(
    n_user_id  serial      NOT NULL,
    s_username varchar(32) NOT NULL,
    PRIMARY KEY (n_user_id)
);

CREATE TABLE Pantry
(
    n_pantry_id       serial NOT NULL,
    n_user_id         int    NOT NULL,
    n_item_id         int    NOT NULL,
    s_unit_type       varchar(32), -- kg, l, mm, ...
    f_amount_in_stock float,
    ts_creation       timestamp DEFAULT CURRENT_TIMESTAMP,
    dt_expire_date    date,
    b_in_stock        boolean   default True,
    PRIMARY KEY (n_pantry_id),
    FOREIGN KEY (n_user_id) REFERENCES USERS (n_user_id),
    FOREIGN KEY (n_item_id) REFERENCES Items (n_item_id)
);

-- CREATE TABLE Recipe_Keywords
-- (
--     n_keyword_id serial       NOT NULL,
--     s_keyword    varchar(128) NOT NULL,
--     n_recipe_id  int          NOT NULL,
--     PRIMARY KEY (n_keyword_id),
--     FOREIGN KEY (n_recipe_id) REFERENCES Recipes (n_recipe_id)
-- );



--
-- CREATE TABLE Rankings
-- (
--     n_ranking_id    serial NOT NULL,
--     n_user_id       int    NOT NULL,
--     n_recipe_id     int    NOT NULL,
--     n_ranking_value int DEFAULT NULL,
--     PRIMARY KEY (n_ranking_id),
--     FOREIGN KEY (n_user_id) REFERENCES USERS (n_user_id),
--     FOREIGN KEY (n_recipe_id) REFERENCES recipes (n_recipe_id)
--
-- );
-- CREATE TABLE Ingredients
-- (
--     n_ingredient_id serial NOT NULL,
--     s_ingredient    varchar(2048),
--     s_raw_ingredient    varchar(2048) NOT NULL,
--     n_recipe_id     int    NOT NULL,
--     n_item_id       int    NOT NULL,
--     s_unit_type       varchar(32), -- kg, l, mm, cups, tablespoons, ...
--     f_amount_needed float,
--
--     PRIMARY KEY (n_ingredient_id),
--     FOREIGN KEY (n_recipe_id) REFERENCES Recipes (n_recipe_id),
--     FOREIGN KEY (n_item_id) REFERENCES Items (n_item_id)
-- );


-- CREATE TABLE Items
-- (
--     n_item_id   serial      NOT NULL,
--     s_item_name varchar(64) NOT NULL,
--     PRIMARY KEY (n_item_id)
-- );

-- CREATE TABLE Recipes
-- (
-- --     n_recipe_id       serial       NOT NULL,
--     n_recipe_id       int,
--     s_recipe_title    varchar(128) NOT NULL,
--     array_ingredients text[200],
--     s_directions      varchar(4096),
--     s_link            varchar(128),
--     s_source          varchar(128),
--     array_NER         text[],
--     PRIMARY KEY (n_recipe_id)
-- );
