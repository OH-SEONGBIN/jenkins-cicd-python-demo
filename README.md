# ⚙️ Jenkins CI/CD 실습 프로젝트: Python 자동 테스트 파이프라인 구축

> Jenkins를 활용하여 GitHub에 Push된 Python 코드를 자동으로 Clone → 테스트 → 배포하는  
CI/CD 파이프라인을 구성한 실습 프로젝트입니다.

---

## 🧠 개요 (Overview)

이 프로젝트는 Jenkins를 이용해 Python 코드의 자동화된 테스트 및 빌드 환경을 구축하는 것을 목표로 합니다.  
GitHub 저장소와 Jenkins를 연동하여, 커밋/푸시 시 자동으로 CI 파이프라인이 동작하도록 구성했습니다.

> `Jenkinsfile`에 정의된 단계는 다음과 같습니다:
- 소스 코드 클론
- 의존성 설치 (`pip install`)
- 테스트 실행 (`pytest`)
- 결과 출력

---

## 🎯 실습 목표 (Objective)

- Jenkins + GitHub + Python 환경에서 CI/CD 흐름을 실습
- Jenkinsfile을 직접 작성하여 파이프라인 구성 경험
- Python 테스트 자동화 흐름 및 오류 해결 능력 향상
