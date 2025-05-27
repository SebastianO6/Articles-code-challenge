from lib import CONN, CURSOR

class Author:
    def __init__(self, name, id= None):
        self.id = id 
        self.name = name

    def __repr__(self):
        return f"<Author {self.id}: {self.name}>"    
    
    @classmethod
    def create_table(cls):
        sql = """"
           CREATE TABLE IF NOT EXIST authors(
              id INTEGER PRIMARY KEY 
              name TEXT NOT NULL
           )     
        """

        CURSOR.execute(sql) 
        CONN.commit()

    @classmethod
    def drop_table(cls):
        sql = """
           DROP TABLE IF EXISTS authors
           """    
        
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        sql = """
           INSERT INTO authors (name)
           VALUE (?)
        """    

        CURSOR.commit(sql, (self.id,))
        CONN.commit()

        self.id = CURSOR.lastrowid

    @classmethod
    def create(cls, name):
        author = cls(name)
        author.save()
        return author

    def update(self):
        sql ="""
           UPDATE authors 
           SET name = ?
           WHERE id = ? 
        """    

        CURSOR.execute(sql, (self.id, self.name))     
        CONN.commit()

    def delete(self):
        sql = """
           DELETE authors
           WHERE id = ?
        """

        CURSOR.execute(sql, (self.id,))
        CONN.commit()

    @classmethod
    def find_by_id(cls, id, name):
        sql = """
           SELECT * 
           FROM authors
           WHERE id = ? AND name = ?
        """

        row = CURSOR.execute(sql, (id, name)).fetchone()
        if row:
            return cls(id = row['id'], name = row['name'])
        else:
            None

def articles(self):
    conn = CONN
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM articles
        WHERE author_id = ?
    """, (self.id,))
    return cursor.fetchall()

def magazines(self):
    conn = CONN
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DISTINCT m.* FROM magazines m
        JOIN articles a ON m.id = a.magazine_id
        WHERE a.author_id = ?
    """, (self.id,))
    return cursor.fetchall()


def get_most_prolific_author():
    """Returns the author who has written the most articles."""
    conn = CONN
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                authors.*,
                COUNT(articles.id) AS article_count
            FROM authors
            JOIN articles ON authors.id = articles.author_id
            GROUP BY authors.id
            ORDER BY article_count DESC
            LIMIT 1
        """)
        
        result = cursor.fetchone()
        if result:
            return dict(result)  # Convert sqlite3.Row to dict
        return None
    finally:
        conn.close()