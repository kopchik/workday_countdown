#!/usr/bin/env python3

"""
Hello Workday,

I'm Alex and here is my code. It is too verbose at times,
but that's intentionally.

I decided to use functional approach to this problem
because it maps better to this task than OOP.

I had two versions: one bruteforce and one with heuristic,
but heuristic was too complicated. So I chose the simple approach
over more complicated one because debugging it and writing
tests would be a nightmare.

Some functions have "my" prefix to avoid collision with built-in
python functions like eval or format.

``Expression'' (expr) is really a tuple of numbers and corresponding
operators to apply. Operators' precedences does not apply,
expressions are evaluated from left to right.

I tried to make functions ``robust'' without bloating code
with too many checks.

Tests are done with py.test and are in the separate file.
To be launched as `py.test ./workday_countdown_test.py' .

The formatting does not take care much about operator precedence:
it just uses parentheses to make correct expressions.
Let me know if this an issue, I'll fix this with
Shunting-yard algorithm.
"""


from operator import add, sub, mul, truediv
from itertools import permutations, combinations_with_replacement


operators = [add, sub, mul, truediv]
symap = {add: '+', sub: '-', mul: '*', truediv: '/'}


def myeval(nums, ops):
    """ Evaluates raw expression. May raise exception like ZeroDivisionError. """
    r = nums[0]
    for i, op in enumerate(ops):
        r = op(r, nums[i + 1])
    return r


def _countdown(numbers, target, operators=operators):
    """ It plays countdown game (seems very popular in  Ireland).

    Parameters
    ----------
    numbers: list of integers in [0, 1024] (not really checked here)
    target:  value we should get at the end
    operators: allowed operation to achieve the target value

    Returns
    -------
    Raw expression along with the result.
    """

    best_value = numbers[0]
    best_expr = ([numbers[0]], [])
    best_error = abs(best_value - target)

    for i in range(1, len(numbers) + 1):
        for nums in permutations(numbers, i):
            for ops in combinations_with_replacement(operators, len(nums) - 1):
                try:
                    r = myeval(nums, ops)
                except Exception:
                    continue
                err = abs(target - r)
                #print(">", nums, ops, r, err)
                if err < best_error:
                    if r == target:
                        return (nums, ops), r  # shortcut if we found solution
                    else:
                        best_expr = nums, ops
                        best_error = err
                        best_value = r
    return best_expr, best_value


def myformat(expr, value):
    """ It does what is says :) """
    nums, ops = expr
    result = [nums[0]]
    for num, op in zip(nums[1:], ops):
        result.append(symap[op])
        result.append(num)
        if op in [add, sub]:
            result.insert(0, '(')
            result.append(')')
    result.append('=')
    result.append(value)
    return " ".join(map(str, result))


def countdown(rawinpt):
    """ Converts input string into python-friendly format: 6 numbers and target value.
        Then calls _countdown and myformat to produce the actual result.
        Also does input validation.
    """
    assert isinstance(rawinpt, str), "needs string as input"
    inpt = list(map(int, rawinpt.split()))
    assert all(n in range(0, 1024) for n in inpt), "input value not in range"
    assert len(inpt) == 7, "expected 7 numbers, got %s" % len(inpt)
    *numbers, target = inpt
    expr, result = _countdown(numbers, target)
    return myformat(expr, result)


if __name__ == '__main__':
    inpt = input("Enter 7 numbers: ")
    print(countdown(inpt))
