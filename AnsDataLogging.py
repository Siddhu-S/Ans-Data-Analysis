import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.title("Flavor Tour Manual Tracker")

CSV_FILE = "flavor_tour_data.csv"


for side in ["L", "R"]:
    for key in ["start_time", "end_time", "checkout_time", "reset"]:
        full_key = f"{side}_{key}"
        if full_key not in st.session_state:
            st.session_state[full_key] = ""
    if f"group_size_{side}" not in st.session_state:
        st.session_state[f"group_size_{side}"] = 1
    if f"flavor_tour_{side}" not in st.session_state:
        st.session_state[f"flavor_tour_{side}"] = "Yes"
    if f"notes_{side}" not in st.session_state:
        st.session_state[f"notes_{side}"] = ""

left_col, right_col = st.columns(2)


def reset_fields(side):
    st.session_state[f"group_size_{side}"] = 1
    st.session_state[f"{side}_start_time"] = ""
    st.session_state[f"{side}_end_time"] = ""
    st.session_state[f"{side}_checkout_time"] = ""
    st.session_state[f"start_time_input_{side}"] = ""
    st.session_state[f"end_time_input_{side}"] = ""
    st.session_state[f"checkout_time_input_{side}"] = ""
    st.session_state[f"flavor_tour_{side}"] = "Yes"
    st.session_state[f"notes_{side}"] = ""
    st.session_state[f"{side}_reset"] = False
    st.rerun()


def flavor_form(side, col):
    if st.session_state.get(f"{side}_reset", False):
        reset_fields(side)

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
            store = st.selectbox(
                f"Store Location ({side})",
                ["Hatmakers", "Dry Cleaning", "Electronics Repair"],
                key=f"store_{side}"
            )

            start_time = st.text_input("Start Time", value=st.session_state[f"{side}_start_time"], key=f"start_time_input_{side}")
            end_time = st.text_input("End Time", value=st.session_state[f"{side}_end_time"], key=f"end_time_input_{side}")
            checkout_time = st.text_input("Checkout Time (optional)", value=st.session_state[f"{side}_checkout_time"], key=f"checkout_time_input_{side}")

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

                st.session_state[f"{side}_reset"] = True
                st.rerun()

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
    if st.button("Delete All Data"):
        if os.path.exists(CSV_FILE):
            os.remove(CSV_FILE)
            st.success("All data has been deleted.")
        else:
            st.info("No data file found to delete.")

st.markdown("Export Data")
if os.path.exists(CSV_FILE):
    with open(CSV_FILE, "rb") as f:
        st.download_button(
            label="Download flavor_tour_data.csv",
            data=f,
            file_name=CSV_FILE,
            mime="text/csv"
        )
else:
    st.info("No data available to download yet.")