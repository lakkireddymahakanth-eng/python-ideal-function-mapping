# Src/DataProcessor.py
import numpy as np
from math import sqrt


class DataProcessor:
    def __init__(self, train_df, ideal_df):
        self.train = train_df.sort_values('x').reset_index(drop=True)
        self.ideal = ideal_df.sort_values('x').reset_index(drop=True)  # Fixed typo!
        self.train_cols = ['y1', 'y2', 'y3', 'y4']

    def least_squares_deviation(self, train_y, ideal_y):
        return np.sum((train_y - ideal_y) ** 2)

    def select_best_functions(self):
        mapping = {}
        for col in self.train_cols:
            train_y = self.train[col].values
            min_dev = float('inf')
            best_ideal = None
            for i in range(1, 51):
                ideal_col = f'y{i}'
                dev = self.least_squares_deviation(train_y, self.ideal[ideal_col].values)
                if dev < min_dev:
                    min_dev = dev
                    best_ideal = ideal_col
            mapping[col] = (best_ideal, min_dev)
        return mapping

    def map_test_points(self, test_df, mapping):
        results = []
        threshold_factor = sqrt(2)

        for _, row in test_df.iterrows():
            x, y = row['x'], row['y']
            mapped = False

            for train_col, (ideal_col, train_dev) in mapping.items():
                ideal_row = self.ideal[self.ideal['x'] == x]
                if ideal_row.empty:
                    continue
                ideal_y = ideal_row[ideal_col].iloc[0]
                delta = abs(y - ideal_y)
                threshold = threshold_factor * sqrt(train_dev / len(self.train))

                if delta <= threshold:
                    results.append({
                        'x': x,
                        'y': y,
                        'delta_y': round(delta, 6),
                        'ideal_function_no': ideal_col
                    })
                    mapped = True
                    break

            if not mapped:
                print(f"Info: Test point (x={x}, y={y}) is an outlier → not mapped (normal)")

        return results