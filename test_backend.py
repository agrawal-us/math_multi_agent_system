import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    force=True,
)

from math_agent_backend.graph.workflow import run_workflow


def test_solve():
    print("\n--- SOLVE TEST ---")
    response = run_workflow("solve 2x + 5 = 11")
    print(response)


def test_concept():
    print("\n--- CONCEPT TEST ---")
    response = run_workflow("explain derivative")
    print(response)


def test_quiz():
    print("\n--- QUIZ TEST ---")
    response = run_workflow("generate 3 medium questions on algebra")
    print(response)


def test_invalid():
    print("\n--- INVALID TEST ---")
    response = run_workflow("solve nonsense")
    print(response)


if __name__ == "__main__":
    test_solve()
    test_concept()
    test_quiz()
    test_invalid()
