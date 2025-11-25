import psycopg2
from app.core.config import settings
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def inspect_database():
    """
    Connects directly to the database to inspect tables and row counts.
    """
    print(f"Connecting to database: {settings.POSTGRES_DB} at {settings.POSTGRES_HOST}:{settings.POSTGRES_PORT} as {settings.POSTGRES_USER}")
    
    try:
        conn = psycopg2.connect(
            dbname=settings.POSTGRES_DB,
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
            host=settings.POSTGRES_HOST,
            port=settings.POSTGRES_PORT
        )
        cur = conn.cursor()
        
        # 1. List all tables
        print("\n--- Tables in Database ---")
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        tables = cur.fetchall()
        for table in tables:
            print(f"- {table[0]}")
            
        # 2. Check langchain_pg_collection
        print("\n--- Checking 'langchain_pg_collection' ---")
        try:
            cur.execute("SELECT * FROM langchain_pg_collection")
            collections = cur.fetchall()
            print(f"Found {len(collections)} collections:")
            for col in collections:
                # uuid, name, cmetadata
                print(f"  UUID: {col[0]}, Name: '{col[1]}', Metadata: {col[2]}")
                
                if col[1] == settings.COLLECTION_NAME:
                    print(f"  ✅ MATCH: Found collection '{settings.COLLECTION_NAME}' used by config.")
                else:
                    print(f"  ⚠️ MISMATCH: Config uses '{settings.COLLECTION_NAME}', but found '{col[1]}'.")
        except Exception as e:
            print(f"Error querying collection table: {e}")

        # 3. Check langchain_pg_embedding
        print("\n--- Checking 'langchain_pg_embedding' ---")
        try:
            cur.execute("SELECT count(*) FROM langchain_pg_embedding")
            total_count = cur.fetchone()[0]
            print(f"Total rows in embedding table: {total_count}")
            
            if total_count > 0:
                print("\nRows per Collection:")
                cur.execute("""
                    SELECT c.name, count(*)
                    FROM langchain_pg_collection c
                    LEFT JOIN langchain_pg_embedding e ON c.uuid = e.collection_id
                    GROUP BY c.name
                """)
                counts = cur.fetchall()
                for name, count in counts:
                    print(f"  Collection '{name}': {count} rows")
                    
                cur.execute("SELECT collection_id, embedding, document, cmetadata FROM langchain_pg_embedding LIMIT 1")
                row = cur.fetchone()
                print(f"\nSample Row:")
                print(f"  Collection ID: {row[0]}")
                print(f"  Document Snippet: {row[2][:50]}...")
                print(f"  Metadata: {row[3]}")
                print(f"  Embedding Raw Preview: {str(row[1])[:50]}...")
        except Exception as e:
            print(f"Error querying embedding table: {e}")

        cur.close()
        conn.close()
        print("\n--- Inspection Complete ---")

    except Exception as e:
        print(f"❌ CRITICAL: Could not connect to database. Error: {e}")

if __name__ == "__main__":
    inspect_database()
