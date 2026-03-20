# 쇼핑인사이트 (Shopping Insights) API 레퍼런스

네이버 통합검색의 쇼핑 영역과 네이버쇼핑 서비스의 검색 결과에서 사용자가 클릭한 상품 데이터를 다양한 세부 기준으로 조회할 수 있는 최적화된 API입니다. 이 API는 특히 시장의 수요를 분석해야 하는 예비 창업자 및 소상공인에게 큰 도움을 주기 위해 전략적으로 기획 및 개발되었습니다. 쇼핑 분야별, 검색 키워드별, 연령별, 성별, 접속 기기별(PC, 모바일) 트렌드 정보와 검색 상대 비율을 분석할 수 있습니다.

## 1. 쇼핑 인사이트 개요 및 특징

### 1.1 분야별 통계를 확인할 수 있습니다
네이버쇼핑 서비스에는 `카테고리 1 > 카테고리 2 > 카테고리 3 > 카테고리 4`와 같이 4단계의 깊은 수준으로 나뉘는 세부 쇼핑 분야 분류 엔진이 적용되어 있습니다. 쇼핑 분야 중심의 디테일한 통계 정보를 1차부터 4차까지 카테고리별로 상세히 제공하여 상인의 재고 관리와 마케팅에 매우 유의미하게 활용할 수 있습니다.

### 1.2 검색어 클릭 추이 및 대상 고객층 파악이 가능합니다
지정한 쇼핑 분야의 상품이 사용자에게 얼마나 검색되고, 결과가 클릭되었는지 일 단위나 주 단위, 월 단위로 파악할 수 있습니다. 네이버쇼핑 서비스를 통해 주력으로 진행 중인 아이템 품목의 연령별 분포 비중, 접속 기기 비중 내지는 성별 분포 비중들을 면밀히 추적하고 최적화할 수 있습니다. 
※ **카테고리 분야 코드 구하는 법**: 분야 조회는 네이버쇼핑 서비스 URL 구조 자체에서 `cat_id` 파라미터의 값으로 조회할 수 있습니다. 예: `cat_id=50000805` (패션의류 > 여성의류 > 니트/스웨터). 

### 1.3 오픈 API 지원 및 정책 특징 
- **비로그인 방식 API**: 인증 없이 오픈된 정보를 획득하는 API로, 사용자 로그인을 통한 Access Token 방식을 요구하지 않으며, 네이버 개발자 센터에서 발행받은 클라이언트 아이디/시크릿 페어만으로 즉각 이용 가능합니다.
- **상대적 값 산출**: 쇼핑인사이트에 제공되는 모든 수치 데이터는, 요청한 조회 구간(기간) 중 총 클릭 횟수가 가장 높은 시점의 값을 자동으로 `100`으로 둡니다. 그리고 나머지 기간의 클릭 비율 값은 최대값에 대한 상대적인 등락 곡선 좌표를 0에서 100 사이의 상대적 비율로 환산해서 제공합니다.
- **일일 호출 한도**: 정책상 일일 기본 호출 한도는 `1,000회`입니다. 대량의 카테고리 조회가 필요한 경우 개발자 포럼을 통한 한도 추가 요청이 요구됩니다.

---

## 2. API 공통 요청 조건

- 프로토콜: `HTTPS`
- 메서드: `POST` (Body에 분석 파라미터를 JSON 객체로 전달)
- HTTP 헤더: 
  - `X-Naver-Client-Id` : 등록한 개발자 애플리케이션 아이디
  - `X-Naver-Client-Secret` : 등록한 개발자 애플리케이션 시크릿
  - `Content-Type` : `application/json`

---

## 3. 세부 API 엔드포인트 레퍼런스

### 3.1 쇼핑인사이트 분야별 트렌드 조회
특정 카테고리에 대한 날짜별 클릭 비율 트렌드 추이를 반환합니다.

- **요청 URL**: `https://openapi.naver.com/v1/datalab/shopping/categories`
- **JSON 파라미터 구조**:
  - `startDate` (string, 필수) : 시점 (`YYYY-MM-DD`)
  - `endDate` (string, 필수) : 종점 (`YYYY-MM-DD`)
  - `timeUnit` (string, 필수) : `date`, `week`, `month`
  - `category` (array, 필수) : 분야 배열. 내부 객체로 `name`(주제어 문자열)과 `param`(카테고리 id 정보 리스트)을 전달합니다.
  - `device`, `gender`, `ages` (선택) : 필터 옵션.

