from __future__ import annotations

import pandas as pd


class DataPipeline:
    """Handles cleaning, transformation, and parsing of extracted data."""

    def __init__(self) -> None:
        self.columns = ["field", "value"]

    def process(self, raw_data: list[dict]) -> list[dict]:
        dataframe = pd.DataFrame(raw_data, columns=self.columns)

        dataframe = dataframe.dropna(subset=["value"])
        dataframe["value"] = dataframe["value"].astype(str).str.strip()
        dataframe["value"] = dataframe["value"].replace({r"\s+": " "}, regex=True)

        cleaned_records = dataframe.to_dict(orient="records")
        return cleaned_records
