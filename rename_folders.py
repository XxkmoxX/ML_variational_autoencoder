import os
from pathlib import Path
from tqdm import tqdm

def rename_folders(base_dir: str, start_range: int, end_range: int, offset: int, dry_run: bool = True) -> None:
    """
    Rename numbered folders by adding an offset.
    
    Args:
        base_dir (str): Base directory containing numbered folders
        start_range (int): Start of original range (inclusive)
        end_range (int): End of original range (inclusive)
        offset (int): Number to add to each folder name
        dry_run (bool): If True, only simulate renaming
    """
    base_path = Path(base_dir)
    folders_to_rename = []

    # Collect all folders that need to be renamed
    for dir_path in base_path.iterdir():
        if dir_path.is_dir() and dir_path.name.isdigit():
            dir_num = int(dir_path.name)
            if start_range <= dir_num <= end_range:
                folders_to_rename.append(dir_path)

    # Sort folders in reverse order to avoid conflicts
    folders_to_rename.sort(key=lambda x: int(x.name), reverse=True)
    
    if not folders_to_rename:
        print(f"No folders found in range {start_range}-{end_range}")
        return

    # Show summary
    print(f"\nFound {len(folders_to_rename)} folders to rename")
    print(f"Original range: {start_range} to {end_range}")
    print(f"New range: {start_range + offset} to {end_range + offset}")
    print(f"First folder will change from {folders_to_rename[-1].name} to {int(folders_to_rename[-1].name) + offset}")
    print(f"Last folder will change from {folders_to_rename[0].name} to {int(folders_to_rename[0].name) + offset}")

    if dry_run:
        print("\nDRY RUN - No folders will be renamed")
        return

    # Confirm renaming
    confirm = input("\nProceed with renaming? (y/N): ")
    if confirm.lower() != 'y':
        print("Operation cancelled")
        return

    # Rename folders with progress bar
    print("\nRenaming folders...")
    renamed_count = 0
    errors = []

    for dir_path in tqdm(folders_to_rename):
        try:
            old_num = int(dir_path.name)
            new_num = old_num + offset
            new_path = dir_path.parent / str(new_num)
            dir_path.rename(new_path)
            renamed_count += 1
        except Exception as e:
            errors.append((dir_path, str(e)))

    # Print summary
    print(f"\nOperation complete:")
    print(f"Successfully renamed: {renamed_count} folders")
    if errors:
        print(f"Errors encountered: {len(errors)}")
        for path, error in errors:
            print(f"  - {path}: {error}")

if __name__ == "__main__":
    work_dir = os.getcwd()
    
    # Configuration
    START_RANGE = 0
    END_RANGE = 12799
    OFFSET = 12800  # This will shift 0->12800, 1->12801, etc.

    # First run in dry-run mode
    print("Performing dry run...")
    rename_folders(work_dir, START_RANGE, END_RANGE, OFFSET, dry_run=True)

    # Ask to proceed with actual renaming
    if input("\nRun actual renaming? (y/N): ").lower() == 'y':
        rename_folders(work_dir, START_RANGE, END_RANGE, OFFSET, dry_run=False)