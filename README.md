# KGUPC Archive

지난 KGUPC 대회의 문제와 에디토리얼을 보관합니다.
각 대회 폴더에는 `problems/`, `solutions/`, 주최자·스폰서 이미지가 있습니다.
템플릿·글꼴·PDF 생성기는 별도 [kgupc-toolkit](https://github.com/SOLUTIO-NEST/kgupc-toolkit)에서 설치하며, 이 저장소에는 복사하지 않습니다.

## 편집

Python 3.10 이상과 XeLaTeX·latexmk가 포함된 TeX Live가 필요합니다.
VS Code에서는 LaTeX Workshop을 설치하고 **이 저장소의 루트 폴더**를 열어 주세요.

처음 작업할 때는 다음 순서로 진행합니다.

1. Python, Git, TeX Live, VS Code와 LaTeX Workshop을 설치합니다. `python`, `git`, `xelatex`, `latexmk`를 터미널에서 실행할 수 있어야 합니다.
2. 저장소 전체를 클론하고 VS Code에서 저장소 루트를 엽니다.

   ```powershell
   git clone https://github.com/KGU-SOLUTIO/kgupc-archive.git
   cd kgupc-archive
   ```

3. 편집할 문제집을 최초 빌드합니다. 필요한 툴킷은 자동 설치됩니다.

   ```powershell
   python build.py 2026-advanced/problems/main.tex
   ```

4. `problems/A/statement-sections/korean/legend.tex` 등의 본문을 수정해 저장하고 PDF를 확인합니다. 에디토리얼은 해당 `solutions/main.tex`를 먼저 빌드한 뒤 해설 파일을 수정합니다.
5. 수정한 소스와 갱신된 PDF를 함께 커밋합니다.

현재 툴킷에는 공백이 있는 경로에서 예제 파일을 읽지 못하는 문제가 있습니다. 수정 전까지는 저장소를 공백 없는 경로에 두어 주세요.

모든 대회의 툴킷을 미리 설치하려면 아래 명령을 사용할 수 있습니다. 필수 단계는 아닙니다.

```powershell
python build.py --setup
```

각 대회의 `toolkit.lock.json`에는 툴킷 버전·소스 커밋·내용 해시를 기록합니다.
위 명령은 지정된 툴킷들을 `.venv/toolkits/`에 설치합니다. 같은 툴킷을 사용하는 대회는 설치를 공유합니다.
툴킷 저장소를 따로 클론하거나 가상환경을 활성화할 필요는 없습니다.
설치 폴더는 Git에 올리지 않으며, 설치할 때만 인터넷 연결이 필요합니다.
설정을 먼저 실행하지 않아도 첫 빌드에서 필요한 툴킷을 설치합니다.

편집할 문제집 또는 에디토리얼의 `main.tex`를 열고 LaTeX Workshop으로 한 번 빌드합니다.
이후 본문이나 해설을 수정해 저장하면 PDF가 자동 갱신됩니다.
문제집을 빌드하면 개별 문제 PDF도 함께 갱신됩니다.

명령줄에서는 저장소 루트에서 실행합니다.

```powershell
python build.py 2026-advanced/problems/main.tex
python build.py 2026-advanced/solutions/main.tex
python build.py 2026-beginner/solutions/main.tex
```

`build.py`는 편집하는 파일이 속한 대회의 `toolkit.lock.json`을 읽고, 해당 툴킷의 내용 해시를 검증한 뒤 빌드합니다.
문서의 `build/toolkit-path.tex`는 빌드 시 자동 생성되므로 설치 경로를 직접 적을 필요는 없습니다.
2026 비기너의 다른 부문 해설 링크를 위해 어드밴스드 에디토리얼을 먼저 빌드합니다.
2025는 `1.0.0`, 2026 두 부문은 `1.0.1`로 지정되어 있습니다. 같은 버전 번호 안에서도 소스 커밋과 내용 해시를 고정하므로, 최신 툴킷 변경이 과거 대회에 자동으로 적용되지 않습니다.

표지 로고는 `main.tex`에서 지정합니다.

```tex
\organizerimage{../organizers.png}
\sponsorimage{../sponsors.png}
```

웹 PDF 배포는 `.github/workflows/publish-pdfs.yml`에서 처리합니다. 빌드한 PDF를 함께 올리면 됩니다.
