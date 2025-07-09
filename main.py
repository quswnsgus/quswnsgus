# 학업 피드백 시스템
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="학업 피드백 시스템", layout="wide")
st.title("📘 나의 학업 피드백 시스템")

# SessionState 초기화
if "study_data" not in st.session_state:
    st.session_state.study_data = pd.DataFrame(columns=["날짜", "과목", "공부 시간", "목표", "성취도"])

# ========================================
# 1. 데이터 입력 (다중 과목 입력 폼)
# ========================================
st.sidebar.header("📥 하루 학습 데이터 입력")

with st.sidebar.form("multi_subject_form"):
    date = st.date_input("날짜", datetime.today())
    num_subjects = st.number_input("입력할 과목 수", min_value=1, max_value=10, value=1, step=1)
    
    subject_data = []
    for i in range(int(num_subjects)):
        st.markdown(f"**과목 {i+1}**")
        subject = st.text_input(f"과목 이름 {i+1}", key=f"subject_{i}")
        hours = st.number_input(f"공부 시간 (시간) - {i+1}", 0.0, 24.0, step=0.5, key=f"hours_{i}")
        if subject:
            subject_data.append({"날짜": date, "과목": subject, "공부 시간": hours})
    
    goal = st.text_area("오늘 목표", "")
    achievement = st.text_area("성취도/결과", "")
    submit = st.form_submit_button("저장")

if submit and subject_data:
    new_df = pd.DataFrame(subject_data)
    new_df["목표"] = goal
    new_df["성취도"] = achievement
    st.session_state.study_data = pd.concat(
        [st.session_state.study_data, new_df],
        ignore_index=True
    )
    st.success(f"✅ {len(subject_data)}개 과목 데이터가 저장되었습니다.")

# ========================================
# 2. 데이터프레임 구성
# ========================================
if not st.session_state.study_data.empty:
    df = st.session_state.study_data.copy()
    df["날짜"] = pd.to_datetime(df["날짜"])
else:
    df = pd.DataFrame()

# ========================================
# 3. 시각화
# ========================================
st.subheader("📊 학습 데이터 시각화")

if not df.empty:
    tab1, tab2 = st.tabs(["과목별 학습 시간", "날짜별 학습 추이"])

    with tab1:
        subject_sum = df.groupby("과목")["공부 시간"].sum().reset_index()
        fig = px.bar(subject_sum, x="과목", y="공부 시간", color="과목",
                     title="📚 과목별 누적 학습 시간")
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        date_sum = df.groupby("날짜")["공부 시간"].sum().reset_index()
        fig2 = px.line(date_sum, x="날짜", y="공부 시간", title="📆 날짜별 공부 시간 추이")
        st.plotly_chart(fig2, use_container_width=True)
else:
    st.info("학습 데이터를 먼저 입력해 주세요.")

# ========================================
# 4. 피드백 제공
# ========================================
st.subheader("🧠 자동 피드백")

if not df.empty:
    subject_total = df.groupby("과목")["공부 시간"].sum()
    min_subject = subject_total.idxmin()
    avg_hours = df.groupby("날짜")["공부 시간"].sum().mean()

    st.markdown(f"📌 공부 시간이 가장 적은 과목은 **{min_subject}** 입니다. 더 많은 시간 투자가 필요합니다.")
    st.markdown(f"📈 현재 하루 평균 공부 시간은 **{avg_hours:.2f}시간**입니다.")

    # 비교 기준
    korea_uni_avg = 9.0

    # 비교 피드백
    st.markdown("---")
    if avg_hours < 3:
        st.error("😟 이렇게 해서 대학 갈 수 있을까요? 지금처럼은 부족합니다. **절실함이 필요합니다.**")
        st.info(f"📊 참고: 고려대학교 합격생들의 평균 공부 시간은 하루 **{korea_uni_avg}시간**입니다.")
    elif avg_hours < 6:
        st.warning("⚠️ 아직 갈 길이 멉니다. 조금 더 집중해 봐요.")
        st.info(f"📊 목표까지 평균 **{korea_uni_avg - avg_hours:.1f}시간** 더 공부해야 합니다.")
    elif avg_hours < korea_uni_avg:
        st.success("💪 괜찮은 수준입니다. 하지만 상위권 목표라면 조금만 더 분발합시다.")
        st.info(f"📊 고려대 평균까지 **{korea_uni_avg - avg_hours:.1f}시간** 더 필요합니다.")
    else:
        st.balloons()
        st.success("🎉 훌륭합니다! 이미 고려대 평균을 넘는 학습량이에요.")
        st.info("🚀 이 페이스를 유지한다면 상위권 목표도 충분합니다.")

# ========================================
# 5. 데이터 다운로드
# ========================================
st.sidebar.markdown("---")
if not df.empty:
    csv = df.to_csv(index=False).encode('utf-8-sig')
    st.sidebar.download_button("📤 데이터 다운로드", csv, "학습데이터.csv", "text/csv")
