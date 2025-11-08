import socket
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox

# Constants
HOST = 'localhost'
PORT = 12345
BUFFER_SIZE = 4096

class FileSearchClientApp:
    """
    A Tkinter-based client application that connects to a file search server.
    Users can enter search queries for specific keywords or logical expressions,
    and view the search results in the GUI.
    """
    def __init__(self, root):
        """
        Initialize the FileSearchClientApp with a specified Tk root object. 
        Attempts to connect to the server upon creation. If it fails, 
        an error message is displayed and the application closes.

        :param root: The root Tkinter window.
        """
        self.root = root
        self.root.title("File Search Client")
        self.root.geometry("800x500")
        self.root.configure(bg="#2E4053")

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect((HOST, PORT))
            self.create_widgets()
        except Exception as e:
            messagebox.showerror("Connection Error", f"Unable to connect to server: {str(e)}")
            self.root.quit()

    def create_widgets(self):
        """
        Creates and places all the required widgets in the Tkinter window:
         - Title label
         - Entry box for the search query
         - Search button
         - ScrolledText widget for displaying results
         - Exit button
        """
        # Title Label
        title_label = tk.Label(
            self.root,
            text="File Search Client",
            font=("Helvetica", 16),
            bg="#2E4053",
            fg="white"
        )
        title_label.pack(pady=10)

        # Query Entry
        self.query_entry = tk.Entry(
            self.root,
            font=("Helvetica", 12),
            width=50
        )
        self.query_entry.pack(pady=10)
        # Enable pressing 'Enter' to trigger send_query
        self.query_entry.bind('<Return>', lambda event: self.send_query())

        # Search Button
        search_button = tk.Button(
            self.root,
            text="Search",
            font=("Helvetica", 12),
            command=self.send_query,
            bg="#1ABC9C",
            fg="white"
        )
        search_button.pack(pady=5)

        # Results Text Box
        self.results_text = scrolledtext.ScrolledText(
            self.root,
            wrap=tk.WORD,
            width=70,
            height=15,
            font=("Helvetica", 10),
            bg="#F2F4F4"
        )
        self.results_text.pack(pady=10)

        # Exit Button
        exit_button = tk.Button(
            self.root,
            text="Exit",
            font=("Helvetica", 12),
            command=self.exit_client,
            bg="#E74C3C",
            fg="white"
        )
        exit_button.pack(pady=5)

    def send_query(self):
        """
        Sends the query from the entry box to the server. If the query is empty,
        displays a warning. If the query is 'exit', close the client.
        Otherwise, send the query to the server and display the response in the
        ScrolledText widget.
        """
        query = self.query_entry.get().strip()
        if not query:
            messagebox.showwarning("Invalid Input", "Please enter a valid search query.")
            return

        if query.lower() == 'exit':
            self.exit_client()
            return

        try:
            # Send query to the server
            self.client_socket.sendall(query.encode('utf-8'))
            # Receive response from the server
            response = self.client_socket.recv(BUFFER_SIZE).decode('utf-8')
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.INSERT, response)
        except Exception as e:
            messagebox.showerror("Error", f"Error sending query: {str(e)}")

    def exit_client(self):
        """
        Sends an 'exit' signal to the server, closes the socket, and quits the application.
        """
        try:
            self.client_socket.sendall(b'exit')
            self.client_socket.close()
        except Exception as e:
            print(f"Error closing socket: {str(e)}")
        finally:
            self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = FileSearchClientApp(root)
    root.mainloop()
