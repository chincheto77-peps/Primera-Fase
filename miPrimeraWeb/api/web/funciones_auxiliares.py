import decimal
import json

class Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal): return float(obj)


def calculariva(base, tasa=21):
    """Calcular el IVA de una base imponible.

    Args:
        base (int|float|Decimal): importe sobre el que calcular el IVA.
        tasa (int|float): porcentaje de IVA (por ejemplo 21 para 21%).

    Returns:
        float: importe del IVA redondeado a 2 decimales.
    """
    valor = float(base) * float(tasa) / 100.0
    # Redondeamos a 2 decimales para un comportamiento predecible
    return round(valor, 2)


