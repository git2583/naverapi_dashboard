# 네이버 데이터랩 (DataLab) API - 통합검색어 트렌드

네이버 통합검색의 검색어 트렌드 데이터를 제공하는 API입니다. 
통합검색어 트렌드는 네이버 통합검색에서 발생하는 검색어를 연령별, 성별, 기기별(PC, 모바일)로 세분화해서 조회할 수 있는 API입니다. 사용자들은 특정 주제어에 대한 검색 추이를 파악하고 이를 기반으로 데이터 분석을 수행할 수 있습니다.

## 1. 개요 및 특징

### 1.1 분석하고 싶은 주제군을 설정합니다
궁금한 주제어를 설정하고, 하위 주제어에 해당하는 검색어를 쉼표(,)로 구분해 입력합니다. 여러 검색어에 대한 데이터를 합산하여 전체적인 해당 주제가 네이버에서 얼마나 검색되는지 조회할 수 있습니다.
- **예시**: 주제어 `캠핑` -> 하위 주제어: `캠핑`, `Camping`, `캠핑용품`, `겨울캠핑`, `캠핑장`, `글램핑`, `오토캠핑`, `캠핑카`, `텐트`, `캠핑요리` 등 쉼표로 구분하여 입력.

### 1.2 세분화된 정보를 확인할 수 있습니다
설정한 주제군에 대해 기간을 **일간, 주간, 월간 단위**로 조회할 수 있습니다. 
또한, 5살 단위로 연령을 세분화해 조회할 수 있습니다. 연령을 5살 간격으로 설정한 이유는 연령 이외에 직업군 유추도 어느 정도 가능할 것이라고 보기 때문입니다. 성별도 남성, 여성으로 세분화해 조회가 가능하며, 마지막으로 기기 환경(PC와 모바일)을 각각 구분해서 조회할 수 있습니다.

### 1.3 상대적 값으로만 제공됩니다
검색어 트렌드는 요청된 기간 중 검색 횟수가 가장 높은 시점을 **100**으로 두고 나머지는 상대적 값으로 제공하고 있습니다. 검색 횟수의 절대적인 수치 제공은 내부 정책상 제공하지 않으며, 현재 고려하지 않고 있습니다. 하지만 상대적인 값만으로도 특정 주제, 검색어의 트렌드를 추적하고 빅데이터 분석을 수행하는 데는 충분한 인사이트를 제공합니다.

## 2. API 인증 및 사전 준비 사항

데이터랩 API는 **비로그인 방식 오픈 API**입니다. 네이버 개발자 센터에서 발급 받은 **클라이언트 아이디(Client ID)**와 **클라이언트 시크릿(Client Secret)**을 HTTP 헤더에 담아서 전송해야 합니다. 
별도의 네이버 사용자 로그인 과정(OAuth 접근 토큰 획득)이 필요하지 않습니다.

- HTTP 헤더 파라미터 `X-Naver-Client-Id`: 발급받은 클라이언트 아이디.
- HTTP 헤더 파라미터 `X-Naver-Client-Secret`: 발급받은 클라이언트 시크릿.

## 3. 통합검색어 트렌드 API 레퍼런스

### 3.1 기본 정보
- **요청 URL**: `https://openapi.naver.com/v1/datalab/search`
- **HTTP 메서드**: `POST`
- **프로토콜**: `HTTPS`
- **Content-Type**: `application/json`
- **일일 호출 한도**: 1,000회

### 3.2 요청 파라미터 (Request JSON)
이 API는 `POST` 방식을 사용하며, 조건 파라미터를 JSON 형식의 Body로 전달합니다.

