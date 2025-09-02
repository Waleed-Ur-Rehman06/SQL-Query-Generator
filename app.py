import streamlit as st
from db_utils import get_db_connection, get_table_schema, execute_sql_query
from llm_utils import get_gemini_response
import pandas as pd
import plotly.express as px

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="SQL Query with Gemini AI",
    page_icon="🤖",
    layout="wide",
)

st.markdown(
    """
    <style>
    .stApp {
        background-color: #f0f2f6;
    }
    .main-header {
        text-align: center;
        font-size: 3.5rem;
        font-weight: bold;
        color: #4a90e2;
        padding-top: 2rem;
    }
    .subheader {
    display: block;
    text-align: center;
    margin-left: auto;
    margin-right: auto;
    font-size: 1.5rem;
    color: #555;
    margin-bottom: 2rem;
}

    .query-input {
        font-size: 1.2rem;
    }
    .results-container {
        margin-top: 2rem;
        padding: 1.5rem;
        background-color: #ffffff;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .stDataFrame {
        width: 100%;
    }
    .stButton>button {
        background-color: #4a90e2;
        color: white;
        font-size: 1.2rem;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #357ABD;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<h1 class="main-header">SQL Query Generator</h1>', unsafe_allow_html=True)
st.markdown('<p class="subheader">Ask a question about database in natural language.</p>', unsafe_allow_html=True)



# Initialize session state for query history
if 'query_history' not in st.session_state:
    st.session_state.query_history = []

# --- SIDEBAR FOR HISTORY ---
with st.sidebar:
    st.header("Query History")
    if st.session_state.query_history:
        for i, (q, sql) in enumerate(st.session_state.query_history):
            with st.expander(f"Question #{i+1}"):
                st.write(f"**Question:** {q}")
                st.code(sql, language='sql')
    else:
        st.info("No queries yet.")

# --- MAIN APPLICATION LOGIC ---
conn = get_db_connection()
schema = get_table_schema(conn)

question = st.text_input("Input your question here:", key="input", placeholder="e.g., How many students are there in the DevOps class?")

submit_button = st.button("Generate & Execute Query")

if submit_button and question:
    with st.spinner("Generating and executing query..."):
        try:
            # Get SQL query from LLM
            sql_query = get_gemini_response(question, schema)
            
            st.success("Query generated successfully!")
            
            # Execute the SQL query
            conn_for_exec = get_db_connection()
            df, error_message = execute_sql_query(sql_query, conn_for_exec)
            
            if error_message:
                st.error(f"Error executing query: {error_message}")
                st.code(sql_query, language='sql')
            else:
                st.session_state.query_history.append((question, sql_query))
                
                with st.container():
                    st.markdown('<div class="results-container">', unsafe_allow_html=True)
                    st.subheader("Results")
                    st.write("---")
                    
                    st.markdown("##### AI-Generated SQL Query")
                    st.code(sql_query, language='sql')
                    
                    st.markdown("##### Query Results")
                    if not df.empty:
                        st.dataframe(df, use_container_width=True)
                        
                        # Check if columns are numerical for visualization
                        numeric_cols = df.select_dtypes(include=['int', 'float']).columns.tolist()
                        if numeric_cols:
                            st.markdown("---")
                            st.markdown("##### Data Visualization")
                            
                            # Use the first numeric column for the chart
                            col_to_visualize = numeric_cols[0]
                            
                            try:
                                # Try to use the first non-numeric column as x-axis
                                non_numeric_cols = df.select_dtypes(include=['object']).columns.tolist()
                                if non_numeric_cols:
                                    x_axis_col = non_numeric_cols[0]
                                    fig = px.bar(df, x=x_axis_col, y=col_to_visualize, title=f'{col_to_visualize} by {x_axis_col}')
                                else:
                                    fig = px.bar(df, y=col_to_visualize, title=f'{col_to_visualize}')
                                st.plotly_chart(fig, use_container_width=True)
                            except Exception as e:
                                st.warning(f"Could not create a visualization. Error: {e}")

                    else:
                        st.info("The query returned no results.")
                    st.markdown('</div>', unsafe_allow_html=True)

        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
            
elif submit_button:
    st.warning("Please enter a question.")


