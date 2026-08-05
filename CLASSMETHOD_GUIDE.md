# `cls`와 `@classmethod` 아주 쉽게 이해하기

이 글을 읽고 나면 `cls`가 무엇인지, `Quiz.from_dict()`가 어떻게 딕셔너리를 `Quiz` 객체로 바꾸는지 설명할 수 있습니다.

## 먼저 한 문장으로 이해하기

```text
@classmethod는 객체가 없어도 클래스 이름으로 호출할 수 있는 메서드입니다.
cls는 그 메서드를 호출한 클래스를 가리킵니다.
```

아직 어렵다면 아래 비유부터 읽어보세요.

## 붕어빵으로 비유하기

클래스는 붕어빵을 만드는 틀과 같습니다.

```text
Quiz 클래스 = 붕어빵 틀
Quiz 객체   = 틀로 만든 붕어빵
```

`state.json`에서 읽은 딕셔너리는 주문서와 같습니다.

```python
quiz_data = {
    "question": "Python 리스트의 기호는?",
    "choices": ["()", "[]", "{}", "<>"],
    "answer": 2,
    "hint": "대괄호를 생각해 보세요.",
}
```

이 주문서는 문제 정보를 가지고 있지만 아직 `Quiz` 객체는 아닙니다.

```text
주문서인 딕셔너리
        ↓ Quiz.from_dict()
붕어빵인 Quiz 객체
```

`from_dict()`는 주문서를 보고 붕어빵을 만들어 주는 버튼이라고 생각하면 됩니다.

## 일반 메서드의 `self`

일반 메서드를 사용하려면 먼저 객체가 있어야 합니다.

```python
quiz = Quiz(
    "Python 리스트의 기호는?",
    ["()", "[]", "{}", "<>"],
    2,
    "대괄호를 생각해 보세요.",
)

quiz.display(1, 5)
```

`quiz.display()`를 호출하면 `self`는 `quiz` 객체를 가리킵니다.

```text
quiz.display()
      ↓
self = quiz 객체
```

따라서 `self.question`은 `quiz` 객체가 가진 문제를 뜻합니다.

## 클래스 메서드의 `cls`

JSON에서 딕셔너리를 읽은 순간에는 아직 `Quiz` 객체가 없습니다. 그래서 객체 없이 `Quiz` 클래스에서 직접 호출할 수 있는 클래스 메서드를 사용합니다.

```python
class Quiz:
    @classmethod
    def from_dict(cls, data):
        return cls(
            data["question"],
            data["choices"],
            data["answer"],
            data.get("hint", ""),
        )
```

다음과 같이 호출합니다.

```python
quiz = Quiz.from_dict(quiz_data)
```

이때 Python은 `cls`에 `Quiz` 클래스를 자동으로 넣습니다.

```text
Quiz.from_dict(quiz_data)
        ↓
cls = Quiz
```

그러므로 메서드 안의 다음 코드는:

```python
return cls(
    data["question"],
    data["choices"],
    data["answer"],
    data.get("hint", ""),
)
```

사실상 다음 코드와 같습니다.

```python
return Quiz(
    data["question"],
    data["choices"],
    data["answer"],
    data.get("hint", ""),
)
```

`Quiz(...)`가 실행되면 `__init__()`이 호출되고 새로운 `Quiz` 객체가 만들어집니다.

## 전체 동작 순서

```text
1. state.json에서 딕셔너리를 읽습니다.
2. Quiz.from_dict(딕셔너리)를 호출합니다.
3. Python이 cls에 Quiz 클래스를 넣습니다.
4. from_dict()가 cls(...)를 실행합니다.
5. cls(...)는 Quiz(...)와 같으므로 __init__()이 호출됩니다.
6. 완성된 Quiz 객체를 반환합니다.
```

여기서 꼭 기억할 점이 있습니다.

> `@classmethod`가 자동으로 객체를 만드는 것은 아닙니다. 메서드 안에서 `cls(...)`를 실행했기 때문에 객체가 만들어집니다.

