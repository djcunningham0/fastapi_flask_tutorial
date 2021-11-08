INSERT INTO user (username, hashed_password)
VALUES
  ('test', '$2b$12$Qjg76DZ1ix6.Fgd7N0Ka4u/FdEGK7VFl3q8PZpPNOAbatrDE6fEL.'),  -- test
  ('other', '$2b$12$P8tP7WmYx3IoK8duwUKzJuZ7ZtNTZs8ZWpoaW.BRkImWhh/UDkK32')  -- passWord1
;

INSERT INTO post (title, body, author_id, created)
VALUES
  ('test title', 'test' || x'0a' || 'body', 1, '2018-01-01 00:00:00'),
  ('second post', 'second body', 2, '2021-10-27 01:02:03')
;