import streamlit as st
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
from services.naver_client import NaverAPIClient
from services.data_pipeline import DataPipeline
from components.charts import render_eda_charts
from components.search_tabs import render_search_tabs
import os

st.set_page_config(page_title="네이버 트렌드 대시보드", page_icon="📈", layout="wide")

st.sidebar.title("트렌드 분석 설정")

default_start = datetime.now() - relativedelta(years=1)
start_date_input = st.sidebar.date_input("분석 시작일", value=default_start)
end_date_input = st.sidebar.date_input("분석 종료일", value=datetime.now())

keyword1 = st.sidebar.text_input("키워드 1", value="선풍기")
cat1 = st.sidebar.selectbox("키워드 1 카테고리", options=["50000003", "50000007", "50000008", "50000000"], format_func=lambda x: {"50000003": "디지털/가전", "50000007": "스포츠/레저", "50000008": "생활/건강", "50000000": "패션의류"}.get(x, x))
keyword2 = st.sidebar.text_input("키워드 2", value="핫팩")
cat2 = st.sidebar.selectbox("키워드 2 카테고리", options=["50000007", "50000003", "50000008", "50000000"], format_func=lambda x: {"50000003": "디지털/가전", "50000007": "스포츠/레저", "50000008": "생활/건강", "50000000": "패션의류"}.get(x, x), index=0)

run_button = st.sidebar.button("분석 시작")

@st.cache_data(ttl=3600)
def load_trend_data(kw1, c1, kw2, c2, sd_str, ed_str):
    client = NaverAPIClient()
    
    payload1 = {
        "startDate": sd_str, "endDate": ed_str, "timeUnit": "date",
        "category": c1, "keyword": [{"name": kw1, "param": [kw1]}],
        "device": "", "gender": "", "ages": []
    }
    payload2 = {
        "startDate": sd_str, "endDate": ed_str, "timeUnit": "date",
        "category": c2, "keyword": [{"name": kw2, "param": [kw2]}],
        "device": "", "gender": "", "ages": []
    }
    
    res1 = client.fetch_shopping_keywords_trend(payload1)
    res2 = client.fetch_shopping_keywords_trend(payload2)
    
    dates1, trend1 = DataPipeline.parse_trend_data(res1) if res1 and 'results' in res1 else ([], {})
    dates2, trend2 = DataPipeline.parse_trend_data(res2) if res2 and 'results' in res2 else ([], {})
    
    all_dates = sorted(list(set(dates1) | set(dates2)))
    data_list = []
    import pandas as pd
    for d in all_dates:
        r1 = trend1.get(d, {}).get(kw1, 0.0) if d in trend1 else 0.0
        r2 = trend2.get(d, {}).get(kw2, 0.0) if d in trend2 else 0.0
        data_list.append({
            "조회 일자": d,
            f"{kw1} (상대 비율)": r1,
            f"{kw2} (상대 비율)": r2
        })
        
    df = pd.DataFrame(data_list)
    if not df.empty:
        df['조회 일자'] = pd.to_datetime(df['조회 일자'])
        df['월'] = df['조회 일자'].dt.month
        df['요일'] = df['조회 일자'].dt.day_name()
    return df

st.title("🛍️ 쇼핑 트렌드 탐색적 데이터 분석 대시보드")

if run_button or ('trend_df' in st.session_state):
    if run_button:
        with st.spinner("네이버 데이터랩 API 결과 로딩 중..."):
            sd_str = start_date_input.strftime("%Y-%m-%d")
            ed_str = end_date_input.strftime("%Y-%m-%d")
            df = load_trend_data(keyword1, cat1, keyword2, cat2, sd_str, ed_str)
            st.session_state['trend_df'] = df
            st.session_state['kw1'] = keyword1
            st.session_state['kw2'] = keyword2
    else:
        df = st.session_state['trend_df']
        keyword1 = st.session_state['kw1']
        keyword2 = st.session_state['kw2']

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 기초 EDA", "🛒 쇼핑 검색", "📝 블로그 리뷰", "☕ 카페 여론", "📰 최신 뉴스"])
    
    with tab1:
        render_eda_charts(df, keyword1, keyword2)
        
    with tab2:
        render_search_tabs("shop", keyword1)
        
    with tab3:
        render_search_tabs("blog", keyword1)
        
    with tab4:
        render_search_tabs("cafearticle", keyword1)
        
    with tab5:
        render_search_tabs("news", keyword1)
else:
    st.info("좌측 사이드바에서 분석할 키워드를 설정하고 [분석 시작] 버튼을 눌러주세요.")
