import os
import re
import socket
import threading
import PyPDF2
import pandas as pd
from bs4 import BeautifulSoup

# Constants
HOST = 'localhost'
PORT = 12345
MAX_CLIENTS = 10
BUFFER_SIZE = 4096

# Directory paths (adjust these as needed)
PDF_PATH = "pdf_files/"
EXCEL_PATH = "excel_files/"
TEXT_PATH = "text_files/"
HTML_PATH = "html_files/"

def evaluate_logical_expression(expression, line):
    """
    Evaluates a string against a logical expression where only uppercase 'AND' or 'OR'
    operators are recognized. If no uppercase operator is found, the expression is treated
    as a standard substring search.

    Example:
        - "TERM1 AND (TERM2 OR TERM3)" will be interpreted using logical operators.
        - "term1 and term2" will be treated as a normal substring search (case-insensitive).
    
    :param expression: The expression containing search terms and optional logical operators (str).
    :param line: The line of text to search against (str).
    :return: True if the line matches the logical expression, False otherwise (bool).
    """
    line_lower = line.lower()

    # Split by " AND " first
    and_parts = expression.split(' AND ')

    # If no "AND" is present, 'and_parts' will be [expression]
    # This means there might be no logical operators, or only 'OR' operators.
    for and_part in and_parts:
        # Split by " OR "
        or_parts = and_part.split(' OR ')

        # If no "OR" is present, 'or_parts' will be [and_part]
        # Check if at least one 'or_part' is found in 'line_lower'
        if not any(re.search(or_part, line_lower, re.IGNORECASE) for or_part in or_parts):
            return False

    return True

def search_in_text_file(file_path, keyword):
    """
    Reads a text file line by line and checks if each line matches the keyword expression.
    Returns a list of lines where matches were found, along with line numbers.

    :param file_path: The path to the text file (str).
    :param keyword: The search keyword or logical expression (str).
    :return: A list of matching results, each describing file name and matching line(s).
    """
    results = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            matching_lines = []
            for i, line in enumerate(file):
                if evaluate_logical_expression(keyword, line):
                    matching_lines.append(f"Line {i + 1}: {line.strip()}")
            if matching_lines:
                results.append(f"File: {os.path.basename(file_path)}, Matches: {'; '.join(matching_lines)}")
    except Exception as e:
        results.append(f"Error reading {file_path}: {str(e)}")
    return results

def search_in_pdf(file_path, keyword):
    """
    Searches for a keyword/logical expression in a PDF. Returns matching page numbers if found.

    :param file_path: The path to the PDF file (str).
    :param keyword: The search keyword or logical expression (str).
    :return: A list of matching results, indicating file name and matching page(s).
    """
    results = []
    try:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            matching_pages = []
            for page_num, page in enumerate(reader.pages):
                text = page.extract_text() or ""
                if evaluate_logical_expression(keyword, text):
                    matching_pages.append(f"Page {page_num + 1}")
            if matching_pages:
                results.append(f"File: {os.path.basename(file_path)}, Matches: {'; '.join(matching_pages)}")
    except Exception as e:
        results.append(f"Error reading {file_path}: {str(e)}")
    return results

def search_in_excel(file_path, keyword):
    """
    Searches for a keyword/logical expression in all sheets of an Excel file.
    Returns matching cells along with their sheet names, row indices, and column indices.

    :param file_path: The path to the Excel file (str).
    :param keyword: The search keyword or logical expression (str).
    :return: A list of matching results, indicating file name and the matching cell references.
    """
    results = []
    try:
        # Read all sheets in the Excel file
        sheets = pd.read_excel(file_path, sheet_name=None, header=None)  # Pandas decides the engine
        matching_cells = []
        for sheet_name, df in sheets.items():
            for row_idx, row in df.iterrows():
                for col_idx in df.columns:
                    value = row[col_idx]
                    if pd.notna(value) and evaluate_logical_expression(keyword, str(value)):
                        matching_cells.append(
                            f"{sheet_name} - Row {row_idx + 1}, Column {col_idx}: {value}"
                        )
        if matching_cells:
            results.append(f"File: {os.path.basename(file_path)}, Matches: {'; '.join(matching_cells)}")
    except Exception as e:
        results.append(f"Error reading {file_path}: {str(e)}")
    return results