**요청 (Request) 예시**:
```bash
curl "https://openapi.naver.com/v1/datalab/shopping/categories" \
  --header "X-Naver-Client-Id: {발급받은 클라이언트 아이디 값}" \
  --header "X-Naver-Client-Secret: {발급받은 클라이언트 시크릿 값}" \
  --header "Content-Type: application/json" \
  --data '{ 
    "startDate": "2017-08-01", 
    "endDate": "2017-09-30", 
    "timeUnit": "month", 
    "category": [ 
      {"name": "패션의류", "param": ["50000000"]}, 
      {"name": "화장품/미용", "param": ["50000002"]} 
    ], 
    "device": "pc", 
    "gender": "f", 
    "ages": ["20", "30"] 
}'
```

---

### 3.2 쇼핑인사이트 분야 내 기기별 / 성별 / 연령별 트렌드 조회
특정 카테고리에 대해서만 기기별, 성별별, 연령별 분포 및 추이를 반환합니다.

- **기기별 트렌드 URL**: `https://openapi.naver.com/v1/datalab/shopping/category/device`
- **성별 트렌드 URL**: `https://openapi.naver.com/v1/datalab/shopping/category/gender`
- **연령별 트렌드 URL**: `https://openapi.naver.com/v1/datalab/shopping/category/age`

위 3가지 엔드포인트는 리스트 형태의 `category` 파라미터가 아니라, 문자열 형태의 `category` 파라미터 1개만 입력받습니다.

**응답 (Response) 예시 (연령별 조회 시)**:
```json
{
  "startDate": "2017-08-01",
  "endDate": "2017-09-30",
  "timeUnit": "month",
  "results": [
    {
      "title": "50000000",
      "category": ["50000000"],
      "data": [
        { "period": "2017-08-01", "group": "20", "ratio": 45.12345 },
        { "period": "2017-08-01", "group": "30", "ratio": 30.15873 },
        { "period": "2017-09-01", "group": "20", "ratio": 100.0 },
        { "period": "2017-09-01", "group": "30", "ratio": 50.12345 }
      ]
    }
  ]
}
```

---

### 3.3 쇼핑인사이트 키워드 트렌드 기반 조회
특정 분야 하위에 존재하는 특수 검색 키워드의 클릭 추이를 상세하게 분석합니다.

- **기본 트렌드 URL**: `https://openapi.naver.com/v1/datalab/shopping/category/keywords`
- **기기별 분류 URL**: `https://openapi.naver.com/v1/datalab/shopping/category/keyword/device`
- **성별별 분류 URL**: `https://openapi.naver.com/v1/datalab/shopping/category/keyword/gender`
- **연령별 분류 URL**: `https://openapi.naver.com/v1/datalab/shopping/category/keyword/age`

**요청 (Request) 본문 JSON 예시**:
```json
{
  "startDate": "2022-01-01",
  "endDate": "2022-03-31",
  "timeUnit": "month",
  "category": "50000000",
  "keyword": [
    {"name": "패션의류/정장", "param": ["정장"]},
    {"name": "패션의류/비지니스 캐주얼", "param": ["비지니스 캐주얼"]}
  ],
  "device": "",
  "gender": "",
  "ages": []
}
```

**응답 데이터 구성**:
- 응답 JSON 내부에 `results` 배열로 결과 그룹이 삽입됩니다. 
- 필터 조건인 `group`(분류) 필드는 엔드포인트에 따라 달라집니다.
- 연령 조회 `group` 포맷 : "10" (10대 이하), "20" (20대 전체), "30" (30대 전체), "40", "50", "60" 등 10단위 반올림 구성.
- 성별 조회 `group` 포맷 : "m" (남성 사용자), "f" (여성 사용자).
- 기기 조회 `group` 포맷 : "pc" (PC 웹 브라우저), "mo" (모바일 웹/앱 환경).

---

## 4. 언어별 API 구현 예제 모음

