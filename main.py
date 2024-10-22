from gui import MinesweeperGUI
from event_dispatcher import EventDispatcher
from settings import Settings

def main():
    dispatcher = EventDispatcher()
    settings = Settings()
    app = MinesweeperGUI(settings, dispatcher)
    app.run()

if __name__ == "__main__":
    main()