def search_in_html(file_path, keyword):
    """
    Searches for a keyword/logical expression in an HTML file by extracting its text content.
    Returns matching lines (trimmed) if they are less than 100 characters.

    :param file_path: The path to the HTML file (str).
    :param keyword: The search keyword or logical expression (str).
    :return: A list of matching results, indicating file name and the matching text line(s).
    """
    results = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')
            text = soup.get_text()
            lines = text.splitlines()
            for line in lines:
                if evaluate_logical_expression(keyword, line):
                    line = line.strip()
                    if len(line) < 100:
                        results.append(f"File: {os.path.basename(file_path)}, Match: {line}")
    except Exception as e:
        results.append(f"Error reading {file_path}: {str(e)}")
    return results

def search_files_in_directory(directory, extension, search_function, keyword):
    """
    Iterates through all files in a given directory, and applies a designated search function
    to files matching the specified extension. Accumulates any matching results.

    :param directory: The path to the directory (str).
    :param extension: The file extension to look for (e.g., '.txt') (str).
    :param search_function: The function used to search within files (callable).
    :param keyword: The search keyword or logical expression (str).
    :return: A list of all matching results from the directory.
    """
    results = []
    if not os.path.isdir(directory):
        return results
    with os.scandir(directory) as entries:
        for entry in entries:
            if entry.is_file() and entry.name.lower().endswith(extension):
                results.extend(search_function(os.path.join(directory, entry.name), keyword))
    return results

def process_query_multiple_types(keyword, file_types):
    """
    Processes a search query for multiple file types. If 'all' is specified in file_types,
    searches all file types (txt, pdf, excel, html). Otherwise, searches only the given types.

    :param keyword: The search keyword or logical expression (str).
    :param file_types: A list of file types to search (e.g., ['txt', 'pdf']) (list of str).
    :return: A consolidated list of matching results from the specified file types.
    """
    results = []
    # If 'all' is in file_types, ignore other types and search everything
    if 'all' in file_types:
        file_types = ['txt', 'pdf', 'excel', 'html']

    # Search each specified file type
    for ft in file_types:
        ft = ft.lower()
        if ft == 'txt':
            results.extend(search_files_in_directory(TEXT_PATH, ".txt", search_in_text_file, keyword))
        elif ft == 'pdf':
            results.extend(search_files_in_directory(PDF_PATH, ".pdf", search_in_pdf, keyword))
        elif ft == 'excel':
            results.extend(search_files_in_directory(EXCEL_PATH, ".xlsx", search_in_excel, keyword))
        elif ft == 'html':
            results.extend(search_files_in_directory(HTML_PATH, ".html", search_in_html, keyword))
        # You can add more file types here if needed

    return results

def handle_client(client_socket):
    """
    Manages the interaction with a connected client. Receives queries, processes them,
    and sends back results. Also handles 'exit' commands to close the connection.

    :param client_socket: The socket object for the client (socket.socket).
    """
    try:
        while True:
            query = client_socket.recv(BUFFER_SIZE).decode('utf-8').strip()
            if not query:
                continue
            if query.lower() == 'exit':
                break

            file_types = []
            keyword = ''

            # Check if the query starts with "filetype:"
            if query.lower().startswith('filetype:'):
                # Extract everything after "filetype:"
                after_ft = query[len('filetype:'):].strip()
                # Split once by space to separate filetypes from the keyword
                parts = after_ft.split(' ', 1)
                # First part contains the requested file types
                requested_types = parts[0].split(',')
                # Clean up and store them
                file_types = [ft.strip().lower() for ft in requested_types]

                # If there is a keyword after the filetypes
                if len(parts) > 1:
                    keyword = parts[1].strip()
                else:
                    keyword = ''
            else:
                # If no filetype was specified, default to searching all
                file_types = ['all']
                keyword = query

            # Perform the search
            results = process_query_multiple_types(keyword, file_types)

            # Send results to the client
            if results:
                response = "\n".join(results)
                client_socket.sendall(response.encode('utf-8'))
            else:
                client_socket.sendall(b"No matches found in any file type.\n")
    except ConnectionResetError:
        print("Client connection was closed unexpectedly.")
    except Exception as e:
        print(f"Error handling client: {str(e)}")
        try:
            client_socket.sendall(f"Error: {str(e)}\n".encode('utf-8'))
        except ConnectionResetError:
            print("Failed to send error message to the client because the connection was closed.")
    finally:
        client_socket.close()

def start_server():
    """
    Initializes and starts the server. Listens for incoming connections,
    and spawns a new thread to handle each client.

    :return: None
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(MAX_CLIENTS)
    print(f"Server started on {HOST}:{PORT}")

    try:
        while True:
            client_socket, addr = server.accept()
            print(f"Connection established with {addr}")
            client_handler = threading.Thread(target=handle_client, args=(client_socket,))
            client_handler.start()
    except KeyboardInterrupt:
        print("\nShutting down the server...")
    finally:
        server.close()

if __name__ == "__main__":
    start_server()
