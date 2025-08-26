#!/usr/bin/env python3
import re
import sys
import os
import logging
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt

from backend.scripts.data_tools.data_converter import DataConverter

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


class SalesPredictor:
    def __init__(self):
        self.model = None
        self.df = None

    # ---------------- Extraction ----------------
    def extract_pdf(self, path):
        text = pdf_extract_text(path)
        logging.info(f"Extracted {len(text)} characters from PDF")
        return text

    def extract_docx(self, path):
        doc = docx.Document(path)
        paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
        text = "\n".join(paragraphs)
        logging.info(f"Extracted {len(paragraphs)} paragraphs from DOCX")
        return text

    def extract_image(self, path):
        img = Image.open(path)
        text = pytesseract.image_to_string(img)
        logging.info(f"Extracted {len(text)} characters from image")
        return text

    # ---------------- Parsing ----------------
    DATE_PATTERNS = [
        r"(?P<date>\d{4}[-/]\d{1,2}[-/]\d{1,2})",  # YYYY-MM-DD
        r"(?P<date>\d{1,2}[-/]\d{1,2}[-/]\d{4})",  # DD-MM-YYYY
        r"(?P<date>\d{4}[-/]\d{1,2})",             # YYYY-MM
    ]
    NUMBER_PATTERN = r"(?P<num>\d{1,3}(?:[,\s]\d{3})*(?:\.\d+)?|\d+(?:\.\d+)?)"

    def try_parse_date(self, s):
        for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%d-%m-%Y", "%m-%d-%Y", "%Y-%m", "%Y/%m"):
            try:
                return datetime.strptime(s, fmt)
            except Exception:
                continue
        return None

    def parse_sales(self, text):
        rows = []
        lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
        for ln in lines:
            date_found, num = None, None
            for pat in self.DATE_PATTERNS:
                m = re.search(pat, ln)
                if m:
                    dt = self.try_parse_date(m.group("date"))
                    if dt:
                        date_found = dt
                        break
            nums = re.findall(self.NUMBER_PATTERN, ln)
            if nums:
                try:
                    num = float(nums[0].replace(",", "").replace(" ", ""))
                except Exception:
                    num = None
            if date_found and num is not None:
                rows.append({"date": pd.to_datetime(date_found), "sales": num})

        if not rows:
            logging.warning("No sales data found")
            return pd.DataFrame(columns=["date", "sales"])
        df = pd.DataFrame(rows).drop_duplicates().sort_values("date")
        return df

    # ---------------- Model ----------------
    def train(self, df):
        df = df.dropna()
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df = df.dropna(subset=["date", "sales"])  # ensure valid rows only
        
        # create time index feature
        df["t"] = (df["date"] - df["date"].min()).dt.days
        
        X = df[["t"]].values
        y = df["sales"].values
        
        # ✅ Use RandomForest instead of Linear Regression
        model = RandomForestRegressor(
            n_estimators=200, 
            random_state=42,
            max_depth=None,
            n_jobs=-1
        )
        model.fit(X, y)
        
        self.model = model
        self.df = df
        logging.info("RandomForest model trained on %d samples", len(df))
        return model


    def forecast(self, days=30):
        if self.model is None or self.df is None:
            raise RuntimeError("Model not trained")
        last_t = self.df["t"].max()
        future_dates = [self.df["date"].max() + timedelta(days=i) for i in range(1, days + 1)]
        future_t = np.array([last_t + i for i in range(1, days + 1)]).reshape(-1, 1)
        preds = self.model.predict(future_t)
        return pd.DataFrame({"date": future_dates, "sales": preds})

    def plot_forecast(self, forecast_df, output_path="forecast.png"):
        plt.figure(figsize=(10, 6))
        plt.plot(self.df["date"], self.df["sales"], label="Historical", marker="o")
        plt.plot(forecast_df["date"], forecast_df["sales"], label="Forecast", linestyle="--", marker="x")
        plt.legend()
        plt.grid(True)
        plt.title("Sales Forecast")
        plt.xlabel("Date")
        plt.ylabel("Sales")
        plt.savefig(output_path)
        plt.close()
        logging.info(f"Saved forecast plot to {output_path}")


# ---------------- CLI ----------------
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python prediction.py <command> <file> [options]")
        print("Commands:")
        print("  csv <path>")
        print("  pdf <path>")
        print("  docx <path>")
        print("  image <path>")
        print("  xml <path>")
        print("  json <path>")
        print("Example: python prediction.py pdf sales.pdf")
        sys.exit(1)

    predictor = SalesPredictor()
    command, path = sys.argv[1], sys.argv[2]

    if command == "csv" or command == "xml" or command == "json":
        df = DataConverter.auto_read(path)
    elif command == "pdf":
        text = predictor.extract_pdf(path)
        df = predictor.parse_sales(text)
    elif command == "docx":
        text = predictor.extract_docx(path)
        df = predictor.parse_sales(text)
    elif command == "image":
        text = predictor.extract_image(path)
        df = predictor.parse_sales(text)
    else:
        print("Unknown command")
        sys.exit(1)

    if df is not None and not df.empty:
        predictor.train(df)
        forecast_df = predictor.forecast(30)
        predictor.plot_forecast(forecast_df)
        print("Forecast completed. Saved plot as forecast.png")
    else:
        print("No data extracted.")
