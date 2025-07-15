import streamlit as st
from pymongo import MongoClient
import pandas as pd

# DB connection
client = MongoClient("mongodb+srv://sjmarketng:j24CgjFIXRSoFe2A@atbcluster.jamyzti.mongodb.net/?retryWrites=true&w=majority&appName=ATBCluster")

db = client['trading_bot']
paper_trades_col = db['paper_trades']

# Load closed paper trades
trades = list(paper_trades_col.find({"status": "closed"}))
df = pd.DataFrame(trades)

st.title("🚀 Paper Trades Dashboard")

if not df.empty:
    wins = df[df["result"] == "take_profit"]
    losses = df[df["result"] == "stop_loss"]
    win_rate = (len(wins) / len(df)) * 100 if len(df) > 0 else 0

    st.metric("Total Trades", len(df))
    st.metric("Wins", len(wins))
    st.metric("Losses", len(losses))
    st.metric("Win Rate", f"{win_rate:.2f}%")

    st.subheader("Trade Details")
    st.dataframe(df[["datetime", "signal", "entry_price", "close_price", "result"]])
else:
    st.write("No closed trades yet. Let the bot run and generate trades!")
