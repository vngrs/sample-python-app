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
    return 'hello ' + str(storage.pageview())


class Storage():
  def __init__(self):
    self.db_config = self._get_config()
    self.db = MySQLdb.connect(
      user   = os.getenv('MYSQL_USERNAME') || self.db_config['user'],
      passwd = os.getenv('MYSQL_PASSWORD') || self.db_config['passwd'],
      db     = os.getenv('MYSQL_INSTANCE_NAME') || self.db_config['db'],
      host   = os.getenv('MYSQL_SERVICE_HOST') || self.db_config['host'],
      port   = int(os.getenv('MYSQL_SERVICE_PORT')) || self.db_config['port']
    )

    cur = self.db.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS pageviews(pageview INT)")

  def _get_config():
    with open('./config.json', 'r') as config_file:
      return json.loads(config_file.read())

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
    application.run(host='0.0.0.0', port=3000)


