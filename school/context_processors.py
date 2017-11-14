from django.db import connection,transaction


def flash_message(request):
    query = 'SELECT * FROM MARQUEE'
    cur = connection.cursor()
    cur.execute(query)
    marquee = cur.fetchall()
    cur.close()
    return {'messages':marquee}