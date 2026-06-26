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


def add_problem(
    app_type,
    question,
    answer,
    memo="",
    error_type=""
):
    

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO problems (
            app_type,
            question,
            answer,
            memo,
            error_type,
            correct,
            total
        )
        VALUES (?, ?, ?, ?, ?, 0, 0)
    """, (
        app_type,
        question,
        answer,
        memo,
        error_type
    ))

    conn.commit()
    conn.close()



def exists_question(app_type, question):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute(
        "SELECT COUNT(*) FROM problems WHERE  app_type = ? AND question = ?",
        (app_type, question)
    )

    exists = cur.fetchone()[0] > 0

    conn.close()

    return exists

def get_random_problem(app_type):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        SELECT problem_id, question, answer, memo
        FROM problems
        WHERE app_type = ?
        ORDER BY RANDOM()
        LIMIT 1
    """, (app_type,))

    row = cur.fetchone()
    conn.close()

    return row


def delete_english_problems():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        DELETE FROM problems
        WHERE app_type = ?
    """, ("english",))

    conn.commit()
    conn.close()

