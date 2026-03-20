import matplotlib.pyplot as plt
import koreanize_matplotlib # 한글 폰트 글로벌 설정 모듈
import logging

class TrendPlotter:
    """Matplotlib을 활용한 트렌드 데이터 시각화 클래스"""

    def __init__(self, start_date_str: str, end_date_str: str):
        self.start_date_str = start_date_str
        self.end_date_str = end_date_str

    def plot_comparison(self, dates: list, trend_data: dict, keywords: list, output_filename: str):
        """복수의 키워드 데이터를 선형 그래프로 오버레이 시각화합니다."""
        if not dates or not keywords:
            logging.error("그래프를 그릴 대상 데이터나 키워드가 부족합니다.")
            return

        try:
            plt.figure(figsize=(14, 7))
            
            # 사전에 정의된 색상 및 투명도 팔레트 설정
            colors = ["royalblue", "crimson", "seagreen", "goldenrod"]
            
            for idx, keyword in enumerate(keywords):
                ratios = [trend_data[d].get(keyword, 0) for d in dates]
                color = colors[idx % len(colors)]
                plt.plot(dates, ratios, label=keyword, color=color, alpha=0.8, linewidth=2)
            
            plt.title(f"최근 1년 쇼핑 키워드 클릭 트렌드 비교\n({self.start_date_str} ~ {self.end_date_str})", fontsize=16, pad=15)
            plt.xlabel("조회 일자", fontsize=12)
            plt.ylabel("상대 클릭 비율 (Max=100)", fontsize=12)
            
            # X축 눈금이 너무 많아 텍스트가 겹치지 않도록 30일 간격 표시
            plt.xticks(dates[::30], rotation=45)
            
            plt.grid(True, linestyle="--", alpha=0.5)
            plt.legend(fontsize=12, loc="upper right")
            plt.tight_layout()
            
            plt.savefig(output_filename, dpi=300)
            logging.info(f"시각화 그래프 저장 완료: '{output_filename}'")
            
            # CLI 환경이 아닐 경우 창을 띄웁니다
            # 배치 잡(Batch Job)으로 서버에서 돌 때는 아래 줄을 주석처리합니다.
            # plt.show() 
            plt.close()
            
        except Exception as e:
            logging.error(f"시각화 과정 중 오류 발생: {e}")
            raise e
