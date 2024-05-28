class Queries:
    CREATE_SURVEY_TABLE = """
        CREATE TABLE IF NOT EXISTS surveys (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name = TEXT,
            age = INTEGER,
            occupation = TEXT,
            salary = TEXT,
            grade = TEXT,
            rating INTEGER
        );
    """
