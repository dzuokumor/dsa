import os

class UniqueIntegersProcessor:
    @staticmethod
    def process(input_file_path, output_file_path):
        unique_numbers = set()

        try:
            with open(input_file_path, 'r') as infile:
                for line in infile:
                    numbers = line.strip().split()
                    if len(numbers) != 1:
                        continue
                    number_str = numbers[0]
                    try:
                        number = int(number_str)
                        if -1023 <= number <= 1023:
                            unique_numbers.add(number)
                    except ValueError:
                        pass
        except FileNotFoundError:
            print(f"Error: {input_file_path} not found.")
            return

        with open(output_file_path, 'w') as outfile:
            for number in sorted(unique_numbers):
                outfile.write(f"{number}\n")

        print(f"Processed {input_file_path}. Output written to {output_file_path}.")

if __name__ == "__main__":
    input_folder = os.path.join(os.path.dirname(__file__), '../../sample_inputs/')
    output_folder = os.path.join(os.path.dirname(__file__), '../../sample_results/')

    input_files = [
        'sample_01.txt',
        'sample_02.txt',
        'sample_03.txt',
        'sample_04.txt',
        'small_sample_input_01.txt',
        'small_sample_input_02.txt',
        'small_sample_input_03.txt',
        'small_sample_input_04.txt'
    ]

    for input_file in input_files:
        input_file_path = os.path.join(input_folder, input_file)
        output_file_path = os.path.join(output_folder, f'{input_file}_results.txt')
        UniqueIntegersProcessor.process(input_file_path, output_file_path)
