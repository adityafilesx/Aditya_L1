import numpy as np
from typing import List, Tuple

class TimeSeriesCrossValidator:
    """Implements time-series safe validation strategies to prevent data leakage."""
    
    @staticmethod
    def walk_forward_split(n_samples: int, n_splits: int = 5, test_size: int = None) -> List[Tuple[np.ndarray, np.ndarray]]:
        """Walk Forward Validation: expands the training window, testing on the next chunk."""
        indices = np.arange(n_samples)
        if test_size is None:
            test_size = int(n_samples / (n_splits + 1))
            
        splits = []
        for i in range(n_splits):
            train_end = test_size + i * test_size
            test_end = train_end + test_size
            if test_end > n_samples:
                test_end = n_samples
                
            train_idx = indices[:train_end]
            test_idx = indices[train_end:test_end]
            if len(test_idx) > 0:
                splits.append((train_idx, test_idx))
        return splits

    @staticmethod
    def rolling_window_split(n_samples: int, n_splits: int = 5, window_size: int = None, test_size: int = None) -> List[Tuple[np.ndarray, np.ndarray]]:
        """Rolling Window Validation: fixed-size training window that slides forward."""
        indices = np.arange(n_samples)
        if test_size is None:
            test_size = int(n_samples / (n_splits + 1))
        if window_size is None:
            window_size = test_size * 2
            
        splits = []
        for i in range(n_splits):
            train_start = i * test_size
            train_end = train_start + window_size
            test_end = train_end + test_size
            if test_end > n_samples:
                break
                
            train_idx = indices[train_start:train_end]
            test_idx = indices[train_end:test_end]
            splits.append((train_idx, test_idx))
        return splits

    @staticmethod
    def blocked_time_series_split(n_samples: int, n_splits: int = 5) -> List[Tuple[np.ndarray, np.ndarray]]:
        """Blocked Time Series Validation: splits the dataset into non-overlapping blocks of train/test."""
        indices = np.arange(n_samples)
        block_size = int(n_samples / n_splits)
        
        splits = []
        for i in range(n_splits):
            start = i * block_size
            end = start + block_size
            if i == n_splits - 1:
                end = n_samples
                
            # Within each block, e.g. 80% train, 20% test
            mid = start + int((end - start) * 0.8)
            train_idx = indices[start:mid]
            test_idx = indices[mid:end]
            if len(train_idx) > 0 and len(test_idx) > 0:
                splits.append((train_idx, test_idx))
        return splits
