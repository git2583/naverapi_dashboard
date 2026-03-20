import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class APIConfig:
    CLIENT_ID = os.getenv("NAVER_CLIENT_ID")
    CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET")
    
    if not CLIENT_ID or not CLIENT_SECRET:
        print("경고: .env 파일에 NAVER_CLIENT_ID 또는 NAVER_CLIENT_SECRET이 설정되지 않았습니다.")

    BASE_URL = "https://openapi.naver.com/v1"
    SHOPPING_CATEGORY_KEYWORD_URL = f"{BASE_URL}/datalab/shopping/category/keywords"