| 파라미터명 | 타입 | 필수 여부 | 설명 |
| :--- | :--- | :---: | :--- |
| `startDate` | string | **Y** | 조회 시작 일자. `YYYY-MM-DD` 형식. |
| `endDate` | string | **Y** | 조회 종료 일자. `YYYY-MM-DD` 형식. |
| `timeUnit` | string | **Y** | 구간 단위. `date`(일간), `week`(주간), `month`(월간) 중 하나를 지정합니다. |
| `keywordGroups` | array | **Y** | 주제어와 주제어에 해당하는 검색어 배열의 묶음. 최대 5개 그룹까지 지정 가능합니다. |
| `device` | string | N | 기기 환경. 빈 문자열이면 모든 기기, `pc`면 PC 기기, `mo`면 모바일 기기를 의미합니다. |
| `gender` | string | N | 성별. 빈 문자열이면 모든 성별, `m`이면 남성, `f`이면 여성을 의미합니다. |
| `ages` | array | N | 연령대. 생략하면 모든 연령대 통계가 반환됩니다. `1`(0~12세), `2`(13~18세), `3`(19~24세), `4`(25~29세), `5`(30~34세), `6`(35~39세), `7`(40~44세), `8`(45~49세), `9`(50~54세), `10`(55~59세), `11`(60세 이상) 스트링 배열로 전달합니다. |

**`keywordGroups` 배열의 구조**
- `groupName` (string, 필수): 주제어 이름.
- `keywords` (array of string, 필수): 주제어에 포함되는 상세 검색어 배열. 최대 20개까지 추가 가능.

### 3.3 응답 형식 (Response JSON)
요청에 성공하면 HTTP 응답 상태 코드 `200`을 반환하며, 데이터 리스트가 포함된 JSON이 전달됩니다.

| 필드명 | 타입 | 설명 |
| :--- | :--- | :--- |
| `startDate` | string | 실제 조회된 시작 일자 (`YYYY-MM-DD` 형식) |
| `endDate` | string | 실제 조회된 종료 일자 (`YYYY-MM-DD` 형식) |
| `timeUnit` | string | 입력된 구간 단위 (`date`, `week`, `month`) |
| `results` | array | 그룹 단위의 검색 트렌드 결과 배열 |
| `results[].title` | string | 주제어 그룹 이름 (`groupName`에 대응됨) |
| `results[].keywords` | array | 주제어 그룹 내부에 포함된 검색어 리스트 |
| `results[].data` | array | 날짜 범위에 해당하는 검색량 데이터 트렌드 배열 |
| `results[].data[].period` | string | 데이터 기간 정보 (`YYYY-MM-DD` 형식) |
| `results[].data[].ratio` | number | 최고 검색량을 100으로 두었을 때의 상대적 검색량 수치 (0 ~ 100 사이의 실수 값) |

---

## 4. API 호출 구현 예제

통합 검색어 트렌드를 가져오기 위해 서버 측에서 직접 API를 POST 통신해야 합니다. 다음은 다양한 언어에서의 API 호출 예제입니다.

### 4.1 cURL 예제
```bash
curl "https://openapi.naver.com/v1/datalab/search" \
    -H "X-Naver-Client-Id: {애플리케이션 등록 시 발급받은 클라이언트 아이디 값}" \
    -H "X-Naver-Client-Secret: {애플리케이션 등록 시 발급받은 클라이언트 시크릿 값}" \
    -H "Content-Type: application/json" \
    -X POST \
    -d '{
        "startDate": "2017-01-01",
        "endDate": "2017-04-30",
        "timeUnit": "month",
        "keywordGroups": [
            {
                "groupName": "한글",
                "keywords": ["한글", "korean"]
            },
            {
                "groupName": "영어",
                "keywords": ["영어", "english"]
            }
        ],
        "device": "pc",
        "ages": ["1", "2"]
    }'
```

### 4.2 Python 예제
```python
import os
import sys
import urllib.request
import json

client_id = "YOUR_CLIENT_ID"
client_secret = "YOUR_CLIENT_SECRET"
url = "https://openapi.naver.com/v1/datalab/search"

# 요청 파라미터 JSON 구성
body = {
    "startDate": "2017-01-01",
    "endDate": "2017-04-30",
    "timeUnit": "month",
    "keywordGroups": [
        {"groupName": "한글", "keywords": ["한글", "korean"]},
        {"groupName": "영어", "keywords": ["영어", "english"]}
    ],
    "device": "pc",
    "ages": ["1", "2"]
}

request = urllib.request.Request(url)
request.add_header("X-Naver-Client-Id", client_id)
request.add_header("X-Naver-Client-Secret", client_secret)
request.add_header("Content-Type", "application/json")

try:
    response = urllib.request.urlopen(request, data=json.dumps(body).encode("utf-8"))
    rescode = response.getcode()
    if(rescode == 200):
        response_body = response.read()
        print(response_body.decode('utf-8'))
    else:
        print("Error Code:" + str(rescode))
except Exception as e:
    print(e)
```

