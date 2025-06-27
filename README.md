# IDOC Script Documenter

**Script Documenter** is a modern, offline Python application that uses Azure OpenAI to automatically generate detailed, easy-to-understand documentation for your code and data scripts. It supports Python (`.py`), SQL (`.sql`), XML (`.xml`), and JSON (`.json`) files. The tool is designed for developers, data engineers, and analysts who want to quickly document their scripts with minimal effort.

---

## Features

- **Automatic Documentation:** Generate markdown documentation for Python, SQL, XML, and JSON scripts using Azure OpenAI.
- **Multi-file Support:** Select scripts from a local repository or drag-and-drop files directly into the app.
- **Chunked Processing:** Handles large scripts by splitting them into manageable chunks for accurate documentation.
- **Modern UI:** Built with Streamlit for an interactive and user-friendly experience.
- **Downloadable Output:** Download your generated documentation as a Markdown file.
- **Offline & Secure:** All processing is local except for secure calls to Azure OpenAI.

---

## Quick Start

### 1. Clone the Repository

```sh
git clone https://github.com/yourusername/script-documenter.git
cd script-documenter
```

### 2. Set Up Your Environment

```sh
python -m venv venv
venv\Scripts\activate  # On Windows
pip install -r requirements.txt
```

### 3. Configure Azure OpenAI

Edit `idoc.py` and set your Azure OpenAI endpoint and API key at the top of the file:

```python
azure_endpoint = "YOUR_AZURE_OPENAI_ENDPOINT"
api_key = "YOUR_AZURE_OPENAI_KEY"
```

### 4. Run the Application

```sh
streamlit run idoc.py
```

---

## How to Use

1. **Select Scripts from Repository:**  
   Enter the path to your local repository to browse and select files for documentation.

2. **Drag and Drop:**  
   Alternatively, drag and drop your `.py`, `.sql`, `.xml`, or `.json` files into the uploader.

3. **Generate Documentation:**  
   Click the "Generate Documentation" button to create markdown documentation for your script.

4. **Download:**  
   Download the generated documentation as a Markdown file for your records or sharing.


## Walkthrough Video


https://github.com/user-attachments/assets/ba43f14f-f6f9-4a03-b97e-45a8ade13360

## Contact

For questions or suggestions, please open an issue or contact the maintainer.
