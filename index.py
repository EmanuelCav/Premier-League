import pandas as pd
import numpy as np

df = pd.read_excel("positions.xlsx")
df2 = pd.read_excel("stats.xlsx")

# Calculate Points

df["Points"] = (df["Won"]*3) + df["Drawn"]

# Calculate goal difference

df["Goal difference"] = df["Goals for"] - df["Goals against"]
            
### Join positions with stats

merged = pd.merge(df, df2)
merged = merged.sort_values("Points", ascending=False).reset_index(drop=True)
merged["Position"] = np.arange(1,21)

### Compare if there are teams with the same points

for i in range(0, merged.shape[0]):
    if merged.iloc[i]["Points"] == merged.iloc[i-1]["Points"]:
        if merged.iloc[i]["Goal difference"] > merged.iloc[i-1]["Goal difference"]:
            print("{} is positioned better than {}".format(
                merged.iloc[i]["Team"], merged.iloc[i-1]["Team"]))
            before = merged.iloc[i-1]
            merged.iloc[i-1] = merged.iloc[i]
            merged.iloc[i] = before
        else:
            print("{} is positioned better than {}".format(
                merged.iloc[i-1]["Team"], merged.iloc[i]["Team"]))

### Yellow and red cards, offsides, passes and goals per match

merged["Yellow cards per match"] = merged["Yellow Cards"]/merged["Played"]
merged["Red cards per match"] = merged["Red Cards"]/merged["Played"]
merged["Offsides per match"] = merged["Offsides"]/merged["Played"]
merged["Passes per match"] = merged["Passes"]/merged["Played"]
merged["Goals per match"] = merged["Goals for"]/merged["Played"]

### Porcentage of own goals and success shots

merged["Own goals percentage"] = (merged["Own Goals"]*100)/merged["Goals against"]
merged["Success shot"] = (merged["Goals for"]*100)/merged["Shots"]

### Average points scored by county

countyDf = merged.groupby(["County"]).agg({
    "Points": 'sum',
    "City": 'count'
})

countyDf["Average Points"] = countyDf["Points"]/countyDf["City"]

### Greater London teams that qualified for international competions

london = merged.loc[merged["County"] == "Greater London"].reset_index(drop=True)
london["International competition"] = pd.cut(london["Position"], bins=[1,4,6,7], labels=["Champions League", "Europe League", "Conference League"])

### Set position as index

merged = merged.set_index(["Position"])







