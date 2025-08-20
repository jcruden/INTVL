import streamlit as st
import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def main():

    st.set_page_config(
        page_title="INTVL FAQ Search",
        page_icon="🏃",  # Running emoji - page_icon only accepts emojis
        layout="wide"
    )
    
    # Try to display logo if it exists
    logo_path = "intvl_logo.png"
    if os.path.exists(logo_path):
        col1, col2 = st.columns([1, 4])
        with col1:
            st.image(logo_path, width=100)
        with col2:
            st.title("INTVL FAQ")
    else:
        st.title("🏃 INTVL FAQ")
    
    st.markdown("Ask any question about INTVL!")
    
    # Main question interface
    st.markdown("---")
    
    # Question input
    question = st.text_input("Ask your question:", placeholder="e.g., How is my country calculated?")
    
    # Threshold slider
    threshold = st.slider("Answer Threshold (Testing - higher threshold = more likely to guess)", min_value=0.1, max_value=1.0, value=0.7, step=0.1, 
                         help="Lower = more strict, Higher = more lenient")
    
    if question:
        with st.spinner("Finding answer..."):
            try:
                from answer_questions import get_answer
                answer = get_answer(question, threshold=threshold)
                
                # Display answer with styling
                if "I'm not sure" in answer:
                    st.warning(f"**Answer:** {answer}")
                elif "Error:" in answer:
                    st.error(f"**Error:** {answer}")
                else:
                    st.success(f"**Answer:** {answer}")
                    
            except Exception as e:
                st.error(f"**Error:** {e}")
                st.info("Make sure embeddings are built first!")
    
    # Footer
    st.markdown("---")
    st.markdown("Built using Streamlit | INTVL FAQ System")

if __name__ == "__main__":
    main()
