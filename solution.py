import pandas as pd
import re

def add_virtual_column(df: pd.DataFrame, role: str, new_column: str) -> pd.DataFrame:
    """
    Add a new column to a DataFrame based on an arithmetic expression
    involving existing columns.

    Parameters
    ----------
    df : pandas.DataFrame
        The source DataFrame containing the columns used in the expression.
    role : str
        An arithmetic expression using valid column names and operators (+, -, *).
        Example: "quantity * price" or "label_one+label_two"
    new_column : str
        The name for the new calculated column.

    Returns
    -------
    pandas.DataFrame
        A copy of the DataFrame with the additional column if valid, else an empty DataFrame.
    """

    valid_col_pattern = r'^[A-Za-z_]+$'
    if not all(re.match(valid_col_pattern, col) for col in df.columns):
        return pd.DataFrame([])

    if not re.match(valid_col_pattern, new_column):
        return pd.DataFrame([])

    role_cleaned = role.strip()
    allowed_ops = ['+', '-', '*']
    tokens = re.split(r'\s*([+\-*])\s*', role_cleaned)

    if not all(t in allowed_ops or re.match(valid_col_pattern, t) for t in tokens):
        return pd.DataFrame([])

    for token in tokens:
        if re.match(valid_col_pattern, token) and token not in df.columns:
            return pd.DataFrame([])

    try:
        df_copy = df.copy()
        df_copy[new_column] = df_copy.eval(role_cleaned)
        return df_copy
    except Exception:
        return pd.DataFrame([])
