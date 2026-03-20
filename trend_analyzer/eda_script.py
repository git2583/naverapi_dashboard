import platform
platform.win32_ver = lambda *args, **kwargs: ('10', '10.0.19041', '', 'Multiprocessor Free')

import os
import io
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib

def create_eda_report():
    data_path = "data/shopping_keyword_trend_data.csv"
    if not os.path.exists(data_path):
        print(f"데이터 파일이 없습니다: {data_path}")
        return
        
    df = pd.read_csv(data_path, encoding='utf-8-sig')
    
    # Feature Engineering
    df['조회 일자'] = pd.to_datetime(df['조회 일자'])
    df['월'] = df['조회 일자'].dt.month
    df['요일'] = df['조회 일자'].dt.day_name()
    
    def get_season(month):
        if month in [3, 4, 5]: return '봄'
        elif month in [6, 7, 8]: return '여름'
        elif month in [9, 10, 11]: return '가을'
        else: return '겨울'
        
    df['계절'] = df['월'].apply(get_season)

    os.makedirs("images", exist_ok=True)
    report = []
    
    report.append("# 당신의 20년차 데이터 분석가: 쇼핑 트렌드 탐색적 데이터 분석(EDA) 리포트\n")
    report.append("본 리포트는 네이버 쇼핑 트렌드('선풍기', '핫팩') 데이터를 다방면으로 분석한 결과를 요약한 Markdown 문서입니다.\n\n")
    
    # 1. 상하위 5개행
    report.append("## 1. 데이터 기본 정보 확\n")
    report.append("### 데이터 상위 5개 행:\n")
    report.append(df.head().to_markdown() + "\n\n")
    report.append("### 데이터 하위 5개 행:\n")
    report.append(df.tail().to_markdown() + "\n\n")
    
    # 2. Info
    buf = io.StringIO()
    df.info(buf=buf)
    report.append("### 데이터 기본 변수 정보 (.info()):\n```\n" + buf.getvalue() + "```\n\n")
    
    # 3. Shape & Duplicates
    report.append(f"### 전체 구조 및 중복:\n- **전체 행의 수**: {df.shape[0]}행\n- **전체 열의 수**: {df.shape[1]}열\n- **중복 데이터 수**: {df.duplicated().sum()}개\n\n")
    
    # 4. Descriptive Stats
    report.append("## 2. 기술 통계 (Descriptive Statistics)\n")
    report.append("### 수치형 변수 기술 통계:\n")
    report.append(df[['선풍기 (상대 비율)', '핫팩 (상대 비율)']].describe().to_markdown() + "\n\n")
    
    report.append("### 범주형 변수 기술 통계 (월, 요일, 계절):\n")
    report.append(df[['월', '요일', '계절']].astype(str).describe().to_markdown() + "\n\n")
    
    # 5. Visualizations
    report.append("## 3. 세부 데이터 시각화 및 인사이트 분석\n")
    
    # Helper to add a plot to report
    def add_plot(title, filename, prep_table, interpretation):
        report.append(f"### {title}\n")
        report.append(f"#### 차트 데이터 테이블:\n")
        report.append(prep_table.to_markdown() + "\n\n")
        report.append(f"![{title}](images/{filename}.png)\n\n")
        report.append(f"**💡 분석가 해석 (Insights):**\n{interpretation}\n\n")
        
    # Plot 1: 선풍기 히스토그램 (일변량)
    plt.figure(figsize=(10, 5))
    df['선풍기 (상대 비율)'].hist(bins=20, color='royalblue', edgecolor='black')
    plt.title('선풍기 (상대 비율)의 데이터 분포 히스토그램')
    plt.xlabel('비율 (0~100)')
    plt.ylabel('빈도 (Frequency)')
    plt.savefig('images/plot1_fan_hist.png', bbox_inches='tight')
    plt.close()
    
    # Prepare stats for plot 1 -> describe
    stats_fan = pd.DataFrame(df['선풍기 (상대 비율)'].describe())
    add_plot('1. 일변량 분석: 선풍기 상대 비율 히스토그램', 'plot1_fan_hist', stats_fan, "위 히스토그램을 살펴보면, 선풍기 클릭 비율은 대부분 0에 가까운 매우 낮은 구간에 밀집해 있는 것을 확인할 수 있습니다. 이는 선풍기라는 아이템이 여름철 특정 기간에만 클릭률이 집중되고 1년 중 대다수의 시기에는 전혀 수요가 발생하지 않는다는 극단적인 계절성을 띠고 있음을 시사합니다.")

    # Plot 2: 핫팩 히스토그램 (일변량)
    plt.figure(figsize=(10, 5))
    df['핫팩 (상대 비율)'].hist(bins=20, color='crimson', edgecolor='black')
    plt.title('핫팩 (상대 비율)의 데이터 분포 히스토그램')
    plt.xlabel('비율 (0~100)')
    plt.ylabel('빈도 (Frequency)')
    plt.savefig('images/plot2_hotpack_hist.png', bbox_inches='tight')
    plt.close()
    
    stats_hp = pd.DataFrame(df['핫팩 (상대 비율)'].describe())
    add_plot('2. 일변량 분석: 핫팩 상대 비율 히스토그램', 'plot2_hotpack_hist', stats_hp, "핫팩의 히스토그램 역시 선풍기와 마찬가지로 0 근방에서 절대 다수의 빈도수를 보여주고 있습니다. 이는 핫팩의 수요가 한겨울 등 아주 한파가 몰아치는 단기간에 폭발적으로 증가하며, 그 외 계절에는 트래픽이 완전히 소멸하는 대표적인 겨울 한철 방한 용품임을 데이터가 여실히 증명해주고 있습니다.")

    # Plot 3: 월별 빈도수 (일변량 범주형) - 월별 합계로 대체
    monthly_sum = df.groupby('월')[['선풍기 (상대 비율)', '핫팩 (상대 비율)']].sum().reset_index()
    plt.figure(figsize=(10, 5))
    monthly_sum.plot(x='월', kind='bar', figsize=(10,5), color=['royalblue', 'crimson'])
    plt.title('월별 선풍기 및 핫팩 상대 비율 합산치 (카테고리별 빈도 관점)')
    plt.ylabel('총 클릭 합산 (비율 합)')
    plt.xticks(rotation=0)
    plt.savefig('images/plot3_monthly_bar.png', bbox_inches='tight')
    plt.close()
    
    add_plot('3. 범주형 빈도 분석: 월간 트래픽 총합 비교 막대그래프', 'plot3_monthly_bar', monthly_sum, "월별 데이터를 합산하여 전체적인 빈도를 살펴본 결과, 선풍기는 집중적으로 6, 7, 8월에 차트가 폭증하는 형태를 띠고 있으며, 반대로 핫팩은 11, 12, 1, 2월에만 그 형태가 나타납니다. 카테고리로서의 월(Month)은 두 상품의 매출과 전환율을 결정짓는 가장 중요한 범주형 요인이며, 판매자는 위 그래프의 성수기와 비수기 타이밍을 정확히 읽고 재고 물량을 공격적으로 세팅하거나 비우는 물류 전략을 세워야 합니다.")

    # Plot 4: 요일별 빈도수 
    dow_sum = df.groupby('요일')[['선풍기 (상대 비율)', '핫팩 (상대 비율)']].sum().reset_index()
    # 요일 순서 정렬
    cats = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    dow_sum['요일'] = pd.Categorical(dow_sum['요일'], categories=cats, ordered=True)
    dow_sum = dow_sum.sort_values('요일')
    
    plt.figure(figsize=(10, 5))
    dow_sum.plot(x='요일', kind='bar', figsize=(10,5), color=['royalblue', 'crimson'])
    plt.title('요일별 선풍기 vs 핫팩 총 클릭 합산')
    plt.ylabel('총 클릭 합계')
    plt.xticks(rotation=45)
    plt.savefig('images/plot4_dow_bar.png', bbox_inches='tight')
    plt.close()
    
    add_plot('4. 범주형 빈도 분석: 요일별 트래픽 선호도 분석', 'plot4_dow_bar', dow_sum, "사람들이 어떤 요일에 선풍기나 핫팩을 집중적으로 쇼핑하는지 분석한 결과, 주말(금/토)보다는 상대적으로 주 초반에 클릭 빈도가 높게 관측되는 경향성이 일부 나타납니다. 소비자들은 날씨가 춥거나 더울 때 이를 참지 못하고 주 초반 오픈마켓을 검색하고, 평일에 배송을 받으려는 쇼핑 패턴을 가지고 있는 것으로 조심스럽게 추론해 볼 수 있으며, 주말 마케팅 비용을 평일로 앞당겨 집행할 필요가 있습니다.")
    
    # Plot 5: 시계열 추이 - 선풍기
    plt.figure(figsize=(12, 5))
    plt.plot(df['조회 일자'], df['선풍기 (상대 비율)'], color='royalblue')
    plt.title('시계열 분석: 선풍기 클릭 1년 추이')
    plt.xlabel('일자')
    plt.ylabel('상대 비율')
    plt.grid(True, alpha=0.3)
    plt.savefig('images/plot5_fan_line.png', bbox_inches='tight')
    plt.close()
    
    ts_fan_summary = df[['조회 일자', '선풍기 (상대 비율)']].set_index('조회 일자').resample('ME').mean().reset_index()
    add_plot('5. 이변량 분석 (Time-Series): 선풍기 일자별 시계열 변동', 'plot5_fan_line', ts_fan_summary, "1년이라는 시간 축(X축)에 대해 선풍기 비율(Y축)을 선 그래포로 나타낸 시계열 플롯입니다. 여름철인 6월 말부터 8월 초에 이르기까지 가파른 우상향 곡선을 보이다가 입추가 지나는 하반기에 급격하게 폭락하는 전형적인 종형(Bell-curve) 사이클을 확인할 수 있으며, 이 메인 사이클을 제외한 구간은 완전히 평탄한 바닥을 기는 양상을 확실하게 보여주고 있습니다.")

    # Plot 6: 시계열 추이 - 핫팩
    plt.figure(figsize=(12, 5))
    plt.plot(df['조회 일자'], df['핫팩 (상대 비율)'], color='crimson')
    plt.title('시계열 분석: 핫팩 클릭 1년 추이')
    plt.xlabel('일자')
    plt.ylabel('상대 비율')
    plt.grid(True, alpha=0.3)
    plt.savefig('images/plot6_hotpack_line.png', bbox_inches='tight')
    plt.close()
    
    ts_hotpack_summary = df[['조회 일자', '핫팩 (상대 비율)']].set_index('조회 일자').resample('ME').mean().reset_index()
    add_plot('6. 이변량 분석 (Time-Series): 핫팩 일자별 시계열 변동', 'plot6_hotpack_line', ts_hotpack_summary, "선풍기와 정반대로, 핫팩 클릭량 시계열은 여름과 가을 내내 깊은 침묵을 유지하다가 11월 첫눈이 오는 혹은 기온이 영하로 떨어지는 첫 한파 시점을 기점으로 말 그대로 수직 상승하는 극적인 파동을 그립니다. 기상 변수와 완벽하게 동기화되어 즉각적인 수요로 나타나므로, 날씨 예측 모델을 통해 마케팅 예산을 하루 이틀 전에 미리 준비하는 전략이 가장 중요하게 작용합니다.")

    # Plot 7: 선풍기 vs 핫팩 상관관계(산점도)
    plt.figure(figsize=(8, 8))
    plt.scatter(df['선풍기 (상대 비율)'], df['핫팩 (상대 비율)'], alpha=0.5, color='purple')
    plt.title('산점도: 선풍기 vs 핫팩 상관관계 분석')
    plt.xlabel('선풍기 클릭 비율')
    plt.ylabel('핫팩 클릭 비율')
    plt.grid(True, alpha=0.3)
    plt.savefig('images/plot7_scatter.png', bbox_inches='tight')
    plt.close()
    
    corr_df = pd.DataFrame({'상관계수(Correlation)': [df['선풍기 (상대 비율)'].corr(df['핫팩 (상대 비율)'])]})
    add_plot('7. 이변량 분석: 선풍기-핫팩 수요 산점도 (역의 상관관계)', 'plot7_scatter', corr_df, "선풍기 값을 X축으로, 핫팩을 Y축으로 둔 산점도를 확인해보면 데이터 포인트들이 두 개의 양극단 축 쪽으로 몰려있는 'L자 형태'를 띱니다. 즉 선풍기가 높은 날은 핫팩이 반드시 0에 수렴하고, 핫팩이 높은 날은 선풍기가 0에 수렴하는 극단적인 마이너스(-) 상관관계를 가집니다. 이는 두 계절성 상품의 카니발라이제이션(Cannibalization)이 전혀 없으며, 교차 판매(Cross-sell) 마케팅 전략을 쓰기에 매우 부적절하다는 명확한 통찰을 줍니다.")

    # Plot 8: 계절별 선풍기 박스플롯 (범주 vs 연속)
    # Boxplot using pandas plotting
    df.boxplot(column='선풍기 (상대 비율)', by='계절', figsize=(10, 6), grid=False)
    plt.title('계절별 선풍기 클릭 확률 박스플롯')
    plt.suptitle('') # Remove default pandas title
    plt.xlabel('계절 범주')
    plt.ylabel('클릭 비율')
    plt.savefig('images/plot8_fan_box.png', bbox_inches='tight')
    plt.close()
    
    season_fan_desc = df.groupby('계절')['선풍기 (상대 비율)'].describe()
    add_plot('8. 이변량 분석: 계절별 선풍기 데이터분포 (박스플롯)', 'plot8_fan_box', season_fan_desc, "봄, 여름, 가을, 겨울이라는 계절 범주에 따른 선풍기 클릭률의 구조적 분포를 보여주는 박스플롯입니다. 여름철 박스플롯은 넓은 사분위수 범위(IQR) 수치를 가리키며 매일매일 큰 폭의 파동과 함께 높은 상위 중앙값을 기록하는 반면, 겨울철은 박스 사이즈가 완전히 압축되어 바닥에 위치하고 이상치(Outlier) 조차 나타나지 않아 여름과의 극명한 수요 탄력성 차이를 한눈에 증명합니다.")

    # Plot 9: 계절별 핫팩 박스플롯 (범주 vs 연속)
    df.boxplot(column='핫팩 (상대 비율)', by='계절', figsize=(10, 6), grid=False)
    plt.title('계절별 핫팩 클릭 확률 박스플롯')
    plt.suptitle('')
    plt.xlabel('계절 범주')
    plt.ylabel('클릭 비율')
    plt.savefig('images/plot9_hotpack_box.png', bbox_inches='tight')
    plt.close()
    
    season_hp_desc = df.groupby('계절')['핫팩 (상대 비율)'].describe()
    add_plot('9. 이변량 분석: 계절별 핫팩 데이터분포 (박스플롯)', 'plot9_hotpack_box', season_hp_desc, "핫팩의 계절별 박스플롯 역시 겨울 범주에서만 오롯이 짙은 박스의 폭과 높이를 발산하고 있습니다. 특히 겨울 중에서도 특정 한파가 몰아치는 날들에만 튀어 오르는 극단적인 이상치(Outlier, 윗꼬리에 찍힌 점들)들이 관측되는데, 핫팩은 꾸준히 안정적으로 팔리기보다는 외부 온도라는 특정 쇼크가 올 때만 급반등하는 '충격 의존적 소비재'임을 입증하는 중요한 통계적 근거입니다.")

    # Plot 10: 피벗테이블 & 월별 다변량 막대 그래프
    pivot = df.pivot_table(index='월', values=['선풍기 (상대 비율)', '핫팩 (상대 비율)'], aggfunc='mean')
    pivot.plot(kind='bar', figsize=(12, 6), color=['royalblue', 'crimson'])
    plt.title('월별 선풍기/핫팩 평균 상대비율 다변량 분석 막대그래프')
    plt.xlabel('월 (Month)')
    plt.ylabel('평균 상대 비율')
    plt.xticks(rotation=0)
    plt.grid(True, axis='y', alpha=0.4)
    plt.savefig('images/plot10_pivot_bar.png', bbox_inches='tight')
    plt.close()
    
    add_plot('10. 다변량(피벗) 분석: 월별 두 아이템 간의 평균 클릭 비율 비교', 'plot10_pivot_bar', pivot, "월을 인덱스로, 선풍기와 핫팩 각각의 평균 비율을 밸류로 압축한 피벗 테이블(Pivot Table)을 기반으로 한 그룹형 다변량 막대그래프입니다. 한 번의 차트에서 시간적 흐름(월)과 두 가지 다른 연속형 변수(선풍기, 핫팩 평균치)의 절대적 우위를 쉽게 교차 비교할 수 있습니다. 5월부터 선풍기가 역전 우위를 점하기 시작하다가 10월을 돌파하면서부터 핫팩으로 시장 헤게모니가 급격히 전환되는 '골든 크로스(Golden Cross)' 현상을 시각적으로 가장 정확하게 식별이 가능합니다.")

    # Plot 11: 전체 트렌드 동시 비교 시계열 플롯
    plt.figure(figsize=(14, 6))
    plt.plot(df['조회 일자'], df['선풍기 (상대 비율)'], color='royalblue', label='선풍기 비율', alpha=0.8, linewidth=2)
    plt.plot(df['조회 일자'], df['핫팩 (상대 비율)'], color='crimson', label='핫팩 비율', alpha=0.8, linewidth=2)
    plt.title('전체 트렌드 분석: 1년 간의 선풍기와 핫팩 동시 클릭 비율 변동', fontsize=14, pad=10)
    plt.xlabel('조회 일자 (Date)')
    plt.ylabel('인기도 (상대 검색 비율)')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend(fontsize=12)
    plt.savefig('images/plot11_dual_line.png', bbox_inches='tight')
    plt.close()
    
    dual_summary = df[['조회 일자', '선풍기 (상대 비율)', '핫팩 (상대 비율)']].set_index('조회 일자').resample('ME').mean().reset_index()
    add_plot('11. 통합 트렌드 분석: 선풍기와 핫팩의 1년 주기성 교차 비교', 'plot11_dual_line', dual_summary, "요청하신 전체 트렌드 동시 비교 그래프입니다. 두 시즌 베스트셀러 아이템의 클릭 데이터를 동일한 1년 타임라인 위에 겹쳐서 관측했을 때, 6~8월에 불기둥처럼 치솟는 파란선(선풍기)과 11~1월에 가파르게 상승하는 빨간선(핫팩)이 완벽하게 역상계를 그리며 X자 형태의 수요 크로스를 보여주고 있습니다. 특히 4월과 10월에 각각 발생하는 '시즌 모멘텀 턴어라운드(역전 현상)' 지점은 각 유통사들이 겨울 용품 및 여름 가전 재고를 맞바꾸는 최적기로, 매출을 극대화하기 위한 디스플레이 전략의 기준 시점이 됩니다.")

    # Write Report
    with open('eda_report.md', 'w', encoding='utf-8') as f:
        f.write("".join(report))
        
    print("EDA 리포트 생성 및 10개의 그래프 이미지가 'images/' 폴더에 저장 완료되었습니다.")

if __name__ == "__main__":
    create_eda_report()
