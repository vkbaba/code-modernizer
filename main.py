import argparse
from analyzer.analyzer import PHPProjectAnalyzer
import os 

def main():
    parser = argparse.ArgumentParser(description="Analyze a PHP project structure.")
    parser.add_argument("project_root", help="Root directory of the PHP project")
    parser.add_argument("--exclude-images", action="store_true", help="Exclude image files from analysis")
    
    args = parser.parse_args()
    
    if not os.path.isdir(args.project_root):
        print(f"エラー: 指定されたディレクトリ '{args.project_root}' は存在しません。")
        exit(1)
    
    analyzer = PHPProjectAnalyzer(args.project_root, args.exclude_images)
    
    try:
        analyzer.analyze_dependencies()
        analyzer.visualize_dependencies()
        # analyzer.generate_report()
    except Exception as e:
        print(f"エラー: 解析中に問題が発生しました: {e}")

if __name__ == "__main__":
    main()