import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from classes.quiz import Quiz
from classes.quizgame import QuizGame


class QuizTest(unittest.TestCase):
    def test_quiz_checks_answer_and_converts_to_dict(self):
        quiz = Quiz("문제", ["1", "2", "3", "4"], 2, "힌트")

        self.assertTrue(quiz.is_correct(2))
        self.assertFalse(quiz.is_correct(1))
        self.assertEqual(Quiz.from_dict(quiz.to_dict()).answer, 2)

    def test_quiz_rejects_invalid_data(self):
        with self.assertRaises(ValueError):
            Quiz("문제", ["1", "2"], 1, "힌트")
        with self.assertRaises(ValueError):
            Quiz("문제", ["1", "2", "3", "4"], 5, "힌트")


class QuizGameTest(unittest.TestCase):
    def setUp(self):
        self.temp_directory = tempfile.TemporaryDirectory()
        self.state_path = Path(self.temp_directory.name) / "state.json"
        self.game = QuizGame(self.state_path)

    def tearDown(self):
        self.temp_directory.cleanup()

    def test_missing_file_uses_five_default_quizzes(self):
        self.assertEqual(len(self.game.quizzes), 5)
        self.assertTrue(all(len(quiz.choices) == 4 for quiz in self.game.quizzes))

    def test_read_int_retries_empty_text_and_out_of_range_values(self):
        with patch("builtins.input", side_effect=["", "abc", "9", " 3 "]):
            with redirect_stdout(io.StringIO()):
                result = self.game.read_int("선택: ", 1, 7)

        self.assertEqual(result, 3)

    def test_play_uses_hint_once_and_saves_score(self):
        self.game.quizzes = [Quiz("문제", ["1", "2", "3", "4"], 2, "힌트")]

        answer_input = ["1", "", "abc", "0", "5", "h", "h", "2"]
        with patch("builtins.input", side_effect=answer_input):
            with patch(
                "classes.quizgame.random.sample",
                return_value=self.game.quizzes,
            ) as sample:
                with redirect_stdout(io.StringIO()):
                    self.game.play_quiz()

        sample.assert_called_once_with(self.game.quizzes, 1)
        self.assertEqual(self.game.best_record["score"], 90)
        self.assertEqual(self.game.history[0]["hints_used"], 1)
        self.assertTrue(self.state_path.exists())

        loaded_game = QuizGame(self.state_path)
        self.assertEqual(loaded_game.best_record["score"], 90)
        self.assertEqual(len(loaded_game.history), 1)

    def test_add_and_delete_are_saved(self):
        add_input = ["새 문제", "보기 1", "보기 2", "보기 3", "보기 4", "2", "새 힌트"]
        with patch("builtins.input", side_effect=add_input):
            with redirect_stdout(io.StringIO()):
                self.game.add_quiz()

        self.assertEqual(len(QuizGame(self.state_path).quizzes), 6)

        with patch("builtins.input", return_value="6"):
            with redirect_stdout(io.StringIO()):
                self.game.delete_quiz()

        self.assertEqual(len(QuizGame(self.state_path).quizzes), 5)

    def test_empty_quiz_list_remains_empty_after_reload(self):
        self.game.quizzes = [Quiz("문제", ["1", "2", "3", "4"], 1, "힌트")]
        self.game.save_state()

        with patch("builtins.input", return_value="1"):
            with redirect_stdout(io.StringIO()):
                self.game.delete_quiz()

        loaded_game = QuizGame(self.state_path)
        self.assertEqual(loaded_game.quizzes, [])

    def test_broken_json_and_schema_recover_defaults(self):
        self.state_path.write_text("{broken", encoding="utf-8")
        with redirect_stdout(io.StringIO()):
            broken_json_game = QuizGame(self.state_path)
        self.assertEqual(len(broken_json_game.quizzes), 5)

        self.state_path.write_text(
            json.dumps({"quizzes": "잘못된 형식"}, ensure_ascii=False),
            encoding="utf-8",
        )
        with redirect_stdout(io.StringIO()):
            broken_schema_game = QuizGame(self.state_path)
        self.assertEqual(len(broken_schema_game.quizzes), 5)

    def test_interrupted_input_saves_and_exits_without_error(self):
        for error in (EOFError, KeyboardInterrupt):
            with self.subTest(error=error.__name__):
                with patch("builtins.input", side_effect=error):
                    with redirect_stdout(io.StringIO()) as output:
                        self.game.run()

                self.assertIn("게임을 종료합니다", output.getvalue())
                self.assertTrue(self.state_path.exists())

    def test_save_error_returns_false(self):
        unavailable_path = Path(self.temp_directory.name) / "missing" / "state.json"
        game = QuizGame(unavailable_path)

        with redirect_stdout(io.StringIO()):
            result = game.save_state()

        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
