from lib import CURSOR, CONN

class Magazine:

    all = {}
    
    def __init__(self, name, category, id = None):
        self.id = id
        self.name = name
        self.category = category

    def __repr__(self):
        return f"<Magazine {self.id}: {self.name}, {self.category}"

    @classmethod
    def create_table(cls):
        sql = """
          CREATE TABLE IF NOT EXISTS magazines (
          id INTEGER PRIMARY KEY,
          name TEXT NOT NULL,
          category TEXT NOT NULL
          )
        """    

        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        sql = """
           DROP TABLE IF EXISTS magazines 
        """    

        CURSOR.execute(sql)
        CONN.commit

    def save(self):
        sql = """
           INSERT INTO authors (name, category)
           VALUE (? , ?)
        """

        CURSOR.execute(sql, (self.id, self.name, self.category))
        CONN.commit()

        self.id = CURSOR.lastrowid

    @classmethod
    def create(cls, name, category):
        magazine = cls(name, category)
        magazine.save()
        return magazine
    
    def update(self):
        sql = """
           UPDATE magazines
           SET name = ?, category = ?
           WHERE id = ?
        """

        CURSOR.execute(sql, (self.name, self.category))
        CONN.commit()

    def delete(self):
        sql = """
           DELETE magazines
           WHERE id = ?
        """    

        CURSOR.execute(sql, (self.id,))
        CONN.commit()

    def find_by_all(cls, id, name, category):
        sql = """
           SELECT *
           FROM magazines
           WHERE id = ? AND name = ? AND category = ?
        """    
        row = CURSOR.execute(sql, (id, category, name)).fetchone()
        if row:
            cls(id = row['id'], name = row['name'], category = row['category'])
        else:
            None   

def get_authors_for_magazine(magazine_id):
    conn = CONN  
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT DISTINCT authors.*
            FROM authors
            JOIN articles ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
        """, (magazine_id,))
        
        return cursor.fetchall()
    finally:
        cursor.close()  

def get_authors_for_magazine(magazine_id):
    conn = CONN
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT DISTINCT authors.*
        FROM authors
        JOIN articles ON authors.id = articles.author_id
        WHERE articles.magazine_id = ?
    """, (magazine_id,))
    
    authors = cursor.fetchall()
    conn.close()
    return authors



def count_articles_per_magazine():
    conn = CONN
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                magazines.id,
                magazines.name,
                COUNT(articles.id) AS article_count
            FROM magazines
            LEFT JOIN articles ON magazines.id = articles.magazine_id
            GROUP BY magazines.id
            ORDER BY article_count DESC
        """)
        return [dict(row) for row in cursor.fetchall()]
    finally:
        conn.close()
        