## `cls`는 정해진 문법이 아님

`cls`는 Python 예약어가 아닙니다. 다음처럼 다른 이름을 사용해도 실행됩니다.

```python
@classmethod
def from_dict(quiz_class, data):
    return quiz_class(
        data["question"],
        data["choices"],
        data["answer"],
        data.get("hint", ""),
    )
```

하지만 모든 Python 개발자가 현재 클래스를 `cls`라고 부릅니다. 다른 사람이 코드를 바로 이해할 수 있도록 `cls`를 사용하는 것이 좋습니다.

## 여러 퀴즈를 한 번에 바꾸기

`state.json`의 `quizzes`에는 여러 딕셔너리가 들어 있습니다.

```python
self.quizzes = [
    Quiz.from_dict(quiz_data)
    for quiz_data in raw["quizzes"]
]
```

이 코드는 하나의 함수가 아닙니다. 리스트를 만드는 짧은 반복문입니다. 길게 쓰면 다음과 같습니다.

```python
self.quizzes = []

for quiz_data in raw["quizzes"]:
    quiz = Quiz.from_dict(quiz_data)
    self.quizzes.append(quiz)
```

딕셔너리가 5개라면 `Quiz.from_dict()`를 5번 호출합니다. 결과적으로 `self.quizzes`에는 `Quiz` 객체 5개가 들어갑니다.

```text
딕셔너리 5개
    ↓ Quiz.from_dict()를 각각 호출
Quiz 객체 5개
```

## `QuizGame`이 `Quiz`를 만들어도 되는 이유

`QuizGame`은 게임 전체를 관리합니다. 따라서 JSON을 읽고 여러 `Quiz` 객체를 만드는 것이 자연스럽습니다.

```text
QuizGame
├── JSON 불러오기
├── Quiz 객체 만들기
├── 여러 Quiz 객체 보관하기
└── 문제를 순서대로 출제하기
```

`Quiz`는 문제 하나만 관리합니다.

```text
Quiz
├── 문제
├── 선택지
├── 정답
├── 힌트
└── 정답 확인
```

선생님이 문제 카드를 여러 장 준비하고 관리하는 것처럼 `QuizGame`이 여러 `Quiz` 객체를 만들고 관리한다고 생각하면 됩니다.

## 직접 확인하기

다음 코드를 실행해 보세요.

```python
quiz_data = {
    "question": "Python 리스트의 기호는?",
    "choices": ["()", "[]", "{}", "<>"],
    "answer": 2,
    "hint": "대괄호입니다.",
}

quiz = Quiz.from_dict(quiz_data)

print(type(quiz))
print(quiz.question)
print(quiz.answer)
```

예상 결과는 다음과 같습니다.

```text
<class 'classes.quiz.Quiz'>
Python 리스트의 기호는?
2
```

딕셔너리가 실제 `Quiz` 객체로 바뀌었다는 뜻입니다.

## 마지막 확인 문제

1. `cls`는 Python 예약어인가요?
   - 아닙니다. 현재 클래스를 나타내기 위해 사용하는 표준 이름입니다.
2. `@classmethod`가 객체를 자동으로 만드나요?
   - 아닙니다. `from_dict()` 안에서 `cls(...)`를 호출해서 객체가 만들어집니다.
3. `Quiz.from_dict(data)`를 호출할 때 `cls`는 무엇인가요?
   - `Quiz` 클래스입니다.
4. JSON 딕셔너리가 5개라면 몇 개의 `Quiz` 객체가 만들어지나요?
   - 5개입니다.

## 한 문장으로 말하기

평가에서는 다음처럼 설명하면 됩니다.

> `@classmethod`는 객체 없이 클래스에서 직접 호출하는 메서드입니다. `cls`는 현재 클래스를 가리키며, `from_dict()`에서는 `cls(...)`를 호출해 딕셔너리로 새로운 `Quiz` 객체를 만듭니다.
