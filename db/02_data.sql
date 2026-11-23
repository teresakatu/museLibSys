INSERT INTO artist (name, bio) VALUES
('Taylor Swift',      'American singer-songwriter known for narrative pop and country songwriting.'),
('Kendrick Lamar',    'Compton, California rapper and Pulitzer Prize winner.'),
('SZA',               'American R&B singer-songwriter from St. Louis, Missouri.'),
('Bad Bunny',         'Puerto Rican rapper and singer, leading figure in reggaeton and Latin trap.'),
('Billie Eilish',     'American singer-songwriter who writes and produces with her brother FINNEAS.'),
('The Weeknd',        'Canadian singer and producer known for dark, synth-driven R&B.'),
('Daft Punk',         'French electronic music duo active from 1993 to 2021.'),
('Pharrell Williams', 'American producer, singer and member of The Neptunes.'),
('Olivia Rodrigo',    'American singer-songwriter and actress.'),
('Frank Ocean',       'American singer-songwriter known for experimental R&B.');

INSERT INTO song (title, duration, genre, release_date) VALUES
('Anti-Hero',           200, 'Pop',        '2022-10-21'),
('Cruel Summer',        178, 'Pop',        '2019-08-23'),
('Lavender Haze',       202, 'Pop',        '2022-10-21'),
('HUMBLE.',             177, 'Hip-Hop',    '2017-03-30'),
('DNA.',                185, 'Hip-Hop',    '2017-04-14'),
('Not Like Us',         274, 'Hip-Hop',    '2024-05-04'),
('All The Stars',       232, 'Hip-Hop',    '2018-01-04'),
('Kill Bill',           153, 'R&B',        '2022-12-09'),
('Snooze',              201, 'R&B',        '2022-12-09'),
('Good Days',           279, 'R&B',        '2020-12-25'),
('Tití Me Preguntó',    243, 'Reggaeton',  '2022-05-06'),
('Me Porto Bonito',     178, 'Reggaeton',  '2022-05-06'),
('bad guy',             194, 'Pop',        '2019-03-29'),
('BIRDS OF A FEATHER',  210, 'Pop',        '2024-05-17'),
('LUNCH',               179, 'Pop',        '2024-05-17'),
('Blinding Lights',     200, 'Synth-pop',  '2019-11-29'),
('Save Your Tears',     215, 'Synth-pop',  '2020-03-20'),
('Starboy',             230, 'R&B',        '2016-09-22'),
('Get Lucky',           369, 'Disco',      '2013-04-19'),
('Instant Crush',       337, 'Electronic', '2013-05-17'),
('Happy',               233, 'Pop',        '2013-11-21'),
('drivers license',     242, 'Pop',        '2021-01-08'),
('good 4 u',            178, 'Pop-punk',   '2021-05-14'),
('vampire',             219, 'Pop',        '2023-06-30'),
('Pink + White',        184, 'R&B',        '2016-08-20'),
('Nights',              307, 'R&B',        '2016-08-20');

INSERT INTO song_artist (song_id, artist_id) VALUES
(1,1),(2,1),(3,1),
(4,2),(5,2),(6,2),(7,2),(7,3),
(8,3),(9,3),(10,3),
(11,4),(12,4),
(13,5),(14,5),(15,5),
(16,6),(17,6),(18,6),(18,7),
(19,7),(19,8),(20,7),
(21,8),
(22,9),(23,9),(24,9),
(25,10),(26,10);

INSERT INTO album (title, release_date, cover_image) VALUES
('Midnights',               '2022-10-21', 'covers/midnights.jpg'),
('Lover',                   '2019-08-23', 'covers/lover.jpg'),
('DAMN.',                   '2017-04-14', 'covers/damn.jpg'),
('SOS',                     '2022-12-09', 'covers/sos.jpg'),
('Un Verano Sin Ti',        '2022-05-06', 'covers/un_verano_sin_ti.jpg'),
('HIT ME HARD AND SOFT',    '2024-05-17', 'covers/hmhas.jpg'),
('After Hours',             '2020-03-20', 'covers/after_hours.jpg'),
('Starboy',                 '2016-11-25', 'covers/starboy.jpg'),
('Random Access Memories',  '2013-05-17', 'covers/ram.jpg'),
('SOUR',                    '2021-05-21', 'covers/sour.jpg'),
('GUTS',                    '2023-09-08', 'covers/guts.jpg'),
('Blonde',                  '2016-08-20', 'covers/blonde.jpg');

