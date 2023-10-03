from typing import Union


class A:
    x = 1

    def divide(self, a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
        if not isinstance(a, Union[int, float]) and not isinstance(
            b, Union[int, float]
        ):
            raise TypeError
        if b == 0:
            raise ZeroDivisionError
        return a / b

    def multiply(self, a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
        return a * b
