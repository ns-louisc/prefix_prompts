import argparse
import csv
from pathlib import Path

import pandas as pd


class CSVProcessor:
    def __init__(self, input_file: str, output_file: str):
        self.input_file = Path(input_file)
        self.output_file = Path(output_file)

    def preview_output(self, manipulation_id: str, prefix: str, num_rows: int = 5) -> pd.DataFrame:
        df = self._read_csv()
        preview_df = df.head(num_rows).copy()
        preview_df["manipulation_id"] = manipulation_id
        preview_df["probe"] = prefix + preview_df["prompt"]

        return preview_df

    def process_csv(self, manipulation_id: str, prefix: str) -> None:
        df = self._read_csv()
        df["manipulation_id"] = manipulation_id
        df["probe"] = prefix + df["prompt"]

        self._write_formatted_csv(df)

        print(f"Processed {len(df)} rows")
        print(f"Output saved to: {self.output_file}")

    def _read_csv(self) -> pd.DataFrame:
        df = pd.read_csv(self.input_file, dtype=object)

        if "prompt" not in df.columns:
            raise ValueError("Input CSV must contain a 'prompt' column")

        return df

    def _write_formatted_csv(self, df: pd.DataFrame) -> None:
        df.to_csv(
            self.output_file,
            index=False,
            encoding="utf-8",
            lineterminator="\n",
            quoting=csv.QUOTE_ALL,
            quotechar='"',
            doublequote=True
        )


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Process CSV file with manipulation_id and probe fields")
    parser.add_argument("input_file", help="Input CSV file path")
    parser.add_argument("output_file", help="Output CSV file path")
    parser.add_argument("--manipulation-id", required=True, help="Manipulation method ID")
    parser.add_argument("--prefix", required=True, help="Prefix string for probes")
    parser.add_argument("--preview", action="store_true", help="Preview output without writing file")
    parser.add_argument("--preview-rows", type=int, default=5, help="Number of rows to preview")

    return parser


def main() -> None:
    args = create_parser().parse_args()
    processor = CSVProcessor(args.input_file, args.output_file)

    if args.preview:
        preview = processor.preview_output(args.manipulation_id, args.prefix, args.preview_rows)
        print("Preview of processed data:")
        print(preview.to_string(justify="left", index=False))
    else:
        processor.process_csv(args.manipulation_id, args.prefix)


if __name__ == "__main__":
    main()