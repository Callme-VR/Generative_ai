import streamlit as st
from agent import Critical_improvement_loop, SAMPLE_PROMPTS
from dotenv import load_dotenv

load_dotenv()


st.set_page_config(
    page_title="AI Critical Reasoning Engine",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 Critical Reasoning AI")
st.write("Generate answers using a multi-step reasoning + critique + improvement loop.")

# Sidebar controls
st.sidebar.header("⚙️ Settings")

iterations = st.sidebar.slider(
    "Number of Improvement Iterations",
    min_value=1,
    max_value=5,
    value=2
)

prompt = st.text_area(
    "Enter your question",
    height=150,
)

st.sidebar.markdown("### Sample Prompts")

for p in SAMPLE_PROMPTS:
    if st.sidebar.button(p):
        prompt = p

run_button = st.button("🚀 Generate Answer")


if run_button:

    if not prompt.strip():
        st.warning("Please enter a question")
        st.stop()

    result = Critical_improvement_loop(
        prompt=prompt,
        max_iteration=iterations
    )

    st.success("Generation Completed!")

    st.subheader("🏆 Final Answer")
    st.write(result["Final_answers"])

    st.divider()

    st.subheader("🔎 Reasoning Process")

    for i, iteration in enumerate(result["iterations"]):

        if iteration["type"] == "initial":
            with st.expander(f"Initial Answer"):
                st.write(iteration["answer"])

        else:
            with st.expander(f"Iteration {i}"):

                st.markdown("**Critiques**")
                st.write(iteration["critiques"])

                st.markdown("**Revised Answer**")
                st.write(iteration["answer"])
