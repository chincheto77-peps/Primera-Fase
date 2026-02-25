from api.web.funciones_auxiliares import calculariva


def test_calculariva100():
    resultado_esperado = 21
    resultado = calculariva(100)
    assert resultado == resultado_esperado


def test_calculariva_zero():
    assert calculariva(0) == 0


def test_calculariva_decimal():
    # comprobamos redondeo a 2 decimales
    esperado = round(19.99 * 21 / 100, 2)
    assert calculariva(19.99) == esperado
