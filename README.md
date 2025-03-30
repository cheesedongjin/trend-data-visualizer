# 📰 trend-data-visualizer

**한국 주요 뉴스 웹사이트의 실시간 트렌드 키워드를 시각화하는 GUI 애플리케이션입니다.**  
웹사이트로부터 뉴스 본문을 크롤링하고, 형태소 분석을 통해 명사를 추출한 뒤 빈도수를 계산하여 키워드 그래프를 생성합니다.

## 📌 주요 기능

- 네이버뉴스, 조선일보, 다음뉴스, 연합뉴스, KBS에서 뉴스 데이터 수집
- 형태소 분석기를 사용한 명사 추출 및 불용어 제거
- 캐시 기능으로 중복 크롤링 방지
- 웹사이트별 키워드 빈도 비교 시각화 (Stacked Bar Chart)
- Tkinter 기반 GUI 제공, 사이트별 키워드 필터링 체크박스 지원

## ⚙️ 설치 및 실행 방법

### 1. 필수 패키지 설치

Python 3.8 이상이 필요합니다. 아래 패키지를 설치해 주세요:

```bash
pip install requests beautifulsoup4 konlpy matplotlib
```

> `konlpy`는 Java 기반이며, 실행을 위해 Java 설치가 필요할 수 있습니다.  
> Windows에서는 JDK 설치 및 환경변수 설정이 필요할 수 있습니다.

### 2. 불용어 파일 준비

`stopwords.txt` 파일은 이미 저장소에 포함되어 있습니다. 한 줄에 하나씩 불용어가 저장되어 있습니다.

### 3. 실행

```bash
python main.py
```

> `main.py`는 실제 코드가 작성된 Python 파일의 이름으로 바꿔주세요.

## 🗂️ 디렉토리 구조

```
trend-data-visualizer/
├── main.py
├── stopwords.txt
└── cache/
    └── YYYY-MM-DD_site_freq.json  # 자동 생성되는 캐시 파일
```

## 📝 폰트 설정

Windows에서는 기본적으로 `Malgun Gothic` 폰트를 사용합니다.

```python
font_path = "C:/Windows/Fonts/malgun.ttf"
```

운영체제에 따라 폰트 경로가 다를 수 있으니, 필요 시 수정하세요.

## 📅 캐시 기능

- 매일 사이트별 키워드 빈도를 캐시에 저장합니다.
- 다음 실행 시 같은 날짜의 캐시가 있으면 크롤링 없이 이를 사용합니다.
- 오래된 캐시는 자동으로 삭제됩니다.

## 📌 참고

- 웹사이트 구조 변경 시 크롤링이 실패할 수 있습니다.
- 사이트별 정확한 뉴스 데이터 추출을 원한다면 각 사이트의 RSS 또는 공식 API 사용을 고려하세요.

## 📜 라이선스

MIT License

