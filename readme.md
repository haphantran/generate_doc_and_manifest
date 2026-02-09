# Document and Manifest Generation Tools

This project contains scripts to generate dummy document files and corresponding manifest files for testing purposes.

## Scripts

### 1. `generate_files.py`

This script generates a specified number of simple text files with random content.

**Usage:**

```bash
python3 generate_files.py --output-dir <directory> [options]
```

**Arguments:**

*   `--output-dir`: (Required) Directory to save the generated files.
*   `--count`: Number of files to generate (default: 1000).
*   `--length`: Length of random text in each file (default: 10).
*   `--content-prefix`: Prefix string for the file content (default: "").
*   `--filename-prefix`: Prefix for the filenames (default: "test_file_").

**Example:**

```bash
python3 generate_files.py --output-dir docs --count 1000 --length 20 --content-prefix "here are some info " --filename-prefix "doc_"
```

### 2. `generate_manifests.py`

This script generates manifest files based on the documents present in a specified input directory. It calculates SHA256 checksums and assigns random metadata from configurable lists.

**Usage:**

```bash
python3 generate_manifests.py --input-dir <directory> --output-dir <directory> [options]
```

**Arguments:**

*   `--input-dir`: (Required) Directory containing the source document files.
*   `--output-dir`: (Required) Directory to save the generated manifest files.
*   `--files-per-manifest`: Number of files to list in each manifest file (default: 10).
*   `--max-files`: Maximum total number of files to process (default: all files).
*   `--multi-target`: Enable multi-target mode to assign multiple emails per document.
*   `--max-targets`: Maximum number of target emails per document; actual count is random between 1 and this value (default: 3, only used with `--multi-target`).

**Configuration:**

You can modify the following lists at the top of `generate_manifests.py` to customize the metadata generation:

*   `TARGET_EMAILS_LIST`
*   `DOC_TYPES_LIST`
*   `TARGET_DIRS_LIST`
*   `DOC_CATEGORIES_LIST`
*   `START_DATE` and `END_DATE` (for random `DOC_POSTED_ON` date generation)

**Examples:**

Single target mode (default):

```bash
python3 generate_manifests.py --input-dir docs --output-dir manifests --files-per-manifest 50
```

Multi-target mode (outputs to `manifests/multi_target/` with filenames `manifest_multi_target_*.manifest`):

```bash
python3 generate_manifests.py --input-dir docs --output-dir manifests --files-per-manifest 50 --multi-target
```

Multi-target mode with custom max targets (each document gets 1-5 random emails):

```bash
python3 generate_manifests.py --input-dir docs --output-dir manifests --files-per-manifest 50 --multi-target --max-targets 5
```

### 3. `generate_files_from_pdf_seed.py`

This script generates multiple PDF files from a seed PDF by adding unique text annotations to ensure each file has a different hash. Useful for testing with realistic PDF documents.

**Requirements:**

```bash
python3 -m venv venv && source venv/bin/activate && pip install PyMuPDF
```

**Usage:**

```bash
source venv/bin/activate
python3 generate_files_from_pdf_seed.py --seed-pdf <path> --output-dir <directory> [options]
```

**Arguments:**

*   `--seed-pdf`: (Required) Path to the seed PDF file.
*   `--output-dir`: (Required) Directory to save the generated PDF files.
*   `--count`: Number of files to generate (default: 10000).
*   `--filename-prefix`: Prefix for the filenames (default: "doc_").

Files are named with 6-digit zero-padded counters for proper sorting: `doc_000001.pdf`, `doc_000002.pdf`, etc.

**Example:**

```bash
source venv/bin/activate
python3 generate_files_from_pdf_seed.py --seed-pdf seed_file/t5013_seed.pdf --output-dir generated_pdfs --count 10000
```

## Workflow Examples

### Workflow 1: Text Files

1.  **Generate Documents:** Create 1000 dummy text files in the `docs` folder.
    ```bash
    python3 generate_files.py --output-dir docs --length 20 --content-prefix "here are some info " --filename-prefix "doc_"
    ```

2.  **Generate Manifests:** Create manifest files in the `manifests` folder, with 50 documents per manifest, using the files from `docs`.
    ```bash
    python3 generate_manifests.py --input-dir docs --output-dir manifests --files-per-manifest 50
    ```

### Workflow 2: PDF Files with Batch Manifest Generation

1.  **Setup virtual environment (one-time):**
    ```bash
    python3 -m venv venv && source venv/bin/activate && pip install PyMuPDF
    ```

