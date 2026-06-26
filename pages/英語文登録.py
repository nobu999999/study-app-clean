import pandas as pd
import streamlit as st
import csv
import io
from database import add_problem
from database import exists_question

st.title("CSV一括登録")

csv_text = st.text_area(
    "CSV形式で貼り付け",
    height=300,
    placeholder="app_type,question,answer,memo\nenglish,今日は忙しかった。,I was busy today.,日常会話"
)
#csv_text = st.text_area("CSVを貼り付け", height=300)

if csv_text:

    df = pd.read_csv(io.StringIO(csv_text))
    errors = []

    for i, row in df.iterrows():

        if pd.isna(row["question"]):
            errors.append(f"{i+2}行目：問題文が空です")

        if pd.isna(row["answer"]):
            errors.append(f"{i+2}行目：解答が空です")

    if errors:
        for error in errors:
            st.error(error)
    else:
        st.subheader("登録予定")
        duplicate = []
        for _, row in df.iterrows():
            duplicate.append(exists_question(row["app_type"], row["question"]))

        df["登録状態"] = [
            "🔴 登録済み" if d else "🟢 新規"
            for d in duplicate
        ]

    st.dataframe(df)
    # st.dataframe(
    #     df,
    #     use_container_width=True
    # )

if st.button("登録"):
    if not csv_text.strip():
        st.warning("CSVを入力してください")
    else:
        registered_count = 0
        for _, row in df.iterrows():        
            if exists_question(row["app_type"], row["question"]):continue
            add_problem(
                app_type=row["app_type"],
                question=row["question"],
                answer=row["answer"],
                memo=row.get("memo", "")
            )
            registered_count += 1
        st.success(f"{registered_count}件登録しました")

