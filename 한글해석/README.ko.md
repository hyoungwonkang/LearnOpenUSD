# Learn OpenUSD

[![라이선스](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

[Learn OpenUSD](https://docs.nvidia.com/learn-openusd/latest/index.html)는 개발자가 OpenUSD Development Certification을 준비할 수 있도록 구성된 전체 학습 과정입니다. 이 오픈 소스 저장소는 누구나 더 나은 학습 경험을 만드는 데 기여할 수 있도록 공개되어 있으며, 교사와 강사도 콘텐츠를 가져와 자신의 학습 대상에 맞게 활용할 수 있습니다.

학습 콘텐츠만 이용하려면 빌드된 [Learn OpenUSD 웹사이트](https://docs.nvidia.com/learn-openusd/latest/index.html)를 방문하세요.

## 환경 구성

### uv

이 저장소는 의존성 관리를 위해 [uv](https://docs.astral.sh/uv/)를 사용합니다. uv가 처음이더라도 자세한 사용법을 모두 알 필요는 없으며, [빌드 방법](#문서-빌드-방법)에 나온 명령어만 사용하면 됩니다. 먼저 [uv를 설치](https://docs.astral.sh/uv/getting-started/installation/)하는 것을 권장합니다.

### Git LFS

이 저장소는 이미지, 동영상 및 USD 콘텐츠를 저장하기 위해 Git Large File Storage를 사용합니다. 저장소를 원활하게 이용하려면 복제하기 전에 Git LFS가 설치되어 있는지 확인하세요.

**설치:**

*(컴퓨터마다 한 번만 실행하면 됩니다.)*

```bash
git lfs install
```

Git LFS를 설치하기 전에 이 저장소를 복제했다면 모든 LFS 파일을 내려받아 저장소를 올바르게 구성할 수 있습니다.

**LFS 파일 다운로드:**

*(이 저장소에서 한 번만 실행하면 됩니다.)*

```bash
git lfs pull
```

## 문서 빌드 방법

1. `uv run sphinx-build -M html docs/ docs/_build/`

### 빌드 시스템 세부 정보

빌드는 다음 순서로 진행됩니다.

1. MyST-NB가 Python 코드 셀을 실행합니다.
2. Sphinx가 지시문과 상호 참조를 처리합니다.
3. 사용자 정의 확장이 에셋을 복사하고 실습용 ZIP 파일을 생성합니다.
4. 대화형 그래프에 사용할 용어집을 추출합니다.
5. 사용자 정의 테마를 적용한 HTML을 생성합니다.

## 문서 미리보기 방법

1. `uv run python -m http.server 8000 -d docs/_build/html/`
2. 웹 브라우저에서 `http://localhost:8000`을 엽니다.

## Notebook 실행 방법

1. `rm -rf docs/_build/`
2. 위의 [문서 빌드 방법](#문서-빌드-방법)을 실행합니다.
3. `uv run launch_notebooks`

## 새로운 예제나 콘텐츠에 대한 아이디어가 있나요?

다른 개발자에게 도움이 될 수 있는 새로운 콘텐츠 아이디어는 언제나 환영합니다. 원하는 콘텐츠의 종류를 설명하는 [새 이슈](https://github.com/NVIDIA-Omniverse/LearnOpenUSD/issues)를 만들고 제목 끝에 `[New Request]`를 붙여 주세요. NVIDIA 팀이나 OpenUSD 커뮤니티 구성원이 해당 요청을 검토할 것입니다. 직접 기여해 주셔도 좋습니다!

## 오타나 오류를 발견했나요?

잘못된 내용이나 작동하지 않는 예제 또는 실습을 발견하면 알려 주세요. 버그임을 명시하여 [이슈를 등록](https://github.com/NVIDIA-Omniverse/LearnOpenUSD/issues)해 주세요.

## 기여하기

누구나 이 프로젝트에 기여할 수 있습니다. 기여하려면 먼저 [기여 가이드](./CONTRIBUTING.md)를 읽고 기여 절차를 확인해 주세요.
