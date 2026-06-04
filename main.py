#start program->call organizer->show results

import argparse
from organiser import organise_files


def main():
    parser= argparse.ArgumentParser(description="File Organizer")
    
    parser.add_argument(
        "--path",
        type=str, required=True, help="Path to the directory to organize"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview the changes without moving files"
    )
    parser.add_argument(
        "--execute",
        action="store_true", help="Execute and move files according to the plan"
    )
    args=parser.parse_args()

    if args.dry_run and args.execute:
        print("Please choose either --dry-run or --execute, not both.")
        return
    
    if not args.dry_run and not args.execute:
        print("Please choose either --dry-run or --execute.")
        return
    
    dry_run_mode=args.dry_run

    organise_files(args.path, dry_run=dry_run_mode)

if __name__ == "__main__":
    main()

