import streamlit as st
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

st.set_page_config(layout="wide")
st.title("Top 15 Saham LQ45 Berdasarkan % Change Hari Ini")

# Daftar lengkap simbol LQ45
lq45_symbols = [
    "ACES.JK", "ADMR.JK", "ADRO.JK", "AKRA.JK", "AMMN.JK", "AMRT.JK", "ANTM.JK",
    "ARTO.JK", "ASII.JK", "BBCA.JK", "BBNI.JK", "BBRI.JK", "BBTN.JK", "BMRI.JK",
    "BRIS.JK", "BRPT.JK", "CPIN.JK", "CTRA.JK", "ESSA.JK", "EXCL.JK", "GOTO.JK",
    "ICBP.JK", "INCO.JK", "INDF.JK", "INKP.JK", "ISAT.JK", "ITMG.JK", "JPFA.JK",
    "JSMR.JK", "KLBF.JK", "MAPA.JK", "MAPI.JK", "MBMA.JK", "MDKA.JK", "MEDC.JK",
    "PGAS.JK", "PGEO.JK", "PTBA.JK", "SIDO.JK", "SMGR.JK", "SMRA.JK", "TLKM.JK",
    "TOWR.JK", "UNTR.JK", "UNVR.JK"
]

end = datetime.now()
start = end - timedelta(days=1)
dfs = []
summary = []

for symbol in lq45_symbols:
    try:
        df = yf.download(symbol, start=start, end=end, interval="5m", progress=False)
        if df.empty: continue
        df["Symbol"] = symbol.replace(".JK", "")
        change_pct = (df["Close"][-1] - df["Open"][0]) / df["Open"][0] * 100
        df["% Change"] = change_pct
        df["Volume 11"] = df.between_time("10:59", "11:01")["Volume"].mean()
        df["Volume 14"] = df.between_time("13:59", "14:01")["Volume"].mean()
        df["Volume 15:10"] = df.between_time("15:09", "15:11")["Volume"].mean()
        df["Total Volume"] = df["Volume"].sum()
        summary.append({
            "Symbol": df["Symbol"][0],
            "% Change": round(change_pct, 2),
            "Volume 11:00": int(df["Volume 11"][0]),
            "Volume 14:00": int(df["Volume 14"][0]),
            "Volume 15:10": int(df["Volume 15:10"][0]),
            "Total Volume": int(df["Total Volume"][0])
        })
    except:
        continue

# Buat dataframe hasil dan sort
df_summary = pd.DataFrame(summary)
top15 = df_summary.sort_values(by="% Change", ascending=False).head(15)

# Tampilkan grafik per saham
for _, row in top15.iterrows():
    st.subheader(f"{row['Symbol']} - Change: {row['% Change']}%")
    fig, ax = plt.subplots()
    ax.bar(["11:00", "14:00", "15:10"],
           [row["Volume 11:00"], row["Volume 14:00"], row["Volume 15:10"]],
           color="orange")
    ax.set_ylabel("Volume")
    ax.set_title(f"{row['Symbol']} - Volume Intraday")
    st.pyplot(fig)

# Tabel ringkasan
st.subheader("Tabel Ringkasan Top 15 Saham Hari Ini")
st.dataframe(top15.set_index("Symbol"))
