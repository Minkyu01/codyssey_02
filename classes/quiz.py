class Quiz:
    def __init__(
        self,
        question: str,
        choices: list[str],
        answer: int,
        hint: str = "",
    ):
        self.question = question
        self.choices = list(choices)
        self.answer = answer
        self.hint = hint

    def display_quiz(self, number, total):
        print(f"\n[{number}/{total}] {self.question}")
        for index, choice in enumerate(self.choices, start=1):
            print(f"{index}. {choice}")
        print("5. 힌트 보기")
        

    def display_hint(self, number):
        print(f"{number}. {self.hint}")

        
    def is_correct(self, selected):
        return self.answer == selected


    # 기본적으로 class내부에선 첫 인자로 self를 받음, 
    # 그런데 Quiz객체는 이 함수를 통해서 Quiz객체를 만듬 -> TODO 공부 필요
    # hint만 get인 이유 -> 키가 없을때 기본값 지정, 나머지는 없다면 json오류 발생
    @classmethod
    def from_dict(cls, data):
        return cls(
            data["question"],
            data["choices"],
            data["answer"],
            data.get("hint", ""),
        )

    def to_dict(self):
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
            "hint": self.hint,
        }