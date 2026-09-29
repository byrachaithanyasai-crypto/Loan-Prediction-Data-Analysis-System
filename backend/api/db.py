import os
import psycopg2
import psycopg2.extras

DATABASE_URL = os.environ.get("DATABASE_URL")

def get_db_connection():
    if not DATABASE_URL:
        return None
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(DATABASE_URL, sslmode='prefer')
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

def init_db():
    conn = get_db_connection()
    if not conn:
        print("No DATABASE_URL provided. Skipping DB initialization.")
        return
    try:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS predictions (
                    id SERIAL PRIMARY KEY,
                    age INTEGER,
                    income DOUBLE PRECISION,
                    credit_score INTEGER,
                    loan_amount DOUBLE PRECISION,
                    loan_term_months INTEGER,
                    employment_status VARCHAR(50),
                    risk_status VARCHAR(50),
                    model VARCHAR(50)
                )
            """)
        conn.commit()
    except Exception as e:
        print(f"Error initializing database table: {e}")
    finally:
        conn.close()

def save_prediction(prediction_data):
    conn = get_db_connection()
    if not conn:
        return
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO predictions (age, income, credit_score, loan_amount, loan_term_months, employment_status, risk_status, model)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                prediction_data.get('Age'),
                prediction_data.get('Income'),
                prediction_data.get('Credit_Score'),
                prediction_data.get('Loan_Amount'),
                prediction_data.get('Loan_Term_Months'),
                prediction_data.get('Employment_Status'),
                prediction_data.get('Risk_Status'),
                prediction_data.get('Model')
            ))
        conn.commit()
    except Exception as e:
        print(f"Error saving prediction to DB: {e}")
    finally:
        conn.close()

def load_predictions():
    conn = get_db_connection()
    if not conn:
        return []
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute("SELECT * FROM predictions ORDER BY id ASC")
            rows = cur.fetchall()
            return [{
                'Age': row['age'],
                'Income': row['income'],
                'Credit_Score': row['credit_score'],
                'Loan_Amount': row['loan_amount'],
                'Loan_Term_Months': row['loan_term_months'],
                'Employment_Status': row['employment_status'],
                'Risk_Status': row['risk_status'],
                'Model': row['model']
            } for row in rows]
    except Exception as e:
        print(f"Error loading predictions from DB: {e}")
        return []
    finally:
        conn.close()
