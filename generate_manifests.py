import os
import random
import hashlib
import datetime
import argparse

# --- Configuration ---
TARGET_EMAILS_LIST = ["anoop.pxw+docpipe@gmail.com", "user1@example.com", "admin@test.com"]

DOC_TYPES_LIST = ["Sub Docs Outstanding", "Invoice", "Contract", "Report"]

TARGET_DIRS_LIST = ["HV56/Sub Docs", "QEV/Sub Docs", "SJE/Sub Docs", "General/Files"]

DOC_CATEGORIES_LIST = ["Financial", "Legal", "Operational", "HR"]

START_DATE = "2025-01-01"
END_DATE = "2025-12-31"

# --- Helper Functions ---


def calculate_sha256(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        # Read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def get_working_days(start_date_str, end_date_str):
    start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d").date()
    end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d").date()

    days = []
    current_date = start_date
    while current_date <= end_date:
        # Monday is 0 and Sunday is 6
        if current_date.weekday() < 5:
            days.append(current_date)
        current_date += datetime.timedelta(days=1)
    return days


def get_random_working_day(working_days):
    if not working_days:
        return datetime.date.today().strftime("%Y-%m-%d")
    return random.choice(working_days).strftime("%Y-%m-%d")


def generate_manifests(input_dir, output_dir, files_per_manifest):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Get all files from input directory
    all_files = [
        f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f)) and not f.startswith(".")
    ]
    all_files.sort()  # Ensure deterministic order if needed, or shuffle

    if not all_files:
        print(f"No files found in {input_dir}")
        return

    working_days = get_working_days(START_DATE, END_DATE)

    # Process in chunks
    total_manifests = 0
    for i in range(0, len(all_files), files_per_manifest):
        chunk = all_files[i : i + files_per_manifest]
        manifest_filename = f"manifest_{total_manifests + 1}.manifest"
        manifest_path = os.path.join(output_dir, manifest_filename)

        with open(manifest_path, "w") as mf:
            mf.write(f"DOCUMENT_COUNT={len(chunk)}\n")

            for idx, filename in enumerate(chunk):
                file_path = os.path.join(input_dir, filename)

                # Generate metadata
                doc_no = idx + 1
                target_email = random.choice(TARGET_EMAILS_LIST)
                doc_type = random.choice(DOC_TYPES_LIST)
                target_dir = random.choice(TARGET_DIRS_LIST)
                doc_category = random.choice(DOC_CATEGORIES_LIST)
                posted_on = get_random_working_day(working_days)
                sha256 = calculate_sha256(file_path)

                mf.write(f"DOCUMENT_NO={doc_no}\n")
                mf.write(f"TARGET_EMAILS={target_email}\n")
                mf.write(f"DOC_TYPE={doc_type}\n")
                mf.write(f"DOC_CATEGORY={doc_category}\n")
                mf.write(f"FILENAME={filename}\n")
                mf.write(f"TARGET_DIR={target_dir}\n")
                mf.write(f"DOC_POSTED_ON={posted_on}\n")
                mf.write(f"SHA256SUM={sha256}\n")

            mf.write("END_DOCUMENTS\n")

        total_manifests += 1
        print(f"Generated {manifest_filename} with {len(chunk)} documents.")

    print(f"Finished. Generated {total_manifests} manifest files in '{output_dir}'.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate manifest files for documents.")
    parser.add_argument("--input-dir", required=True, help="Directory containing the document files")
    parser.add_argument("--output-dir", required=True, help="Directory to save the manifest files")
    parser.add_argument("--files-per-manifest", type=int, default=10, help="Number of files per manifest")

    args = parser.parse_args()

    generate_manifests(args.input_dir, args.output_dir, args.files_per_manifest)
