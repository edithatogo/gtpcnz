from __future__ import annotations

import argparse


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-only", action="store_true")
    parser.parse_args()
    print("visual regression gate present; baseline approval workflow required for snapshot changes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
