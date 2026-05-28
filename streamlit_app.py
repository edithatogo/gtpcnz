import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

def main() -> None:
    from models.primarycare_model.app import render_app

    render_app()


if __name__ == "__main__":
    main()
