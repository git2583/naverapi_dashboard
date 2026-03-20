# 작업지시서: 최근 1년간 일자별 쇼핑 트렌드 수집 및 시각화

본 작업지시서는 사전에 수집된 네이버 API 문서(특히 `datalab_shopping_insights.md`)를 기반으로, 외부 개발자 및 분석가가 **최근 1년간의 '선풍기'와 '핫팩' 검색 키워드에 대한 일자별 쇼핑 클릭 트렌드를 파이썬 언어로 수집하고 차트로 확인하며, 그 결과 데이터를 CSV로 영구 저장**할 수 있도록 구체적인 아키텍처와 환경 설정, 실행 과정을 지시하는 가이드입니다.

---

## 1. 작업 개요 및 사전 준비 (API 발급)

### 1.1 작업 개요 정의
본 파이썬 스크립트 기반 데이터 수집 작업의 명확한 방향성을 위해 다음 핵심 사항을 우선 정의합니다.
- **작업 목적**: 
  대표적인 계절성 상품인 **'선풍기(여름)'**와 **'핫팩(겨울)'** 키워드에 대하여 네이버 쇼핑 사용자들이 검색하고 클릭한 장기적인 트렌드 맥락(계절적 변동성)을 분석합니다. 이를 일자별 선형 그래프(Line Graph)로 직관적으로 시각화하고, 정량적인 원천 데이터(CSV 파일) 형태로 영구 확보하여 시즌별 상품 소싱 전략 및 마케팅 캠페인 시기 조율에 직접 활용합니다.
- **대상 API**: 
  네이버 데이터랩(DataLab) 산하 쇼핑인사이트 - **쇼핑인사이트 키워드별 트렌드 조회 API** 
  (*엔드포인트: `https://openapi.naver.com/v1/datalab/shopping/category/keywords`, 비로그인 POST 방식*)
- **데이터 수집 범위**: 
  - **수집 기간**: 스크립트를 구동하는 현재 날짜(Today)를 기준으로 **정확하게 최근 1년(365일) 전부터 전일/당일까지의 데이터**.
  - **시간 간격**: 주간/월간이 아닌 **일자별(`date`)** 세밀한 간격 수집.
  - **분석 대상 키워드**: 가전 카테고리(예: `50000015`) 내의 **'선풍기'** 및 생활 카테고리 등 범용 기준의 **'핫팩'** 키워드 배열.
  - **반환 데이터**: 해당 기간 동안 두 아이템 각각의 클릭 상대 비율 (가장 클릭이 높았던 날을 100으로 둔 0~100 사이의 상대적 비율).

