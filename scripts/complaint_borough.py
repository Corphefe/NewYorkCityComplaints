#/!usr/bin/env python3

import argparse
import pandas as pd

def get_parser():
    parser = argparse.ArgumentParser(
        prog="compliant_borough.py",
        description="Counts NYC 311 compliats per borough within a data range."
    )
    parser.add_argument("-i", "--input", required=True, help="Path to input CSV source file.")
    parser.add_argument("-s", "--start", required=True, help="Start date of date range (MM/DD/YYYY).")
    parser.add_argument("-e", "--end", required=True, help="End date of date range (MM/DD/YYYY).")
    parser.add_argument("-o", "--output", required=False, help="Optional output file.")

    return parser

def main():
    args = get_parser().parse_args()
    use_cols = ["Closed Date", "Complaint Type", "Borough"]
    df = pd.read_csv(args.input, 
                     usecols=use_cols, 
                     parse_dates=["Closed Date"],
                     date_format="%m/%d/%Y %I:%M:%S %p"
                     )
    start = pd.to_datetime(args.start)
    end = pd.to_datetime(args.end)
    mask = df["Closed Date"].between(start, end, inclusive="both")
    df = df.loc[mask].dropna(subset=["Borough"])

    counts = (
        df.groupby(["Complaint Type", "Borough"])
        .size()
        .reset_index(name="count")
        .sort_values("count", ascending=False)
    )

    header = ["complaint type", "borough", "count"]
    if args.output:
        counts.to_csv(args.output, index=False, header=header)
    else:
        print(",".join(header))
        for _, row in counts.iterrows():
            print(f"{row['Complaint Type']},{row['Borough']},{row['count']}")


if __name__ == "__main__":
    main()