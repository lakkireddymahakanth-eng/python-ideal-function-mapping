import sys

class DataFormatError(Exception):
    """Raised when CSV is missing required columns."""
    def __init__(self, message="CSV file has incorrect or missing columns"):
        self.message = message
        super().__init__(self.message)


class FunctionMappingError(Exception):
    """Raised when test point cannot be mapped to any ideal function."""
    def __init__(self, x_value, y_value):
        self.message = f"Test point (x={x_value}, y={y_value}) cannot be mapped to any ideal function"
        super().__init__(self.message)
