#!/usr/bin/env python
import os
import flask
import MySQLdb
import json 

application = flask.Flask(__name__)
application.debug = True

@application.route('/hello')
def index():
    storage = Storage()
    storage.populate()
    return 'Hello Microsoft! ' + str(storage.pageview())


class Storage():
  def __init__(self):
    self.db = MySQLdb.connect(
      user   = os.getenv('MYSQL_USERNAME'),
      passwd = os.getenv('MYSQL_PASSWORD'),
      db     = os.getenv('MYSQL_DATABASE_NAME'),
      host   = os.getenv('MYSQL_HOST'),
      port   = int(os.getenv('MYSQL_PORT'))
    )

    cur = self.db.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS pageviews(pageview INT)")

  def populate(self):
    cur = self.db.cursor()
    cur.execute("INSERT INTO pageviews(pageview) VALUES(1234)")
    self.db.commit()

  def pageview(self):
    cur = self.db.cursor()
    cur.execute("SELECT count(*) FROM pageviews")
    row = cur.fetchone()
    return row[0]


if __name__ == "__main__":
    application.run(host='0.0.0.0', port=80)