INSERT INTO album_artist (album_id, artist_id) VALUES
(1,1),(2,1),(3,2),(4,3),(5,4),(6,5),(7,6),(8,6),(9,7),(10,9),(11,9),(12,10);

INSERT INTO album_song (album_id, song_id, track_number) VALUES
(1,3,1),(1,1,3),
(2,2,2),
(3,5,2),(3,4,8),
(4,8,9),(4,9,10),
(5,12,2),(5,11,3),
(6,14,4),(6,15,2),
(7,16,9),(7,17,11),
(8,18,1),
(9,19,8),(9,20,5),
(10,22,3),(10,23,6),
(11,24,2),
(12,25,3),(12,26,7);

INSERT INTO listener (username, password_hash, email, created_date) VALUES
('sgraciano', crypt('Sun$et2026',   gen_salt('bf')), 'sgraciano@asu.edu',     '2026-08-20 10:15:00'),
('flopez',    crypt('Desert#Rose9', gen_salt('bf')), 'flopez@asu.edu',        '2026-08-21 14:02:00'),
('tnguyen',   crypt('Lotus!Beats4', gen_salt('bf')), 'tnguyen@asu.edu',       '2026-08-22 09:45:00'),
('mkhan',     crypt('Ocean&Wave77', gen_salt('bf')), 'maya.khan@example.com', '2026-09-01 18:30:00'),
('jrivera',   crypt('Cactus*Jam12', gen_salt('bf')), 'jrivera@example.com',   '2026-09-10 21:10:00'),
('achen',     crypt('Neon@Night55', gen_salt('bf')), 'alex.chen@example.com', '2026-10-02 08:05:00');

INSERT INTO song_library (user_id, created_date)
SELECT user_id, created_date FROM listener ORDER BY user_id;

INSERT INTO playlist (user_id, name, description, created_date) VALUES
(1, 'Gym Hype',          'High-energy tracks for lifting.',              '2026-08-25 07:00:00'),
(1, 'Late Night Drive',  'Synths and slow R&B for the 101.',             '2026-09-02 23:40:00'),
(2, 'Study Session',     'Low-key songs for focus.',                     '2026-08-28 16:20:00'),
(3, 'Summer 2026',       'Everything I played on repeat this summer.',   '2026-08-30 12:00:00'),
(3, 'Throwbacks',        NULL,                                           '2026-09-15 19:05:00'),
(4, 'Fiesta',            'Reggaeton and dance.',                         '2026-09-05 20:00:00'),
(5, 'Sad Girl Hours',    'For when it rains (rarely, in Phoenix).',      '2026-09-12 01:15:00'),
(6, 'New Finds',         NULL,                                           '2026-10-03 10:00:00');

INSERT INTO playlist_song (playlist_id, song_id, position) VALUES
(1,4,1),(1,6,2),(1,16,3),(1,23,4),(1,19,5),
(2,16,1),(2,17,2),(2,26,3),(2,18,4),
(3,25,1),(3,10,2),(3,14,3),(3,9,4),
(4,2,1),(4,12,2),(4,14,3),(4,8,4),(4,1,5),
(5,19,1),(5,21,2),(5,13,3),
(6,11,1),(6,12,2),(6,19,3),
(7,22,1),(7,24,2),(7,8,3),(7,1,4);

INSERT INTO library_song (song_library_id, song_id, saved_date) VALUES
(1,4,'2026-08-25 07:05'),(1,6,'2026-08-25 07:06'),(1,16,'2026-09-02 23:45'),(1,19,'2026-09-03 08:00'),
(2,25,'2026-08-28 16:30'),(2,10,'2026-08-28 16:31'),(2,14,'2026-09-01 11:00'),(2,8,'2026-09-04 13:10'),
(3,2,'2026-08-30 12:10'),(3,1,'2026-08-30 12:11'),(3,14,'2026-08-31 09:00'),(3,12,'2026-09-01 15:20'),(3,21,'2026-09-15 19:10'),
(4,11,'2026-09-05 20:05'),(4,12,'2026-09-05 20:06'),(4,16,'2026-09-08 22:00'),
(5,22,'2026-09-12 01:20'),(5,24,'2026-09-12 01:21'),(5,8,'2026-09-12 01:22'),(5,1,'2026-09-13 18:00'),(5,14,'2026-09-20 17:45'),
(6,6,'2026-10-03 10:05'),(6,16,'2026-10-04 12:30');
