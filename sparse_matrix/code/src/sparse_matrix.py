import sys


class SparseMatrix:
    def __init__(self, rows=0, cols=0):
        self.rows_count = rows
        self.cols_count = cols
        self.values = {}

    @staticmethod
    def create_from_file(file_path):
        try:
            with open(file_path, 'r') as f:
                lines = f.readlines()
                rows = int(lines[0].strip().split('=')[1])
                cols = int(lines[1].strip().split('=')[1])
                matrix = SparseMatrix(rows, cols)
                for line in lines[2:]:
                    line = line.strip()
                    if not line:
                        continue
                    if line[0] != '(' or line[-1] != ')':
                        raise ValueError("Incorrect format in input file")
                    row, col, value = map(int, line[1:-1].split(','))
                    matrix.set_value(row, col, value)
                return matrix
        except Exception as e:
            raise ValueError(f"Error while processing file {file_path}: {e}")

    def set_value(self, row, col, value):
        if value != 0:
            self.values[(row, col)] = value
        elif (row, col) in self.values:
            del self.values[(row, col)]

    def get_value(self, row, col):
        return self.values.get((row, col), 0)

    def addition(self, other):
        if self.rows_count != other.rows_count or self.cols_count != other.cols_count:
            raise ValueError("Matrix dimensions must match for addition operation")
        result = SparseMatrix(self.rows_count, self.cols_count)
        for (row, col), value in self.values.items():
            result.set_value(row, col, value + other.get_value(row, col))
        for (row, col), value in other.values.items():
            if (row, col) not in self.values:
                result.set_value(row, col, value)
        return result

    def subtraction(self, other):
        if self.rows_count != other.rows_count or self.cols_count != other.cols_count:
            raise ValueError("Matrix dimensions must match for subtraction operation")
        result = SparseMatrix(self.rows_count, self.cols_count)
        for (row, col), value in self.values.items():
            result.set_value(row, col, value - other.get_value(row, col))
        for (row, col), value in other.values.items():
            if (row, col) not in self.values:
                result.set_value(row, col, -value)
        return result

    def multiplication(self, other):
        if self.cols_count != other.rows_count:
            raise ValueError(f"Matrix dimensions must match for multiplication: {self.cols_count} (cols) != {other.rows_count} (rows)")
        result = SparseMatrix(self.rows_count, other.cols_count)
        for (row, col), value in self.values.items():
            for k in range(other.cols_count):
                if (col, k) in other.values:
                    result.set_value(row, k, result.get_value(row, k) + value * other.get_value(col, k))
        return result

    def write_to_file(self, file_path):
        with open(file_path, 'w') as f:
            f.write(f"rows={self.rows_count}\n")
            f.write(f"cols={self.cols_count}\n")
            for (row, col), value in sorted(self.values.items()):
                f.write(f"({row}, {col}, {value})\n")


def execute_operations():
    if len(sys.argv) != 4:
        print("Usage: python sparse_matrix.py <operation> <matrix_file_1> <matrix_file_2>")
        print("Available operations: add, subtract, multiply")
        return

    operation = sys.argv[1]
    matrix_file_1 = sys.argv[2]
    matrix_file_2 = sys.argv[3]

    # Create matrices from specified files
    try:
        matrix1 = SparseMatrix.create_from_file(matrix_file_1)
        matrix2 = SparseMatrix.create_from_file(matrix_file_2)
    except ValueError as e:
        print(e)
        return

    print(f"Matrix 1 dimensions: {matrix1.rows_count}x{matrix1.cols_count}")
    print(f"Matrix 1 values: {matrix1.values}")
    print(f"Matrix 2 dimensions: {matrix2.rows_count}x{matrix2.cols_count}")
    print(f"Matrix 2 values: {matrix2.values}")

    try:
        if operation == 'add':
            result = matrix1.addition(matrix2)
        elif operation == 'subtract':
            result = matrix1.subtraction(matrix2)
        elif operation == 'multiply':
            result = matrix1.multiplication(matrix2)
        else:
            print("Invalid operation")
            return

        output_file = rf'C:\Users\USER\PycharmProjects\dsa\sparse_matrix\sample_results\sample_results_{operation}.txt'
        result.write_to_file(output_file)
        print(f"Results saved to {output_file}")
    except ValueError as e:
        print(e)


if __name__ == "__main__":
    execute_operations()
