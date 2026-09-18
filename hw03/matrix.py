"""Модуль с классом Matrix для задания 3.1."""

from __future__ import annotations

from collections.abc import Iterator, Sequence
from contextlib import contextmanager

Number = int | float


def parse_number(token: str) -> Number:
    try:
        return int(token)
    except ValueError:
        return float(token)


class Matrix:
    """Класс матрицы с поддержкой арифметики, хеширования и форматирования.

    Примеры использования:
        >>> m = Matrix([[1, 2], [3, 4]])
        >>> m + Matrix([[5, 6], [7, 8]])
        Matrix([[6, 8], [10, 12]])
    """

    def __init__(self, data: Sequence[Sequence[Number]]) -> None:
        self._data: tuple[tuple[Number, ...], ...] = tuple(tuple(row) for row in data)
        if not self._data or not self._data[0]:
            raise ValueError("matrix must have at least one row and one column")
        if len({len(row) for row in self._data}) != 1:
            raise ValueError("all rows must have the same length")
        for row in self._data:
            for value in row:
                if not isinstance(value, (int, float)):
                    raise TypeError(f"matrix elements must be numbers, got {type(value).__name__}")

    @property
    def data(self) -> tuple[tuple[Number, ...], ...]:
        return self._data

    @property
    def rows(self) -> int:
        return len(self._data)

    @property
    def cols(self) -> int:
        return len(self._data[0])

    @property
    def shape(self) -> tuple[int, int]:
        return self.rows, self.cols

    def __getitem__(self, index: int) -> tuple[Number, ...]:
        return self._data[index]

    def __iter__(self) -> Iterator[tuple[Number, ...]]:
        return iter(self._data)

    def __add__(self, other: object) -> Matrix:
        if not isinstance(other, Matrix):
            return NotImplemented
        self._check_same_shape(other)
        return Matrix(
            [
                [left + right for left, right in zip(own, foreign)]
                for own, foreign in zip(self._data, other._data)
            ]
        )

    def __sub__(self, other: object) -> Matrix:
        if not isinstance(other, Matrix):
            return NotImplemented
        self._check_same_shape(other)
        return Matrix(
            [
                [left - right for left, right in zip(own, foreign)]
                for own, foreign in zip(self._data, other._data)
            ]
        )

    def __mul__(self, scalar: object) -> Matrix:
        if not isinstance(scalar, (int, float)):
            return NotImplemented
        return Matrix([[value * scalar for value in row] for row in self._data])

    def __rmul__(self, scalar: object) -> Matrix:
        return self.__mul__(scalar)

    def __matmul__(self, other: object) -> Matrix:
        if not isinstance(other, Matrix):
            return NotImplemented
        if self.cols != other.rows:
            raise ValueError(f"cannot multiply shapes {self.shape} and {other.shape}")
        return Matrix(
            [
                [
                    sum(row[index] * other._data[index][column] for index in range(self.cols))
                    for column in range(other.cols)
                ]
                for row in self._data
            ]
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Matrix):
            return NotImplemented
        return self._data == other._data

    def __hash__(self) -> int:
        return hash(self._data)

    def __repr__(self) -> str:
        return f"Matrix({[list(row) for row in self._data]!r})"

    def __str__(self) -> str:
        return format(self, "")

    def __format__(self, format_spec: str) -> str:
        cells = [[format(value, format_spec) for value in row] for row in self._data]
        width = max(len(cell) for row in cells for cell in row)
        return "\n".join(" ".join(cell.rjust(width) for cell in row) for row in cells)

    @classmethod
    def parse(cls, text: str) -> Matrix:
        data = [
            [parse_number(token) for token in line.split()]
            for line in text.splitlines()
            if line.strip()
        ]
        if not data:
            raise ValueError("text contains no numbers")
        return cls(data)

    @classmethod
    @contextmanager
    def from_file(cls, path: str) -> Iterator[Matrix]:
        """Контекстный менеджер для чтения матрицы из файла.

        Использование::

            with Matrix.from_file("data.txt") as m:
                print(m)

        Формат файла: строки матрицы, элементы через пробел.
        """
        with open(path, encoding="utf-8") as stream:
            matrix = cls.parse(stream.read())
        yield matrix

    def _check_same_shape(self, other: Matrix) -> None:
        if self.shape != other.shape:
            raise ValueError(f"shapes {self.shape} and {other.shape} do not match")
