import streamlit as st

from database import (
    load_questions,
    update_correct,
    update_wrong,
    save_miss_info,
)

from quiz import (
    make_choices,
    get_problem_values,
)

st.set_page_config(
    page_title="復習管理アプリ",
    layout="centered"
)

st.title("復習管理アプリ")
st.write("左メニューからページを選んでください。")
# ===== ID作成関数 =====
def create_next_id():

    df = load_questions()
    last_id = df["problem_id"].iloc[-1]

    # Q010 → 10
    num = int(last_id.replace("Q",""))

    # 11 → Q011
    return f"Q{num+1:03}"
# ===== ID作成関数 =====

df=load_questions()
df=df.fillna("")
# st.dataframe(df)

# 初期化
if "random_row" not in st.session_state:
    st.session_state.random_row = None

if "answered" not in st.session_state:
    st.session_state.answered = False

if "is_correct" not in st.session_state:
    st.session_state.is_correct = None

# 問題表示ボタン
#if st.button("問題を表示"):
# 初回だけ問題作成
if st.session_state.random_row is None:
    st.session_state.random_row = df.sample(1)

# 問題が選ばれているときだけ表示
if st.session_state.random_row is not None:
    random_row = st.session_state.random_row
    problem = get_problem_values(random_row)
#    df.loc[df["problem_id"] == random_row["problem_id"].values[0], "next_review"] = str(date.today() + timedelta(days=3))

    st.write("問題ID:", problem["problem_id"])
    st.write("問題  :", problem["question"])
#    st.write("分野:", problem["category"])
#    st.write("ミス理由:", problem["error_type"])
#    st.write("メモ:", problem["memo"])

    # 初回だけ選択肢生成
    if "choices" not in st.session_state:
        st.session_state.choices = make_choices(random_row["choice1"].values[0],random_row["choice2"].values[0],random_row["choice3"].values[0],random_row["choice4"].values[0])
    my_answer = st.radio(
        "答えを選んでください",
        st.session_state.choices
    )

    if st.button("答え合わせ") and not st.session_state.answered:   
        st.session_state.answered = True
        st.session_state.is_correct = (my_answer == problem["answer"])

        if st.session_state.is_correct:
            update_correct(problem["problem_id"])
        else:
            update_wrong(problem["problem_id"])

    if st.session_state.answered:
    
        answer = problem["answer"]

        if st.session_state.is_correct:
            st.success("正解です！")

        else:
            st.error("不正解です。正解は：" + answer + "間違えた原因は\""+str(df.loc[df["problem_id"] == problem["problem_id"],"error_type"].values[0])+"\"です。")
            st.error("メモ：" + str(df.loc[df["problem_id"] == problem["problem_id"],"memo"].values[0]))

            error = st.selectbox(
                "間違えた理由",
                [
                    "公式忘れ",
                    "問題文読み違い",
                    "分布選択ミス",
                    "計算ミス",
                    "理解不足"
                ],
                key="error_reason"
            )

            memo = st.text_input(
                "次回気をつけること",
                key="memo_input"
            )

            if st.button("ミス内容を保存"):
                save_miss_info(
                    problem["problem_id"],
                    error,
                    memo
                )
                st.success("ミス内容を保存しました")


    if st.button("次の問題"):
        # st.write(df)
        # time.sleep(10)
        #st.session_state.random_row = df.sample(1)
        #情報を更新
        df["accuracy"] = df.apply(
            lambda row: row["correct"] / row["total"] if row["total"] > 0 else 0,
            axis=1
        )

#        save_df(df)

        #正答率が低い問題ほど出題しやすい
        df["weight"] = (1 - df["accuracy"])+0.2
        df.loc[df["total"] == 0, "weight"] = 2

        st.session_state.random_row = df.sample(1,weights=df["weight"])
        st.session_state.answered = False
        st.session_state.is_correct = None

        if "choices" in st.session_state:
            del st.session_state.choices

        if "error_reason" in st.session_state:
            del st.session_state.error_reason

        if "memo_input" in st.session_state:
            del st.session_state.memo_input

        st.rerun()

