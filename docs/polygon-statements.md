# Polygon 지문과 KGUPC PDF

문제 본문은 Polygon의 지문 필드에 맞춰 분리합니다. toolkit이 제목, 제한, 절 제목과 예제 상자를 조합하고, pol2dom은 Polygon에서 가져온 데이터를 이 구조로 내보냅니다. 구조를 맞췄다고 자동으로 Polygon과 동기화되는 것은 아닙니다. 인증·다운로드와 DOMjudge 업로드는 다음 구현 단계입니다.

## 현재 문제 구조

```text
2025/problems/A/
  kgu-solutio-kgu-ai-cse.tex      # 조립 지시 한 줄, 개별 PDF 이름 유지
  kgu-solutio-kgu-ai-cse.pdf
  statement.json                # toolkit의 메타데이터 형식
  statement-sections/korean/
    name.tex                    # 제목만, TeX 특수문자는 이스케이프
    legend.tex                  # 본문·그림
    input.tex                   # 입력 형식
    output.tex                  # 출력 형식
    notes.tex                   # 예제 뒤 설명; 빈 파일이면 제목도 생략
    example.01                  # 예제 1 표시용 입력, 일반 텍스트
    example.01.a                # 예제 1 표시용 출력, 일반 텍스트
    example.02
    example.02.a
    SOLUTIO 로고.png
```

`statement.json`은 Polygon의 공식 파일이 아니라 toolkit에서 사용하는 메타데이터입니다. `timeLimit`은 Polygon API와 동일하게 밀리초, `memoryLimit`은 MB입니다. `language`는 지문 폴더와 일치해야 합니다. `sampleLayout`은 `auto`, `paired`, `stacked` 중 하나이며 기본값은 `auto`입니다.

```json
{
  "language": "korean",
  "timeLimit": 1000,
  "memoryLimit": 256,
  "inputFile": "stdin",
  "outputFile": "stdout",
  "interactive": false,
  "sampleLayout": "auto"
}
```

`timeLimit: 1000`은 `1초`로 표시됩니다. 제한이 미정이면 `null`로 둡니다. 입력·출력 파일명과 interactive 정보는 Polygon 데이터를 보존하기 위한 값이며 현재 예제 제목은 `예제 입력 N` / `예제 출력 N`으로 통일합니다. 인터랙티브 문제는 `interaction.tex`도 필요합니다.

원본 조립 파일은 다음처럼 유지합니다.

```tex
% !TeX root = ../main.tex
\polygonstatement{A}{statement-sections/korean}
```

본문 파일에는 `\problemheader`, `\InputSection`, `\SampleSection`, `minipage` 같은 KGUPC 레이아웃 명령을 넣지 않습니다. 필요한 절 제목은 렌더러가 붙입니다. 추가 `scoring.tex`는 배점, `interaction.tex`는 인터랙션으로 표시합니다. `tutorial.tex`는 풀이이므로 문제 PDF에 포함하지 않습니다. statement `notes`와 Polygon 문제 관리용 `note`도 서로 다릅니다.

## 예제에 영향을 주는 Polygon 요소

