import json
import random
from datetime import datetime
from pathlib import Path

from .quiz import Quiz

MIN = 1
MAX = 7

class QuizGame:
    DEFAULT_QUIZZES = [
        (
            "Python에서 리스트를 만들 때 사용하는 기호는 무엇인가요?",
            ["소괄호 ()", "대괄호 []", "중괄호 {}", "꺾쇠괄호 <>"],
            2,
            "여러 값을 순서대로 저장하며 인덱스로 접근하는 자료형입니다.",
        ),
        (
            "Python에서 조건에 따라 다른 코드를 실행할 때 사용하는 키워드는 무엇인가요?",
            ["for", "def", "if", "import"],
            3,
            "조건이 참인지 거짓인지 판단할 때 사용하는 키워드입니다.",
        ),
        (
            "Python에서 오류를 처리할 때 사용하는 구문은 무엇인가요?",
            ["if / else", "try / except", "for / while", "def / return"],
            2,
            "예외가 발생할 수 있는 코드와 처리 코드를 나누어 작성합니다.",
        ),
        (
            "Git에서 변경한 파일을 커밋 대상으로 등록하는 명령어는 무엇인가요?",
            ["git push", "git add", "git clone", "git pull"],
            2,
            "변경 사항을 스테이징 영역에 올리는 명령어입니다.",
        ),
        (
            "Git에서 원격 저장소를 복제하는 명령어는 무엇인가요?",
            ["git merge", "git commit", "git clone", "git checkout"],
            3,
            "원격 저장소를 처음 내려받을 때 사용합니다.",
        ),
    ]

    def __init__(self, state_path="state.json"):
        self.state_path = Path(state_path) # 데이터 경로 저장
        self.quizzes = [] # 퀴즈 변경사항들 저장
        self.best_record = None # 최고 기록 저장
        self.history = [] # 게임 기록 저장

    def run(self):
        while True:
            self.show_menu()
            choice = self.read_int()

            if choice == 7:
                print("게임을 종료합니다.")
                break

            # actions[choice]()

    # 메인 화면 보여주기
    def show_menu(self):
        print("\n=== Python & Git 퀴즈 게임 ===")
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 퀴즈 삭제")
        print("5. 최고 점수 확인")
        print("6. 플레이 기록 확인")
        print("7. 종료")

    # 입력 검사 
    def read_int(self):
        while True:
            # strip() -> 문자열 앞뒤 공백 문자 제거
            choice = input("값을 입력해 주세요 : ").strip()

            try :
                number = int(choice)
            except ValueError:
                print("숫자를 입력해 주세요.")
                continue
            if MIN <= number <= MAX:
                return number

            print(f"{MIN}부터 {MAX} 사이의 값을 입력해주세요.")
