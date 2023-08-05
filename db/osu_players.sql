CREATE TABLE osu_players (
    id INT auto_increment primary key,
    username VARCHAR(255) NOT NULL,
    osu_id INT NOT NULL,
    country VARCHAR(50) NOT NULL,
    global_rank INT NOT NULL,
    is_nl BOOL NOT NULL,
    game_mode VARCHAR(50) NOT NULL
);