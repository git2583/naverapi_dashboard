import streamlit as st
from services.naver_client import NaverAPIClient
import datetime

def render_search_tabs(node: str, keyword: str):
    st.subheader(f"'{keyword}' 현재 실시간 검색 결과 ({node.upper()})")
    
    # 상태 관리(Pagination)
    page_key = f"page_{node}_{keyword}"
    if page_key not in st.session_state:
        st.session_state[page_key] = 1
        
    client = NaverAPIClient()
    display_count = 10
    start_index = (st.session_state[page_key] - 1) * display_count + 1
    
    with st.spinner("네이버 API 서버와 통신 중..."):
        res = client.fetch_search_results(node, keyword, start=start_index, display=display_count)
        
    if not res or 'items' not in res or len(res['items']) == 0:
        st.warning(f"관련된 {node} 검색 결과가 없습니다.")
        return
        
    for item in res['items']:
        # 네이버 API가 반환하는 강조용 <b> 태그 제거 후 클리닝
        title = item.get('title', '').replace('<b>', '').replace('</b>', '')
        desc = item.get('description', '').replace('<b>', '').replace('</b>', '')
        link = item.get('link', '#')
        
        # 새 탭 여는 외부 링크 적용
        st.markdown(f"#### <a href='{link}' target='_blank' style='text-decoration: none;'>🔗 {title}</a>", unsafe_allow_html=True)
        st.write(desc)
        if 'pubDate' in item:
            st.caption(f"발행일: {item['pubDate']}")
        if 'mallName' in item:
            st.caption(f"판매처: {item['mallName']} | 가격: {item.get('lprice', 'N/A')}원")
        st.markdown("---")
        
    # 하단 페이징 컨트롤 바
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("⬅️ 이전 10건", key=f"prev_{node}_{keyword}"):
            if st.session_state[page_key] > 1:
                st.session_state[page_key] -= 1
                st.rerun()
    with col2:
        st.markdown(f"<div style='text-align: center; margin-top: 5px; font-weight: bold;'>[ {st.session_state[page_key]} 페이지 ]</div>", unsafe_allow_html=True)
    with col3:
        if st.button("다음 10건 ➡️", key=f"next_{node}_{keyword}"):
            if start_index + display_count <= 1000: # 네이버 API 최대 1000건 제한
                st.session_state[page_key] += 1
                st.rerun()
