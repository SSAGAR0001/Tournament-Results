#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
	try:
		data_name = 'tournament'
		db = psycopg2.connect("dbname={}".format(data_name))
		cur = db.cursor()
		return db, cur
	except:
	    print("Unable To Connect!!")

def deleteMatches():
	db, cur = connect()
	q = "TRUNCATE " + 'games'
	cur.execute(q)
	db.commit()
	db.close()

def deletePlayers():
	db, cur = connect()
	q = "TRUNCATE " + 'players'
	cur.execute(q)
	db.commit()
	cur.close()
	db.close()

def countPlayers():
    """Returns the number of players currently registered."""
    db, cur = connect()
    q = "select count(*) from players"
    cur.execute(q)
    value = cur.fetchall()
    cur.close()
    db.close()
    return int(value[0][0])

def registerPlayer(name):
	if name:
	    q = "isert into players(name) values(%s)"
	    db,cur = connect()
	    cur.execute(q, (name, ))
	    db.commit()
	    cur.close()
	else:
		return false
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
    q = "select p_id, name, wins, played from rank"
    db, cur = connect()
    cur.execute(q)
    value = cur.fetchall()
    db.close()
    cur.close()
    return value

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db, cur = connect()
    q = "insert into game(winner, loser) values(%s, %s)"
    cur.execute(q, (winner, loser))
    db.commit()
    db.close()
    cur.close()
 
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
    pairing = []
    total_players = countPlayers()
    for i in range(0, total_players, 2):
	    q = """select p_id, name from rank order by wins 
	    limit 2 offset""" + str(i)
	    result = running(q)
	    result = result[0] + result[1]
	    pairing.append(result)

	    return pairing

def running(query):
    db, cur = connect()
    cur.execute(query)
    value = cur.fetchall()
    cur.close()
    db.close()
    return value