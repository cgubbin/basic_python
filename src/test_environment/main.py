"""The main entry point to our module."""

import numpy as np
import numpy.typing as npt


def sum_of_vector(vector: npt.NDArray[np.float_]) -> np.float_:
    """Sum a 1-dimensional array.

    Sums all elements in the input array which is assumed 1D

    Args:
        vector: The input vector: a 1D array of floats

    Returns:
        A float

    Example:
        >>> import numpy as np
        >>> x = np.array([1.0, 2.0, 3.0])
        >>> sum = sum_of_vector(x)
        >>> sum == 6.0
        True
    """
    result: np.float_ = np.sum(vector)
    return result


x: npt.NDArray[np.float64] = np.array([1.0, 1.0, 1.0, 1.0, 1.0])
result: np.float64 = sum_of_vector(x)
print(f"The result is {result}, from the sum of {x}")
