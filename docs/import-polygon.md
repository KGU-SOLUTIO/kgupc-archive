# Polygon에서 종료된 대회 지문 가져오기

변환 코드는 kgupc-pol2dom에, 템플릿과 렌더러는 kgupc-toolkit에 있습니다. 아카이브는 가져온 공개 지문과 PDF를 보관합니다.

1. kgupc-pol2dom 환경에 toolkit `v1.0.0`과 pol2dom을 설치합니다. 대회의 `toolkit.lock.json`과 설치 내용이 일치해야 합니다.
2. Polygon Settings에서 API 키를 발급해 로컬 환경변수 또는 kgupc-pol2dom의 Git에서 제외된 `.env`에 `POLYGON_API_KEY`, `POLYGON_API_SECRET`을 설정합니다. 필요한 경우 `POLYGON_PIN`을 설정합니다. 인증 정보를 Git이나 채팅에 넣지 않습니다.
3. `.env`에 `POLYGON_CONTEST_URL`도 설정하고 `polygon-list`로 대상 대회와 문제 목록을 확인합니다. 종료된 2025는 [확인된 대응표](../2025/polygon-import.json)를 사용할 수 있습니다. 아카이브 반영에는 명시적인 `contestId`가 필요하며, `.env`의 대회와 다르면 중단합니다.
4. Polygon의 지문이 대회 최종본인지 확인하고 커밋한 뒤, 원하는 문제만 가져옵니다.

API 키 위치는 Polygon에 로그인한 뒤 Settings의 API Key 항목입니다. [공식 API 인증 안내](https://codeforces.github.io/polygon-misc/API#authorization)를 참고하세요. pol2dom 루트에서 실행하면 그 폴더의 `.env`를 자동으로 읽습니다. 다른 폴더에서 실행할 때는 `--env-file`로 경로를 지정할 수 있습니다. Windows 사용자 변수를 쓸 경우 시작 메뉴의 **계정의 환경 변수 편집 → 사용자 변수 → 새로 만들기**에서 값을 저장하면 됩니다. 특정 터미널의 `$env:`에만 설정하면 그 터미널에서 실행한 CLI에만 적용됩니다.

아래는 **kgupc-pol2dom 루트**에서 실행합니다. 경로는 실제 로컬 위치로 바꾸세요.

```powershell
.venv/Scripts/python -m kgupc_pol2dom polygon-list
.venv/Scripts/python -m kgupc_pol2dom archive-import ../../KGU-SOLUTIO/kgupc-archive/2025/polygon-import.json --contest ../../KGU-SOLUTIO/kgupc-archive/2025 --letters B C D E F G --replace --render
```

이 명령은 A를 보존하고, B~G를 A와 동일한 분리 지문 구조로 만들고, 문제 목록과 통합/개별 PDF를 갱신합니다. B의 기존 틀은 `2025/build/polygon-backups/`에 백업한 뒤 교체합니다. 지문 변경은 Polygon에서 하고 이 명령으로 다시 가져오는 것을 권장합니다.

준비 중인 신규 대회는 `.env`에 해당 대회 URL을 설정한 뒤 `prepare --render`로 생성합니다. 기본 출력은 사용자 홈의 `kgupc-work/contest-<ID>/`이며 문제 번호와 ID 대응표도 자동으로 생성합니다. `--output`으로 경로를 바꿀 수 있지만 모든 Git 작업 트리 내부 경로는 거부합니다. 지문 수정 후 `prepare --replace --render`로 갱신합니다. 아카이브는 대회가 종료되고 공개해도 되는 자료만 별도 `archive-import` 명령으로 반영합니다. 명령 자체가 대회 종료 여부를 판단하지 않으므로 운영진의 확인이 필요합니다.

`polygon-source.json`은 문제 ID와 revision, 가져온 시각을 기록합니다. API는 현재 작업 사본을 읽으므로 이 방식으로 임의의 과거 revision을 지정할 수는 없습니다. 과거 최종본과 Polygon 현재 지문이 다르면 먼저 최종본을 확보해야 합니다. 생성 정답이 없거나 한글 지문이 없거나 가져오는 동안 revision이 바뀌면 실패합니다. 미커밋 변경 허용 옵션 `--working-copy`는 준비 중인 로컬 대회용입니다.

전체 테스트·채점기와 DOMjudge 업로드는 이 단계에 포함하지 않습니다. 종료된 대회의 공개 지문·리소스·예제·PDF만 검토해 커밋합니다. 유지할 문제까지 포함해 임시 폴더에서 통합/개별 PDF를 완성한 뒤 반영하므로 다운로드나 PDF 빌드 실패 시 기존 문제는 보존됩니다. PDF 뷰어가 결과물 교체를 막으면 반영된 지문과 백업은 남으므로 뷰어를 닫고 다시 가져오거나 빌드하세요.
