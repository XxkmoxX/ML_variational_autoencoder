import os
import shutil
from pathlib import Path
from tqdm import tqdm

def remove_numbered_directories(base_dir: str, start_num: int, end_num: int, dry_run: bool = True) -> None:
    """
    Remove numbered directories within specified range including all contents.
    
    Args:
        base_dir (str): Base directory containing numbered folders
        start_num (int): Start of range to delete (inclusive)
        end_num (int): End of range to delete (inclusive)
        dry_run (bool): If True, only simulate deletion
    """
    base_path = Path(base_dir)
    dirs_to_delete = []

    # Find all numbered directories in range
    for dir_path in base_path.iterdir():
        if dir_path.is_dir() and dir_path.name.isdigit():
            dir_num = int(dir_path.name)
            if start_num <= dir_num <= end_num:
                dirs_to_delete.append(dir_path)

    # Sort directories numerically
    dirs_to_delete.sort(key=lambda x: int(x.name))
    
    if not dirs_to_delete:
        print(f"No directories found in range {start_num}-{end_num}")
        return

    # Show summary
    print(f"\nFound {len(dirs_to_delete)} directories to delete")
    print(f"Range: {start_num} to {end_num}")
    print(f"First directory: {dirs_to_delete[0]}")
    print(f"Last directory: {dirs_to_delete[-1]}")

    if dry_run:
        print("\nDRY RUN - No files will be deleted")
        return

    # Confirm deletion
    confirm = input("\nProceed with deletion? (y/N): ")
    if confirm.lower() != 'y':
        print("Operation cancelled")
        return

    # Delete directories with progress bar
    print("\nDeleting directories...")
    deleted_count = 0
    errors = []

    for dir_path in tqdm(dirs_to_delete):
        try:
            shutil.rmtree(dir_path)
            deleted_count += 1
        except Exception as e:
            errors.append((dir_path, str(e)))

    # Print summary
    print(f"\nOperation complete:")
    print(f"Successfully deleted: {deleted_count} directories")
    if errors:
        print(f"Errors encountered: {len(errors)}")
        for path, error in errors:
            print(f"  - {path}: {error}")

if __name__ == "__main__":
    work_dir = os.getcwd()
    
    # Example: Delete directories numbered 25600 to 35637
    START_RANGE = 25600
    END_RANGE = 35637

    # First run in dry-run mode
    print("Performing dry run...")
    remove_numbered_directories(work_dir, START_RANGE, END_RANGE, dry_run=True)

    # Ask to proceed with actual deletion
    if input("\nRun actual deletion? (y/N): ").lower() == 'y':
        remove_numbered_directories(work_dir, START_RANGE, END_RANGE, dry_run=False)