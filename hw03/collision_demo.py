"""Демонстрация хеширования и коллизий для задания 3.3."""

from hw03.matrix import Matrix


def demonstrate_set_dict() -> dict:
    """Демонстрация использования Matrix в set и dict.

    Returns:
        dict с ключами:
        - "matrices_in_set": set из Matrix объектов
        - "matrix_dict": dict с Matrix ключами
    """
    identity = Matrix([[1, 0], [0, 1]])
    doubled = identity * 2
    return {
        "matrices_in_set": {identity, doubled, Matrix([[1, 0], [0, 1]])},
        "matrix_dict": {identity: "identity", doubled: "doubled"},
    }


# зачем нужно a == b -> hash(a) == hash(b): корзину ищут по хешу, а ключи внутри
# сверяют через __eq__. если у равных объектов хеши разные, они улетят в разные
# корзины: один и тот же ключ ляжет в dict дважды, а in начнёт врать. наоборот
# можно, это просто коллизия, её разрулит __eq__, только поиск чуть медленнее
def demonstrate_collision() -> tuple[Matrix, Matrix]:
    """Демонстрация коллизии хешей.

    Returns:
        Кортеж из двух матриц (m1, m2), где:
        - m1 != m2 (разные матрицы)
        - hash(m1) == hash(m2) (одинаковый хеш)
    """
    # честная коллизия, без подмены __hash__: в CPython hash(-1) и hash(-2) оба -2,
    # а хеш кортежа складывается из хешей элементов
    return Matrix([[-1, -1], [-1, -1]]), Matrix([[-2, -2], [-2, -2]])


if __name__ == "__main__":
    print("=== Демонстрация Matrix в set/dict ===")
    result = demonstrate_set_dict()
    print(f"Матрицы в set: {result['matrices_in_set']}")
    print(f"Matrix dict: {result['matrix_dict']}")

    print("\n=== Демонстрация коллизии хешей ===")
    m1, m2 = demonstrate_collision()
    print(f"m1 = {m1!r}")
    print(f"m2 = {m2!r}")
    print(f"m1 == m2: {m1 == m2}")
    print(f"hash(m1) == hash(m2): {hash(m1) == hash(m2)}")
    print(f"Обе в set: { {m1, m2} }")
