import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def render_eda_charts(df: pd.DataFrame, kw1: str, kw2: str):
    st.subheader("1. 일별 트렌드 추이 시계열 차트")
    # 차트 1: 시계열 듀얼 라인
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=df['조회 일자'], y=df[f'{kw1} (상대 비율)'], mode='lines', name=kw1))
    fig1.add_trace(go.Scatter(x=df['조회 일자'], y=df[f'{kw2} (상대 비율)'], mode='lines', name=kw2))
    fig1.update_layout(title="일별 검색 트렌드 연속 비교", xaxis_title="조회 일자", yaxis_title="상대 비율(%)")
    st.plotly_chart(fig1, use_container_width=True)
    with st.expander("데이터 표 보기"):
        st.dataframe(df[['조회 일자', f'{kw1} (상대 비율)', f'{kw2} (상대 비율)']])

    # 차트 2: 월별 비중 막대그래프
    st.subheader("2. 월간 누적 파이 점유율 (막대형)")
    monthly_df = df.groupby('월')[[f'{kw1} (상대 비율)', f'{kw2} (상대 비율)']].mean().reset_index()
    fig2 = px.bar(monthly_df, x='월', y=[f'{kw1} (상대 비율)', f'{kw2} (상대 비율)'], title="월별 평균 검색 비율", barmode='group')
    st.plotly_chart(fig2, use_container_width=True)
    with st.expander("데이터 표 보기"):
        st.dataframe(monthly_df)

    # 차트 3: 요일별 박스플롯
    st.subheader("3. 주간 요일별 트래픽 강도 분석 (Box Plot)")
    fig3 = go.Figure()
    fig3.add_trace(go.Box(y=df[f'{kw1} (상대 비율)'], x=df['요일'], name=kw1))
    fig3.add_trace(go.Box(y=df[f'{kw2} (상대 비율)'], x=df['요일'], name=kw2))
    fig3.update_layout(title="주간 선호 요일 변동성 테스트", xaxis_title="요일", boxmode='group')
    st.plotly_chart(fig3, use_container_width=True)
    with st.expander("데이터 표 보기"):
        st.dataframe(df.groupby('요일')[[f'{kw1} (상대 비율)', f'{kw2} (상대 비율)']].describe())

    # 차트 4: 상관관계 산점도
    st.subheader("4. 수요 대체성 분석 (상관 산점도)")
    fig4 = px.scatter(df, x=f'{kw1} (상대 비율)', y=f'{kw2} (상대 비율)', trendline="ols", title=f"{kw1} vs {kw2} 카니발라이제이션 산점도")
    st.plotly_chart(fig4, use_container_width=True)
    with st.expander("데이터 표 보기"):
        corr = df[[f'{kw1} (상대 비율)', f'{kw2} (상대 비율)']].corr()
        st.dataframe(corr)

    # 차트 5: 최근 30일 모멘텀 도넛 차트
    st.subheader("5. 최근 한 달(30일) 시장 주도권 (모멘텀)")
    recent_df = df.tail(30)
    sum1 = recent_df[f'{kw1} (상대 비율)'].sum()
    sum2 = recent_df[f'{kw2} (상대 비율)'].sum()
    pie_data = pd.DataFrame({'키워드': [kw1, kw2], '점유율': [sum1, sum2]})
    fig5 = px.pie(pie_data, values='점유율', names='키워드', hole=0.4, title="최단기(최근 30일) 종합 마켓 쉐어")
    st.plotly_chart(fig5, use_container_width=True)
    with st.expander("데이터 표 보기"):
        st.dataframe(pie_data)
