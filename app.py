
import streamlit as st
from langchain_core.messages import AIMessage
from utils import run_agent_sync


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="AI Learning Path Generator",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 MCP - AI-Powered Personalized Learning Path Generator")

st.markdown(
    "Generate personalized learning paths using AI, "
    "research YouTube videos, and organize your learning resources."
)


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "current_step" not in st.session_state:
    st.session_state.current_step = ""

if "progress" not in st.session_state:
    st.session_state.progress = 0

if "is_generating" not in st.session_state:
    st.session_state.is_generating = False


# --------------------------------------------------
# SIDEBAR CONFIGURATION
# --------------------------------------------------

st.sidebar.header("Configuration")

google_api_key = st.sidebar.text_input(
    "Google Gemini API Key",
    type="password",
    help="Enter your Gemini API key."
)

st.sidebar.success(
    "Composio MCP connection configured through .env"
)

st.sidebar.markdown(
    """
    **Connected integrations**
    - YouTube
    - Google Drive
    - Notion
    """
)


# --------------------------------------------------
# APPLICATION GUIDE
# --------------------------------------------------

st.info(
    """
    **Quick Guide**

    1. Enter your Gemini API key.
    2. Connect YouTube, Google Drive and Notion through Composio.
    3. Enter your learning goal and duration.
    4. Select Google Drive or Notion as your document destination.
    5. Generate your personalized learning path.
    """
)


# --------------------------------------------------
# USER INPUT
# --------------------------------------------------

st.header("Enter Your Learning Goal")

user_goal = st.text_input(
    "What do you want to learn?",
    placeholder="Example: I want to learn Python in 7 days."
)

destination = st.selectbox(
    "Choose your document destination",
    ["Google Drive", "Notion"]
)


# --------------------------------------------------
# PROGRESS TRACKING
# --------------------------------------------------

progress_container = st.container()
progress_bar = st.empty()


def update_progress(message: str):

    st.session_state.current_step = message

    if "Setting up" in message:
        st.session_state.progress = 0.1

    elif "Connecting to Composio" in message:
        st.session_state.progress = 0.2

    elif "Discovering available" in message:
        st.session_state.progress = 0.3

    elif "Loaded" in message:
        st.session_state.progress = 0.4

    elif "Creating AI agent" in message:
        st.session_state.progress = 0.5

    elif "Generating your learning path" in message:
        st.session_state.progress = 0.6

    elif "Learning path generation complete" in message:
        st.session_state.progress = 1.0
        st.session_state.is_generating = False

    progress_bar.progress(st.session_state.progress)

    with progress_container:
        st.write(f"➡️ {message}")


# --------------------------------------------------
# GENERATE LEARNING PATH
# --------------------------------------------------

if st.button(
    "Generate Learning Path",
    type="primary",
    disabled=st.session_state.is_generating
):

    if not google_api_key.strip():
        st.error("Please enter your Gemini API key.")

    elif not user_goal.strip():
        st.warning("Please enter your learning goal.")

    else:

        try:

            st.session_state.is_generating = True
            st.session_state.progress = 0

            progress_bar.progress(0)

            complete_user_goal = (
                f"{user_goal}\n\n"
                f"Selected document destination: {destination}.\n"
                "Use this destination for creating the learning resource document."
            )

            with st.spinner(
                "Building your personalized learning path..."
            ):

                result = run_agent_sync(
                    google_api_key=google_api_key,
                    user_goal=complete_user_goal,
                    progress_callback=update_progress
                )

            st.session_state.is_generating = False

            # ------------------------------------------
            # DISPLAY FINAL AI RESPONSE ONLY
            # ------------------------------------------

            st.header("Your Learning Path")

            if result and "messages" in result:

                ai_messages = [
                    msg
                    for msg in result["messages"]
                    if isinstance(msg, AIMessage)
                    and msg.content
                ]

                if ai_messages:

                    final_content = ai_messages[-1].content

                    if isinstance(final_content, str):
                        st.markdown(final_content)

                    elif isinstance(final_content, list):

                        for block in final_content:

                            if isinstance(block, dict):
                                if block.get("type") == "text":
                                    st.markdown(block.get("text", ""))

                            else:
                                st.write(block)

                else:
                    st.error(
                        "The AI did not generate a final response."
                    )

            else:
                st.error("No results were generated.")

        except Exception as error:

            st.session_state.is_generating = False

            st.error(f"An error occurred: {error}")

            st.exception(error)
