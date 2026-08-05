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
        print("\n입력이 중단되었습니다.")
        
        if game.game_save():
                print("현재 데이터를 저장했습니다.")
        else:
            print("현재 데이터를 저장하지 못했습니다.")

        print("게임을 안전하게 종료합니다.")

if __name__ == "__main__":
    main()
