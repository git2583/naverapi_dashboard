# 네이버 오픈API 종류

인증 여부에 따라 **로그인 방식 오픈 API**와 **비로그인 방식 오픈 API**로 구분됩니다.

## 1. 로그인 방식 오픈 API
'네이버 로그인' 인증을 받아 접근 토큰(access token)을 획득해야 사용할 수 있는 API입니다.
- **네이버 로그인**: 별도의 아이디와 비밀번호 없이 네이버 아이디로 로그인.
- **카페**: 외부 서비스에서 네이버 카페에 가입, 게시글 등록.
- **캘린더**: 외부 서비스에서 네이버 캘린더에 일정 등록.

### 주요 요청 URL
- 인증: `https://nid.naver.com/oauth2.0/authorize`
- 토큰 획득: `https://nid.naver.com/oauth2.0/token`
- 내 정보: `https://openapi.naver.com/v1/nid/me`

## 2. 비로그인 방식 오픈 API
HTTP 헤더에 클라이언트 아이디와 클라이언트 시크릿 값만 전송하여 접근 토큰 없이 사용할 수 있는 API입니다.
- **데이터랩**: 네이버 데이터랩의 검색어 트렌드와 쇼핑인사이트 실행 관련 API.
- **검색**: 뉴스, 백과사전, 블로그, 쇼핑 등 검색 결과 제공.
- **이미지/음성 캡차**: 자동입력 방지용 기능.
- **네이버 공유하기 / 오픈메인**: 웹 등 콘텐츠를 네이버 생태계에 담는 플러그.
- **Clova Face Recognition**: 사진 내 얼굴 인식 기능 API.

### 주요 요청 URL
- 데이터랩 (검색 추이): `https://openapi.naver.com/v1/datalab/search`
- 데이터랩 (쇼핑 인사이트 분야): `https://openapi.naver.com/v1/datalab/shopping/categories`
- 검색 (쇼핑): `https://openapi.naver.com/v1/search/shop`
- Clova 얼굴 인식: `https://openapi.naver.com/v1/vision/face`
