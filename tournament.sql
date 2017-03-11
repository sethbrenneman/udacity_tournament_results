-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

create table players (
  player_id serial,
  player_name varchar(20),
  PRIMARY KEY(player_id)
);

create table player_standings (
  player_id int references players(player_id),
  player_name varchar(20),
  wins int,
  matches int,
  PRIMARY KEY(player_id)
);

create table matches (
  match_id serial,
  winner int references players(player_id),
  loser int references players(player_id),
  PRIMARY KEY(match_id)
);