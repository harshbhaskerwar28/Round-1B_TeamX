import sys
from pathlib import Path
from typing import List

# Re-use the existing pipeline defined in app.py
from app import main as process_collection

def find_collections(input_root: Path) -> List[Path]:
    """Return paths that qualify as a collection inside *input_root*.

    A *collection* is defined as any directory that contains a
    ``challenge1b_input.json`` file **and** at least one PDF file.  This
    helper now treats the *input_root* itself as a potential collection in
    addition to its immediate sub-directories so that the common layout
    where all assets live directly under ``input/`` is handled gracefully.
    """

    def is_collection(path: Path) -> bool:
        return (
            path.is_dir()
            and (path / "challenge1b_input.json").exists()
            and any(p.suffix.lower() == ".pdf" for p in path.glob("*.pdf"))
        )

    collections: List[Path] = []

    # First, check if the root folder itself is a collection.
    if is_collection(input_root):
        collections.append(input_root)

    # Then, look for collections in immediate sub-directories.
    for child in input_root.iterdir():
        if is_collection(child):
            collections.append(child)

    return collections


def ensure_output_dir(base_output: Path, collection_name: str) -> Path:
    """Create output folder for a collection and return its path."""
    out_dir = base_output / collection_name
    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir


def run_batch(input_root: Path, output_root: Path):
    """Process each collection in input_root and write results under output_root."""
    collections = find_collections(input_root)
    if not collections:
        print(f"No collections with challenge1b_input.json found in {input_root}")
        return

    for coll_path in collections:
        input_json = coll_path / "challenge1b_input.json"
        # Treat collection directory itself as containing PDFs
        pdf_dir = coll_path
        # Find any PDF files directly under coll_path
        pdf_files = list(pdf_dir.glob("*.pdf"))
        if not pdf_files:
            print(f"Skipping {coll_path.name}: no PDF files found in {pdf_dir}")
            continue

        # If we're processing the *input_root* itself as a collection, write
        # results directly under ``output_root`` (no extra nesting). Otherwise
        # create/ensure a sub-folder named after the collection.
        output_dir = output_root if coll_path == input_root else ensure_output_dir(output_root, coll_path.name)
        output_json = output_dir / "challenge1b_output.json"

        print(f"Processing collection {coll_path.name} ...")
        try:
            process_collection(str(input_json), str(pdf_dir), str(output_json))
            print(f"✓ Saved output to {output_json}\n")
        except Exception as e:
            print(f"✗ Failed to process {coll_path.name}: {e}\n")


def main():
    # Use fixed input/ and output/ directories in the script's directory
    script_dir = Path(__file__).parent.resolve()
    input_root = script_dir / "input"
    output_root = script_dir / "output"

    if not input_root.exists() or not input_root.is_dir():
        print(f"Input folder '{input_root}' does not exist or is not a directory")
        sys.exit(1)

    output_root.mkdir(parents=True, exist_ok=True)
    run_batch(input_root, output_root)


if __name__ == "__main__":
    main() 