import random


def make_choices(choice1, choice2, choice3, choice4):
    choices = [choice1, choice2, choice3, choice4]
    random.shuffle(choices)
    return choices


def get_problem_values(random_row):
    return {
        "problem_id": random_row["problem_id"].values[0],
        "question": random_row["question"].values[0],
        "answer": random_row["answer"].values[0],
        "category": random_row["category"].values[0],
        "choice1": random_row["choice1"].values[0],
        "choice2": random_row["choice2"].values[0],
        "choice3": random_row["choice3"].values[0],
        "choice4": random_row["choice4"].values[0],
    }

