SELECT ps.position                                      AS "#",
       s.title,
       STRING_AGG(DISTINCT a.name, ', ')                AS artists,
       COALESCE(MAX(al.title), '(single)')              AS album,
       TO_CHAR(MAKE_INTERVAL(secs => s.duration), 'MI:SS') AS length
FROM listener l
JOIN playlist p        ON p.user_id = l.user_id
JOIN playlist_song ps  ON ps.playlist_id = p.playlist_id
JOIN song s            ON s.song_id = ps.song_id
JOIN song_artist sa    ON sa.song_id = s.song_id
JOIN artist a          ON a.artist_id = sa.artist_id
LEFT JOIN album_song als ON als.song_id = s.song_id
LEFT JOIN album al       ON al.album_id = als.album_id
WHERE l.username = 'sgraciano' AND p.name = 'Gym Hype'
GROUP BY ps.position, s.song_id, s.title, s.duration
ORDER BY ps.position;

SELECT s.title,
       STRING_AGG(DISTINCT a.name, ', ')        AS artists,
       COUNT(DISTINCT ls.song_library_id)       AS times_saved,
       COUNT(DISTINCT ps.playlist_id)           AS on_playlists
FROM song s
JOIN song_artist sa        ON sa.song_id = s.song_id
JOIN artist a              ON a.artist_id = sa.artist_id
JOIN library_song ls       ON ls.song_id = s.song_id
LEFT JOIN playlist_song ps ON ps.song_id = s.song_id
GROUP BY s.song_id, s.title
HAVING COUNT(DISTINCT ls.song_library_id) >= 2
ORDER BY times_saved DESC, on_playlists DESC, s.title;

INSERT INTO playlist_song (playlist_id, song_id, position)
SELECT p.playlist_id,
       (SELECT song_id FROM song WHERE title = 'Not Like Us'),
       COALESCE((SELECT MAX(position) FROM playlist_song
                 WHERE playlist_id = p.playlist_id), 0) + 1
FROM playlist p
JOIN listener l ON l.user_id = p.user_id
WHERE l.username = 'achen' AND p.name = 'New Finds'
RETURNING *;

UPDATE playlist
SET    name = 'Throwback Thursdays',
       description = 'Older favorites, 2013-2019.'
WHERE  name = 'Throwbacks'
  AND  user_id = (SELECT user_id FROM listener WHERE username = 'tnguyen')
RETURNING playlist_id, user_id, name, description;

DELETE FROM library_song
WHERE song_library_id = (SELECT sl.song_library_id
                         FROM song_library sl
                         JOIN listener l ON l.user_id = sl.user_id
                         WHERE l.username = 'flopez')
  AND song_id = (SELECT song_id FROM song WHERE title = 'Kill Bill')
RETURNING *;
