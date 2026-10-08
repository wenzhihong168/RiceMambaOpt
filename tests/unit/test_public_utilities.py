import unittest

from ricemambaopt.datasets import (
    InverseDesignRequest,
    MillingObservation,
    ProcessBounds,
    StudyRole,
)
from ricemambaopt.evaluation.metrics import (
    joint_normalized_rmse,
    per_target_metrics,
    regression_metrics,
)
from ricemambaopt.optimization import (
    ConstraintSet,
    LinearConstraint,
    weighted_normalized_squared_error,
)


class SchemaTests(unittest.TestCase):
    def test_observation_and_request_validate_units(self):
        observation = MillingObservation(
            "sample-1",
            "batch-1",
            "cultivar-a",
            30.0,
            1200.0,
            {"hardness": 4.2, "digestibility": 0.7},
            StudyRole.DEVELOPMENT,
        )
        bounds = ProcessBounds((10.0, 60.0), (800.0, 1600.0))
        request = InverseDesignRequest(
            "cultivar-a", {"hardness": 4.0}, bounds=bounds
        )
        self.assertTrue(bounds.contains(observation.time_seconds, observation.speed_rpm))
        self.assertEqual(request.weights["hardness"], 1.0)

    def test_mismatched_weights_are_rejected(self):
        with self.assertRaises(ValueError):
            InverseDesignRequest("a", {"x": 1.0}, {"y": 1.0})


class MetricTests(unittest.TestCase):
    def test_regression_metrics(self):
        metrics = regression_metrics([1.0, 2.0, 3.0], [1.0, 2.0, 4.0])
        self.assertAlmostEqual(metrics.mae, 1 / 3)
        self.assertAlmostEqual(metrics.bias, 1 / 3)
        self.assertLess(metrics.r2, 1.0)

    def test_multi_target_metrics_and_joint_normalization(self):
        truth = {"a": [0.0, 1.0], "b": [10.0, 12.0]}
        prediction = {"a": [0.0, 2.0], "b": [10.0, 10.0]}
        results = per_target_metrics(truth, prediction)
        self.assertEqual(set(results), {"a", "b"})
        value = joint_normalized_rmse(truth, prediction, {"a": 1.0, "b": 2.0})
        self.assertGreater(value, 0.0)


class OptimizationTests(unittest.TestCase):
    def setUp(self):
        bounds = ProcessBounds((10.0, 60.0), (800.0, 1600.0))
        dose = LinearConstraint("dose", 10.0, 0.1, "<=", 650.0)
        self.constraints = ConstraintSet(bounds, (dose,))

    def test_constraints_return_named_residuals(self):
        feasible = self.constraints.evaluate(30.0, 1200.0)
        infeasible = self.constraints.evaluate(60.0, 1600.0)
        self.assertTrue(feasible.feasible)
        self.assertFalse(infeasible.feasible)
        self.assertIn("dose", infeasible.violations)

    def test_projection_and_objective(self):
        self.assertEqual(self.constraints.project_to_bounds(5.0, 2000.0), (10.0, 1600.0))
        error = weighted_normalized_squared_error(
            {"a": 3.0, "b": 8.0},
            {"a": 2.0, "b": 10.0},
            {"a": 1.0, "b": 2.0},
            {"a": 1.0, "b": 3.0},
        )
        self.assertAlmostEqual(error, 1.0)


if __name__ == "__main__":
    unittest.main()
