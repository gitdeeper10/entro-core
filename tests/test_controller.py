"""
Unit tests for ENTRO-CORE controller
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from entro_core import (
    normalize_psi,
    compute_control,
    sigmoid,
    tanh,
    ActuationStrategy,
    apply_actuation,
    ENTROCOREController,
    create_controller
)


class TestNormalization(unittest.TestCase):
    def test_normalize_zero(self):
        self.assertEqual(normalize_psi(0), 0.0)
    
    def test_normalize_positive(self):
        result = normalize_psi(1.0)
        self.assertGreater(result, 0)
        self.assertLess(result, 2.0)
    
    def test_normalize_known(self):
        # Known values from Perplexity case
        self.assertAlmostEqual(normalize_psi(48.3), 1.657, places=2)
    
    def test_normalize_large(self):
        result = normalize_psi(1000)
        self.assertLess(result, 2.0)


class TestSigmoid(unittest.TestCase):
    def test_sigmoid_zero(self):
        self.assertEqual(sigmoid(0), 0.5)
    
    def test_sigmoid_positive(self):
        self.assertGreater(sigmoid(1), 0.5)
        self.assertLess(sigmoid(1), 1.0)
    
    def test_sigmoid_negative(self):
        self.assertLess(sigmoid(-1), 0.5)
        self.assertGreater(sigmoid(-1), 0.0)


class TestTanh(unittest.TestCase):
    def test_tanh_zero(self):
        self.assertEqual(tanh(0), 0.0)
    
    def test_tanh_positive(self):
        self.assertGreater(tanh(1), 0)
        self.assertLess(tanh(1), 1)
    
    def test_tanh_negative(self):
        self.assertLess(tanh(-1), 0)
        self.assertGreater(tanh(-1), -1)


class TestControlLaw(unittest.TestCase):
    def test_control_bounds(self):
        u = compute_control(0.5, 0, 0)
        self.assertGreaterEqual(u, 0)
        self.assertLessEqual(u, 1)
    
    def test_control_increases_with_psi(self):
        u1 = compute_control(0.5, 0, 0)
        u2 = compute_control(1.5, 0, 0)
        self.assertGreaterEqual(u2, u1)
    
    def test_control_increases_with_velocity(self):
        u1 = compute_control(1.0, 0, 0)
        u2 = compute_control(1.0, 0.5, 0)
        self.assertGreaterEqual(u2, u1)


class TestActuation(unittest.TestCase):
    def test_linear(self):
        result = apply_actuation(0.58, ActuationStrategy.LINEAR)
        self.assertEqual(result, 0.58)
    
    def test_exponential(self):
        result = apply_actuation(0.58, ActuationStrategy.EXPONENTIAL)
        self.assertGreater(result, 0.58)
        self.assertLess(result, 1.0)
    
    def test_quadratic(self):
        result = apply_actuation(0.58, ActuationStrategy.QUADRATIC)
        self.assertLess(result, 0.58)
    
    def test_threshold(self):
        result = apply_actuation(0.2, ActuationStrategy.THRESHOLD)
        self.assertEqual(result, 0.0)
        
        result = apply_actuation(0.5, ActuationStrategy.THRESHOLD)
        self.assertEqual(result, 0.5)


class TestController(unittest.TestCase):
    def test_controller_creation(self):
        controller = create_controller("linear")
        self.assertIsNotNone(controller)
    
    def test_controller_step(self):
        controller = create_controller("linear")
        output = controller.step(1.0)
        self.assertIsNotNone(output)
        self.assertGreaterEqual(output.u, 0)
        self.assertLessEqual(output.u, 1)
    
    def test_controller_sequence(self):
        controller = create_controller("exponential")
        psi_values = [0.5, 0.8, 1.2, 1.6, 1.9, 2.1, 1.8, 1.4, 1.1, 0.9]
        
        for psi in psi_values:
            output = controller.step(psi)
            self.assertIsNotNone(output)
    
    def test_controller_reset(self):
        controller = create_controller("linear")
        controller.step(1.0)
        controller.reset()
        self.assertIsNone(controller.last_output)


if __name__ == "__main__":
    unittest.main()
