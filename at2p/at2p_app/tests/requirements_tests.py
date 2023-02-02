# from django.test import TestCase
# from at2p_app.domain.common.temperature import (
#     TempRange,
#     Temperature,
# )
# from at2p_app.domain.common.requirements import (
#     TemperatureChecker,
#     TempReq,
#     TempRequirmentChecker,
#     AbsoluteTempReqChecker,
#     OptimalTempReqChecker,
# )


# class TempRangeCheckerTests(TestCase):
#     def setUp(self) -> None:
#         self.r = TempRange(1, 100)
#         self.check = TemperatureChecker(self.r)

#         return super().setUp()

#     def test_instantiation(self):
#         self.assertIsInstance(self.check, TemperatureChecker)

#     def test_check_a_temp(self):
#         t = Temperature(50)
#         self.assertTrue(self.check.temp_in_range(t))
#         t = Temperature(10000)
#         self.assertFalse(self.check.temp_in_range(t))

#     def test_a_range(self):
#         inner_range = TempRange(40, 60)
#         self.assertTrue(self.check.range_in_range(inner_range))

#         outer_range = TempRange(0, 200)
#         self.assertFalse(self.check.range_in_range(outer_range))

#         crossing_range = TempRange(50, 200)
#         self.assertFalse(self.check.range_in_range(crossing_range))


# class RequirementsTests(TestCase):
#     def setUp(self) -> None:
#         optimal = TempRange(60, 70)
#         absolute = TempRange(40, 90)
#         self.optimal = TempReq(optimal)
#         self.absolute = TempReq(absolute)
#         self.opt_check = OptimalTempReqChecker(self.optimal)
#         self.abs_check = AbsoluteTempReqChecker(self.absolute)
#         return super().setUp()

#     def test_instantiation(self):
#         self.assertIsInstance(self.opt_check, OptimalTempReqChecker)
#         self.assertIsInstance(self.abs_check, AbsoluteTempReqChecker)

