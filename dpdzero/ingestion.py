import pandas as pd
import logging
import pandas as pd
def read_csv_with_validation(file_path, expected_columns, key_columns):
    try:
        logging.info(f"Reading file: {file_path}")
        df = pd.read_csv(file_path)

        logging.info(f"Columns found in {file_path}: {df.columns.tolist()}")

        missing_cols = [col for col in expected_columns if col not in df.columns]
        if missing_cols:
            logging.error(f"Missing expected columns in {file_path}: {missing_cols}")
        else:
            logging.info(f"All expected columns found in {file_path}")

        for col in key_columns:
            if col not in df.columns:
                logging.error(f"Required key column {col} is missing in {file_path}")
            elif df[col].isnull().any():
                null_count = df[col].isnull().sum()
                logging.warning(f"Column {col} has {null_count} missing values in {file_path}")

        before = len(df)
        df = df.drop_duplicates()
        after = len(df)
        if before != after:
            logging.info(f"Dropped {before - after} duplicate rows from {file_path}")
        else:
            logging.info(f"No duplicates found in {file_path}")

        return df
    except Exception as e:
        logging.error(f"Failed to read or validate {file_path}: {e}")
        return pd.DataFrame()
