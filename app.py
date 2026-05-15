import streamlit as st
import sys, os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from auth import init_db, login_user, register_user, user_exists, is_logged_in, do_login, do_logout, get_username

init_db()

st.set_page_config(
    page_title="BookLens",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Session defaults ───────────────────────────────────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "username" not in st.session_state:
    st.session_state["username"] = ""
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "home"

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
div[data-testid="column"] button {
    width: 100% !important;
    height: 160px !important;
    border-radius: 14px !important;
    border: 1.5px solid !important;
    background-color: #1E1E2E !important;
    cursor: pointer !important;
    font-size: 1rem !important;
    white-space: pre-wrap !important;
}
div[data-testid="column"]:nth-child(1) button { border-color: #7F77DD !important; color: #7F77DD !important; }
div[data-testid="column"]:nth-child(2) button { border-color: #1D9E75 !important; color: #1D9E75 !important; }
div[data-testid="column"]:nth-child(3) button { border-color: #FAC775 !important; color: #FAC775 !important; }
div[data-testid="column"]:nth-child(4) button { border-color: #F09595 !important; color: #F09595 !important; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# NOT LOGGED IN → Login / Signup
# ══════════════════════════════════════════════════════════════════════════════
if not is_logged_in():
    st.markdown("""
        <h1 style='text-align:center; color:#7F77DD; font-size:2.8rem; margin-bottom:0'>📚 BookLens</h1>
        <p style='text-align:center; color:gray; margin-top:4px; margin-bottom:32px'>
            Your personal book analytics platform
        </p>
    """, unsafe_allow_html=True)

    tab_login, tab_signup = st.tabs(["🔑  Login", "📝  Sign Up"])

    with tab_login:
        st.markdown("<br>", unsafe_allow_html=True)
        _, center, _ = st.columns([1, 2, 1])
        with center:
            st.markdown("### 👋 Welcome back")
            login_email = st.text_input("Email address", key="login_email", placeholder="you@email.com")
            login_pass  = st.text_input("Password",      key="login_pass",  placeholder="••••••••", type="password")
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔑 Login", use_container_width=True, key="login_btn"):
                if not login_email or not login_pass:
                    st.warning("Please fill in both fields.")
                else:
                    name = login_user(login_email.strip(), login_pass)
                    if name:
                        do_login(name)
                        st.session_state["current_page"] = "home"
                        st.rerun()
                    else:
                        st.error("❌ Incorrect email or password.")
            st.caption("Don't have an account? Click the **Sign Up** tab above.")

    with tab_signup:
        st.markdown("<br>", unsafe_allow_html=True)
        _, center, _ = st.columns([1, 2, 1])
        with center:
            st.markdown("### ✨ Create Account")
            signup_name  = st.text_input("Full Name",        key="signup_name",  placeholder="Your Name")
            signup_email = st.text_input("Email address",    key="signup_email", placeholder="you@email.com")
            signup_pass  = st.text_input("Password",         key="signup_pass",  placeholder="Min 6 characters", type="password")
            signup_conf  = st.text_input("Confirm Password", key="signup_conf",  placeholder="Repeat password",  type="password")
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("📝 Create Account", use_container_width=True, key="signup_btn"):
                if not signup_name or not signup_email or not signup_pass or not signup_conf:
                    st.warning("Please fill in all fields.")
                elif signup_pass != signup_conf:
                    st.error("❌ Passwords do not match.")
                elif len(signup_pass) < 6:
                    st.error("❌ Password must be at least 6 characters.")
                elif user_exists(signup_email.strip()):
                    st.error("❌ An account with this email already exists.")
                else:
                    if register_user(signup_name.strip(), signup_email.strip(), signup_pass):
                        do_login(signup_name.strip())
                        st.session_state["current_page"] = "home"
                        st.rerun()
                    else:
                        st.error("Something went wrong. Please try again.")
            st.caption("Already have an account? Click the **Login** tab above.")

# ══════════════════════════════════════════════════════════════════════════════
# LOGGED IN → Full App with manual routing
# ══════════════════════════════════════════════════════════════════════════════
else:
    username = get_username()

    # ── Sidebar ────────────────────────────────────────────────────────────────
    with st.sidebar:
        st.markdown("## 📚 BookLens")
        st.markdown(f"👤 **{username}**")
        st.markdown("---")
        if st.button("🏠 Home",        use_container_width=True, key="nav_home"):
            st.session_state["current_page"] = "home"
            st.rerun()
        if st.button("📊 Dashboard",   use_container_width=True, key="nav_dash"):
            st.session_state["current_page"] = "dashboard"
            st.rerun()
        if st.button("🔮 Future Hits", use_container_width=True, key="nav_future"):
            st.session_state["current_page"] = "future"
            st.rerun()
        if st.button("💎 Hidden Gems", use_container_width=True, key="nav_gems"):
            st.session_state["current_page"] = "gems"
            st.rerun()
        if st.button("🤖 Recommend",   use_container_width=True, key="nav_rec"):
            st.session_state["current_page"] = "recommend"
            st.rerun()
        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True, key="logout_btn"):
            do_logout()
            st.rerun()
        st.caption("Built with ❤️ using Streamlit & Python")

    # ── Page Router ────────────────────────────────────────────────────────────
    page = st.session_state["current_page"]

    # ── HOME ───────────────────────────────────────────────────────────────────
    if page == "home":
        st.markdown(f"""
            <h1 style='text-align:center; color:#7F77DD; font-size:3rem; margin-bottom:0'>📚 BookLens</h1>
            <p style='text-align:center; color:gray; font-size:1.1rem; margin-top:6px'>
                Welcome back, <strong>{username}</strong> 👋
            </p>
        """, unsafe_allow_html=True)
        st.markdown("---")

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("📊\n\nDashboard\n\nGenre trends, ratings & bestseller stats", key="card_dash"):
                st.session_state["current_page"] = "dashboard"
                st.rerun()
        with col2:
            if st.button("🔮\n\nFuture Hits\n\nBooks predicted to become next bestsellers", key="card_future"):
                st.session_state["current_page"] = "future"
                st.rerun()
        with col3:
            if st.button("💎\n\nHidden Gems\n\nHighly rated books most people haven't found", key="card_gems"):
                st.session_state["current_page"] = "gems"
                st.rerun()
        with col4:
            if st.button("🤖\n\nRecommend\n\nGet personalised book recommendations", key="card_rec"):
                st.session_state["current_page"] = "recommend"
                st.rerun()

        st.markdown("---")
        st.info("👆 Click any card above or use the sidebar to navigate")

    # ── DASHBOARD ──────────────────────────────────────────────────────────────
    elif page == "dashboard":
        exec(open("pages/Dashboard.py", encoding="utf-8").read())

    # ── FUTURE HITS ────────────────────────────────────────────────────────────
    elif page == "future":
        exec(open("pages/Future_Hits.py", encoding="utf-8").read())

    # ── HIDDEN GEMS ────────────────────────────────────────────────────────────
    elif page == "gems":
        exec(open("pages/Gems.py", encoding="utf-8").read())

    # ── RECOMMEND ──────────────────────────────────────────────────────────────
    elif page == "recommend":
        exec(open("pages/Recommend.py", encoding="utf-8").read())