2.  **Generate 10,000 PDF files from seed:**
    ```bash
    source venv/bin/activate
    python3 generate_files_from_pdf_seed.py --seed-pdf seed_file/t5013_seed.pdf --output-dir generated_pdfs --count 10000
    ```

3.  **Generate manifests for different file counts** (200, 500, 1000, 3000, 5000, 10000):

    All manifests are saved to the same folder (`manifests_pdf`). Filenames include the file count for distinction (e.g., `manifest_200files_1.manifest`).
    ```bash
    source venv/bin/activate
    python3 generate_manifests.py --input-dir generated_pdfs --output-dir manifests_pdf --files-per-manifest 50 --max-files 200
    python3 generate_manifests.py --input-dir generated_pdfs --output-dir manifests_pdf --files-per-manifest 50 --max-files 500
    python3 generate_manifests.py --input-dir generated_pdfs --output-dir manifests_pdf --files-per-manifest 50 --max-files 1000
    python3 generate_manifests.py --input-dir generated_pdfs --output-dir manifests_pdf --files-per-manifest 50 --max-files 3000
    python3 generate_manifests.py --input-dir generated_pdfs --output-dir manifests_pdf --files-per-manifest 50 --max-files 5000
    python3 generate_manifests.py --input-dir generated_pdfs --output-dir manifests_pdf --files-per-manifest 50 --max-files 10000
    ```

    Or as a single command:
    ```bash
    source venv/bin/activate && \
    python3 generate_files_from_pdf_seed.py --seed-pdf seed_file/t5013_seed.pdf --output-dir generated_pdfs --count 10000 && \
    python3 generate_manifests.py --input-dir generated_pdfs --output-dir manifests_pdf --files-per-manifest 50 --max-files 200 && \
    python3 generate_manifests.py --input-dir generated_pdfs --output-dir manifests_pdf --files-per-manifest 50 --max-files 500 && \
    python3 generate_manifests.py --input-dir generated_pdfs --output-dir manifests_pdf --files-per-manifest 50 --max-files 1000 && \
    python3 generate_manifests.py --input-dir generated_pdfs --output-dir manifests_pdf --files-per-manifest 50 --max-files 3000 && \
    python3 generate_manifests.py --input-dir generated_pdfs --output-dir manifests_pdf --files-per-manifest 50 --max-files 5000 && \
    python3 generate_manifests.py --input-dir generated_pdfs --output-dir manifests_pdf --files-per-manifest 50 --max-files 10000
    ```

4.  **Generate manifests with multi-target emails** (optional):

    Add `--multi-target` flag to assign multiple random emails per document. Manifests will be saved to a `multi_target/` subdirectory (e.g., `manifests_pdf/multi_target/`).
    ```bash
    source venv/bin/activate
    python3 generate_manifests.py --input-dir generated_pdfs --output-dir manifests_pdf --files-per-manifest 50 --max-files 200 --multi-target
    python3 generate_manifests.py --input-dir generated_pdfs --output-dir manifests_pdf --files-per-manifest 50 --max-files 500 --multi-target
    python3 generate_manifests.py --input-dir generated_pdfs --output-dir manifests_pdf --files-per-manifest 50 --max-files 1000 --multi-target
    python3 generate_manifests.py --input-dir generated_pdfs --output-dir manifests_pdf --files-per-manifest 50 --max-files 3000 --multi-target
    python3 generate_manifests.py --input-dir generated_pdfs --output-dir manifests_pdf --files-per-manifest 50 --max-files 5000 --multi-target
    python3 generate_manifests.py --input-dir generated_pdfs --output-dir manifests_pdf --files-per-manifest 50 --max-files 10000 --multi-target
    ```

    Or as a single command:

    ```bash
    source venv/bin/activate && \
    python3 generate_manifests.py --input-dir generated_pdfs --output-dir manifests_pdf --files-per-manifest 200 --max-files 500 --multi-target && \
    python3 generate_manifests.py --input-dir generated_pdfs --output-dir manifests_pdf --files-per-manifest 200 --max-files 1000 --multi-target && \
    python3 generate_manifests.py --input-dir generated_pdfs --output-dir manifests_pdf --files-per-manifest 200 --max-files 3000 --multi-target && \
    python3 generate_manifests.py --input-dir generated_pdfs --output-dir manifests_pdf --files-per-manifest 200 --max-files 5000 --multi-target && \
    python3 generate_manifests.py --input-dir generated_pdfs --output-dir manifests_pdf --files-per-manifest 200 --max-files 10000 --multi-target
