import urllib.request
import urllib.error
import urllib.parse
import json
import logging
from config.api_env import APIConfig

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class NaverAPIClient:
    """네이버 API 통신을 전담하는 HTTP 클라이언트"""

    def __init__(self):
        self.url = APIConfig.SHOPPING_CATEGORY_KEYWORD_URL
        self.headers = {
            "X-Naver-Client-Id": APIConfig.CLIENT_ID,
            "X-Naver-Client-Secret": APIConfig.CLIENT_SECRET,
            "Content-Type": "application/json"
        }

    def fetch_shopping_keywords_trend(self, payload: dict) -> dict:
        """쇼핑 키워드 트렌드 API를 호출하고 JSON 결과를 반환합니다."""
        if not APIConfig.CLIENT_ID or not APIConfig.CLIENT_SECRET:
            raise ValueError("API 자격 증명이 누락되었습니다. .env 파일을 확인해주세요.")

        req = urllib.request.Request(self.url)
        for key, value in self.headers.items():
            req.add_header(key, value)

        try:
            data = json.dumps(payload).encode("utf-8")
            response = urllib.request.urlopen(req, data=data)
            res_code = response.getcode()
            
            if res_code == 200:
                response_body = response.read()
                logging.info("API 호출 성공 (200 OK)")
                return json.loads(response_body.decode('utf-8'))
            else:
                logging.error(f"예기치 않은 상태 코드 반환: {res_code}")
                return {}

        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8')
            logging.error(f"HTTP 에러 발생: {e.code} - {error_body}")
            if e.code == 429:
                logging.error("일일 API 호출 한도를 초과했습니다 (429 Rate Limit Exceeded).")
            elif e.code == 401:
                logging.error("인증 실패 (401 Unauthorized). 클라이언트 아이디와 시크릿을 확인하세요.")
            raise e
        except Exception as e:
            logging.error(f"알 수 없는 통신 오류: {e}")
            raise e

    def fetch_search_results(self, node: str, keyword: str, start: int = 1, display: int = 10) -> dict:
        """네이버 검색 API(블로그, 카페, 뉴스, 쇼핑)를 호출합니다."""
        if not APIConfig.CLIENT_ID or not APIConfig.CLIENT_SECRET:
            raise ValueError("API 자격 증명이 누락되었습니다.")
            
        url = f"https://openapi.naver.com/v1/search/{node}.json?query={urllib.parse.quote(keyword)}&start={start}&display={display}"
        req = urllib.request.Request(url)
        for key, value in self.headers.items():
            req.add_header(key, value)
            
        try:
            response = urllib.request.urlopen(req)
            if response.getcode() == 200:
                return json.loads(response.read().decode('utf-8'))
            return {}
        except Exception as e:
            logging.error(f"Search API 통신 오류 ({node}): {e}")
            return {}
