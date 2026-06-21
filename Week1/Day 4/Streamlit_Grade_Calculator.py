import streamlit as st

# -----------------------------
# Streamlit UI Setup
# -----------------------------
st.set_page_config(page_title="Grade Calculator", page_icon="🎓", layout="centered")

st.markdown(
    """
    <h1 style='text-align: center; color: #4CAF50; font-size: 42px;'>🎓 Grade Calculator</h1>
    <p style='text-align: center; font-size: 20px; color: #555;'>
        Enter your marks and get your grade in a beautifully styled card.
    </p>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# Grade Logic with Beautiful UI
# -----------------------------
def grade(marks):
    try:
        marks = int(marks)

        if marks < 0 or marks > 100:
            return {
                "grade": "❌ Invalid",
                "color": "#ff4d4d",
                "bg": "linear-gradient(135deg, #ffcccc, #ff9999)",
                "message": "Marks must be between 0 and 100."
            }

        if 90 <= marks <= 100:
            return {"grade": "🅰", "color": "#2ecc71", "bg": "linear-gradient(135deg, #d4fcd7, #a8f0b6)", "message": "Excellent performance!"}
        elif 80 <= marks < 90:
            return {"grade": "🅱", "color": "#3498db", "bg": "linear-gradient(135deg, #d6eaff, #a8d4ff)", "message": "Great job!"}
        elif 70 <= marks < 80:
            return {"grade": "🅲", "color": "#e67e22", "bg": "linear-gradient(135deg, #ffe2c6, #ffc48a)", "message": "Good effort!"}
        elif 60 <= marks < 70:
            return {"grade": "🅳", "color": "#9b59b6", "bg": "linear-gradient(135deg, #ecd9f9, #d3b4f2)", "message": "You passed!"}
        elif 50 <= marks < 60:
            return {"grade": "🅴", "color": "#f1c40f", "bg": "linear-gradient(135deg, #fff4c2, #ffe680)", "message": "Needs improvement."}
        else:
            return {"grade": "🅵", "color": "#e74c3c", "bg": "linear-gradient(135deg, #ffd6d6, #ffb3b3)", "message": "Better luck next time."}

    except ValueError:
        return {
            "grade": "❌ Invalid",
            "color": "#ff4d4d",
            "bg": "linear-gradient(135deg, #ffcccc, #ff9999)",
            "message": "Please enter a valid number."
        }

# -----------------------------
# Input Box
# -----------------------------
marks = st.text_input("Enter your marks (0–100):", "")

# -----------------------------
# Button + Beautiful Output Card
# -----------------------------
if st.button("Calculate Grade"):
    result = grade(marks)

    st.markdown(
        f"""
        <div style="
            margin-top: 30px;
            padding: 30px;
            border-radius: 15px;
            background: {result['bg']};
            box-shadow: 0 4px 15px rgba(0,0,0,0.15);
            text-align: center;
            animation: fadeIn 1s ease-in-out;
        ">
            <h1 style="font-size: 70px; margin: 0; color: {result['color']};">{result['grade']}</h1>
            <p style="font-size: 22px; color: #333; margin-top: 10px;">{result['message']}</p>
        </div>

        <style>
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
