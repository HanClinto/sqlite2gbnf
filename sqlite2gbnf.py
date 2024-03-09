import sqlite3

def extract_schema(db_path):
    """Extracts tables and columns from the SQLite database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Extract table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    # Extract columns for each table
    schema = {}
    for table in tables:
        table_name = table[0]
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        schema[table_name] = [col[1] for col in columns]  # Assuming col[1] is the column name
    
    conn.close()
    return schema

db_path = 'AllPrintings.sqlite'  # Update this path
schema = extract_schema(db_path)
print(schema)

def generate_gbnf(schema):
    """Generate GBNF syntax based on the schema."""
    gbnf = "root ::= SELECT columns FROM tables\n\n"
    gbnf += "columns ::= '*' | column (',' column)*\n"
    gbnf += "column ::= " + " | ".join([f"'{col}'" for table in schema for col in schema[table]]) + "\n"
    gbnf += "tables ::= " + " | ".join([f"'{table}'" for table in schema]) + "\n"
    
    return gbnf

gbnf = generate_gbnf(schema)
print(gbnf)

def save_gbnf(gbnf, file_path):
    """Saves the GBNF syntax to a file."""
    with open(file_path, 'w') as file:
        file.write(gbnf)

save_gbnf(gbnf, 'database_schema.gbnf')

