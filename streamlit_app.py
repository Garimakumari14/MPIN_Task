import streamlit as st
from mpin_checker import MPINEvaluator
from streamlit_lottie import st_lottie
import json
import time


@st.cache_data
def load_lottie_animation(filepath):
    """Loads a Lottie animation from a JSON file."""
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return None 

def apply_custom_css(filepath="style.css"):
    """Applies custom CSS from a file."""
    try:
        with open(filepath) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass 

# --- Load Lottie Animations (Centralized Loading) ---
lottie_header = load_lottie_animation("assets/animation.json") 

lottie_success = load_lottie_animation("assets/success.json")
lottie_warning = load_lottie_animation("assets/warning.json")
lottie_loading = load_lottie_animation("assets/loading_cube.json")

apply_custom_css()


st.set_page_config(
    page_title="Guardian MPIN Shield 🛡️", 
    page_icon="🔑",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- Session State for Page Navigation ---
if 'page' not in st.session_state:
    st.session_state.page = 'welcome' 

# --- Welcome Page ---
if st.session_state.page == 'welcome':
    
    st.image("assets/welcome_image.png", use_container_width=True, caption="Your Digital Security Starts Here") 
    
    st.markdown("<h1 class='welcome-title'>Welcome to Guardian MPIN Shield! 🛡️</h1>", unsafe_allow_html=True)
    st.markdown(
        """
        <p class='welcome-text'>
            Your digital security starts with a strong MPIN.
            This tool helps you analyze and strengthen your MPIN against common vulnerabilities.
            Protect your accounts, protect your peace of mind.
        </p>
        """,
        unsafe_allow_html=True
    )
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔐 Let's Get Started!", key="start_button"):
        st.session_state.page = 'main_app'
        st.rerun() # Using st.rerun() for page navigation

    st.markdown("</div>", unsafe_allow_html=True)

# --- Main Application Page ---
elif st.session_state.page == 'main_app':
    st.markdown("<div class='header-container'>", unsafe_allow_html=True)
    if lottie_header:
        st_lottie(lottie_header, height=150, speed=0.8, loop=True, key="header_animation_main")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<h1 class='main-title'>🔒 MPIN Strength Evaluator</h1>", unsafe_allow_html=True)
    st.markdown(
        """
        <p class='intro-text'>
            Enter your MPIN and a few personal dates. We'll analyze its strength against common patterns and demographic data.
            Your privacy is paramount; **no data is stored.**
        </p>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown("---") 

    # --- Input Section (Sidebar) ---
    with st.sidebar:
        st.markdown("<h2 class='sidebar-title'>Personal Information 👤</h2>", unsafe_allow_html=True)
        st.info("Your personal details help us identify common, easily guessable patterns. **All data is processed locally and discarded.**")

        mpin = st.text_input("🔑 Enter your MPIN", type="password", max_chars=6, help="Your 4 or 6-digit Personal Identification Number.")
        
        show_mpin = st.checkbox("👁️ Show MPIN", help="Toggle to view the MPIN you entered.")
        if show_mpin:
            st.code(mpin, language="text") 
            
        st.markdown("---") 

        st.markdown("<h3 class='sidebar-subtitle'>Important Dates 🗓️</h3>", unsafe_allow_html=True)
        dob_self = st.date_input("🎂 Your Date of Birth", help="This is crucial for robust analysis.", value=None)
        dob_spouse = st.date_input("💑 Spouse's Date of Birth (Optional)", help="Leave blank if not applicable.", value=None)
        anniversary = st.date_input("🎉 Anniversary Date (Optional)", help="Enter if applicable.", value=None)

    # --- Evaluation Button & Logic ---
    st.markdown("<br>", unsafe_allow_html=True) 
    if st.button("🚀 Evaluate My MPIN", key="evaluate_button"):
        if not mpin:
            st.error("Please enter your MPIN to proceed with evaluation. 🤔")
        elif not (mpin.isdigit() and len(mpin) in [4, 6]):
            st.error("🚨 MPIN must be numeric and either 4 or 6 digits long. Please double-check!")
        elif not dob_self:
            st.warning("⚠️ **Your Date of Birth is required** for comprehensive analysis. Please provide it.")
        else:
            # Spinner with Lottie animation
            with st.status("Analyzing your MPIN strength...", expanded=True) as status:
                st.write("Fetching demographic patterns...")
                time.sleep(0.5)
                st.write("Cross-referencing common weak spots...")
                time.sleep(0.5)
                st.write("Calculating final strength score...")
                
                evaluator = MPINEvaluator(
                    mpin=mpin,
                    dob_self=dob_self.strftime("%Y-%m-%d") if dob_self else None,
                    dob_spouse=dob_spouse.strftime("%Y-%m-%d") if dob_spouse else None,
                    anniversary=anniversary.strftime("%Y-%m-%d") if anniversary else None
                )
                result = evaluator.evaluate_strength()
                status.update(label="MPIN analysis complete!", state="complete", expanded=False)

            st.markdown("---") 

            st.markdown("<h2 class='result-title'>🎯 Your MPIN Evaluation Report</h2>", unsafe_allow_html=True)
            st.markdown(f"<p class='mpin-display'>**MPIN Entered:** <span class='mpin-value'>`{result['MPIN']}`</span></p>", unsafe_allow_html=True)

            strength_color = "green" if result["Strength"] == "STRONG" else "orange" if result["Strength"] == "MODERATE" else "red"
            st.markdown(f"<p class='strength-display'>**Overall Strength:** <span class='strength-{strength_color}'>{result['Strength']}</span></p>", unsafe_allow_html=True)

            if result["Strength"] == "WEAK":
                if lottie_warning:
                    st_lottie(lottie_warning, height=100, speed=1, key="warning_animation_result")
                st.error("🚨 **Immediate Action Recommended: Your MPIN is WEAK!** It's highly susceptible to being guessed by malicious actors. Please change it!")
                st.markdown("<h3 class='reasons-title'>Reasons for Weakness:</h3>", unsafe_allow_html=True)
                for reason in result["Reasons"]:
            
                    st.markdown(f"- 💡 <span class='reason-text'>{reason}</span>", unsafe_allow_html=True) 
                st.info("💡 **Tip:** Avoid using personal dates, repetitive numbers, or simple sequences. Combine unique digits.")
            elif result["Strength"] == "MODERATE":
                if lottie_warning: 
                    st_lottie(lottie_warning, height=100, speed=0.8, key="moderate_animation_result")
                st.warning("🟠 **Good, but could be stronger: Your MPIN is MODERATE.** While not easily guessable, there are identifiable patterns.")
                st.markdown("<h3 class='reasons-title'>Suggestions for Improvement:</h3>", unsafe_allow_html=True)
                for reason in result["Reasons"]:
                  
                    st.markdown(f"- 📝 <span class='reason-text'>{reason}</span>", unsafe_allow_html=True)
                st.info("💡 **Tip:** Introduce more randomness. Think of digits that don't relate to your personal life or simple patterns.")
            else: 
                if lottie_success:
                    st_lottie(lottie_success, height=100, speed=1, key="success_animation_result")
                st.success("🎉 **Outstanding Security! Your MPIN is STRONG and highly secure.** You've chosen wisely! 🔐")
                st.balloons() 
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("---") 
            st.markdown("<h3 class='small-tip'>Want to try another MPIN? Just adjust the inputs above!</h3>", unsafe_allow_html=True)


    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🏠 Back to Welcome Screen", key="back_to_welcome"):
        st.session_state.page = 'welcome'
        st.rerun() 
st.markdown("---")
st.caption("Crafted by Garima | Powered by Streamlit & Python | © OneBanc")