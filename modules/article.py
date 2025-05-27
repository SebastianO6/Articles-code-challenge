from lib import CURSOR, CONN

class Article:

    all = {}
    
    def __init__(self, title, magazine, author, id = None,):
        self.id = id
        self.title = title
        self.author = author
        self.magazine = magazine

    def __repr__(self):
        return f"<Article {self.id}: {self.title}, {self.magazine}, {self.author}"

    @classmethod
    def create_table(cls):
        sql = """
          CREATE TABLE IF NOT EXISTS magazines (
          id INTEGER PRIMARY KEY,
          title TEXT NOT NULL,
          magazine TEXT NOT NULL,
          author TEXT NOT NULL
          )
        """    

        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        sql = """
           DROP TABLE IF EXISTS articles 
        """    

        CURSOR.execute(sql)
        CONN.commit

    def save(self):
        sql = """
           INSERT INTO authors (name, title, magazine, author)
           VALUE (? , ?, ?, ?)
        """

        CURSOR.execute(sql, (self.id, self.title, self.magazine, self.author))
        CONN.commit()

        self.id = CURSOR.lastrowid

    @classmethod
    def create(cls, title, magazine, author):
        article = cls(title, magazine, author)
        article.save()
        return article
    
    def update(self):
        sql = """
           UPDATE articles
           SET title = ?, magazine = ?, author = ?
           WHERE id = ?
        """

        CURSOR.execute(sql, (self.title, self.magazine, self.author))
        CONN.commit()

    def delete(self):
        sql = """
           DELETE articles
           WHERE id = ?
        """    

        CURSOR.execute(sql, (self.id,))
        CONN.commit()

    def find_by_all(cls, id, title, magazine, author):
        sql = """
           SELECT *
           FROM articles
           WHERE id = ? AND title = ? AND magazine = ? AND author = ?
        """    
        row = CURSOR.execute(sql, (id, title, magazine, author)).fetchone()
        if row:
            cls(id = row['id'], title = row['title'], magazine = row['magazine'], author = row['author'])
        else:
            None   