### 4.3 Java 예제
```java
import java.io.*;
import java.net.HttpURLConnection;
import java.net.URL;

public class DataLabSearchTrend {
    public static void main(String[] args) {
        String clientId = "YOUR_CLIENT_ID"; // 애플리케이션 클라이언트 아이디
        String clientSecret = "YOUR_CLIENT_SECRET"; // 애플리케이션 클라이언트 시크릿
        String apiURL = "https://openapi.naver.com/v1/datalab/search";

        try {
            URL url = new URL(apiURL);
            HttpURLConnection con = (HttpURLConnection)url.openConnection();
            con.setRequestMethod("POST");
            con.setRequestProperty("X-Naver-Client-Id", clientId);
            con.setRequestProperty("X-Naver-Client-Secret", clientSecret);
            con.setRequestProperty("Content-Type", "application/json");

            String postParams = "{\"startDate\":\"2017-01-01\",\"endDate\":\"2017-04-30\",\"timeUnit\":\"month\",\"keywordGroups\":[{\"groupName\":\"한글\",\"keywords\":[\"한글\",\"korean\"]},{\"groupName\":\"영어\",\"keywords\":[\"영어\",\"english\"]}],\"device\":\"pc\",\"ages\":[\"1\",\"2\"]}";
            
            con.setDoOutput(true);
            try (DataOutputStream wr = new DataOutputStream(con.getOutputStream())) {
                wr.write(postParams.getBytes("UTF-8"));
                wr.flush();
            }

            int responseCode = con.getResponseCode();
            BufferedReader br;
            if (responseCode == 200) { 
                br = new BufferedReader(new InputStreamReader(con.getInputStream(), "UTF-8"));
            } else {  
                br = new BufferedReader(new InputStreamReader(con.getErrorStream(), "UTF-8"));
            }

            String inputLine;
            StringBuilder response = new StringBuilder();
            while ((inputLine = br.readLine()) != null) {
                response.append(inputLine);
            }
            br.close();
            System.out.println(response.toString());
        } catch (Exception e) {
            System.out.println(e);
        }
    }
}
```

## 5. 오류 코드 및 문제 해결

| 에러 코드 | HTTP 상태 코드 | 메시지 (에러 원인) | 조치 방향 |
| :--- | :---: | :--- | :--- |
| `SE01` | 400 | `Incorrect query request. ` (잘못된 쿼리요청입니다.) | 파라미터가 JSON 문법에 맞지 않거나 필수 값이 누락되었는지 확인하세요. `keywordGroups` 포맷 오류 점검. |
| `SE02` | 400 | `Invalid date format.` (유효하지 않은 날짜 형식입니다.) | `startDate`, `endDate`의 값이 `YYYY-MM-DD`인지 검토하세요. |
| `SE03` | 400 | `Invalid date range.` (유효하지 않은 날짜 범위입니다.) | `startDate`가 `endDate`보다 미래에 있거나 2016-01-01 이전인지 확인하세요. |
| `SE04` | 400 | `Invalid time unit.` (유효하지 않은 기간 단위입니다.) | `timeUnit`의 값이 `date`, `week`, `month` 에 속하는지 확인. |
| `403` | 403 | `API 권한 없음` | 클라이언트 아이디/시크릿이 틀렸거나 권한을 신청하지 않았습니다. 개발자 센터 내 애플리케이션 세팅 화면에서 DataLab 검색 기능이 활성화되었는지 확인하세요. |
| `429` | 429 | `Rate Limit Exceeded` | 일일 호출 허용량(1,000회)을 초과했습니다. 다음 날 다시 요청이 필요합니다. |
| `500` | 500 | `Internal Server Error` | 네이버 내부 서버 오류이므로 시간이 지난 뒤에 다시 호출해야 합니다. |

추가적으로, 데이터랩 오픈 API 호출 결과는 데이터가 매일 갱신되며, 새벽 시간에 호출될 경우 전일자 통계가 아직 반영되지 않을 수 있으므로, 최신 정보를 원한다면 운영시간을 고려한 데이터 수집 스케줄링 방식을 추천합니다.