### 1.2 네이버 개발자 포털 접근 권한 확보
1. [NAVER Developers](https://developers.naver.com) 에 방문하여 애플리케이션 등록 후 `데이터랩 (쇼핑인사이트)` API 권한을 필수로 체크합니다.
2. 애플리케이션 파트너 승인이 완료되면 본인의 `Client ID`와 `Client Secret` 고유 문자열 쌍을 발급받아 복사해 둡니다. 이는 HTTP 통신 코드에서 중요한 인증 헤더 값으로 사용됩니다.

---

## 2. 작업 환경 구축 지시 사항

파이썬에서 HTTP 요청을 수행하고 안정적으로 통계 자료를 그리기 위해 아래 규칙을 철저히 준수하여 프로젝트 구동 환경을 초기화합니다.

**[2단계] 가상 환경 구성 및 패키지 설치**
1. **환경 격리**: 전역 시스템을 오염시키지 않기 위하여 **`uv`** 패키지 매니저를 전적으로 활용합니다.
2. 지정된 폴더 위치에서 명령 프롬프트를 열고 다음 명령어를 실행하여 `.venv` 이름의 파이썬 가상환경을 조성합니다. (단, 기존에 `.venv` 가상환경 폴더가 성공적으로 존재한다면 새로 만들지 말고 기존 환경을 그대로 진입/활용합니다.)
   ```bash
   # 가상 환경이 없을 때만 실행
   uv venv .venv
   ```
3. 만들어진 가상환경을 파워쉘 환경에 맞춰 활성화시킵니다.
   ```powershell
   .venv\Scripts\activate
   ```
4. **필수 라이브러리 설치**: API 통신체인 `requests`와 일자별 변화를 그래프로 그릴 `matplotlib` 패키지, 그리고 한글 폰트가 깨지는 것을 방지할 `koreanize-matplotlib`를 설치합니다. (※ 시각화 시 `seaborn` 관련 라이브러리나 셋업은 절대로 사용하지 않습니다.)
   ```bash
   uv pip install requests matplotlib koreanize-matplotlib python-dateutil python-dotenv
   ```

---

## 3. 핵심 스크립트 작성 조감도

**[3단계] 데이터 수집 및 시각화 코드 작성**
루트 폴더 하위에 `trend_analyzer.py` 라는 파이썬 파일을 생성하고 아래의 뼈대를 베이스로 API 호출 로직을 구성합니다. 선풍기와 핫팩 2개 키워드를 동시 쿼리하여 비교 분석합니다.

### 3.1 파이썬 예제 코드 로직 (API 호출 + CSV 저장 + 시각화)

```python
import os
import urllib.request
import json
import csv
from datetime import datetime
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
import koreanize_matplotlib # 한글 폰트 깨짐 방지용 플러그인 모듈
from dotenv import load_dotenv

# 1. API 키 세팅 (.env 파일 로드)
load_dotenv()
client_id = os.getenv("NAVER_CLIENT_ID")
client_secret = os.getenv("NAVER_CLIENT_SECRET")
# 키워드별 트렌드 조회를 위한 전용 엔드포인트 URL
url = "https://openapi.naver.com/v1/datalab/shopping/category/keywords"

# 2. 날짜 설정 (최근 딱 1년 동적으로 계산)
end_dt = datetime.now()
start_dt = end_dt - relativedelta(years=1)
start_date_str = start_dt.strftime("%Y-%m-%d")
end_date_str = end_dt.strftime("%Y-%m-%d")

# 3. 데이터랩 Payload (바디) 정의
# 쇼핑인사이트 키워드 API는 최상위 카테고리(category) 문자열 1개가 필수입니다. 
# 여기서는 디지털/가전(50000015) 또는 생활/건강(50000021) 등 통합검색을 위해 대표 카테고리를 하나 지정합니다.
# (모든 분야 포괄이 불가능하므로, 예시로 '생활/건강' 카테고리 ID를 기준 파라미터로 잡습니다.)
body = {
    "startDate": start_date_str,
    "endDate": end_date_str,
    "timeUnit": "date",
    "category": "50000021", 
    "keyword": [
        {"name": "선풍기", "param": ["선풍기"]},
        {"name": "핫팩", "param": ["핫팩"]}
    ],
    "device": "",
    "gender": "",
    "ages": []
}

# 4. HTTP 요청 발신
req = urllib.request.Request(url)
req.add_header("X-Naver-Client-Id", client_id)
req.add_header("X-Naver-Client-Secret", client_secret)
req.add_header("Content-Type", "application/json")

try:
    response = urllib.request.urlopen(req, data=json.dumps(body).encode("utf-8"))
    res_code = response.getcode()
    if res_code == 200:
        response_body = response.read()
        res_json = json.loads(response_body.decode('utf-8'))
        
        # 5. 응답 JSON 파싱 (선풍기와 핫팩 2개의 results가 리턴됨)
        results = res_json['results']
        
        # 날짜 베이스 및 비율 딕셔너리 생성
        trend_data = {}
        for res in results:
            title = res['title'] # '선풍기' or '핫팩'
            for item in res['data']:
                period = item['period']
                ratio = item['ratio']
                if period not in trend_data:
                    trend_data[period] = {}
                trend_data[period][title] = ratio

        # 6. CSV 영구 저장 처리 (utf-8-sig 인코딩)
        dates = sorted(list(trend_data.keys()))
        csv_filename = "shopping_keyword_trend_data.csv"
        with open(csv_filename, mode='w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow(["조회 일자", "선풍기 (상대 비율)", "핫팩 (상대 비율)"])
            for d in dates:
                fan_ratio = trend_data[d].get("선풍기", 0)
                hotpack_ratio = trend_data[d].get("핫팩", 0)
                writer.writerow([d, fan_ratio, hotpack_ratio])
                
        print(f"데이터 수집 성공: '선풍기'와 '핫팩'의 1년치 데이터가 '{csv_filename}'에 영구 저장되었습니다.")
        
        # 7. Matplotlib 시각화 처리
        plt.figure(figsize=(14, 7))
        
        fan_ratios = [trend_data[d].get("선풍기", 0) for d in dates]
        hotpack_ratios = [trend_data[d].get("핫팩", 0) for d in dates]
        
        plt.plot(dates, fan_ratios, label="선풍기 (여름 계절성)", color="royalblue", alpha=0.8)
        plt.plot(dates, hotpack_ratios, label="핫팩 (겨울 계절성)", color="crimson", alpha=0.8)
        
        plt.title(f"최근 1년 간 '선풍기' vs '핫팩' 쇼핑 클릭 트렌드 비교\n({start_date_str} ~ {end_date_str})")
        plt.xlabel("조회 일자")
        plt.ylabel("상대 클릭 비율 (Max=100)")
        plt.xticks(dates[::30], rotation=45)
        plt.grid(True, linestyle="--", alpha=0.5)
        plt.legend()
        plt.tight_layout()
        
        image_filename = "shopping_keyword_trend_result.png"
        plt.savefig(image_filename)
        print(f"시각화 완료: 그래프가 '{image_filename}' 파일로 저장되었습니다.")
        
        plt.show() # 결과 그래픽 창 출력
    else:
        print("API 요청 실패 에러 코드:" + str(res_code))
except Exception as e:
    print("스크립트 실행 중 오류 발생:", e)
```

---

## 4. 데이터 수집 실행 및 영구 저장소 확보 확인

**[4단계] 산출물 뷰잉 및 CSV 영구 저장 확인 가이드**
1. 파워쉘 터미널에서 스크립트 실행 명령어(`python trend_analyzer.py`)를 통해 시스템 단 장애 없이 통신이 원활히 되는지 실행시킵니다.
2. 실행 직후 콘솔에 **`데이터 수집 성공: ... 'shopping_keyword_trend_data.csv'에 영구 저장되었습니다.`** 라는 메시지가 정상적으로 찍혔는지 1차 검수합니다. 
3. 루트 폴더 내에 수집 데이터 원본인 **`shopping_keyword_trend_data.csv`** 파일이 생성되었는지 점검합니다. 엑셀 등 외부 툴에서 열람하여 날짜(행) 별로 '선풍기'와 '핫팩'의 클릭 점유율 열(Column)이 각각 생성되어 있는지 데이터 무결성을 검증합니다.
4. 동일 디렉토리에 차트 사진인 **`shopping_keyword_trend_result.png`** 이미지 파일이 성공적으로 도출되는지 2차 검수합니다. 특히 여름(선풍기)과 겨울(핫팩)에 솟구치는 상반된 트렌드 곡선과 범례가 시각적으로 잘 나타나는지 확인합니다.
