import psycopg
from psycopg.rows import dict_row
from scripts.eval1.myLib import settings

class Db:
    def __init__(self, autoCommit=True, autoPrintResults=False, getRowsAsDicts=True):
        self.getRowsAsDicts = getRowsAsDicts
        self.conn = psycopg.connect(
            dbname=settings.POSTGRES_DB,
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
            host=settings.POSTGRES_HOST,
            port=settings.POSTGRES_PORT
        )
        self.autoPrintResults = autoPrintResults
        self.autoCommit = autoCommit

        if self.getRowsAsDicts:
            self.cursor = self.conn.cursor(row_factory=dict_row)
        else:
            self.cursor = self.conn.cursor()
        
        self.result = None

    def query(self, query, params=None):
        self.cursor.execute(query, params)
        if self.autoCommit:
            self.conn.commit()
            
        if "insert" in query.lower() or "select" in query.lower():
            self.result = self.cursor.fetchall()
        else:
            self.result = self.cursor.rowcount
            
        if self.autoPrintResults:
            print(self.result)

    def disconnect(self):
        self.cursor.close()
        self.conn.close()

    def __del__(self):
        self.disconnect()