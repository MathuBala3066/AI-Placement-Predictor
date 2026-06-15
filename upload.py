import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql://postgres:Mathu%4012345@localhost:5432/placement_ai_db"
)

df = pd.read_csv("placementdata.csv")

df.to_sql(
    "placementdata",
    engine,
    if_exists="replace",
    index=False
)

print("Dataset uploaded successfully!")