공식 [Statement](https://codeforces.github.io/polygon-misc/API#statement), [Test](https://codeforces.github.io/polygon-misc/API#test), [saveTest](https://codeforces.github.io/polygon-misc/API#problemsavetest) 문서를 기준으로 합니다.

| 요소 | 의미 | 내보내기 처리 |
| --- | --- | --- |
| 지문 언어 | 본문·제목·설명 언어 선택 | 지정한 언어의 지문과 리소스 사용 |
| `useInStatements` | 예제에 포함할 테스트 선택 | `true`인 테스트만 내보냄 |
| `index` / testset | 테스트 식별과 순서 | 호출자는 한 testset의 데이터를 전달; index 순서대로 예제 1부터 부여 |
| `manual`, `scriptLine` | 수동·생성 테스트 입력의 출처 | 생성 입력은 먼저 Polygon에서 가져와야 함; 생성기 실행을 여기서 추측하지 않음 |
| `inputBase64` | 수동 테스트 입력의 정확한 바이트 | 표시용 입력이 없으면 원본 바이트 사용; 손실 가능성이 있는 `input` 문자열에 의존하지 않음 |
| `inputForStatement` | 실제 입력 대신 지문에 표시할 입력 | 지정돼 있으면 우선 사용; 빈 문자열도 의도된 값으로 보존 |
| `outputForStatement` | 실제 정답 대신 지문에 표시할 출력 | 지정돼 있으면 우선 사용; 빈 문자열도 보존 |
| 생성된 정답 | 주 풀이 등으로 생성한 답 | 표시용 출력이 없으면 가져온 정답 사용; 없으면 실패 |
| `verifyInputOutputForStatements` | 표시용 입출력 검증 여부 | Polygon의 validator/checker 검증에 맡김; PDF 생성만으로 검증됐다고 간주하지 않음 |
| `notes` | 지문에 보이는 설명 | 예제 뒤에 표시 |
| 공백·탭·개행·특수문자 | 예제 데이터 자체 | 텍스트 파일을 listings로 읽음; `_`, `%`, `#` 등을 TeX 코드로 실행하지 않음 |

내보낸 `example.NN` / `.a`는 **최종 표시용 예제**입니다. 실제 채점 데이터와 다를 수 있으므로 이 파일로 DOMjudge 테스트를 덮어쓰지 않습니다. toolkit은 파일의 숫자 순서로 출력하고, 입력이나 출력 파일이 빠지면 빌드를 거부합니다. 지문에 선택되지 않은 테스트를 자동으로 공개하지 않습니다.

짧은 예제는 입력과 출력을 같은 행에, 다음 예제는 다음 행에 배치합니다. 긴 예제는 `auto`에서 전체 폭 상자로 전환해 페이지를 나눌 수 있게 합니다. `paired`는 강제 가로 배치이므로 긴 예제에는 사용하지 않습니다.

## 수정과 빌드

```powershell
python scripts/build.py 2025/problems/A/statement-sections/korean/legend.tex
python scripts/build.py 2025/problems/A/statement-sections/korean/example.02
```

둘 다 같은 통합본과 개별 PDF를 갱신합니다. `.tex` 파일에는 `% !TeX root = ../../../main.tex`를 넣어 두었습니다. 원시 예제 파일에는 주석을 넣지 않습니다. VS Code의 `onFileChange` 설정은 LaTeX가 읽은 예제·메타데이터 의존 파일 변경도 감지합니다. 처음에는 한 번 빌드해 의존 파일을 등록해야 합니다.

조립 결과는 무시되는 `problems/build/statements/`에 생성됩니다. 직접 편집하지 않습니다. 예제 추가·삭제와 빈 notes의 변경도 다음 빌드에서 조립 결과에 반영됩니다.

## pol2dom 변환 경계

`kgupc_pol2dom.polygon.export_statement()`은 이미 가져온 `problem.info`, 선택 언어의 `problem.statements`, 한 testset의 `problem.tests`, `problem.testInput` / `problem.testAnswer` 결과와 리소스 바이트를 받습니다. 새 로컬 폴더에 위 구조를 생성합니다. 기존 자료가 있는 폴더는 덮어쓰지 않습니다.

인증·API 호출, 검증 실행, DOMjudge 패키지 생성·업로드는 아직 구현하지 않았습니다. 향후 Polygon 패키지를 가져올 때도 동일한 렌더러에 연결할 수 있습니다. 공개 pol2dom 저장소에는 실제 준비 중인 대회 자료를 넣지 않습니다.

그림과 일반 TeX 표현은 [Polygon 지문 매뉴얼](https://polygon.codeforces.com/docs/statements-tex-manual)의 지원 구문을 사용합니다. Polygon 전용 커스텀 명령을 쓴 지문은 정의 파일을 함께 처리하는 추가 작업이 필요합니다.
