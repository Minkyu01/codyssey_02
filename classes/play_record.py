from datetime import datetime

class PlayRecord:
    def __init__(
        self,
        played_at,
        total,
        correct,
        hints_used,
        score,
    ):
        if not isinstance(played_at, str):
                raise TypeError("플레이 시간은 문자열이어야 합니다.")
        try:
            datetime.fromisoformat(played_at)
        except ValueError:
            raise ValueError("플레이 시간 형식이 올바르지 않습니다.")
        if type(total) is not int or total < 1:
            raise ValueError("전체 문제 수는 1 이상의 정수여야 합니다.")
        if (
            type(correct) is not int
            or not 0 <= correct <= total
        ):
            raise ValueError("정답 수가 올바르지 않습니다.")
        if (
            type(hints_used) is not int
            or not 0 <= hints_used <= total
        ):
            raise ValueError("힌트 사용 수가 올바르지 않습니다.")
        if (
            isinstance(score, bool)
            or not isinstance(score, (int, float))
            or not 0 <= score <= 100
        ):
            raise ValueError("점수는 0부터 100 사이여야 합니다.")
        self.played_at = played_at
        self.total = total
        self.correct = correct
        self.hints_used = hints_used
        self.score = score

    @classmethod
    def create(cls, total, correct, hints_used, score):
        return cls(
            played_at=datetime.now().isoformat(timespec="seconds"),
            total=total,
            correct=correct,
            hints_used=hints_used,
            score=score,
        )

    @classmethod
    def from_dict(cls, data):
        if not isinstance(data, dict):
            raise TypeError("플레이 기록은 객체 형식이어야 합니다.")

        return cls(
            played_at=data["played_at"],
            total=data["total"],
            correct=data["correct"],
            hints_used=data["hints_used"],
            score=data["score"],
        )

    def to_dict(self):
        return {
            "played_at": self.played_at,
            "total": self.total,
            "correct": self.correct,
            "hints_used": self.hints_used,
            "score": self.score,
        }