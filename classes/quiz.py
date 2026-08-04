class Quiz:
    def __init__(self, question, choices, answer, hint):
        question: str
        choices: list[str]
        answer: int
        hint: str = ''

        self.question = question
        self.choices = list(choices)
        self.answer = answer
        self.hint = hint

    def display(self, number, total):
        print(f"\n[{number}/{total}] {self.question}")
        for index, choice in enumerate(self.choices, start=1):
            print(f"{index}. {choice}")
        print("h. 힌트 보기")

    def is_correct(self, selected):
        return self.answer == selected
