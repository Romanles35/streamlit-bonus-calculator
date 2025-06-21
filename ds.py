import streamlit as st
import calendar

st.set_page_config(page_title="מחשבון שכר עידוד", layout="centered")
st.title("💼 מחשבון שכר עידוד לפיזיותרפיסט במכבי")

mode = st.radio("בחר מצב:", ["חישוב רגיל (סוף חודש)", "תחזית עתידית (אמצע חודש)"])

# קבועים
LOWER_LIMIT = 1.85
UPPER_LIMIT = 2.5
UNIT_VALUE = 62.5
MAX_BONUS = 6500

if mode == "חישוב רגיל (סוף חודש)":
    st.subheader("🔁 חישוב לפי נתוני חודש מלא")
    treatments = st.number_input("טיפולים משוקללים", min_value=0.0, step=0.1, format="%.2f")
    hours = st.number_input("שעות לתגמול", min_value=0.0, step=0.1, format="%.2f")
    position = st.number_input("אחוז משרה", min_value=0.0, max_value=100.0, step=0.5, format="%.1f")

    if st.button("חשב שכר עידוד"):
        if hours == 0:
            st.error("שעות לתגמול לא יכולות להיות אפס.")
        else:
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

elif mode == "תחזית עתידית (אמצע חודש)":
    st.subheader("📈 תחזית לפי מצב נוכחי בחודש")

    year = st.number_input("שנה (למשל 2025)", min_value=2000, max_value=2100, value=2025, step=1)
    month = st.selectbox("חודש", list(range(1, 13)), format_func=lambda m: f"חודש {m}")
    current_day = st.number_input("תאריך היום בחודש", min_value=1, max_value=31, value=21)

    days_in_month = calendar.monthrange(year, month)[1]

    treatments_so_far = st.number_input("טיפולים משוקללים עד כה", min_value=0.0, step=0.1, format="%.2f")
    hours_so_far = st.number_input("שעות לתגמול עד כה", min_value=0.0, step=0.1, format="%.2f")
    position = st.number_input("אחוז משרה", min_value=0.0, max_value=100.0, step=0.5, format="%.1f")

    if st.button("חשב תחזית"):
        if hours_so_far == 0 or current_day == 0 or current_day > days_in_month:
            st.error("יש להזין ערכים תקינים.")
        else:
            progress_ratio = current_day / days_in_month
            estimated_total_hours = hours_so_far / progress_ratio
            estimated_total_treatments = treatments_so_far / progress_ratio
            output = estimated_total_treatments / estimated_total_hours

            if output <= LOWER_LIMIT:
                bonus = 0
                st.warning(f"תפוקה צפויה: {output:.2f} — אם תמשיך בקצב זה, לא תהיה זכאות לשכר עידוד.")
            else:
                effective_output = min(output, UPPER_LIMIT)
                bonus = (effective_output - LOWER_LIMIT) * estimated_total_hours * UNIT_VALUE
                max_bonus_by_position = MAX_BONUS * (position / 100)
                bonus = min(bonus, max_bonus_by_position)

                st.success(f"תפוקה צפויה: {output:.2f}")
                st.info(f"שכר עידוד צפוי בקצב הנוכחי: ₪{bonus:,.2f}")

            if output < 1.85:
                st.warning("🔺 כדאי להגביר את קצב הטיפולים כדי לעמוד ביעד שכר העידוד.")
