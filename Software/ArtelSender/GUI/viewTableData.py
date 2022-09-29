from rich_dataframe import prettify
import pandas as pd
matrixData = pd.read_csv('locations.csv', header=None)

table = prettify(matrixData)