import os, sys
from importlib import import_module

if __name__ == "__main__":
    path = os.path.join(os.path.dirname(__file__), 'GUI')
    sys.path.append(path)
    import GUI
    GUI.main()