from datetime import datetime

def get_valid_polls(cursor, offset):
	try: 
		offset = int(offset)
	except:
		offset = 0
	cursor.execute("SELECT id, question, adminonly, dontshow FROM poll_question LIMIT 50 OFFSET " + str(offset))
	result = cursor.fetchall()
	dat = "<ul class='left'>"
	for pollid, question, adminonly, dontshow in result:
		if adminonly == 1 or dontshow == 1:
			continue
		dat += f"<li>Poll {pollid} {question} | <a href='/poll/{pollid}'>View</a></li>"
	dat += "</ul>"

	return dat


def handle_polltype(cursor, pollid):
	pollid = str(pollid)
	cursor.execute('SELECT * FROM poll_question WHERE id = ' + pollid)
	result = cursor.fetchall()
	x = result[0]

	if x[5] == 1 or x[9] == 1:
		return "<p>Access Denied</p>"

	dat = f"""
<p>Question: {x[4]}</p>
<p>Type: {x[1]}</p>
<p>Start time: {x[2].strftime('%d %B %Y - %H:%M:%S')}</p>
<p>End time: {x[3].strftime('%d %B %Y - %H:%M:%S')}</p>
	"""

	if x[1] == "OPTION":
		dat += poll_option(cursor, pollid)
	elif x[1] == "TEXT":
		dat += poll_text(cursor, pollid)
	elif x[1] == "NUMVAL":
		dat += poll_numval(cursor, pollid)
	elif x[1] == "MULTICHOICE":
		dat += poll_multichoice(cursor, pollid)
	elif x[1] == "IRV":
		dat += poll_irv(cursor, pollid)

	return dat


def poll_option(cursor, pollid):
	dat = "<p><b>Options:</b></p>"
	cursor.execute('SELECT text FROM poll_option WHERE pollid = ' + pollid)
	result = cursor.fetchall()
	cursor.execute('SELECT COUNT(*) FROM poll_vote WHERE pollid = ' + pollid + ' AND optionid = 1')
	first = cursor.fetchall()
	cursor.execute('SELECT COUNT(*) FROM poll_vote WHERE pollid = ' + pollid + ' AND optionid = 2')
	second = cursor.fetchall()
	dat += f"<p>1. {result[0][0]}: {first[0][0]}</p>"
	dat += f"<p>2. {result[1][0]}: {second[0][0]}</p>"

	return dat


def poll_text(cursor, pollid):
	cursor.execute('SELECT replytext FROM poll_textreply WHERE pollid = ' + pollid)
	result = cursor.fetchall()
	dat = "<p><b>Replies:</b></p>"
	for z in range(len(result)):
		dat += f"<p><b>{z}:</b> {result[z][0]}</p>"

	return dat


def poll_numval(cursor, pollid):
	cursor.execute('SELECT * FROM poll_option WHERE pollid = ' + pollid)
	result = cursor.fetchall()
	dat = f"""
<p><b>Options:</b></p>
<p>Poll description: {result[0][2]}</p>
<p>Minimum rating description: {result[0][5]}</p>
<p>Middle rating description: {result[0][6]}</p>
<p>Maximum rating description: {result[0][7]}</p>
<p>Minimum rating: {result[0][3]}</p>
<p>Maximum rating: {result[0][4]}</p>
<p><b>Votes:</b></p>
"""
	for x in range(result[0][4] + 1):
		cursor.execute('SELECT COUNT(*) FROM poll_vote WHERE pollid = ' + pollid + ' AND rating = ' + str(x))
		result = cursor.fetchall()
		dat += f"<p>Rating {x}: {result[0][0]}</p>"

	return dat


def poll_multichoice(cursor, pollid):
	dat = "<p><b>Options:</b></p>"
	cursor.execute('SELECT COUNT(v.id) as VOTES, p.text FROM poll_vote v LEFT JOIN poll_option p ON v.optionid = p.id WHERE v.pollid = ' + pollid + ' GROUP BY v.optionid')
	result = cursor.fetchall()
	for x in result:
		dat += f"<p>{x[1]} : {x[0]}</p>"
	return dat


def poll_irv(cursor, pollid):
	return "<p>This type of poll is currently not implemented.</p>"