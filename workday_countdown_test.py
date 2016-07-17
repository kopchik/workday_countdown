"""
These are tests for code of countdown problem.
Most of them are ``full-stack''.
"""


from workday_countdown import countdown, _countdown, myformat
from operator import mul, add
import pytest
import cProfile

def test_countdown_input_validation():
  # not enough arguments
  with pytest.raises(AssertionError):
    countdown("1 2 3")

  # negative arguments
  with pytest.raises(AssertionError):
    countdown("1 2 3 4 5 6 -7")


def test_countdown_correctness():
  # trivial case
  assert countdown("1 2 3 4 5 6 1") == "1 = 1"

  # provided examples
  assert countdown("1 2 3 4 5 6 12") == "2 * 6 = 12"
  assert countdown("5 8 6 25 13 87 390") == "5 * 6 * 13 = 390"

  # operations with zeros (incl. div by zero)
  assert countdown("0 0 0 0 0 0 1000") == "0 = 0"


def test_countdown_performance():
  """ Evaluates the performance in the worst case. """
  profiler = cProfile.Profile()
  profiler.enable()
  countdown("0 0 0 0 0 0 1000")
  profiler.disable()
  stats = profiler.getstats()
  tot_time = stats[0].totaltime
  assert tot_time < 3, "Wow, your computer is really slow. Or is it my code?"


def test_myformat():
  # test parentheses
  assert myformat(expr=([1,2],[add]),value=3) == "( 1 + 2 ) = 3"
  assert myformat(expr=([1,2,3],[add, mul]),value=9) == "( 1 + 2 ) * 3 = 9"
