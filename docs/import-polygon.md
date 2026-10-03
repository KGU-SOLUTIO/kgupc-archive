# 종료된 대회 폴더 인계하기

템플릿과 PDF 빌드는 kgupc-toolkit, Polygon 다운로드와 DOMjudge 연동은 kgupc-pol2dom이 담당합니다. 이 저장소는 종료된 대회의 편집 가능한 지문·해설과 PDF를 보관합니다. **pol2dom이 archive 저장소를 직접 수정하지 않습니다.**

## pol2dom에서 독립 폴더 생성

kgupc-pol2dom의 `.env`에 `CONTEST_SLUG=2026-fall`, PDF 제목·날짜, Polygon 및 DOMjudge 접속 정보를 설정하고 전체 `deploy --build-packages`를 실행하면 `build/archive/2026-fall/`도 자동 생성됩니다. 일반 인계는 이 폴더를 복사하는 것으로 충분합니다. 전체 재실행 시 이전 폴더는 pol2dom의 무시된 `build/archive/history/`에 백업됩니다.

실제 대회 최종 연동에 사용한 전체 bundle의 실행 폴더를 보관합니다. 내보내기는 해당 로컬 파일을 복사하므로 Polygon의 현재 지문을 다시 가져오지 않습니다. 부분 연동 결과는 전체 대회 내보내기에 사용할 수 없습니다.

과거 특정 bundle을 별도로 내보내야 할 때만 아래 명령을 사용합니다. kgupc-pol2dom 루트에서 실행하며, 경로는 예시입니다.

```powershell
.venv/Scripts/python -m kgupc_pol2dom export-archive "C:/Users/me/kgupc-work/deploy-12345/runs/최종-실행-ID" --name 2026-fall
```

출력은 kgupc-pol2dom의 Git에서 제외된 `build/archive/2026-fall/`입니다.

```text
2026-fall/
  toolkit.lock.json
  requirements.txt
  archive-source.json
  problems/
    main.tex
    main.pdf
    problem-list.tex
    A/
      <문제 이름>.tex
      <문제 이름>.pdf
      statement.json
      polygon-source.json
      statement-sections/korean/
        본문·입력·출력·설명·예제·이미지
    B/ ...
```

내보내기에는 API 접속이나 인증 정보가 필요하지 않습니다. 전체 채점 테스트·채점기·정답 코드가 담긴 ZIP과 `.env`, 빌드 중간 파일은 내보내지 않습니다. PDF와 원본 지문, 대회 템플릿 lock을 그대로 보존합니다. 실제 대회가 종료되고 공개 가능한지는 운영진이 확인합니다.

## 운영자가 archive에 복사

1. 최종 지문·예제·PDF와 공개 가능 여부를 확인합니다.
2. 생성된 **`2026-fall` 폴더 자체를 이 저장소 루트로 복사**합니다. 별도 빈 대회 구조를 만들 필요가 없습니다.
3. `2026-fall/problems/main.tex`의 대회 제목·작성자·날짜를 정리합니다.
4. 해설은 `2026-fall/solutions/`에서 작성하거나 별도로 준비한 해설을 추가합니다. pol2dom이 Polygon 풀이를 Beamer 해설로 자동 변환하지는 않습니다.
5. 해당 대회 lock과 일치하는 toolkit 환경을 준비하고 PDF를 다시 빌드합니다.
6. 변경 내용을 검토해 archive에서 직접 commit/push합니다.

설치·빌드는 이 저장소 루트에서 실행합니다. toolkit 소스 경로는 대회에 사용한 정확한 커밋의 checkout을 가리켜야 합니다.

```powershell
python scripts/setup_toolkit.py 2026-fall --source C:/tools/kgupc-toolkit
python scripts/build.py 2026-fall/problems/main.tex
```

원본 wheel을 보관했다면 `--source` 대신 `--wheel C:/releases/kgupc_toolkit-1.0.0-py3-none-any.whl`을 사용합니다. 버전 번호만 같아도 내용 해시가 다르면 설치를 거부하므로 정확한 커밋 또는 wheel을 보관해야 합니다.

복사 후에는 archive의 `.tex`를 편집하고 toolkit으로 통합·개별 PDF를 재생성할 수 있습니다. Polygon이나 pol2dom에 다시 접속할 필요가 없습니다.

## 기존 자료가 있는 경우

같은 이름의 대회가 이미 있다면 폴더를 통째로 덮어쓰지 말고 필요한 변경만 직접 반영합니다. 특히 현재 2025 archive 지문은 Polygon과 다르므로 기존 교정본을 유지합니다. 과거에 사용한 `polygon-import.json`은 문제 ID 대응 기록이지 대회 당시 지문의 백업이 아닙니다.

`archive-source.json`은 내보낼 당시의 revision과 파일 해시를 기록합니다. archive에서 이후 수정했다면 해시와 달라질 수 있으며, 수정 이력은 Git으로 관리합니다. DOMjudge에서 별도로 수정한 지문은 로컬 bundle에 자동 반영되지 않으므로 공개 전에 실제 최종본과 대조합니다.

기존에 archive 경로를 받아 직접 덮어쓰던 `archive-import` 명령은 제거했습니다.
