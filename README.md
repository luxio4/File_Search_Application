# File Search Application (SAE32 Communicating Application)

This repository provides a **client-server application** that allows users to search for specific keywords or **regex patterns** across various file types (PDF, TXT, Excel, HTML) located in designated directories. The server handles the search logic, while the **Tkinter** client application provides an interactive GUI for users to input their queries and view the results.

---

## Table of Contents
1. [Features](#features)  
2. [Project Structure](#project-structure)  
3. [Installation & Requirements](#installation--requirements)  
4. [How to Run](#how-to-run)  
5. [Usage](#usage)  
6. [Search Behavior & Logical Expressions](#search-behavior--logical-expressions)  
7. [Using Regular Expressions](#using-regular-expressions)  
8. [Additional Information Returned](#additional-information-returned)  
9. [Code Quality](#code-quality)  
10. [License](#license)  

---

## Features

1. **Client-Server Communication**  
   - Uses sockets to establish a communication channel between the server and multiple clients.

2. **Graphical User Interface (GUI)**  
   - A user-friendly interface (using **Tkinter**) for sending queries and displaying results.

3. **Support for Multiple File Types**  
   - **TXT**: Searches line by line, returning matching lines and their line numbers.  
   - **PDF**: Uses **PyPDF2** to scan for matches, returning matching page numbers.  
   - **Excel**: Uses **pandas** to read all sheets and return matching cells along with sheet names, row indices, and column indices.  
   - **HTML**: Uses **BeautifulSoup** to parse text and returns matching lines.  

4. **Logical Expressions & Optional Regex**  
   - **Case-insensitive** search for textual matching.
   - Recognizes **uppercase** logical operators `AND` and `OR` in your keyword expression.
   - Supports **regex** patterns for more advanced searching (see [Using Regular Expressions](#using-regular-expressions)).

5. **Detailed Information**  
   - For each match, the application returns relevant context: page numbers (PDF), line numbers (TXT/HTML), and cell references (Excel).

6. **Configurable Directory Paths**  
   - Directories for PDFs, Excel, Text, and HTML files can be customized by modifying constants in the server script (`PDF_PATH`, `EXCEL_PATH`, `TEXT_PATH`, `HTML_PATH`).

---

## Project Structure

```
.
├── pdf_files/
│   └── [Your PDF Files...]
├── excel_files/
│   └── [Your Excel Files...]
├── text_files/
│   └── [Your TXT Files...]
├── html_files/
│   └── [Your HTML Files...]
├── server.py            # Contains the server code (search logic, socket handling)
├── client.py            # Tkinter-based client application
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

- **Note**: You can rename `server.py` and `client.py` according to your needs.  
- For demonstration, they may be combined in a single file in some examples, but ideally, separate them for clarity.

---

## Installation & Requirements

1. Make sure you have **Python 3.7+** installed.
2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
   
   **Example `requirements.txt`**:
   ```
   PyPDF2==3.0.1
   pandas==1.5.3
   openpyxl==3.0.10
   beautifulsoup4==4.11.1
   lxml==4.9.3
   ```
3. Adjust file paths if needed. In the server script, you can modify:
   ```python
   PDF_PATH = "pdf_files/"
   EXCEL_PATH = "excel_files/"
   TEXT_PATH = "text_files/"
   HTML_PATH = "html_files/"
   ```
   to match your folder structure.

---

## How to Run

1. **Run the Server**  
   Open a terminal in the project folder and run:
   ```bash
   python server.py
   ```
   By default, the server starts on `HOST = 'localhost'` and `PORT = 12345`.  
   You can edit these constants at the top of `server.py` if you want to change them.

2. **Run the Client**  
   In a separate terminal (or from your IDE), run:
   ```bash
   python client.py
   ```
   A Tkinter GUI should appear, showing an entry box for your query and a text area for results.

---

## Usage

1. **Entering a Query**  
   - In the client’s GUI, type your search query in the **Entry** field and press **Enter** or click **Search**.
   - By default, the server searches through **all supported file types**.

2. **Filetype-Specific Queries**  
   - To restrict your search to a specific file type (or multiple types), use the **`filetype:`** prefix followed by a comma-separated list of file types, then your keyword.  
   - Examples:
     - `filetype:pdf,txt data` will search for the keyword **data** in **PDF** and **TXT** files only.  
     - `filetype:all data` will search in **all** file types (equivalent to not specifying any filetype).

3. **Exiting**  
   - Type `exit` in the query box or click **Exit** to close the client.
   - The server remains running until you manually stop it (Ctrl + C in the server terminal).

---

## Search Behavior & Logical Expressions

- **Case-insensitive** matching for text.  
- Uppercase **AND** and **OR** are recognized as logical operators:
  - Example: `TERM1 AND TERM2 OR TERM3`  
---

## Using Regular Expressions

The search function internally uses Python’s `re.search()`, enabling **regex (regular expression)** matching. This means your query can include valid Python regex patterns:
- Basic example: `abc.*123` to match any text containing `abc`, followed by any characters, then `123`.
- OR / group example: `(cat|dog)` to match either `cat` or `dog`.
- Character ranges, quantifiers, lookahead/lookbehind, etc., are also supported if you include them in your search string.

**Important**:  
- If you also use uppercase `AND` or `OR` in your pattern, the application may interpret these as logical operators. To prevent unintended splitting, consider using lowercase `and`, `or`, or escaping as needed.  
- Always be mindful of regex syntax when crafting queries. Unescaped special characters (like `(`, `)`, `?`, `+`, etc.) can alter the matching behavior.

---

## Additional Information Returned

When a match is found, the following details are returned:

- **TXT/HTML**  
  - File name  
  - Line numbers where the match is found, along with the matched text (up to 100 characters for HTML).

- **PDF**  
  - File name  
  - Page numbers where the match is found.  

- **Excel**  
  - File name  
  - Sheet name  
  - Row and column references  
  - The cell value  

This makes it easy to pinpoint exactly where the match occurs, especially in larger files.

---

## Code Quality

- **English-based Code & Comments**: Primarily in English for clarity.
- **PEP 8 Style**: Variable and function names follow PEP 8 guidelines.
- **Consistent Naming & Style**: Constants, variables, and functions have descriptive names.
- **Well-Organized**: Separated server and client code, docstrings, and comments for each function.
- **Relative Paths**: File directory paths can be adjusted easily if using a different structure.
- **Extensible**: You can add new file types, new search logic (including more complex regex behavior), or integrate further front-end designs with minimal changes.

---

## License

This project is provided as-is for educational purposes within the **SAE32** framework.

**Enjoy searching through your files with powerful logical and regex-based matching!**
