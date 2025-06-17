import pandas as pd

def load_data(path="BigBasket.csv"):
    df = pd.read_csv(path)
    df.dropna(subset=["product", "category", "brand"], inplace=True)
    df = df[["product", "category", "brand"]]
    df.drop_duplicates(inplace=True)
    df.reset_index(drop=True, inplace=True)  # Ensures compatibility with similarity matrix
    return df
