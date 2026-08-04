# Python & Git 퀴즈 게임

Python 기초와 Git 개념을 주제로 한 사지선다형 콘솔 퀴즈 게임입니다. 이 주제는 과제를 구현하면서 사용하는 자료형, 조건문, JSON, Git 명령을 문제로 다시 복습하기 위해 선택했습니다.

프로그램은 기본 퀴즈 5개를 제공하며 퀴즈 풀기, 추가, 목록 조회, 최고 점수 조회 기능을 지원합니다. 추가한 퀴즈와 최고 점수는 프로젝트 루트의 `state.json`에 저장되어 재실행 후에도 유지됩니다.

## 실행 환경

- Python 3.10 이상
- 외부 패키지 없음(표준 라이브러리만 사용)
- 검증 환경: macOS 26.5.2, Python 3.14.6, Git 2.50.1

이 컴퓨터의 `/usr/bin/python3`는 3.9.6이므로 과제 조건을 충족하지 않습니다. 여기서는 Homebrew Python을 사용합니다.

```bash
cd /Users/myu/Documents/codeseey/study/piscine/01
/opt/homebrew/bin/python3 main.py
```

다른 환경에서 `python3 --version`이 3.10 이상이면 다음처럼 실행해도 됩니다.

```bash
python3 main.py
```

별도의 상태 파일로 시험하려면 다음 옵션을 사용합니다.

```bash
python3 main.py --state /tmp/quiz-state.json
```

## 기능

1. 저장된 모든 퀴즈 풀기와 정답·오답 피드백
2. 문제, 선택지 4개, 정답 번호를 입력해 퀴즈 추가
3. 저장된 퀴즈 목록 조회
4. 최고 점수 조회 및 갱신
5. 데이터 저장 후 종료

숫자 입력의 앞뒤 공백, 빈 입력, 문자, 범위 밖 숫자를 검사합니다. `Ctrl+C`와 EOF가 발생하면 가능한 범위에서 현재 데이터를 저장하고 종료합니다. 손상된 상태 파일은 `state.json.corrupt-날짜-시간`으로 백업한 뒤 기본 데이터로 복구합니다.

## 파일 구조

```text
01/
├── Ques.md                         # 과제 원문
├── README.md                       # 프로젝트 사용 및 제출 안내
├── main.py                         # 실행 진입점
├── state.json                      # 퀴즈와 최고 점수
├── src/
│   └── quiz_game.py                # Quiz, QuizGame 구현
├── tests/
│   ├── test_quiz_game.py           # 단위 테스트
│   └── static_check.sh             # 필수 파일·구조 검사
├── scripts/
│   └── verify.sh                   # 전체 자동 검증
└── docs/
    ├── getting-started.md          # 빈 폴더부터 재구현하는 방법
    ├── study-guide.md              # 평가 전 학습 문서
    ├── evaluation-study-plan.md    # 학습 순서와 실습 계획
    ├── peer-review.md              # 시연·질문 대비표
    ├── troubleshooting.md          # 문제 해결 기록
    └── evidence/                   # 요구사항별 검증 근거
```

## 데이터 파일

`state.json`은 UTF-8 JSON 파일입니다.

```json
{
  "quizzes": [
    {
      "question": "문제",
      "choices": ["선택지 1", "선택지 2", "선택지 3", "선택지 4"],
      "answer": 1
    }
  ],
  "best_score": null,
  "best_correct": null,
  "best_total": null
}
```

- `quizzes`: 퀴즈 객체 목록
- `best_score`: 최고 점수(0~100) 또는 아직 플레이하지 않은 경우 `null`
- `best_correct`, `best_total`: 최고 점수 당시 정답 수와 전체 문제 수

저장은 임시 파일을 먼저 쓴 뒤 `os.replace`로 교체하는 방식이라 쓰는 도중 원본이 일부만 기록될 위험을 줄였습니다.

## 검증

전체 자동 검증은 Python 3.10 이상 인터프리터를 찾아 문법, 11개 단위 테스트, 실제 콘솔 입력, 재실행 지속성, 잘못된 입력, 손상 JSON 복구, EOF 종료를 검사합니다.

```bash
./scripts/verify.sh
./tests/static_check.sh
```

단위 테스트만 실행하려면 다음 명령을 사용합니다.

```bash
/opt/homebrew/bin/python3 -m unittest discover -s tests -v
```

상세 결과는 [최초 구현 감사](docs/evidence/initial-audit.md), [검증 기록](docs/evidence/verification.md), [요구사항 추적표](docs/evidence/requirement-matrix.md)에서 확인할 수 있습니다.

## 평가·재구현 준비

- [처음부터 재구현하기](docs/getting-started.md)
- [핵심 개념 학습 가이드](docs/study-guide.md)
- [평가 전 학습 계획](docs/evaluation-study-plan.md)
- [동료 평가 시연과 예상 질문](docs/peer-review.md)
- [문제 해결 기록](docs/troubleshooting.md)

## 제출 전 수동 확인

로컬 기능 구현은 검증됐지만 다음 Git·제출 항목은 아직 완료되지 않았습니다.

- [ ] `01` 폴더를 Git에 추가하고 10개 이상의 의미 있는 커밋 기록 준비
- [ ] 별도 브랜치에서 작업한 뒤 `main`에 병합한 그래프 준비
- [ ] 원격 저장소에 푸시하고 접근 가능한 URL 확인
- [ ] 별도 디렉터리에서 `clone`, 수정·푸시, 기존 디렉터리에서 `pull` 수행
- [ ] Python/Git 환경, 퀴즈 추가·목록·플레이·점수, Git 그래프 스크린샷 촬영
- [ ] 스크린샷과 저장소 URL에 토큰, 이메일 등 민감정보가 없는지 확인

현재 Git 근거와 정확한 수행 순서는 [Git 워크플로우 기록](docs/evidence/git-workflow.md)에 정리했습니다.
