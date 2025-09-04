# ⚙️ Jenkins CI/CD 실습 프로젝트: Python 자동 테스트 파이프라인 구축

> Jenkins를 활용하여 GitHub에 Push된 Python 코드를 자동으로 Clone → Lint/테스트/커버리지 측정 → CI 지표 산출(CSV) 까지 수행하는 실습 프로젝트입니다.

---

## 🧠 개요 (Overview)

이 프로젝트는 Jenkins를 이용해 자동화된 테스트 및 빌드 환경을 구성하고,
재현 가능한 수치 지표(테스트 통과율, 커버리지, 실행시간, Lint 경고 수)를 남기도록 개선했습니다.
GitHub 저장소와 Jenkins를 연동하여, 커밋/푸시 시 자동으로 CI 파이프라인이 동작합니다.

> `Jenkinsfile`에 정의된 단계는 다음과 같습니다:
- 소스 코드 클론
- 의존성 설치 (pip install -r requirements.txt)
- 정적 분석 (flake8)
- 단위 테스트 + 커버리지 (pytest --cov …)
- CI 지표 산출 (tools/ci_metrics.py → metrics/ci_metrics.csv 저장)
- (옵션) 병렬 테스트(xdist) 비교 측정

---

## 🎯 실습 목표 (Objective)

- Jenkins × GitHub × Python으로 CI 흐름을 실습하고, PR마다 재현 가능한 수치를 남긴다.
- Jenkinsfile을 직접 작성/개선하여 파이프라인 구성 경험을 쌓는다.
- pytest/coverage/flake8을 통해 품질·속도 지표를 정량화한다.

---

🛠️ 이번 커밋에서 개선된 점 (What’s improved)
- flake8, pytest, pytest-cov, (옵션) pytest-xdist 도입
- CI 메트릭스 스크립트 추가: tools/ci_metrics.py
  → metrics/ci_metrics.csv에 핵심 지표 저장(아래 참조)
- **재현 명령어/리포트 산출** 표준화: reports/(junit/cov/flake8) + metrics/(csv)
- 예시 수치(로컬 측정):
  - junit_time_sec: 2.92s → 2.15s (약 -26%)
  - pass_ratio: 100%
  - coverage_pct: 100% 유지
  - lint_count: 8 → 8 (예시, 규칙 강화 시 감소 목표)
> 수치는 환경에 따라 달라질 수 있으므로, 재현 커맨드를 그대로 실행하면 동일 포맷의 CSV가 생성됩니다.

--- 

📁 폴더 구조 (Structure)

```text

jenkins-cicd-python-demo/
├── src/
│   └── hello.py                # 실습용 모듈 (add 함수 등)
├── tests/
│   ├── test_hello.py           # 단위 테스트
│   └── test_perf.py            # 간단 성능/회귀 테스트(예시)
├── tools/
│   └── ci_metrics.py           # JUnit/Coverage/Flake8 → CSV로 요약
├── reports/                    # junit_xxx.xml, cov_xxx.xml, flake8.txt (gitignore)
├── metrics/
│   └── ci_metrics.csv          # 핵심 지표 CSV 결과
├── requirements.txt
├── pytest.ini                  # pytest 기본 옵션(있다면)
├── .flake8                     # lint 규칙(있다면)
├── Jenkinsfile                 # Jenkins Pipeline 정의
├── .gitignore
└── README.md

```

---

▶️ 로컬 재현 방법 (How to reproduce locally)
> Windows Git Bash / macOS / Linux 공통 예시

1. 가상환경 & 의존성

```text
python -m venv .venv && source .venv/Scripts/activate 2>/dev/null || source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt
```

2. Lint 결과 저장

```text
mkdir -p reports metrics
flake8 src tests | tee reports/flake8.txt || true
```

3. 기준(run=단일): JUnit + Coverage 생성

```text
export PYTHONPATH=src
pytest -n 0 \
  --junitxml=reports/junit_base.xml \
  --cov=src --cov-report=xml:reports/cov_base.xml --cov-report=term
```

4. CSV 지표 산출

```text
python tools/ci_metrics.py \
  --junit reports/junit_base.xml \
  --cov   reports/cov_base.xml \
  --flake reports/flake8.txt \
  --out   metrics/ci_metrics.csv
```

5. (옵션) 병렬 테스트 비교: xdist 사용

```text
export PYTHONPATH=src
pytest -n auto \
  --junitxml=reports/junit_xdist.xml \
  --cov=src --cov-report=xml:reports/cov_xdist.xml --cov-report=term

python tools/ci_metrics.py \
  --junit reports/junit_xdist.xml \
  --cov   reports/cov_xdist.xml \
  --flake reports/flake8.txt \
  --out   metrics/ci_metrics.csv
```

---

📊 CI 지표 스키마 (metrics/ci_metrics.csv)
헤더 예시:
```sql
commit,tests,passed,failures,errors,skipped,pass_ratio,junit_time_sec,coverage_pct,lint_count
```
샘플(예시):
```text
7,7,0,0,0,100.0,2.15,100.0,8
```
- pass_ratio(%): 테스트 성공률
- junit_time_sec: 총 테스트 시간(초)
- coverage_pct(%): 커버리지
- lint_count: flake8 경고/에러 건수(간단 집계)
> PR 본문에 “2.92s → 2.15s(-26%), Cov 100% 유지, Pass 100%” 처럼 전/후 비교 수치를 붙이면 평가자에게 강한 인상을 줍니다.

---

🧩 Jenkinsfile 요약
- agent (예시): Docker 이미지 기반 python 환경
- stages:
  1. Checkout: GitHub에서 소스 체크아웃
  2. Install: pip install -r requirements.txt
  3. Lint: flake8 → reports/flake8.txt
  4. Test: pytest + --cov → reports/junit_*.xml, reports/cov_*.xml
  5. Metrics: tools/ci_metrics.py → metrics/ci_metrics.csv
  6. (옵션) Archive/Publish: CSV/리포트 보관 또는 배지/대시보드 연동

---

🚑 트러블슈팅
- 리포트가 비어있을 때: reports/ 경로를 Jenkins 작업 디렉터리 기준으로 확인
- 커버리지 0%: export PYTHONPATH=src 누락 여부 확인
- flake8 오류로 실패: --exit-zero로 완화 후 점진 개선 가능

---

📌 라이선스

본 예제는 학습·실습 용도입니다. 상용/배포 시 보안·품질 정책에 맞게 보완하세요.

---

👤 Maintainer

- 오성빈 (OH-SEONGBIN)
- 이슈/리뷰/제안은 GitHub Issues로 남겨주세요.

---
