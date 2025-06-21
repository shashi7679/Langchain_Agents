import config

import sqlite3
import pandas as  pd



class DatabaseManager:
    def __init__(self, df:pd.DataFrame):
        self.df = df
        self.conn = sqlite3.connect(config.DATABASE_NAME)
        self.df.to_sql(config.TABLE_NAME, self.conn, if_exists='replace', index=False)
