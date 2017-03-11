#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    c = db.cursor()
    c.execute("DELETE FROM matches")
    c.execute("UPDATE player_standings SET wins = 0, matches = 0")
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    c = db.cursor()
    # Must delete the matches and player_standings tables first because of
    # foreign key dependencies
    c.execute("DELETE FROM matches")
    c.execute("DELETE FROM player_standings")
    c.execute("DELETE FROM players")
    db.commit()
    db.close()



def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    c = db.cursor()
    c.execute("SELECT count(*) FROM players")
    count = c.fetchall()[0][0]
    db.close()
    return count

def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    c = db.cursor()
    c.execute("INSERT INTO players (player_name) VALUES (%s) RETURNING player_id", (name,))
    # Gets the player_id for the new player we just inserted (note the RETURNING clause in SQL above)
    player_id = c.fetchone()[0]
    c.execute("INSERT INTO player_standings (player_id, player_name, wins, matches) VALUES (%s, %s, %s, %s)", (player_id, name, 0, 0))
    db.commit()
    db.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db = connect()
    c = db.cursor()
    c.execute("SELECT * FROM player_standings")
    standings = c.fetchall()
    db.close()
    return standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = connect()
    c = db.cursor()
    c.execute("INSERT INTO matches (winner, loser) VALUES (%s, %s)", (winner, loser))
    # Increment the 'matches' count in player_standings for both participants
    c.execute("UPDATE player_standings SET matches = matches + 1 WHERE player_id = %s or player_id = %s", (winner, loser))
    # Increment the 'win' count in player_standings for the winner
    c.execute("UPDATE player_standings SET wins = wins + 1 WHERE player_id = %s", (winner,))
    db.commit()
    db.close()

def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    db = connect()
    c = db.cursor()
    c.execute("SELECT * FROM player_standings ORDER BY wins DESC")
    returnlist = []
    temp_tuple = ()
    next = c.fetchone()

    # Fetch results one by one.  For each result append it to a temporary tuple
    # If the tuple is full (e.g. contains 2 userids/usernames) append it to our
    # return list and empty out the tuple
    while(next):

        temp_tuple = temp_tuple + (next[0], next[1])
        if len(temp_tuple) >= 4:
            returnlist.append(temp_tuple)
            temp_tuple = ()
        next = c.fetchone()
    db.close()
    return returnlist



