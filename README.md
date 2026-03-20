# 네이버 쇼핑 트렌드 특화 데이터랩 대시보드 (Naver API Dashboard)

본 저장소(Repository)는 네이버 개발자 센터에서 제공하는 방대한 공식 API들의 아키텍처 가이드와 **데이터랩 쇼핑인사이트 키워드 동향 API**를 직접 연동 설계하여 실전적인 탐색적 데이터 분석(EDA) 파이프라인까지 구축한 통합 프로젝트입니다.

---

## 📌 주요 구성 및 산출물 (Key Deliverables)

### 1. 📖 네이버 오픈 API 공식 문서화 (Docs)
네이버 오픈 API와 연동을 위해 상세 규격을 각 100줄 이상씩 상세하게 정리한 기술 마크다운 문서입니다.
- **`datalab.md`**: 데이터랩 기본 개념 및 아키텍처 스펙 분석 가이드
- **`datalab_shopping_insights.md`**: 쇼핑 인사이트 분야별/키워드별 연동 엔드포인트 세부 규격서
- **`search_shopping.md`**: 쇼핑 트렌드 검색 연동 가이드 문서
- **`apilist.md`**: 외부 시스템에서 연동 가능한 모든 네이버 개방형 오픈 API 종합 리스트
- **`openapi_guide.md`**: 전사 통합 관리 및 인증 관련 오픈 API 연동 종합 가이드

### 2. ⚙️ 파이썬 데이터 엔진 파이프라인 (trend_analyzer)
최근 1년 치 '선풍기' 및 '핫팩' 상품의 쇼핑 트렌드를 직접 수집하는 엔터프라이즈급 모듈 구현체 코드가 `trend_analyzer` 디렉토리에 구축되었습니다.
- **`uv` 가상환경 및 `.env` 파일**: 최신 파이썬 패키지 매니저로 구성된 독립된 가상환경과 기밀 보안 관리를 위한 Dotenv 설정
- **`main.py` & `naver_client.py`**: 카테고리 디버깅('선풍기' `50000003`, '핫팩' `50000007`)을 통한 정확한 364일치 시계열 데이터 결합 API HTTP 호출 클라이언트 
- **`data_pipeline.py` & 데이터 영구 저장**: 통신 결과를 정제하여 `data/shopping_keyword_trend_data.csv` 로 추출해 영구 보존하는 스크립트 모듈

### 3. 📊 탐색적 데이터 분석 생태계 및 시각화 (EDA Report)
데이터 분석 전문가 관점에서 1년 간 두 주요 크로스오버 아이템의 수요 상관성을 규명한 마크다운 통계 리포트를 포함합니다. 
> 분석 결과물 위치: **`trend_analyzer/eda_report.md`**, 시각화 이미지 폴더: **`trend_analyzer/images`**
- 일변량 차트 4종: 히스토그램, 빈도 분석형 상대 비중 누적 막대 그래프
- 이변량 및 시계열 4종: '선풍기'와 '핫팩'의 개별 트렌드 라인 플롯, 역상관계 산점도 및 극단적 시간-아웃라이어를 잡아내는 박스플롯
- 다변량 3종: 듀얼 시계열(Dual-Time Series) 크로스 플롯 및 피벗 막대그래프 
- 한글 폰트 글로벌 깨짐 문제 완벽 해결 (`koreanize_matplotlib` 활용) 및 단일 차트당 50자 이상의 전문적인 비즈니스 해석 동봉

---

## 🚀 실행 가이드 (Getting Started)

1. 루트 디렉토리의 `trend_analyzer` 위치에 새로운 `.env` 파일을 생성합니다.
2. 당신의 네이버 `NAVER_CLIENT_ID` 와 `NAVER_CLIENT_SECRET` 을 등록합니다.
3. 쉘에서 가상환경을 활성화(`.venv/Scripts/activate`) 한 후 프로그램을 실행합니다.
   ```bash
   cd trend_analyzer
   python main.py
   python eda_script.py
   ```
4. `trend_analyzer/data/` 에 저장되는 최신 데이터 산출물(CSV)과 `images/`에 렌더링 된 EDA 그래프를 즉시 열람하실 수 있습니다!
