import numpy as np
from typing import List

def normalize_vector(v: np.ndarray) -> np.ndarray:
    """Normalize a vector to unit length."""
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm

def weighted_average(vectors: List[np.ndarray], weight: float) -> np.ndarray:
    """Calculate the weighted average of a list of vectors."""
    if not vectors:
        return np.array([])
    return np.mean(vectors, axis=0) * weight
