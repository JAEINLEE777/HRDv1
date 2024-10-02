import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta

# 가상 직원 데이터
EMPLOYEES = [
    {"name": "김철수", "department": "영업", "position": "과장"},
    {"name": "이영희", "department": "마케팅", "position": "대리"},
    {"name": "박민준", "department": "인사", "position": "차장"},
    {"name": "정수진", "department": "개발", "position": "선임"},
    {"name": "최재훈", "department": "재무", "position": "부장"},
    {"name": "강지영", "department": "영업", "position": "사원"},
    {"name": "윤서연", "department": "마케팅", "position": "과장"},
    {"name": "임동훈", "department": "개발", "position": "책임"},
    {"name": "한미래", "department": "인사", "position": "대리"},
    {"name": "송태양", "department": "재무", "position": "사원"}
]

# 샘플 데이터 생성 함수
def generate_sample_data(start_date=datetime(2024, 1, 1), end_date=datetime(2024, 12, 31)):
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    competencies = ['직무', 'Global', 'SKValues']
    
    data = []
    for employee in EMPLOYEES:
        for date in date_range:
            if np.random.random() > 0.3:  # 70% 확률로 학습 기록 생성
                for competency in competencies:
                    if np.random.random() > 0.5:  # 50% 확률로 각 역량 영역 학습
                        hours = np.random.randint(1, 5)
                        data.append({
                            '날짜': date,
                            '직원': employee['name'],
                            '부서': employee['department'],
                            '직급': employee['position'],
                            '직무역량': competency,
                            '학습시간': hours
                        })
    
    return pd.DataFrame(data)

# 메인 앱
def main():
    st.title('직무역량별 월별 학습시간 이수현황 대시보드')

    # 샘플 데이터 생성
    df = generate_sample_data()

    # 데이터 전처리
    df['월'] = df['날짜'].dt.to_period('M')
    monthly_data = df.groupby(['월', '직원', '부서', '직급', '직무역량'])['학습시간'].sum().reset_index()
    monthly_data['월'] = monthly_data['월'].astype(str)

    # 사이드바 - 월 선택
    months = sorted(monthly_data['월'].unique())
    selected_month = st.sidebar.selectbox('월 선택', months)

    # 사이드바 - 부서 선택
    departments = ['전체'] + sorted(monthly_data['부서'].unique())
    selected_department = st.sidebar.selectbox('부서 선택', departments)

    # 선택된 월과 부서의 데이터 필터링
    filtered_data = monthly_data[monthly_data['월'] == selected_month]
    if selected_department != '전체':
        filtered_data = filtered_data[filtered_data['부서'] == selected_department]

    # 차트 1: 직원별 총 학습시간 (직무역량별로 구분)
    fig1 = px.bar(filtered_data, x='직원', y='학습시간', color='직무역량', 
                  title=f'{selected_month} 직원별 총 학습시간 (직무역량별)',
                  labels={'학습시간': '총 학습시간'}, barmode='stack',
                  hover_data=['부서', '직급'])
    st.plotly_chart(fig1)

    # 차트 2: 월별 평균 학습시간 추이 (직무역량별)
    monthly_avg = monthly_data.groupby(['월', '직무역량'])['학습시간'].mean().reset_index()
    fig2 = px.line(monthly_avg, x='월', y='학습시간', color='직무역량', 
                   title='직무역량별 월별 평균 학습시간 추이',
                   labels={'학습시간': '평균 학습시간'})
    st.plotly_chart(fig2)

    # 통계 정보
    st.subheader(f'{selected_month} 통계')
    col1, col2, col3 = st.columns(3)
    col1.metric("전체 평균 학습시간", f"{filtered_data['학습시간'].mean():.2f}시간")
    col2.metric("최대 학습시간", f"{filtered_data['학습시간'].max()}시간")
    col3.metric("최소 학습시간", f"{filtered_data['학습시간'].min()}시간")

    # 직무역량별 평균 학습시간
    st.subheader(f'{selected_month} 직무역량별 평균 학습시간')
    competency_avg = filtered_data.groupby('직무역량')['학습시간'].mean().reset_index()
    fig3 = px.bar(competency_avg, x='직무역량', y='학습시간', 
                  title=f'{selected_month} 직무역량별 평균 학습시간',
                  labels={'학습시간': '평균 학습시간'})
    st.plotly_chart(fig3)

    # 부서별 평균 학습시간
    st.subheader(f'{selected_month} 부서별 평균 학습시간')
    department_avg = filtered_data.groupby('부서')['학습시간'].mean().reset_index()
    fig4 = px.bar(department_avg, x='부서', y='학습시간', 
                  title=f'{selected_month} 부서별 평균 학습시간',
                  labels={'학습시간': '평균 학습시간'})
    st.plotly_chart(fig4)

    # 데이터 테이블
    st.subheader(f'{selected_month} 상세 데이터')
    st.dataframe(filtered_data)

if __name__ == '__main__':
    main()
