#!usr/bin/env python3

import argparse

def get_parser():
    parser = argparse.ArgumentParser(
        prog="borough_compliants.py",
        description="Counts NYC 311 compliats per borough within a data range."
    )
    parser.add_argument("-i", "--input", required=True, help="Path to input CSV source file.")
    parser.add_argument("-s", "--start", required=True, help="Start date of date range (MM/DD/YYYY).")
    parser.add_argument("-e", "--end", required=True, help="End date of date range (MM/DD/YYYY).")
    parser.add_argument("-o", "--output", required=False, help="Optional output file.")

    return parser

def main():
    args = get_parser().parse_args()


if __name__ == "__main__":
    main()