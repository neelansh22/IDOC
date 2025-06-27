import requests
import streamlit as st
import os

# Azure LLM configuration
azure_endpoint = ""
api_key = ""  # Replace with your actual API key
deployment_name = ""  # Using the gpt-4o deployment


# Function to call Azure LLM for a chunk of the script
def call_llm_chunk(script_chunk):
    url = azure_endpoint
    headers = {
        "Content-Type": "application/json",
        "api-key": api_key,
    }
    data = {
        "messages": [
            {"role": "system", "content": "You are an assistant that generates detailed and easy-to-understand documentation as a markdown, make references to the functions whereever necessary as a method of explaining each functionality, make sure to find a right balance in documenting the script. Also generate an easy to understand description of the script as an algorithm towards the end."},
            {"role": "user", "content": f"Generate a detailed and easy-to-understand documentation for the following python script, remember this is just a chuck and following chunks will follow:\n\n{script_chunk}"}
        ],
        "max_tokens": 4096,  # Adjust token limit as needed
        "temperature": 0.7,
    }
    response = requests.post(url, headers=headers, json=data)
    
    try:
        response_json = response.json()
        if "choices" in response_json:
            return response_json["choices"][0]["message"]["content"].strip()
        else:
            st.error("Unexpected response format: 'choices' not found")
            st.json(response_json)  # Display the full response for debugging
            return "Error: Unable to generate documentation."
    except ValueError:
        st.error("Failed to decode the response as JSON.")
        st.text(response.text)  # Display the raw response text for debugging
        return "Error: Unable to generate documentation."

# Function to split the SQL script into chunks
def split_script_into_chunks(script_content, chunk_size=1500):
    script_lines = script_content.splitlines()
    chunks = []
    current_chunk = []
    current_length = 0
    
    for line in script_lines:
        line_length = len(line.split())
        if current_length + line_length > chunk_size:
            chunks.append("\n".join(current_chunk))
            current_chunk = [line]
            current_length = line_length
        else:
            current_chunk.append(line)
            current_length += line_length
    
    # Append the last chunk if any
    if current_chunk:
        chunks.append("\n".join(current_chunk))
    
    return chunks

# Function to format documentation
def format_documentation(documentation):
    formatted_doc = f"""
    <div style="background-color:#181818; color:#fff; padding: 15px; border-radius: 10px;">
        {documentation}
    </div>
    """
    return formatted_doc

# Function to list SQL scripts in a directory
def list_files(repo_path):
    sql_files = []
    for root, dirs, files in os.walk(repo_path):
        for file in files:
            if file.endswith((".py", ".sql", ".xml" ,".json")):
                sql_files.append(os.path.join(root, file))
    return sql_files

# Streamlit layout
st.title("Script Documenter")

st.sidebar.title("IDOC Navigation")
options = st.sidebar.radio("Lookup Selected", ['Select Scripts from Repository'])

if options == 'Select Scripts from Repository':
    st.header("Select Scripts from Repository")
    
    # Path to the local repository
    repo_path = st.text_input("Enter the path to your local repository:", value="path/to/your/repository")

    # Drag and drop file uploader
    uploaded_file = st.file_uploader("Or drag and drop a script file here (.py, .sql, .xml, .json, .ipynb)", type=["py", "sql", "xml", "json"])

    # Handle uploaded file
    if uploaded_file is not None:
        content = uploaded_file.read().decode("utf-8")
        st.subheader(f"Content of {uploaded_file.name}")
        st.text_area(uploaded_file.name, content, height=300)
        if st.button(f"Generate Documentation for {uploaded_file.name}"):
            script_chunks = split_script_into_chunks(content)
            combined_documentation = ""
            for chunk in script_chunks:
                chunk_doc = call_llm_chunk(chunk)
                combined_documentation += f"\n\n{chunk_doc}"
            formatted_doc = format_documentation(combined_documentation)
            st.markdown(formatted_doc, unsafe_allow_html=True)
            # Download button for markdown
            st.download_button(
                label="Download Documentation (Markdown)",
                data=combined_documentation,
                file_name=f"{uploaded_file.name}_documentation.md",
                mime="text/markdown"
            )

    # Existing repo path logic
    if os.path.isdir(repo_path):
        sql_files = list_files(repo_path)
        selected_files = st.multiselect("Select files to generate documentation:", sql_files)
        
        if selected_files:
            for file_path in selected_files:
                with open(file_path, 'r') as file:
                    content = file.read()
                    st.subheader(f"Content of {os.path.basename(file_path)}")
                    st.text_area(os.path.basename(file_path), content, height=300)
                    
                    if st.button(f"Generate Documentation for {os.path.basename(file_path)}"):
                        script_chunks = split_script_into_chunks(content)
                        combined_documentation = ""
                        for chunk in script_chunks:
                            chunk_doc = call_llm_chunk(chunk)
                            combined_documentation += f"\n\n{chunk_doc}"
                        formatted_doc = format_documentation(combined_documentation)
                        st.markdown(formatted_doc, unsafe_allow_html=True)
                        # Download button for markdown
                        st.download_button(
                            label="Download Documentation (Markdown)",
                            data=combined_documentation,
                            file_name=f"{os.path.basename(file_path)}_documentation.md",
                            mime="text/markdown"
                        )
                
elif options == 'Search Documentation':
    st.header("Search Previous Documentation")
    search_query = st.text_input("Enter your search query")
    
    if st.button("Search"):
        st.write(f"Searching for '{search_query}' - (Placeholder)")
        # Here the search functionality will be integrated with LLM
        
elif options == 'Review Documentation':
    st.header("Review Generated Documentation")
    st.write("List of generated documents - (Placeholder)")
    # Here the review process and listing of documents will be managed

st.sidebar.info("This application helps automate the documentation process for your code (python, sql, .xml and json) scripts.")