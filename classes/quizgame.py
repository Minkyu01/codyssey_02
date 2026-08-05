import json
import random
from datetime import datetime
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

    def run(self):
        # 게임 로드는 한번만
        self.game_load()

        while True:
            self.show_menu()
            choice = self.read_int("값을 입력해 주세요 : ", 1, 7)
            
            if choice == 1:
                self.game_play()
            elif choice == 2:
                self.add_quiz()
            elif choice == 3:
                self.show_list()
            elif choice == 4:
                self.del_quiz()
            elif choice == 5:
                self.show_best_score()
            elif choice == 6:
                self.show_history()
            elif choice == 7:
                print("게임을 종료합니다.")
                self.game_save()
                break


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

    # 입력 검사, 대부분 숫자만 입력
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

    # 퀴즈 추가시 문자열 입력
    def read_text(self, prompt):
        while True:
            text = input(prompt).strip()
            if text:
                return text
            print("값을 입력해 주세요")


    # 게임 데이터 형식을 따로 사용해야 할듯, -> 퀴즈를 푸는 형식
    def game_load(self):
        # 일단 실패할 경우 생각
        try : 
            with open(self.state_path, 'r', encoding='utf-8') as f:
                raw = json.load(f)

            # json 에러 처리
            if not isinstance(raw, dict):
                raise ValueError("전체 데이터가 객체 형식이 아닙니다.")
            if not isinstance(raw.get("quizzes"), list):
                raise ValueError("quizzes가 목록 형식이 아닙니다.")
            
            self.quizzes = [
                Quiz.from_dict(quiz_data)
                for quiz_data in raw["quizzes"]
            ]

            self.best_record = raw.get("best_record")
            self.history = raw.get("history", [])
            
        except FileNotFoundError : 
            print("state.json 파일이 없습니다.")
            self.restore_default_state()
            return False
        
        except (
        json.JSONDecodeError,
        KeyError,
        TypeError,
        ValueError,
        OSError,
        ) as error:
            print(f"데이터를 불러오지 못했습니다: {error}")
            self.restore_default_state()
            return False
        
        return True

    def game_save(self):
        data = {
            "quizzes" : [
                quiz.to_dict() for quiz in self.quizzes
            ],
            "best_record" : self.best_record,
            "history" : self.history
        }

        try :
            with open(
                self.state_path,
                "w",
                encoding="utf-8"
            )as f:
                json.dump(
                    data,
                    f,
                    ensure_ascii=False,
                    indent=2,
                )
            return True

        except OSError as error:
            print(f"저장하지 못했습니다: {error}")
            return False


    # 퀴즈풀기(1) 을 선택했을때
    def game_play(self):
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다. ")
            return

        total = len(self.quizzes)

        # quiz 문제수 입력 받기
        play_count = self.read_int(f"몇 문제를 풀겠습니까? : 1 ~ {total} ", 1, total)

        # 퀴즈 랜덤하게 석기 
        # self.quizzes  → 기존 순서 유지 , play_quizzes → 무작위 순서
        play_quizzes = random.sample(
            self.quizzes,
            play_count,
            # len(self.quizzes),
        )

        correct_count = 0
        hints_used = 0
        score = 0
        point_per_question = 100 / play_count

        # enumerate 란 -> 값과 순서를 함께 꺼내는 함수, 인덱스 시작 번호를 1로 지정한거뿐
        for number, quiz in enumerate(play_quizzes, start=1,):
            quiz.display_quiz(number, play_count)
            hint_used = False

            while True:
                user_input = self.read_int("정답을 입력해 주세요 : ", 1, 5)

                if user_input == 5:
                    if hint_used:
                        print("이 문제에서는 이미 힌트를 사용했습니다.")
                    else:
                        quiz.display_hint(number)
                        hint_used = True
                        hints_used += 1
                    continue
                
                if quiz.is_correct(user_input):
                    correct_count += 1
                    earned_score = point_per_question
                    if hint_used:
                        earned_score *= 0.5

                    score += earned_score
                    print("정답입니다.")
                else:
                    print("오답입니다.")
                break

        score = round(score)
        # 게임 기록 저장
        self.save_record(
            play_count,
            correct_count,
            hints_used,
            score
        )

        print(
            f"\n결과: {play_count}문제 중 "
            f"{correct_count}문제 정답 "
            f"\nscore : {score}"
        )

        self.game_save()


    # 퀴즈 추가(2) 를 선택했을때
    def add_quiz(self):
        print("\n=== 퀴즈 추가 ===")

        question = self.read_text("문제 입력 :")
        choices = []

        for number in range(1,5):
            choice = self.read_text(
                f"{number} 번 선택지 입력 :"
            )
            choices.append(choice)

        answer = self.read_int(
            "정답 번호 (1 ~ 4) : " , 1,4
        )

        hint = self.read_text("힌트 입력 : ")

        new_quiz = Quiz(
            question=question,
            choices = choices,
            answer = answer,
            hint = hint,
        )

        self.quizzes.append(new_quiz)

        if self.game_save():
            print("퀴즈를 성공적으로 추가했습니다.")
        else :
            self.quizzes.pop()
            print("저장에 실패하여 추가를 취소했습니다.")

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

    # 퀴즈 삭제 (4)
    def del_quiz(self):
        total =len(self.quizzes) 
        if not total :
            print("등록된 퀴즈가 없습니다.")
            return False

        value = self.read_int(f"삭제할 퀴즈 번호를 말해주세요 (1 ~ {total}) : ", 1, total)

        self.quizzes.pop(value - 1)

        #  삭제한거 json에 적용하기
        if self.game_save():
            print("퀴즈를 성공적으로 삭제했습니다.")
        else :
            self.quizzes.pop()
            print("삭제를 실패했습니다.")
        return True

    # 최고 점수 기록
    def show_best_score(self):
        if self.best_record is None:
            print("아직 플레이 기록이 없습니다.")
            return
        record = self.best_record

        print("\n=== 최고 점수 ===")
        print(f"점수: {record['score']}점")
        print(f"정답: {record['correct']}/{record['total']}")
        print(f"힌트 사용: {record['hints_used']}회")
        print(f"플레이 시간: {record['played_at']}")

    # history 기록 출력
    def show_history(self):
        if not self.history:
            print("아직 플레이 기록이 없습니다.")
            return

        print("\n=== 플레이 기록 ===")

        for number, record in enumerate(self.history, start=1):
            print(
                f"{number}. {record['score']}점 | "
                f"정답 {record['correct']}/{record['total']} | "
                f"힌트 {record['hints_used']}회 | "
                f"{record['played_at']}"
            )

    # 게임 기록 - history 저장
    def save_record(self, total, correct_count, hints_used, score):
        # base_score = round(correct_count / total * 100)
        # score = max(0, base_score - hints_used * 10)

        record = {
            "played_at": datetime.now().isoformat(timespec="seconds"),
            "total": total,
            "correct": correct_count,
            "hints_used": hints_used,
            "score": score,
        }

        self.history.append(record)

        # 최고 기록 저장
        if (
            self.best_record is None
            or score > self.best_record["score"]
        ):
            self.best_record = record.copy()


        return  self.game_save()

    # state.json이 잘못되거나 없을때 기본 퀴즈 세팅
    def set_default_state(self):
        self.quizzes = [
            Quiz(*quiz_data)
            for quiz_data in self.DEFAULT_QUIZZES
        ]

        self.best_record = None
        self.history = []

    def restore_default_state(self):
        self.set_default_state()

        if self.game_save():
            print("기본 퀴즈 데이터로 초기화했습니다.")
        else:
            print(
                "기본 퀴즈는 사용할 수 있지만 "
                "파일에는 저장하지 못했습니다."
            )