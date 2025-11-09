import unittest
from unittest.mock import Mock
from simulator import SimuladorDescarga

class TestSimulador(unittest.TestCase):
    def setUp(self):
        self.logger = Mock()
        self.simulador = SimuladorDescarga(1.0, 0.375, self.logger)

    def test_iniciar_simulacion(self):
        inicio, fin = self.simulador.iniciar(1.0)
        self.assertIsInstance(inicio, type(fin))
        self.assertLessEqual(inicio, fin)

if __name__ == '__main__':
    unittest.main()
