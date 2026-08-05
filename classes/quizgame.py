import json
import random
from datetime import datetime
# from pathlib import Path
# import Quiz

from .quiz import Quiz


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
        self.state_path = state_path # 데이터 경로 저장
        self.quizzes = [] # json에서 가져온 quiz객체의 데이터모음, 각 문제를 퀴즈 객체로 가지고 있는거임
        self.best_record = None # 최고 기록 저장
        self.history = [] # 게임 기록 저장
        # self.quizzes = [] # quiz 데이터들, 

    def run(self):
        while True:
            self.show_menu()
            choice = self.read_int("값을 입력해 주세요 : ", 1, 7)

            if choice == 7:
                print("게임을 종료합니다.")
                break

            try :
                self.game_load()
            except :
                print("game load error")
            
            if choice == 1:
                # 게임 데이터 로드
                try:
                    self.game_play()
                except :
                    print("game play error")
                    return
            elif choice == 3:
                self.show_list()

                

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
    def read_int(self, prompt, min, max):
        while True:
            # strip() -> 문자열 앞뒤 공백 문자 제거
            choice = input(prompt).strip()

            # if not value:
            #     print("값을 입력해 주세요.")
            # continue
            try :
                number = int(choice)
            except ValueError:
                print("숫자를 입력해 주세요.")
                continue
            if min <= number <= max:
                return number

            print(f"{min}부터 {max} 사이의 값을 입력해주세요.")

    # 게임 데이터 형식을 따로 사용해야 할듯, -> 퀴즈를 푸는 형식
    def game_load(self):
        # 일단 실패할 경우 생각
        try : 
            with open(self.state_path, 'r', encoding='utf-8') as f:
                raw = json.load(f)

            self.quizzes = [
                Quiz.from_dict(quiz_data)
                for quiz_data in raw["quizzes"]
            ]
            # print(self.quizzes)

            self.best_record = raw.get("best_record")
            self.history = raw.get("history", [])
            
        except FileNotFoundError : 
            print("state.json 파일이 없습니다.")
            return False
        
        except (
        json.JSONDecodeError,
        KeyError,
        TypeError,
        ValueError,
        OSError,
        ) as error:
            print(f"데이터를 불러오지 못했습니다: {error}")

            self.quizzes = [
                Quiz(*quiz_data)
                for quiz_data in self.DEFAULT_QUIZZES
            ]

        return False

    def game_save(self):
        return 

    # 퀴즈풀기(1) 을 선택했을때
    def game_play(self):
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다. ")
            return

        total = len(self.quizzes)
        correct_count = 0

        # enumerate 란 -> 값과 순서를 함께 꺼내는 함수, 인덱스 시작 번호를 1로 지정한거뿐
        for number, quiz in enumerate(self.quizzes, start=1,):
            quiz.display_quiz(number, total)

            while True:
                user_input = self.read_int("정답을 입력해 주세요 : ", 1, 5)
                if user_input == 5:
                    quiz.display_hint(5)
                    continue 
                
                if quiz.is_correct(user_input):
                    correct_count += 1
                    print("정답입니다.")
                else:
                    print("오답입니다.")
                break

        print(
            f"\n결과: {total}문제 중 "
            f"{correct_count}문제 정답"
        )


    # 퀴즈 추가(2) 를 선택했을때
    # def add_quiz(self):

    # 퀴즈 목록 보여주기 (3)
    def show_list(self):
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return
        
        print(f"\n등록된 퀴즈 목록 ({len(self.quizzes)}개)")
        print("=" * 30)

        for index, quiz in enumerate(self.quizzes, start=1):
            print(f"{index}. {quiz.question}")
        
        print("=" * 30)
