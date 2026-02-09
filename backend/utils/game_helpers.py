import random
from typing import List, Dict, Any

def roll_dice(sides: int, count: int = 1) -> List[int]:
    return [random.randint(1, sides) for _ in range(count)]

def roll_d20() -> int:
    return random.randint(1, 20)

def roll_d6() -> int:
    return random.randint(1, 6)

def calculate_modifier(stat: int) -> int:
    return (stat - 10) // 2

def shuffle_deck(deck: List[Any]) -> List[Any]:
    shuffled = deck.copy()
    random.shuffle(shuffled)
    return shuffled

def draw_cards(deck: List[Any], count: int) -> tuple:
    drawn = []
    for _ in range(min(count, len(deck))):
        if deck:
            drawn.append(deck.pop())
    return drawn, deck

def calculate_distance(pos1: tuple, pos2: tuple) -> float:
    x1, y1 = pos1
    x2, y2 = pos2
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

def get_adjacent_positions(pos: tuple, grid_size: tuple) -> List[tuple]:
    x, y = pos
    max_x, max_y = grid_size
    
    adjacent = []
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < max_x and 0 <= new_y < max_y:
                adjacent.append((new_x, new_y))
    
    return adjacent

def format_resource_display(resources: Dict[str, int]) -> str:
    parts = []
    for resource, amount in resources.items():
        parts.append(f"{resource}: {amount}")
    return " | ".join(parts)