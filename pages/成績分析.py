import streamlit as st
import pandas as pd

from database import load_questions

st.title("成績分析")

df = load_questions()

df["accuracy"] = df.apply(
    lambda row: row["correct"] / row["total"] if row["total"] > 0 else 0,
    axis=1
)

st.subheader("分野別正答率")

chart_data = df.groupby("category")["accuracy"].mean()

st.bar_chart(chart_data)

st.subheader("ミス理由ランキング")

error_counts = df[df["error_type"] != ""]["error_type"].value_counts()

st.bar_chart(error_counts)

st.subheader("苦手問題一覧")

miss_df = df[df["accuracy"] < 0.5]

st.dataframe(
    miss_df[
        [
            "problem_id",
            "category",
            "question",
            "accuracy",
            "error_type",
            "memo"
        ]
    ]
)



