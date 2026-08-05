from pathlib import Path
from classes.quizgame import QuizGame

# 이럼 루트에 state.json보장이 안됨
# Default_Path = './state.json'

def main():
    # resolve -> 절대경로로 변환, 
    project_root = Path(__file__).resolve().parent
    print(Path(__file__).resolve())

    state_path = project_root / "state.json"

    game = QuizGame(state_path)

    try :
        game.run()
    except (KeyboardInterrupt, EOFError):
        print("예외처리 나중에 해놓기")


if __name__ == "__main__":
    main()
