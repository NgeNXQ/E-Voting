def get_divisors(number: int) -> list[int]:
    divisors = set()

    for i in range(1, int(number ** 0.5) + 1):
        if number % i == 0:
            divisors.add(i)
            divisors.add(number // i)

    return sorted(divisors)

def get_factors_pairs(number: int, is_prime_factor_allowed: bool) -> list[tuple[int, int]]:
    factor: int = 0
    divisors: list[int] = get_divisors(number)
    factors_pairs: list[tuple[int, int]] = list()

    for divisor in divisors:
        factor = number // divisor

        if divisor * factor != number:
            continue

        if not is_prime_factor_allowed and (divisor == number or factor == number):
            continue

        factors_pairs.append((divisor, factor))

    return factors_pairs
