import requests
from bs4 import BeautifulSoup
from konlpy.tag import Okt
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.font_manager as fm
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
import json
from datetime import datetime, date

# 한글 폰트 설정
font_path = "C:/Windows/Fonts/malgun.ttf"  # Windows의 경우 Malgun Gothic 사용 (경로 확인 필요)
font_name = fm.FontProperties(fname=font_path).get_name()
plt.rc('font', family=font_name)
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지

# 캐시 폴더 설정
CACHE_DIR = "cache"
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

# 웹사이트 URL과 이름 설정
websites = [
    {"name": "네이버뉴스", "url": "https://news.naver.com/"},
    {"name": "조선일보", "url": "https://www.chosun.com/"},
    {"name": "다음뉴스", "url": "https://news.daum.net/"},
    {"name": "연합뉴스", "url": "https://www.yna.co.kr/"},
    {"name": "KBS", "url": "https://news.kbs.co.kr/news/pc/main/main.html"},
]

site_colors = {
    "네이버뉴스": "#03C75A",
    "조선일보": "#C8102E",
    "다음뉴스": "#FFB800",
    "연합뉴스": "#005BAC",
    "KBS": "#6A8DFF",
}


def load_stopwords(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            stopwords = set(line.strip() for line in f if line.strip())
        return stopwords
    except FileNotFoundError:
        print(f"불용어 파일 {file_path}을 찾을 수 없습니다. 기본 불용어 없이 진행합니다.")
        return set()


def get_text_from_url(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')

        return soup.get_text(separator=' ', strip=True)
    except Exception as e:
        print(f"URL {url} 크롤링 중 오류 발생: {e}")
        return ""


def clean_cache():
    today = date.today().isoformat()
    for filename in os.listdir(CACHE_DIR):
        file_path = os.path.join(CACHE_DIR, filename)
        if os.path.isfile(file_path):
            file_date = filename.split('_')[0]
            if file_date != today:
                os.remove(file_path)
                print(f"오래된 캐시 삭제: {filename}")


def load_cache():
    today = date.today().isoformat()
    cache_file = os.path.join(CACHE_DIR, f"{today}_site_freq.json")
    if os.path.exists(cache_file):
        with open(cache_file, 'r', encoding='utf-8') as f:
            print(f"오늘의 캐시 로드: {cache_file}")
            return json.load(f)
    return None


def save_cache(site_freq):
    today = date.today().isoformat()
    cache_file = os.path.join(CACHE_DIR, f"{today}_site_freq.json")
    with open(cache_file, 'w', encoding='utf-8') as f:
        json.dump(site_freq, f, ensure_ascii=False)
    print(f"캐시 저장: {cache_file}")


# 캐시 정리
clean_cache()

# 캐시 로드 시도
site_freq = load_cache()

if site_freq is None:
    # Okt 객체 생성 및 데이터 크롤링
    okt = Okt()
    stopwords = load_stopwords('stopwords.txt')
    site_freq = {}

    for site in websites:
        print(f"{site['name']} 크롤링 중...")
        text = get_text_from_url(site["url"])
        nouns = okt.nouns(text)
        nouns = [word for word in nouns if len(word) > 1 and word not in stopwords]
        freq = Counter(nouns)
        site_freq[site["name"]] = dict(freq)

    # 캐시 저장
    save_cache(site_freq)
else:
    site_freq = {site: Counter(freq) for site, freq in site_freq.items()}

# 모든 웹사이트에서 등장한 단어들의 집합 생성
all_words = set()
for freq in site_freq.values():
    all_words.update(freq.keys())

# Tkinter GUI 설정
root = tk.Tk()
root.title("웹사이트별 한국 트렌드 분석")

# 체크박스 변수 설정 (기본적으로 모두 체크됨)
checkbox_vars = {site["name"]: tk.BooleanVar(value=True) for site in websites}


# 그래프 업데이트 함수
def update_plot():
    ax.clear()

    # 선택된 웹사이트만 추출
    selected_sites = [site["name"] for site in websites if checkbox_vars[site["name"]].get()]
    if not selected_sites:
        ax.text(0.5, 0.5, "웹사이트를 선택하세요", ha='center', va='center', fontsize=16)
        ax.set_axis_off()
        canvas.draw()
        return

    # 선택된 웹사이트의 데이터로 combined_counts 재계산
    combined_counts = {}
    for word in all_words:
        combined_counts[word] = {site["name"]: site_freq[site["name"]].get(word, 0) for site in websites if
                                 checkbox_vars[site["name"]].get()}

    # 상위 N개 단어 재계산
    N = 10
    word_total_freq = {word: sum(counts.values()) for word, counts in combined_counts.items()}
    top_words = sorted(word_total_freq.items(), key=lambda x: x[1], reverse=True)[:N]
    top_words = [word for word, total in top_words]

    # 그래프 데이터 준비
    x = np.arange(len(top_words))
    width = 0.6
    bottom = np.zeros(len(top_words))

    for site in websites:
        site_name = site["name"]
        if checkbox_vars[site_name].get():
            counts = [combined_counts[word][site_name] for word in top_words]
            ax.bar(x, counts, width, bottom=bottom, label=site_name, color=site_colors[site_name])
            bottom += np.array(counts)

    ax.set_xlabel("키워드", fontsize=14)
    ax.set_ylabel("빈도", fontsize=14)
    ax.set_title("웹사이트별 한국 트렌드 분석", fontsize=16)
    ax.set_xticks(x)
    ax.set_xticklabels(top_words, rotation=45, fontsize=12)
    ax.tick_params(axis='y', labelsize=12)
    ax.legend(fontsize=12)
    canvas.draw()


# 체크박스 프레임
checkbox_frame = tk.Frame(root)
checkbox_frame.pack(side=tk.LEFT, padx=10, pady=10)

# 체크박스 생성
for site in websites:
    cb = tk.Checkbutton(
        checkbox_frame,
        text=site["name"],
        variable=checkbox_vars[site["name"]],
        command=update_plot,
        font=("Malgun Gothic", 18)
    )
    cb.pack(anchor=tk.W)

# 초기 그래프 생성
fig, ax = plt.subplots(figsize=(15, 8))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)
update_plot()

# Tkinter 메인 루프 실행
root.mainloop()
