# Src/main.py

import os
import pandas as pd

# ✅ Use relative imports inside the Src package
from .DataProcessor import DataProcessor
from .Database import DatabaseHandler
from .visualization import Visualizer
from .exceptions import DataFormatError, FunctionMappingError


def load_csv(path, expected_cols):
    if not os.path.exists(path):
        raise DataFormatError(f"File not found: {path}")
    df = pd.read_csv(path)
    missing = [col for col in expected_cols if col not in df.columns]
    if missing:
        raise DataFormatError(f"{path} missing columns: {missing}")
    return df


def main():
    try:
        # Base project directory = one level above Src
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_dir = os.path.join(base_dir, "Data")
        output_dir = os.path.join(base_dir, "Output")

        print("Loading datasets...")
        train = load_csv(os.path.join(data_dir, "train.csv"), ['x', 'y1', 'y2', 'y3', 'y4'])
        ideal = load_csv(
            os.path.join(data_dir, "ideal.csv"),
            ['x'] + [f'y{i}' for i in range(1, 51)]
        )
        test = load_csv(os.path.join(data_dir, "test.csv"), ['x', 'y'])

        processor = DataProcessor(train, ideal)
        db_path = os.path.join(output_dir, "idealFunctions.db")
        db = DatabaseHandler(db_path)
        viz = Visualizer()

        print("Selecting best ideal functions...")
        mapping = processor.select_best_functions()
        for train_col, (ideal_col, dev) in mapping.items():
            print(f"Selected {ideal_col} for {train_col} (dev={dev:.4f})")

        db.insert_train_data(train)
        db.insert_ideal_data(ideal)

        print("Mapping test points...")
        results = processor.map_test_points(test, mapping)
        for res in results:
            db.insert_test_result(res)

        print("Generating visualization...")
        html_path = os.path.join(output_dir, "FunctionMapping.html")
        viz.plot_all(train, ideal, test, mapping, results, html_path)

        print("\nSUCCESS! Everything completed perfectly!")
        print(f"Open: {html_path}")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
