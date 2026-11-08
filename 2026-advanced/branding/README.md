# 표지 로고

- `../organizers.png`: 경기대학교 소프트웨어중심대학사업단 · 솔리 · 학생회 로고.
- `../sponsors.png`: IITP 정보통신기획평가원 로고.
- `source-sponsors.png`: 분리하기 전 원본 이미지. 기존 로고의 글자와 색상을 보존하기 위해 보관합니다.
- `source-solutio.png`, `source-student-council.png`: 주최 로고 원본.

표제 `Organizers`와 `Sponsors` 및 배치는 공통 toolkit에서 처리합니다. `solutions/main.tex`에서는 이미지 경로만 지정합니다.

```tex
\organizerimage{../organizers.png}
\sponsorimage{../sponsors.png}
```

PNG를 다시 만들려면 이 디렉터리에서 실행합니다.

```powershell
xelatex -interaction=nonstopmode -halt-on-error organizers.tex
xelatex -interaction=nonstopmode -halt-on-error sponsors.tex
pdftoppm -singlefile -r 600 -png organizers.pdf ../organizers
pdftoppm -singlefile -r 600 -png sponsors.pdf ../sponsors
```

로고를 다시 그리지 않고 원본 이미지를 잘라 배치합니다. `trim` 값은 원본 PNG의 해상도에 맞춰져 있습니다.
