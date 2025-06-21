import streamlit as st

st.set_page_config(page_title="מחשבון שכר עידוד", layout="centered")

st.title("💼 מחשבון שכר עידוד למטפל/ת בקהילה")

# קלט מהמשתמש
treatments = st.number_input("טיפולים משוקללים", min_value=0.0, step=0.1, format="%.2f")
hours = st.number_input("שעות לתגמול", min_value=0.0, step=0.1, format="%.2f")
position = st.number_input("אחוז משרה", min_value=0.0, max_value=100.0, step=0.5, format="%.1f")

if st.button("חשב שכר עידוד"):
    if hours == 0:
        st.error("שעות לתגמול לא יכולות להיות אפס.")
    else:
        LOWER_LIMIT = 1.85
        UPPER_LIMIT = 2.5
        UNIT_VALUE = 62.5
        MAX_BONUS = 6500

        output = treatments / hours
        if output <= LOWER_LIMIT:
            bonus = 0
            st.warning(f"תפוקה בפועל: {output:.2f} — אין זכאות לשכר עידוד.")
        else:
            effective_output = min(output, UPPER_LIMIT)
            bonus = (effective_output - LOWER_LIMIT) * hours * UNIT_VALUE
            max_bonus_by_position = MAX_BONUS * (position / 100)
            bonus = min(bonus, max_bonus_by_position)

            st.success(f"תפוקה בפועל: {output:.2f}")
            st.info(f"שכר עידוד לחודש: ₪{bonus:,.2f}")