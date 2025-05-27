from lib.db.connection import get_connection

def add_author_with_articles(author_name, articles_data):
    """
    Add an author and their articles in a single transaction.
    articles_data: list of dicts with keys 'title' and 'magazine_id'
    Example:
        add_author_with_articles("Philip Katsivo", [
            {'title': "Life in Moringa", 'magazine_id': 1},
            {'title': "Future of Robotics", 'magazine_id': 2}
        ])
    """
    conn = get_connection()
    try:       
        conn.execute("BEGIN TRANSACTION")
        cursor = conn.cursor()

        cursor.execute("INSERT INTO authors (name) VALUES (?)", (author_name,))
        author_id = cursor.lastrowid

        for article in articles_data:
            cursor.execute("""
                INSERT INTO articles (title, author_id, magazine_id)
                VALUES (?, ?, ?)
            """, (article['title'], author_id, article['magazine_id']))

        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(f"Transaction failed: {e}")
        return False
    
    finally:
        conn.close()
