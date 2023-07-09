from databases import Database
from config import DATABASE_URL
from sqlalchemy import create_engine
import pandas as pd
engine = create_engine(DATABASE_URL)



database = Database(DATABASE_URL)


def get_csv_data():
    # Отримання даних з бази даних у DataFrame
    df = pd.read_sql_query('SELECT * FROM article', engine)

    # Збереження DataFrame у форматі CSV
    csv_data = df.to_csv(index=False)

    return csv_data