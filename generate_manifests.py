import os
import random
import hashlib
import datetime
import argparse

# --- Configuration ---
TARGET_EMAILS_LIST = [
    "angelo@portfolioxpressway.com",
    "haphan+client@portfolioxpressway.com",
    "tori+jan19englishdefault@thexchangecompany.com",
    "tori+jan19a@thexchangecompany.com",
    "tori+jan19@thexchangecompany.com",
    "tori+jan2b@thexchangecompany.com",
]

DOC_TYPES_LIST = [
    "T3",
    "T5008",
    "R16",
    "R18",
    "NR4",
    "Subscription Agreement",
    "Report",
    "Other Document",
]

TARGET_DIRS_LIST = ["/Tax 2025"]

DOC_CATEGORIES_LIST = [
    "LYZ Individual Tax Slip",
    "CFM Individual Tax Slip",
    "LYS Individual Tax Slip",
    "Sub Docs Outstanding",
    "Sub Docs Pending Cancel",
    "Sub Docs Cancel",
    "Sub Docs Weekly Status",
    "Report Request",
    "Other Document",
]
START_DATE = "2025-10-01"
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


def generate_manifests(input_dir, output_dir, files_per_manifest, multi_target=False, max_targets=None):
    """
    Generate manifest files for documents.

    Args:
        input_dir: Directory containing the document files
        output_dir: Base directory to save the manifest files
        files_per_manifest: Number of files per manifest
        multi_target: If True, assign multiple random emails to each document
        max_targets: Maximum number of target emails per document (only used if multi_target=True)
    """
    # Determine actual output directory and naming based on mode
    if multi_target:
        actual_output_dir = os.path.join(output_dir, "multi_target")
        manifest_prefix = "manifest_multi_target"
    else:
        actual_output_dir = output_dir
        manifest_prefix = "manifest"

    if not os.path.exists(actual_output_dir):
        os.makedirs(actual_output_dir)

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
        manifest_filename = f"{manifest_prefix}_{total_manifests + 1}.manifest"
        manifest_path = os.path.join(actual_output_dir, manifest_filename)

        with open(manifest_path, "w") as mf:
            mf.write(f"DOCUMENT_COUNT={len(chunk)}\n")

            for idx, filename in enumerate(chunk):
                file_path = os.path.join(input_dir, filename)

                # Generate metadata
                doc_no = idx + 1

                # Handle single vs multi-target emails
                if multi_target and max_targets:
                    # Select random number of emails between 1 and max_targets
                    actual_num_targets = random.randint(1, min(max_targets, len(TARGET_EMAILS_LIST)))
                    selected_emails = random.sample(TARGET_EMAILS_LIST, actual_num_targets)
                    target_email = ",".join(selected_emails)
                else:
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

    print(f"Finished. Generated {total_manifests} manifest files in '{actual_output_dir}'.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate manifest files for documents.")
    parser.add_argument("--input-dir", required=True, help="Directory containing the document files")
    parser.add_argument("--output-dir", required=True, help="Directory to save the manifest files")
    parser.add_argument("--files-per-manifest", type=int, default=10, help="Number of files per manifest")
    parser.add_argument(
        "--multi-target",
        action="store_true",
        help="Enable multi-target mode: assign multiple emails per document"
    )
    parser.add_argument(
        "--max-targets",
        type=int,
        default=3,
        help="Maximum number of target emails per document; actual count is random between 1 and this value (only used with --multi-target, default: 3)"
    )

    args = parser.parse_args()

    generate_manifests(
        args.input_dir,
        args.output_dir,
        args.files_per_manifest,
        multi_target=args.multi_target,
        max_targets=args.max_targets
    )
