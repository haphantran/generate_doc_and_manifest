import os
import random
import string
import argparse


def generate_files(output_dir, count, length, content_prefix, filename_prefix):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for i in range(count):
        # Generate random content
        random_chars = "".join(random.choices(string.ascii_letters + string.digits, k=length))
        content = f"{content_prefix}{random_chars}"

        # Generate filename
        filename = f"{filename_prefix}{i+1}.txt"
        file_path = os.path.join(output_dir, filename)

        with open(file_path, "w") as f:
            f.write(content)

    print(f"Successfully generated {count} files in '{output_dir}'")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate simple text files.")
    parser.add_argument("--output-dir", required=True, help="Directory to save the files")
    parser.add_argument("--count", type=int, default=1000, help="Number of files to generate")
    parser.add_argument("--length", type=int, default=10, help="Length of random text in each file")
    parser.add_argument("--content-prefix", default="", help="Prefix for the file content")
    parser.add_argument("--filename-prefix", default="test_file_", help="Prefix for the filenames")

    args = parser.parse_args()

    generate_files(args.output_dir, args.count, args.length, args.content_prefix, args.filename_prefix)