### Node.js 구현 예제
자바스크립트/Node 환경에서는 `request` 모듈 혹은 내장 모듈, 기본 `fetch`를 활용하여 요청할 수 있습니다.
```javascript
var request = require('request');

var client_id = 'YOUR_CLIENT_ID';
var client_secret = 'YOUR_CLIENT_SECRET';

var api_url = 'https://openapi.naver.com/v1/datalab/shopping/categories';
var request_body = {
    "startDate": "2017-08-01",
    "endDate": "2017-09-30",
    "timeUnit": "month",
    "category": [
        {"name": "패션의류", "param": ["50000000"]},
        {"name": "화장품/미용", "param": ["50000002"]}
    ],
    "device": "pc",
    "gender": "f",
    "ages": ["20", "30"]
};

var options = {
    url: api_url,
    body: JSON.stringify(request_body),
    headers: {
        'X-Naver-Client-Id': client_id,
        'X-Naver-Client-Secret': client_secret,
        'Content-Type': 'application/json'
    }
};

request.post(options, function (error, response, body) {
    if (!error && response.statusCode == 200) {
        console.log(body);
    } else {
        console.log('error = ' + response.statusCode);
        console.log('error detail = ' + body);
    }
});
```

### PHP 구현 예제
PHP에서의 cURL 적용 예제는 아래 형태를 만족합니다.
```php
<?php
$client_id = "YOUR_CLIENT_ID";
$client_secret = "YOUR_CLIENT_SECRET";
$url = "https://openapi.naver.com/v1/datalab/shopping/categories";

$post_params = '{
  "startDate": "2017-08-01",
  "endDate": "2017-09-30",
  "timeUnit": "month",
  "category": [
    {"name": "패션의류", "param": ["50000000"]},
    {"name": "화장품/미용", "param": ["50000002"]}
  ],
  "device": "pc",
  "gender": "f",
  "ages": ["20", "30"]
}';

$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $url);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
$headers = array();
$headers[] = "X-Naver-Client-Id: ".$client_id;
$headers[] = "X-Naver-Client-Secret: ".$client_secret;
$headers[] = "Content-Type: application/json";
curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
curl_setopt($ch, CURLOPT_POSTFIELDS, $post_params);
$response = curl_exec ($ch);
$status_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
if($status_code == 200) {
    echo $response;
} else {
    echo "Error Error 내용:".$response;
}
curl_close ($ch);
?>
```

## 5. 자주 발생하는 오류 코드 대응

응답이 비정상일 경우 JSON 컨텐츠 안에 에러 상세 메시지가 표기됩니다. 주요 오류 대처 방법입니다.

| 발생 오류 상태 | 사유 및 메시지 내용 | 해결 방안 |
| :---: | :--- | :--- |
| `HTTP 400` | 필수 파라미터가 누락되거나 날짜 포맷(`YYYY-MM-DD`)이 규정을 지키지 않았을 시 발생합니다. | JSON 객체 속성에 오타가 없는지, `category` 하위의 아이템 형식이 규격을 지키는지 검토 필요합니다. |
| `HTTP 403` | 허가되지 않은 권한으로 접근을 시도할 때 일어납니다. 보통 헤더 추가 누락이나 신청이 안 된 경우입니다. | 네이버 개발자 환경에 로그인 후 `[애플리케이션 설정] -> [이용 API 설정]`으로 진입하여 `데이터랩 (쇼핑인사이트)` 체크박스 항목이 정상적으로 켜져 있는지 가장 먼저 확인해야 합니다. |
| `HTTP 404` | 없는 URL로 메서드를 보냈거나 지원되지 않는 API 버전을 호출했을 경우입니다. | 엔드포인트 URL 라우트 형식이 `/v1/datalab/...` 패턴이 맞는지 꼼꼼히 확인합니다. |
| `HTTP 429` | 요청량이 가이드 한도수치인 하루 1,000회를 초과했습니다. | 캐시 레이어를 도입하거나, 자정 넘어서까지 호출을 일시 정지해야 합니다. |
| `HTTP 5xx` | 내부 네이버 서버에서의 계산 오류나 일시 장애입니다. | 통상적으로 몇 분 뒤 정상적으로 복구되니 Retry 로직을 구축하시기 바랍니다. |
