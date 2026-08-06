# json읽고 쓰기 , 기본 데이터 복구
import json
from .quiz import Quiz
from .play_record import PlayRecord

class StateStore:
    def __init__(self, state_path):
        self.state_path = state_path

    # 에러는 상위 모듈에서
    def load(self):
        # try : 
        with open(self.state_path, 'r', encoding='utf-8') as f:
            raw = json.load(f)

        # json 에러 처리
        if not isinstance(raw, dict):
            raise ValueError("전체 데이터가 객체 형식이 아닙니다.")
        if not isinstance(raw.get("quizzes"), list):
            raise ValueError("quizzes가 목록 형식이 아닙니다.")
        
        quizzes = [
            Quiz.from_dict(quiz_data)
            for quiz_data in raw["quizzes"]
        ]

        # best_record = raw.get("best_record")
        # history = raw.get("history", [])
        best_data = raw["best_record"]
        history_data = raw["history"]

        if not isinstance(history_data, list):
            raise TypeError("history는 목록 형식이어야 합니다.")

        best_record = (
            PlayRecord.from_dict(best_data)
            if best_data is not None
            else None
        )

        history = [
            PlayRecord.from_dict(record_data)
            for record_data in history_data
        ]

        return quizzes, best_record, history


    def save(self, quizzes, best_record, history):
        data = {
            "quizzes": [
                quiz.to_dict()
                for quiz in quizzes
            ],
            "best_record": (
                best_record.to_dict()
                if best_record is not None
                else None
            ),
            "history": [
                record.to_dict()
                for record in history
            ],
        }
        
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