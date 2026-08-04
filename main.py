from pathlib import Path

from classes.quizgame import QuizGame

Default_Path = './state.json'

def main():
    # state_path = Path(__file__).with_name("state.json")
    game = QuizGame(Default_Path)

    try :
        game.run()
    except (KeyboardInterrupt, EOFError):
        print("예외처리 나중에 해놓기")


if __name__ == "__main__":
    main()
