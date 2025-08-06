import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.title("Flavor Tour Manual Tracker")

CSV_FILE = "alldata270735.csv"

for side in ["L", "R"]:
    for key in ["start_time", "end_time", "checkout_time"]:
        full_key = f"{side}_{key}"
        if full_key not in st.session_state:
            st.session_state[full_key] = ""

left_col, right_col = st.columns(2)

def flavor_form(side, col):
    with col:
        st.subheader(f"Side {side}")

        if st.button(f"Set Start Time ({side})"):
            st.session_state[f"{side}_start_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if st.button(f"Set End Time ({side})"):
            st.session_state[f"{side}_end_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if st.button(f"Set Checkout Time ({side})"):
            st.session_state[f"{side}_checkout_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with st.form(f"entry_form_{side}"):
            group_size = st.number_input(f"Group Size ({side})", min_value=1, step=1, key=f"group_size_{side}")
            store = st.selectbox(f"Store Location ({side})", ["Hatmakers", "Dry Cleaning", "Electronics Repair"], key=f"store_{side}")

            start_time = st.text_input("Start Time", value=st.session_state[f"{side}_start_time"], key=f"start_time_input_{side}")
            end_time = st.text_input("End Time", value=st.session_state[f"{side}_end_time"], key=f"end_time_input_{side}")
            checkout_time = st.text_input("Checkout Time", value=st.session_state[f"{side}_checkout_time"], key=f"checkout_time_input_{side}")

            flavor_tour = st.radio("Flavor Tour?", ["Yes", "No"], key=f"flavor_tour_{side}")
            notes = st.text_area("Notes (optional)", key=f"notes_{side}")

            submitted = st.form_submit_button(f"Submit Entry ({side})")

            if submitted:
                entry = {
                    "Day": datetime.now().strftime("%A"),
                    "Store": store,
                    "Group Size": group_size,
                    "Side": side,
                    "Start Time": start_time,
                    "End Time": end_time,
                    "Checkout Time": checkout_time,
                    "Flavor Tour": flavor_tour,
                    "Notes": notes,
                }

                try:
                    df = pd.read_csv(CSV_FILE)
                except FileNotFoundError:
                    df = pd.DataFrame()

                df = pd.concat([df, pd.DataFrame([entry])], ignore_index=True)
                df.to_csv(CSV_FILE, index=False)
                st.success(f"Entry for Side {side} saved!")

flavor_form("L", left_col)
flavor_form("R", right_col)

st.markdown("---")
if st.checkbox("Show collected data", key="show_data"):
    try:
        df = pd.read_csv(CSV_FILE)
        filter_side = st.radio("Filter by Side", ["All", "L", "R"], key="filter_side")
        if filter_side != "All":
            df = df[df["Side"] == filter_side]
        st.dataframe(df)
    except FileNotFoundError:
        st.info("No data collected yet.")

if st.checkbox("I'm sure I want to delete all data", key="confirm_delete"):
    if st.button("❌ Delete All Data"):
        if os.path.exists(CSV_FILE):
            os.remove(CSV_FILE)
            st.success("All data has been deleted.")
        else:
            st.info("No data file found to delete.")
