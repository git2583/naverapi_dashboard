import csv
import logging

class DataPipeline:
    """API 응답 JSON 파싱 및 CSV 변환 서비스"""

    @staticmethod
    def parse_trend_data(json_response: dict) -> tuple:
        """
        API에서 반환받은 JSON 결과를 시계열 딕셔너리로 Flatten 처리합니다.
        Returns:
            dates (list): 정렬된 날짜 리스트
            trend_data (dict): 날짜를 키로 하고, 내부 딕셔너리에 키워드별 비율을 저장한 객체
        """
        if 'results' not in json_response:
            logging.warning("JSON 응답에 'results' 키가 없습니다. 데이터가 비어있을 수 있습니다.")
            return [], {}

        results = json_response['results']
        trend_data = {}
        
        for res in results:
            title = res['title']  # '선풍기' or '핫팩'
            for item in res['data']:
                period = item['period']
                ratio = item['ratio']
                if period not in trend_data:
                    trend_data[period] = {}
                trend_data[period][title] = ratio
                
        dates = sorted(list(trend_data.keys()))
        logging.info(f"데이터 파싱 완료: 총 {len(dates)}일의 데이터 추출됨")
        return dates, trend_data

    @staticmethod
    def save_to_csv(dates: list, trend_data: dict, filename: str, keywords: list):
        """
        파싱된 트렌드 데이터를 CSV 파일로 추출하여 영구 저장소에 저장합니다.
        """
        if not dates:
            logging.warning("저장할 데이터가 존재하지 않아 CSV 생성을 건너뜁니다.")
            return

        headers = ["조회 일자"] + [f"{k} (상대 비율)" for k in keywords]
        
        try:
            with open(filename, mode='w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                writer.writerow(headers)
                
                for d in dates:
                    row = [d]
                    for k in keywords:
                        ratio = trend_data[d].get(k, 0)
                        row.append(ratio)
                    writer.writerow(row)
                    
            logging.info(f"CSV 데이터 저장 완료: '{filename}'")
        except Exception as e:
            logging.error(f"CSV 파일 저장 중 에러 발생: {e}")
            raise e
