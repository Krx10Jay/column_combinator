import streamlit as st
import pandas as pd
from column_mapper import column_maper  
import io

def main():
    # Set page config (reduces those ScriptRunContext warnings)
    st.set_page_config(
        page_title="Column Mapper Pro",
        page_icon="🔀",
        layout="wide"
    )
    
    # Initialize session state for user name if it doesn't exist
    if 'user_name' not in st.session_state:
        st.session_state.user_name = ""
    
    # Sidebar for user input
    with st.sidebar:
        st.title("Welcome!")
        if not st.session_state.user_name:
            user_name = st.text_input("Please enter your name to continue:")
            if user_name:
                st.session_state.user_name = user_name.strip()
                st.rerun()
        else:
            st.success(f"Welcome back, {st.session_state.user_name}!")
            if st.button("Change name"):
                st.session_state.user_name = ""
                st.rerun()
    
    # Main content area
    if st.session_state.user_name:
        # Personalized header
        st.title(f"Hello, {st.session_state.user_name}! 👋")
        st.subheader("Column Mapping Tool")
        
        # App explanation
        with st.expander("ℹ️ What this app does"):
            st.markdown(f"""
            **Hi {st.session_state.user_name},** this app helps you:
            
            - 🔗 Create relationships between two columns in your data
            - 📊 Generate all possible combinations between them
            - 💾 Export the results for analysis
            
            **Example use cases:**
            - Mapping warehouses to all possible SKUs
            - Connecting sales regions to products
            - Creating test cases for data validation
            
            The app will preserve all unique values from both columns and create a comprehensive mapping.
            """)
        
        # File upload section
        st.divider()
        st.header("Let's get started!")
    
        # File upload
        uploaded_file = st.file_uploader("Upload a file", type=["csv", "xlsx"])
        
        if uploaded_file is not None:
            # Determine file type
            file_extension = uploaded_file.name.split(".")[-1].lower()
            doc_type = "csv" if file_extension == "csv" else "excel" if file_extension in ["xlsx", "xls"] else None
            
            if doc_type is None:
                st.error("Unsupported file type. Please upload a CSV or Excel file.")
                return
                
            # Preview the uploaded file
            try:
                # Read the file content into memory first
                file_content = uploaded_file.read()

                if doc_type == "csv":
                    #uploaded_file = StringIO(uploaded_file.getvalue().decode("utf-8"))
                    df = pd.read_csv(io.BytesIO(file_content))
                else:
                    df = pd.read_excel(uploaded_file)
                    
                # st.subheader("File Preview")
                # st.write(df.head())
                
                # Column selection
                st.subheader("Column Selection")
                col1 = st.selectbox("Select first column", df.columns)
                col2 = st.selectbox("Select second column", df.columns)
                
                if st.button("Generate Mappings"):
                    with st.spinner("Processing..."):
                        # Call the column_maper function
                        result_df = column_maper(
                            col1=col1,
                            col2=col2,
                            dataframe=df,
                            doc_type=doc_type
                        )
                        
                        if result_df is not None:
                            st.subheader("Mapped Results")
                            st.write(result_df)
                            
                            # Download button
                            csv = result_df.to_csv(index=False).encode('utf-8')
                            st.download_button(
                                label="Download as CSV",
                                data=csv,
                                file_name="mapped_results.csv",
                                mime="text/csv"
                            )
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()