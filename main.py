#start program->call organiser->show results
import os
import argparse

from organiser import organise_files


def main():
    parser= argparse.ArgumentParser(description="File Organizer")
    subparsers=parser.add_subparsers(dest="command")

    organise_parser=subparsers.add_parser("organise")
    organise_parser.add_argument(
        "--path",
        type=str, required=True, help="Path to the directory to organize"
    )
    organise_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview the changes without moving files"
    )
   
    organise_parser.add_argument(
        "--recursive",
        action="store_true", help="Scan directories recursively"
    )

    stats_parser=subparsers.add_parser("stats")
    
    stats_parser.add_argument(
        "--path",
        type=str, default=".", help="Directory to analyze"
    )

    watch_parser=subparsers.add_parser("watch", help="Watch a directory and automatically organize new files")

    watch_parser.add_argument(
        "--path",
        type=str, default=".", help="Directory to  watch"
    )

    watch_parser.add_argument(
        "--recursive",
        action="store_true",
        help="Watch subdirectories recursively"
    )


    undo_parser = subparsers.add_parser("undo")


    args=parser.parse_args()

    if args.command == "organise":

        abs_path = os.path.abspath(args.path)

        print("\n==============================")
        print(" FILE ORGANIZER STARTING")
        print("==============================")
        print(f"Target Path : {abs_path}")
        print(f"Mode        : {'DRY RUN' if args.dry_run else 'EXECUTE'}")
        print(f"Recursive   : {args.recursive}")
        print("==============================\n")


        organise_files(
            args.path,
            dry_run=args.dry_run,
            recursive=args.recursive
        ) 
        print("\n==============================")
        print(" OPERATION COMPLETED")
        print("==============================\n")

    elif args.command == "stats":
        from organiser import get_folder_stats

        stats = get_folder_stats(args.path)

        print("\n===== FILE STATISTICS =====\n")

        for category, count in stats.items():
            print(f"{category}: {count}")

        print("\n===========================\n")


    elif args.command == "watch":
        from watch import watch_directory

        watch_directory(
            args.path,
            recursive=args.recursive
        )

    elif args.command == "undo":
        from organiser import undo_last_move
        undo_last_move()


if __name__ == "__main__":
    main() 

