import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from ui.web_app import launch_web_gui

def main():
    try:
        launch_web_gui()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"Error starting Apex Hub: {e}")

if __name__ == "__main__":
    main()
