import lorem
import sys


def generate_random_sentences(num_sentences=500, output_file='random_sentences-v:2.0.txt'):
    with open(output_file, 'w') as f:
        for _ in range(num_sentences):
            sentence = lorem.sentence()
            f.write(sentence + '\n')
    print(f"{num_sentences} random sentences written to {output_file}")


if __name__ == "__main__":
    output_file = sys.argv[1] + '.txt'
    generate_random_sentences(output_file=output_file)
