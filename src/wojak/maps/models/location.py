from typing import List, Tuple


class BaseLocation:
    name: str
    description: str
    coordinates: Tuple[float, float]


class GoogleLocation(BaseLocation):
    review_count: str
    review_rating: float
    types: List[str]

