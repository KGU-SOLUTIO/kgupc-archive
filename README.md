# kgupc-archive

종료된 KGUPC 대회의 에디토리얼, 문제 지문, 최종 PDF를 보관하는 저장소입니다. 공통 템플릿과 PDF 생성기는 [kgupc-toolkit](https://github.com/SOLUTIO-NEST/kgupc-toolkit)의 버전이 고정된 Python 패키지를 사용합니다.

Based on:
- [Execushares](https://github.com/hamaluik/Beamer-Theme-Execushares)

문제 및 풀이의 저작권은 각 문제 작성자에게 있습니다.

## 빌드 준비

- Python 3.10 이상과 XeLaTeX, `latexmk`가 필요합니다. TeX Live 전체 설치를 권장합니다.
- `python`, `xelatex`, `latexmk`를 터미널에서 실행할 수 있어야 합니다. MiKTeX에서 `latexmk`를 사용하려면 Perl도 필요합니다.
- VS Code에서는 LaTeX Workshop 확장을 설치하고 저장소 루트 폴더를 엽니다.
- Windows의 기존 Cambria/Consolas 서체를 유지하며, 해당 서체가 없는 환경에서는 toolkit에 포함된 D2Coding을 사용합니다.
- 문제집의 영문은 Arial, 한글은 toolkit에 포함된 Noto Sans CJK KR을 사용합니다. Arial이 없는 환경에서는 toolkit의 Inter로 대체합니다. 수식과 예제 글꼴, 에디토리얼 글꼴은 유지합니다.

각 대회는 `toolkit.lock.json`에 toolkit 버전과 템플릿·글꼴·렌더러 내용 해시를 고정하고, 해당 대회의 `.venv`에 일반 설치합니다. 2025의 초기 버전은 `1.0.0`입니다. 개발 중 toolkit 소스를 바꾸어도 이미 설치된 2025의 템플릿은 변경되지 않습니다. 기존 대회의 lock을 최신 템플릿에 맞춰 덮어쓰지 않습니다.

현재 2025 작업본은 요청에 따라 문단 사이 여백과 예제 글꼴을 조정한 toolkit을 사용하며 버전 번호 `1.0.0`을 유지합니다. 문단 내부의 줄 간격은 원래 `1.08`을 사용하고, 빈 줄로 나뉜 문단 사이에는 `0.75em` 여백을 둡니다. 목록 항목 사이 간격은 `0.2em`, 입력·출력 등의 제목 앞 간격은 `3.5ex`이며, 별도의 ‘예제’ 제목 없이 예제 상자 제목으로 구분합니다. 이 변경에 한해 2025의 내용 해시와 설치 환경을 함께 갱신했습니다. 기존 `v1.0.0` 태그와는 해시가 다르므로 아래 `--source` 명령에 조정된 소스를 사용하거나 일치하는 wheel을 설치해야 합니다. 태그의 원본은 보존하며 다른 대회의 lock은 변경하지 않습니다.

현재 2025의 lock과 일치하는 toolkit 소스는 [커밋 `3732499`](https://github.com/SOLUTIO-NEST/kgupc-toolkit/commit/373249973347711ef7aaed1283aa328ae3c23b66)입니다. 다른 컴퓨터에서 2025를 빌드할 때에는 이 커밋의 소스를 사용합니다.

초기 로컬 개발 환경에서는 toolkit을 별도 저장소로 clone하고 아래 설치를 한 번 실행합니다. 소스에서 wheel을 생성할 때 기본 Python 환경에 `setuptools>=68`이 필요합니다. 원본 저장소를 변경하지 않고 임시 복사본에서 빌드하며, lock과 내용이 일치하는 wheel만 설치합니다.

```powershell
python scripts/setup_toolkit.py 2025 --source ../../SOLUTIO-NEST/kgupc-toolkit
```

원본 wheel 릴리스가 있으면 소스 checkout 없이도 설치할 수 있습니다.

```powershell
python scripts/setup_toolkit.py 2025 --wheel C:/downloads/kgupc_toolkit-1.0.0-py3-none-any.whl
```

정식 `1.0.0` 원본 소스는 toolkit의 `v1.0.0` 태그로 보존합니다. 원본 릴리스의 내용 해시로 고정된 대회는 해당 태그의 소스 또는 wheel을 사용하고, 현재 2025는 위에 명시한 조정된 커밋의 소스 또는 일치하는 wheel을 사용합니다. 설치 전에 고정된 대회 내용 해시를 검증합니다. 패키지 소스는 toolkit에 한 벌만 두고, 대회별 설치 환경과 패키지 캐시는 Git에서 제외합니다.

## PDF 생성

저장소 루트에서 실행합니다.

```powershell
# 에디토리얼
python scripts/build.py 2025/solutions/main.tex

# 문제 통합본과 모든 개별본
python scripts/build.py 2025/problems/main.tex

# A 지문을 지정해도 같은 대회의 통합본과 개별본을 함께 갱신
python scripts/build.py 2025/problems/A/kgu-solutio-kgu-ai-cse.tex
```

| 종류 | 생성 위치 |
| --- | --- |
| 에디토리얼 | `2025/solutions/main.pdf` |
| 문제 통합본 | `2025/problems/main.pdf` |
| 문제 A 개별본 | `2025/problems/A/kgu-solutio-kgu-ai-cse.pdf` |
| 문제 B 개별본 | `2025/problems/B/parking-fee-system.pdf` |
| 문제 C 개별본 | `2025/problems/C/sociality-of-sorting.pdf` |
| 문제 D 개별본 | `2025/problems/D/convention-center-escape.pdf` |
| 문제 E 개별본 | `2025/problems/E/evenly-cooked-steak.pdf` |
| 문제 F 개별본 | `2025/problems/F/connect-the-stars.pdf` |
| 문제 G 개별본 | `2025/problems/G/grand-subterranean-city.pdf` |

통합본에는 표지와 문제 목록이 포함되며, 표지·목록은 쪽 번호에서 제외하고 문제 A부터 1쪽으로 시작합니다. 각 문제는 새 페이지에서 시작합니다. 개별본은 해당 지문만 포함하고 1쪽부터 시작합니다. 두 모드는 **같은 지문과 같은 레이아웃**을 사용합니다. 개별 지문을 복사하거나 PDF를 잘라서 만들지 않습니다.

개별 PDF는 지문 `.tex` 옆에 같은 이름으로 생성됩니다. GitHub에서는 `A/`, `B/`, `C/` 안에서 원본과 PDF를 함께 찾을 수 있고, 빌드용 `build/` 폴더는 표시되지 않습니다.

VS Code에서는 `.tex` 파일을 저장하면 기본 `Archive: editorial / combined + individual problems` 레시피가 위 스크립트를 실행합니다. 문제 A를 수정하고 저장하면 통합본과 A 개별본이 함께 갱신됩니다. 변경되지 않은 개별본은 `latexmk`가 재컴파일을 생략합니다. 에디토리얼 파일을 저장하면 에디토리얼만 빌드합니다.

각 지문/해설 맨 위의 `% !TeX root = ../main.tex`를 유지하세요. `% !TeX program = xelatex`를 추가하면 LaTeX Workshop이 기본 레시피 대신 XeLaTeX만 실행할 수 있으므로 추가하지 않습니다. 자세한 설정 동작은 [LaTeX Workshop 공식 문서](https://github.com/James-Yu/LaTeX-Workshop/wiki/Compile#magic-comments)를 참고하세요.

빌드 오류가 나면 스크립트가 실패로 종료되고, 로그에 파일과 줄 번호가 표시됩니다. 이때 이전 PDF가 남아 있을 수 있으므로 빌드 성공을 확인한 뒤 배포하세요. `build/` 전체는 Git에서 제외됩니다. 각 문제 폴더의 개별 PDF와 `main.pdf`를 함께 커밋하면 됩니다.

## 문제 지문 작성

Polygon에서 종료된 대회의 지문을 가져오려면 [Polygon 가져오기 안내](docs/import-polygon.md)를 참고하세요. kgupc-pol2dom의 읽기 전용 API 가져오기로 지정한 문제만 갱신할 수 있습니다.

Polygon 연동을 위한 기본 구조는 문제별 `statement-sections/korean/` 아래의 `name.tex`, `legend.tex`, `input.tex`, `output.tex`, `notes.tex`와 `example.01` / `example.01.a` 등입니다. 2025의 A~G는 모두 이 구조를 사용합니다. A는 기존 작성본을 보존하고, B~G는 Polygon에서 가져온 지문과 예제를 사용합니다. 제목·제한·절 제목·예제 배치는 toolkit이 조합하며, `statement.json`에서 언어와 제한을 설정합니다. 자세한 구조와 Polygon 예제 선택·표시용 입출력 처리 정책은 [Polygon 지문 안내](docs/polygon-statements.md)를 참고하세요.

본문과 예제 파일을 지정해도 기존 빌드 명령으로 통합본·개별본이 갱신됩니다. `.tex`에는 TeX root 주석을 유지하고, 원시 예제 파일에는 주석을 넣지 않습니다. 기존 단일 `.tex` 방식도 지원합니다.

아래는 호환성을 유지하는 기존 단일 `.tex` 방식의 예시입니다. 2025의 실제 문제는 분리된 본문과 예제를 사용합니다.

```tex
% !TeX root = ../main.tex

\problemheader{A}{문제 제목}
\problemlimits{1}{512}

여기에 문제 본문을 작성합니다.

\InputSection
입력 형식을 작성합니다.

\OutputSection
출력 형식을 작성합니다.

\ConstraintsSection
\begin{itemize}
    \item $1 \le N \le 100$
\end{itemize}

\SampleSection
\begin{SampleInput}[1]
1
\end{SampleInput}
\begin{SampleOutput}[1]
2
\end{SampleOutput}

\ExplanationSection
예제 설명을 작성합니다.
```

`\problemlimits{1}{256}`은 `시간 제한: 1초 | 메모리 제한: 256MB`로 표시됩니다. 숫자만 입력하며 단위는 템플릿에서 붙입니다. `\problemlimits{}{}`처럼 값을 비우면 제한 표시는 생략됩니다. 예제 환경은 공백과 줄바꿈을 보존하며, 본문과 달리 `_`, `%`, `#` 등을 이스케이프하지 않습니다. 그림은 문제 폴더 안의 `images/`에 두고 `\includegraphics{images/파일명.png}`로 참조하면 두 PDF 모드에서 같은 경로를 사용합니다. 상호 참조의 라벨은 `\label{A:figure}`처럼 문제별로 구분하세요.

새 문제 C를 추가할 때는 `2025/problems/C/새문제.tex`를 만들고 `2025/problems/problem-list.tex`에 다음 한 줄을 추가합니다. 파일 맨 위에는 `% !TeX root = ../main.tex`를 넣습니다.

```tex
\includeproblem{C}{새문제.tex}
```

목록의 순서가 통합본 문제 순서입니다. 한 줄에 한 항목씩 등록하며, 문제 번호는 대문자 영문을 사용합니다. 개별 PDF는 다음 빌드에서 자동 생성됩니다. 대회명과 날짜는 `2025/problems/main.tex`에서 설정합니다. 공통 서식은 toolkit의 `src/kgupc_toolkit/resources/latex/layouts/problem.tex`에서 새 버전으로 변경합니다. 새로 공개하는 종료된 대회도 `<대회>/problems`, `<대회>/solutions` 구조와 해당 대회의 toolkit lock·설치 환경을 준비하면 같은 빌드 명령을 사용할 수 있습니다.

## 에디토리얼 작성

`2025/solutions/main.tex`에 대회 정보와 해설 목록을 설정하고, 문제별 폴더의 `.tex`에 Beamer 슬라이드를 작성합니다. 이미지는 해당 문제 폴더의 `images/`에서 참조합니다. 공통 테마는 toolkit의 `src/kgupc_toolkit/resources/latex/layouts/beamer.tex`입니다. `latexmk`가 필요한 횟수만큼 컴파일하므로 목차, 링크, 참조도 갱신됩니다.

에디토리얼의 문제 목록에서 번호나 제목을 클릭하면 해당 해설의 첫 슬라이드로 이동합니다. 새 해설을 추가할 때는 첫 프레임에 `\begin{frame}[label=problem-H]`처럼 라벨을 넣고, 목록에는 `\problemlink{H}{문제 제목}`을 사용합니다. 프레임 라벨과 링크는 [Beamer 공식 사용 설명서](https://tug.org/docs/latex/beamer/beameruserguide.pdf)의 하이퍼링크 기능을 사용합니다.

## 검증

```powershell
& './2025/.venv/Scripts/python.exe' -m unittest discover -s ../../SOLUTIO-NEST/kgupc-toolkit/tests -v
python tests/verify_pdfs.py
python tests/verify_polygon_pdfs.py
```

첫 명령은 toolkit의 경로 선택, 문제 목록과 분리 지문 검증, 버전·내용 검증을 검사합니다. Linux/macOS에서는 `2025/.venv/bin/python`을 사용합니다. PDF 검증에는 `pdftotext`도 필요합니다. `verify_pdfs.py`는 기존 단일 tex 방식의 통합·개별 반영, B 유지, 쪽 번호, 머리말, 그림과 예제 특수문자를 확인합니다. `verify_polygon_pdfs.py`는 분리 본문·예제·메타데이터 수정, 예제 추가·삭제, notes 생략, 풀이 제외, 긴 예제와 의존 파일 기록을 검증합니다. 실제 지문은 수정하지 않습니다. 검증용 PDF와 로그는 `2025/problems/build/` 아래에 남습니다.

## 참고

- **X<sub>E</sub>L<sub>A</sub>T<sub>E</sub>X을 사용해 컴파일해야 합니다.**
- 원본 솔루션과 약간의 차이가 있습니다.
  - 원본 솔루션의 고정폭 폰트는 [PF Din Mono](https://www.myfonts.com/fonts/parachute/pf-din-mono/)라는 유료 폰트로 개인적으로 라이센스를 소유하고 있기 때문에, [D2Coding](https://github.com/naver/d2codingfont)으로 교체했습니다.
  - 수식은 기본 LaTeX 수식 폰트를 사용합니다. `Cambria`는 Windows에서 고정폭 서체 설정에 사용됩니다.
  - 기타 포매팅이 약간씩 다른 부분이 존재합니다.
- 커스텀 커맨드가 있습니다.
  - `\tiertext{Bronze5}`: 난이도를 해당 티어 색상으로 표시합니다.
  - `\difficulty{색상}{텍스트}`: 색상과 굵은 글씨로 표시합니다.
  - `\complexity{math}`: 별도 수식 줄에 `\mathcal{O}(math)`를 표시합니다.
  - `\setproblem{번호}{제목}`: 에디토리얼에서 `\pletter`, `\ptitle`을 설정합니다.
  - `\tagtext{태그}`, `\idtext{아이디}`: 태그 서체와 solved.ac 프로필 링크를 표시합니다.
  - `\sectiontitle` 및 `\sectionmeta`: 슬라이드 참조
