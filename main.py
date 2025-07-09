# 학업 피드백 시스템
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="학업 피드백 시스템", layout="wide")

st.title("📘 나의 학업 피드백 시스템")

# SessionState 사용
if "study_data" not in st.session_state:
    st.session_state.study_data = pd.DataFrame(columns=["날짜", "과목", "공부 시간", "목표", "성취도"])

# 1. 데이터 입력
st.sidebar.header("📥 학습 데이터 입력")

with st.sidebar.form("data_form"):
    date = st.date_input("날짜", datetime.today())
    subject = st.text_input("과목", "")
    hours = st.number_input("공부 시간 (시간)", 0.0, 24.0, step=0.5)
    goal = st.text_area("오늘 목표", "")
    achievement = st.text_area("성취도/결과", "")
    submit = st.form_submit_button("저장")

if submit:
    new_row = {
        "날짜": date,
        "과목": subject,
        "공부 시간": hours,
        "목표": goal,
        "성취도": achievement
    }
    st.session_state.study_data = pd.concat(
        [st.session_state.study_data, pd.DataFrame([new_row])],
        ignore_index=True
    )
    st.success("✅ 데이터가 저장되었습니다.")

# 2. 데이터 시각화
st.subheader("📊 학습 데이터 시각화")

if st.session_state.study_data.empty:
    st.info("학습 데이터를 먼저 입력해 주세요.")
else:
    df = st.session_state.study_data.copy()
    df['날짜'] = pd.to_datetime(df['날짜'])

    tab1, tab2 = st.tabs(["과목별 학습 시간", "날짜별 학습 추이"])

    with tab1:
        subject_sum = df.groupby("과목")["공부 시간"].sum().reset_index()
        fig = px.bar(subject_sum, x="과목", y="공부 시간", color="공부 시간",
                     title="📚 과목별 누적 학습 시간")
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        date_sum = df.groupby("날짜")["공부 시간"].sum().reset_index()
        fig2 = px.line(date_sum, x="날짜", y="공부 시간", title="📆 날짜별 공부 시간 추이")
        st.plotly_chart(fig2, use_container_width=True)

# 3. 피드백 제공
st.subheader("🧠 자동 피드백")

if not df.empty:
    min_subject = df.groupby("과목")["공부 시간"].sum().idxmin()
    avg_hours = df.groupby("날짜")["공부 시간"].sum().mean()

    st.write(f"📌 이번 기간 동안 공부 시간이 가장 적은 과목은 **{min_subject}** 입니다. 집중이 필요해요!")
    st.write(f"📈 하루 평균 공부 시간은 **{avg_hours:.2f}시간** 입니다.")

    if avg_hours < 2:
        st.warning("하루 평균 공부 시간이 낮습니다. 목표를 세워 계획적으로 학습해보세요.")
    else:
        st.success("좋은 학습 페이스를 유지하고 있습니다!")

# 4. 데이터 다운로드
st.sidebar.markdown("---")
if not df.empty:
    csv = df.to_csv(index=False).encode('utf-8-sig')
    st.sidebar.download_button("📤 데이터 다운로드", csv, "학습데이터.csv", "text/csv")
