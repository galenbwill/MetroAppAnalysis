__author__ = 'gwilliam'

import sqlite3 as sqlite

class MetroAppConfiguration:

    #URL_QUERY = "select parentid, name, value from config where value glob 'http*' or value glob '*/*';"
    URL_QUERY = "select parentid, name, value from config where value glob '*http*' order by parentid;"

    def __init__(self, include_parentids=False, separator='\n'):
        self.urls = []
        self.separator = separator
        self.include_parentids = include_parentids

    def extract_urls(self, db):
        with sqlite.connect(db, isolation_level=None) as con:
            cur = con.cursor()
            cur.execute(self.URL_QUERY)
            rows = cur.fetchall()
            for row in rows:
                cur.execute("select name from config where id is %s;" % row[0])
                parent = cur.fetchone()
                head = parent[0]
                if len(row[1]):
                    head += ".%s" % row[1]
                self.urls.append("%s%s: %s" % (head, '(%s)' % row[0] if self.include_parentids else '', row[2]))
        return self

    def __str__(self):
        return self.separator.join(self.urls)

if ( __name__ == "__main__"):
    analysis = MetroAppConfiguration()
    analysis.extract_urls('test/weather.sqlite')
    print(analysis)