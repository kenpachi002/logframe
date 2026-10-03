from __future__ import annotations

import random

from case import Case


def generate_fuzz_cases(
    valid_cases: list[Case], count: int = 300, seed: int = 20261003
) -> list[Case]:
    """Apply seeded, bounded mutations to valid input lines."""
    rng = random.Random(seed)
    cases: list[Case] = []
    operations = ("delete", "swap", "control", "duplicate", "case")

    for index in range(count):
        source = valid_cases[index % len(valid_cases)].line
        mutated = source
        for _ in range(rng.randint(1, 3)):
            operation = rng.choice(operations)
            if operation == "delete" and mutated:
                start = rng.randrange(len(mutated))
                mutated = mutated[:start] + mutated[start + rng.randint(1, 4):]
            elif operation == "swap" and len(mutated) > 1:
                start = rng.randrange(len(mutated) - 1)
                chars = list(mutated)
                chars[start], chars[start + 1] = chars[start + 1], chars[start]
                mutated = "".join(chars)
            elif operation == "control":
                start = rng.randrange(len(mutated) + 1)
                mutated = mutated[:start] + "\x00" + mutated[start:]
            elif operation == "duplicate" and mutated:
                start = rng.randrange(len(mutated))
                end = min(len(mutated), start + rng.randint(1, 8))
                mutated = mutated[:end] + mutated[start:end] + mutated[end:]
            elif operation == "case" and mutated:
                start = rng.randrange(len(mutated))
                char = mutated[start]
                mutated = mutated[:start] + char.swapcase() + mutated[start + 1:]

        cases.append(Case(
            id=f"FUZZ-{index + 1:03}", line=mutated, expect="fuzz",
            note=f"Seed {seed}; mutations applied to corpus case {valid_cases[index % len(valid_cases)].id}.",
        ))

    return cases