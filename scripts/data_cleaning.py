import pandas as pd

df = pd.read_csv(
    "data/311_Service_Requests_from_2024.csv",
    usecols=["Created Date", "Closed Date", "Incident Zip", "Complaint Type", "Borough"],
    dtype={"Incident Zip": str},
    parse_dates=["Created Date", "Closed Date"],
    date_format="%m/%d/%Y %I:%M:%S %p"
)


df = df.dropna(subset=["Closed Date"])

df = df.dropna(subset=["Incident Zip"])

df = df[df["Created Date"] <= df["Closed Date"]]


df.to_csv("data/311_Service_Requests_from_2024_clean.csv", index=False)