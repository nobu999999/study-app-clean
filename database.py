import sqlite3
import pandas as pd

DB_PATH = "data/study_app.db"

def load_questions():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT * FROM problems", conn)
    conn.close()
    return df.fillna("")


def update_correct(problem_id):
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """
        UPDATE problems
        SET correct = correct + 1,
            total = total + 1
        WHERE problem_id = ?
        """,
        (problem_id,)
    )
    conn.commit()
    conn.close()


def update_wrong(problem_id):
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """
        UPDATE problems
        SET total = total + 1
        WHERE problem_id = ?
        """,
        (problem_id,)
    )
    conn.commit()
    conn.close()


def save_miss_info(problem_id, error_type, memo):
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """
        UPDATE problems
        SET error_type = ?,
            memo = ?
        WHERE problem_id = ?
        """,
        (error_type, memo, problem_id)
    )
    conn.commit()
    conn.close()
