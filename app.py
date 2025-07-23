import os
import json
import streamlit as st
import difflib
from supabase_client import supabase

# ------------------------------
# Load FAQ
# ------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
faq_path = os.path.join(BASE_DIR, "faq.json")
log_path = os.path.join(BASE_DIR, "questions_log.txt")

if not os.path.exists(faq_path):
    st.error("faq.json not found!")
    st.stop()

with open(faq_path) as f:
    faq_data = json.load(f)

# ------------------------------
# Find best answer
# ------------------------------
def find_answer(question):
    all_questions = []
    question_to_answer = {}

    for item in faq_data:
        for q in item["questions"]:
            all_questions.append(q.lower())
            question_to_answer[q.lower()] = item["answer"]

    best_match = difflib.get_close_matches(question.lower(), all_questions, n=1, cutoff=0.3)
    if best_match:
        return question_to_answer[best_match[0]]
    return "Sorry, I don't know that yet! Please contact the school office for more details."

# ------------------------------
# Save log
# ------------------------------
def log_question(username, question):
    with open(log_path, "a") as f:
        f.write(f"{username}: {question}\n")

# ------------------------------
# Register user with email
# ------------------------------
def register_user(username, password, email):
    if not username or not password or not email:
        return "All fields are required."
    if len(password) < 6:
        return "Password must be at least 6 characters."
    if "@" not in email:
        return "Invalid email address."

    exists = supabase.table("users").select("*").or_(f"username.eq.{username},email.eq.{email}").execute()
    if exists.data:
        return "Username or email already exists."

    supabase.table("users").insert({
        "username": username,
        "password": password,
        "email": email
    }).execute()
    return "OK"

# ------------------------------
# Login user
# ------------------------------
def check_login(username, password):
    result = supabase.table("users") \
        .select("*") \
        .eq("username", username) \
        .eq("password", password) \
        .execute()
    if result.data:
        return True
    return False

# ------------------------------
# UI
# ------------------------------
st.title("📚 STEM Obour FAQ Chatbot")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

if not st.session_state.logged_in:
    st.subheader("🔑 Login")
    login_user = st.text_input("Username", key="login_user")
    login_pass = st.text_input("Password", type="password", key="login_pass")
    if st.button("Login"):
        if check_login(login_user, login_pass):
            st.session_state.logged_in = True
            st.session_state.username = login_user
            st.success(f"Welcome back, {login_user}!")
        else:
            st.error("Invalid username or password")

    st.divider()

    st.subheader("📝 Register")
    new_user = st.text_input("New Username", key="new_user")
    new_pass = st.text_input("New Password", type="password", key="new_pass")
    new_email = st.text_input("Email", key="new_email")
    if st.button("Register"):
        result = register_user(new_user, new_pass, new_email)
        if result == "OK":
            st.success("Account created! Please log in.")
        else:
            st.error(result)

else:
    st.success(f"✅ Logged in as {st.session_state.username}")

    user_question = st.text_input("Ask your question:")

    if user_question:
        answer = find_answer(user_question)
        st.write(answer)
        log_question(st.session_state.username, user_question)

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""

st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        bottom: 9px;
        right: 15px;
        font-size: 15px;
        color: #555;
    }
    </style>
    <div class="footer">
        Made with ❤️ by Mahmoud Kaddour and Eyad Tamer
    </div>
    """,
    unsafe_allow_html=True
)
