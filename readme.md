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

## Workflow Example

1.  **Generate Documents:** Create 1000 dummy text files in the `docs` folder.
    ```bash
    python3 generate_files.py --output-dir docs --length 20 --content-prefix "here are some info " --filename-prefix "doc_"
    ```

2.  **Generate Manifests:** Create manifest files in the `manifests` folder, with 50 documents per manifest, using the files from `docs`.
    ```bash
    python3 generate_manifests.py --input-dir docs --output-dir manifests --files-per-manifest 50
    ```
