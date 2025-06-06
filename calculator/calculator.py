# filepath: calculator/calculator.py
"""Implementación del servicio de calculadora remota."""

import Ice
import RemoteCalculator

class Calculator(RemoteCalculator.Calculator):
    """Implementación de la interfaz RemoteCalculator.Calculator."""

    def sum(self, a: float, b: float, current: Ice.Current = None) -> float:
        """Calcula la suma de dos números."""
        print(f"Sumando {a} + {b}")
        return a + b

    def sub(self, a: float, b: float, current: Ice.Current = None) -> float:
        """Calcula la resta de dos números."""
        print(f"Restando {a} - {b}")
        return a - b

    def mult(self, a: float, b: float, current: Ice.Current = None) -> float:
        """Calcula la multiplicación de dos números."""
        print(f"Multiplicando {a} * {b}")
        return a * b

    def div(self, a: float, b: float, current: Ice.Current = None) -> float:
        """Calcula la división de dos números. Lanza ZeroDivisionError si b es cero."""
        print(f"Dividiendo {a} / {b}")
        if b == 0:
            raise RemoteCalculator.ZeroDivisionError()
        return a / b
