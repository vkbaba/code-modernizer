import argparse
from modernizer.modernizer import ProjectModernizer
import os

def main():
    parser = argparse.ArgumentParser(description="Analyze a PHP project structure.")
    parser.add_argument("project_root", help="Root directory of the project")
    parser.add_argument("--exclude-images", action="store_true", help="Exclude image files from analysis")
    parser.add_argument("--files", nargs="+", help="Specific files to analyze")
    args = parser.parse_args()

    if not os.path.isdir(args.project_root):
        print(f"Error: The specified directory '{args.project_root}' does not exist.")
        exit(1)

    try:
        modernizer = ProjectModernizer(args.project_root, args.exclude_images)
        entry_points = modernizer.find_entry_points(args.files)
        modernizer.analyze_dependencies(entry_points)
        modernizer.visualize_dependencies()
        # analyzer.generate_report()
    except FileNotFoundError as e:
        print(f"Error: {e}")
        exit(1)
    except Exception as e:
        print(f"Error: An unexpected issue occurred: {e}")
        exit(1)

if __name__ == "__main__":
    main()