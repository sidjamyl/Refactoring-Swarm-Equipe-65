# sandbox/good_code.py
"""Module de fonctions arithmétiques simples."""

from typing import Union


Number = Union[int, float]


def add(a: Number, b: Number) -> Number:
    """Retourne la somme de a et b."""
    return a + b


def multiply(a: Number, b: Number) -> Number:
    """Retourne le produit de a et b."""
    return a * b


def main() -> None:
    """Point d'entrée simple pour tester les fonctions."""
    result_add = add(2, 3)
    result_mul = multiply(2, 3)
    print("Addition:", result_add)
    print("Multiplication:", result_mul)


if __name__ == "__main__":
    main()
