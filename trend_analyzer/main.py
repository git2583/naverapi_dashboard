import platform
# Windows WMI query 멈춤(Hang) 현상을 우회하기 위한 몽키패치
platform.win32_ver = lambda *args, **kwargs: ('10', '10.0.19041', '', 'Multiprocessor Free')

import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta
from services.naver_client import NaverAPIClient
from services.data_pipeline import DataPipeline
from visualization.trend_plotter import TrendPlotter

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_payload(start_date: str, end_date: str, category: str, keywords: list) -> dict:
    """쇼핑인사이트 키워드 조회 API Payload를 생성합니다."""
    keyword_objects = [{"name": kw, "param": [kw]} for kw in keywords]
    return {
        "startDate": start_date,
        "endDate": end_date,
        "timeUnit": "date",
        "category": category,
        "keyword": keyword_objects,
        "device": "",
        "gender": "",
        "ages": []
    }

def main():
    import os
    try:
        logging.info("쇼핑 트렌드 분석기 시작")
        
        data_dir = os.path.join(os.path.dirname(__file__), "data")
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
            logging.info(f"'{data_dir}' 폴더가 생성되었습니다.")
        
        end_dt = datetime.now()
        start_dt = end_dt - relativedelta(years=1)
        start_date_str = start_dt.strftime("%Y-%m-%d")
        end_date_str = end_dt.strftime("%Y-%m-%d")
        
        # 2. 분석 지표 설정: 카테고리가 다른 두 키워드를 별도 호출하여 병합
        queries = [
            {"keyword": "선풍기", "category": "50000003"}, # 디지털/가전 (대분류)
            {"keyword": "핫팩", "category": "50000007"}   # 스포츠/레저 (대분류 - 겨울 캠핑 등)
        ]
        
        api_client = NaverAPIClient()
        merged_trend_data = {}
        all_dates = set()
        
        for q in queries:
            kw = q["keyword"]
            cat = q["category"]
            payload = create_payload(start_date_str, end_date_str, cat, [kw])
            logging.info(f"파라미터 호출: 키워드 '{kw}', 카테고리 '{cat}'")
            json_resp = api_client.fetch_shopping_keywords_trend(payload)
            
            if json_resp:
                dates, t_data = DataPipeline.parse_trend_data(json_resp)
                for d in dates:
                    all_dates.add(d)
                    if d not in merged_trend_data:
                        merged_trend_data[d] = {}
                    merged_trend_data[d][kw] = t_data[d].get(kw, 0)
        
        sorted_dates = sorted(list(all_dates))
        target_keywords = ["선풍기", "핫팩"]
        
        if not sorted_dates:
            logging.error("병합할 데이터가 소실되었습니다.")
            return
            
        csv_path = os.path.join(data_dir, "shopping_keyword_trend_data.csv")
        DataPipeline.save_to_csv(
            dates=sorted_dates, 
            trend_data=merged_trend_data, 
            filename=csv_path, 
            keywords=target_keywords
        )
        
        plotter = TrendPlotter(start_date_str, end_date_str)
        png_path = os.path.join(data_dir, "shopping_keyword_trend_result.png")
        plotter.plot_comparison(
            dates=sorted_dates, 
            trend_data=merged_trend_data, 
            keywords=target_keywords, 
            output_filename=png_path
        )
        
        logging.info("모든 데이터 분석 프로세스가 성공적으로 완료되었습니다.")
        
    except Exception as e:
        logging.critical(f"어플리케이션 크래시 발생: {e}", exc_info=True)

if __name__ == "__main__":
    main()
