CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE listener (
    user_id       INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    username      VARCHAR(50)  NOT NULL UNIQUE,
    password_hash VARCHAR(100) NOT NULL,
    email         VARCHAR(255) NOT NULL UNIQUE,
    created_date  TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_email_format CHECK (email LIKE '%_@_%._%')
);

CREATE TABLE song_library (
    song_library_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id         INT NOT NULL UNIQUE
                    REFERENCES listener(user_id) ON DELETE CASCADE,
    created_date    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE artist (
    artist_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name      VARCHAR(150) NOT NULL,
    bio       TEXT
);

CREATE TABLE song (
    song_id      INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    title        VARCHAR(200) NOT NULL,
    duration     INT NOT NULL CHECK (duration > 0),
    genre        VARCHAR(50),
    release_date DATE
);

CREATE TABLE album (
    album_id     INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    title        VARCHAR(200) NOT NULL,
    release_date DATE,
    cover_image  VARCHAR(500)
);

CREATE TABLE playlist (
    playlist_id  INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id      INT NOT NULL
                 REFERENCES listener(user_id) ON DELETE CASCADE,
    name         VARCHAR(100) NOT NULL,
    description  TEXT,
    created_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_playlist_name_per_user UNIQUE (user_id, name)
);

CREATE TABLE song_artist (
    song_id   INT NOT NULL REFERENCES song(song_id)     ON DELETE CASCADE,
    artist_id INT NOT NULL REFERENCES artist(artist_id) ON DELETE CASCADE,
    PRIMARY KEY (song_id, artist_id)
);

CREATE TABLE album_artist (
    album_id  INT NOT NULL REFERENCES album(album_id)   ON DELETE CASCADE,
    artist_id INT NOT NULL REFERENCES artist(artist_id) ON DELETE CASCADE,
    PRIMARY KEY (album_id, artist_id)
);

CREATE TABLE album_song (
    album_id     INT NOT NULL REFERENCES album(album_id) ON DELETE CASCADE,
    song_id      INT NOT NULL REFERENCES song(song_id)   ON DELETE CASCADE,
    track_number INT NOT NULL CHECK (track_number > 0),
    PRIMARY KEY (album_id, song_id),
    CONSTRAINT uq_album_track UNIQUE (album_id, track_number)
);

CREATE TABLE playlist_song (
    playlist_id INT NOT NULL REFERENCES playlist(playlist_id) ON DELETE CASCADE,
    song_id     INT NOT NULL REFERENCES song(song_id)         ON DELETE CASCADE,
    position    INT NOT NULL CHECK (position > 0),
    added_date  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (playlist_id, song_id)
);

CREATE TABLE library_song (
    song_library_id INT NOT NULL
                    REFERENCES song_library(song_library_id) ON DELETE CASCADE,
    song_id         INT NOT NULL REFERENCES song(song_id)    ON DELETE CASCADE,
    saved_date      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (song_library_id, song_id)
);

CREATE INDEX idx_playlist_user       ON playlist(user_id);
CREATE INDEX idx_song_artist_artist  ON song_artist(artist_id);
CREATE INDEX idx_album_artist_artist ON album_artist(artist_id);
CREATE INDEX idx_library_song_song   ON library_song(song_id);
CREATE INDEX idx_playlist_song_song  ON playlist_song(song_id);
