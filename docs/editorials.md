# 2026 에디토리얼 작성

비기너와 어드밴스드 모두 기존 2025 에디토리얼과 같은 Beamer 형식을 사용합니다.

```text
2026-beginner/ 또는 2026-advanced/
  solutions/
    main.tex                  표지·문제 목록·풀이 연결
    main.pdf                  빌드한 에디토리얼
    afterword.tex             마지막에 붙는 출제진 후기
    A/
      <문제 이름>.tex         A번 풀이
      images/                 A번 풀이에 사용할 그림
    B/ ... L/
```

각 문제의 `.tex`에는 기존 2025 형식의 문제 소개 슬라이드와 빈 풀이 슬라이드가 있습니다. 필요한 내용을 자유롭게 작성하고, 필요한 만큼 `frame`을 추가하면 됩니다. 소스 코드를 넣는 슬라이드에는 `\begin{frame}[fragile]`을 사용합니다.

문제 제목은 `solutions/main.tex`가 `problems/<문제 번호>/statement-sections/korean/name.tex`에서 읽습니다. 풀이 쪽에 제목을 중복으로 적지 않아도 됩니다. 문제 목록의 번호와 제목은 각 풀이의 첫 슬라이드로 연결됩니다. `label=problem-A` 같은 링크 대상은 유지하세요.

각 문제의 `images/`에 그림을 넣고 `\includegraphics{images/파일명.png}`로 참조합니다. 표지는 기존 toolkit의 `\titlepage`를 그대로 사용합니다. `sponsors.png`는 2025 템플릿의 이미지를 복사한 것이므로 2026 후원사 이미지로 교체하면 됩니다.

## 표지의 주최·후원 로고

주최와 후원 이미지를 나눠 표시하려면 `solutions/main.tex`에서 다음처럼 지정합니다.

```tex
\author{출제진 이름}
\organizerimage{../organizers.png}
\sponsorimage{../sponsors.png}
```

toolkit이 `Organizers`·`Sponsors` 제목과 로고의 크기·간격을 처리합니다. 지정하지 않은 로고 영역은 표시하지 않으며, 하나만 지정해도 위쪽부터 배치합니다. 저자 정보는 표지 오른쪽 위에 `solutio-gray`로 표시됩니다. 기존 `\renewcommand{\sponsorimage}{파일명}` 방식도 유지됩니다.

## 출제진 후기

단일 대회에서는 `solutions/afterword.tex`에 출제진 후기를 작성합니다. 문제 목록의 마지막 페이지 아래에 있는 `출제진 후기 보기`를 누르면 마지막 후기 페이지로 이동합니다. 후기 양식은 `2026-advanced/solutions/afterword.tex`에 있으며, 다음처럼 아이디와 본문을 넣습니다.

```tex
\authorreview{아이디}{
    여기에 후기를 작성합니다.
}
```

작성란은 필요한 만큼 추가하거나 삭제할 수 있습니다. 후기가 길어지면 `\begin{frame}{출제진 후기}`로 페이지를 추가하고 작성란을 나눕니다. 링크 대상인 `label=afterword`는 첫 후기 프레임에만 유지합니다. `main.tex`에서는 모든 문제 해설 뒤에 `\input{afterword.tex}`를 둡니다.

2026은 두 부문의 후기를 어드밴스드에 함께 작성합니다. 비기너의 문제 목록에서는 비기너 마지막 안내 페이지로 이동하고, 안내 페이지의 링크는 웹에 배포한 어드밴스드 PDF의 후기 페이지로 연결됩니다. 다른 단일 대회에서는 어드밴스드의 작성 양식을 사용하면 됩니다.

## 다른 부문 해설로 연결하기

비기너 J·L의 해설 링크와 마지막 후기 안내 링크는 [GitHub Pages에 배포한 어드밴스드 PDF](https://kgu-solutio.github.io/kgupc-archive/2026-advanced/solutions/main.pdf)를 엽니다. 로컬 PDF 사이의 상대 경로 링크는 VS Code·Edge에서 작동하지 않아 HTTPS 링크를 사용합니다. 로컬에서 비기너 PDF를 열어도 링크의 대상은 웹에 배포된 PDF이며, 인터넷 연결이 필요합니다.

배포 주소는 비기너 `solutions/main.tex`의 `\AdvancedEditorialURL` 한 곳에서 설정합니다. 각 해설에서는 `\advancededitoriallink{problem-B}{어드밴스드 B번 해설 보기}`처럼 대상 라벨과 표시할 문구를 지정합니다. 페이지 번호는 어드밴스드의 `main.aux`에서 가져와 `#page=`로 연결하므로, 어드밴스드를 수정했다면 어드밴스드와 비기너를 순서대로 다시 빌드합니다. 번호는 표지를 포함한 PDF의 실제 페이지입니다.

`main`에 PDF를 푸시하면 `.github/workflows/publish-pdfs.yml`이 커밋된 문제집·에디토리얼 PDF를 GitHub Pages에 배포합니다. 처음에는 저장소 **Settings → Pages → Source**가 **GitHub Actions**로 설정돼 있어야 합니다. 워크플로는 TeX를 컴파일하지 않으므로, 최신 PDF를 빌드하고 두 부문의 PDF를 함께 커밋합니다.

## 빌드

저장소 루트에서 빌드합니다.

```powershell
python scripts/build.py 2026-advanced/solutions/main.tex
python scripts/build.py 2026-beginner/solutions/main.tex
```

결과는 각 `solutions/main.pdf`입니다. 문제별 풀이 파일을 지정해도 해당 부문의 전체 에디토리얼을 빌드합니다. VS Code에서 LaTeX Workshop을 사용하면 각 풀이 파일의 TeX root 주석과 저장소의 빌드 설정을 통해 같은 명령이 실행됩니다.

다른 컴퓨터에서는 먼저 각 대회의 `toolkit.lock.json`과 일치하는 toolkit을 `scripts/setup_toolkit.py`로 설치합니다. 버전과 내용 해시를 유지하며, 2025 환경은 별도로 사용합니다. 자세한 설치 방법은 [대회 폴더 인계 안내](import-polygon.md)를 참고하세요.
