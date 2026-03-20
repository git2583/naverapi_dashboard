# 쇼핑 검색 API 레퍼런스

## 개요
네이버 검색 결과를 뉴스, 백과사전, 블로그, 쇼핑, 웹 문서, 전문정보, 지식iN, 책, 카페글 등 분야별로 볼 수 있는 API입니다. 
쇼핑 검색은 검색 API를 사용해 네이버 검색의 쇼핑 검색 결과를 반환하는 RESTful API입니다. 쇼핑 검색 결과를 XML 형식 또는 JSON 형식으로 반환합니다.
- 하루 호출 한도는 25,000회입니다.
- **비로그인 방식 오픈 API**이므로 HTTP 요청 헤더에 클라이언트 아이디와 클라이언트 시크릿 값만 전송해 사용합니다.

## 사전 준비 사항
네이버 개발자 센터에서 애플리케이션을 등록하고 클라이언트 아이디와 클라이언트 시크릿을 발급받아야 합니다.

## 쇼핑 검색 결과 조회
네이버 검색의 쇼핑 검색 결과를 XML 또는 JSON 형식으로 반환합니다.

### 요청 URL
- XML: `https://openapi.naver.com/v1/search/shop.xml`
- JSON: `https://openapi.naver.com/v1/search/shop.json`

### 프로토콜
- HTTPS
- HTTP 메서드: GET

### 파라미터 제어
파라미터를 쿼리 스트링 형식으로 전달합니다. (query, display, start, sort 등)

### 요청 예시
```bash
curl "https://openapi.naver.com/v1/search/shop.json?query=%EC%A3%BC%EC%8B%9D&display=10&start=1&sort=sim" \
  -H "X-Naver-Client-Id: {발급받은 클라이언트 아이디 값}" \
  -H "X-Naver-Client-Secret: {발급받은 클라이언트 시크릿 값}" -v
```

### 응답
요청이 성공하면 XML 또는 JSON 형식으로 채널, 아이템 배열, 상품 정보 등을 반환합니다.

### 주요 오류 코드
- `display`: 범위 오류
- `start`: 범위 오류
- `sort`: 값 오류
- `403 오류`: API 권한 없음
