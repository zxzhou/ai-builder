import os
import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
from PIL import Image
import google.generativeai as genai
from dotenv import load_dotenv
import threading

# Load environment variables from .env file
load_dotenv()

# Configure the Google API key
api_key = os.getenv('GOOGLE_API_KEY')
if api_key:
    genai.configure(api_key=api_key)
else:
    print("Warning: GOOGLE_API_KEY not found in environment variables")


def analyze_image(image_path, prompt):
    """Analyze the image using the Gemini API."""
    try:
        img = Image.open(image_path)
    except FileNotFoundError:
        return None, f"Error: File not found at {image_path}"
    except Exception as e:
        return None, f"Error opening image: {e}"

    model = genai.GenerativeModel('gemini-2.5-flash-lite')
    
    try:
        response = model.generate_content([prompt, img])
        return response.text, None
    except Exception as e:
        return None, f"API Error: {e}"


class ImageAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Analyzer - Gemini AI")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Variables
        self.image_path = tk.StringVar()
        self.prompt_text = tk.StringVar(value="Describe the contents of the following image in detail")
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        # Prompt label and entry
        ttk.Label(main_frame, text="Prompt:").grid(row=0, column=0, sticky=tk.W, pady=5)
        prompt_entry = ttk.Entry(main_frame, textvariable=self.prompt_text, width=60)
        prompt_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)
        
        # Image path label and entry
        ttk.Label(main_frame, text="Image Path:").grid(row=1, column=0, sticky=tk.W, pady=5)
        path_frame = ttk.Frame(main_frame)
        path_frame.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)
        path_frame.columnconfigure(0, weight=1)
        
        path_entry = ttk.Entry(path_frame, textvariable=self.image_path, width=50)
        path_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        
        browse_btn = ttk.Button(path_frame, text="Browse", command=self.browse_image)
        browse_btn.grid(row=0, column=1)
        
        # Analyze button
        analyze_btn = ttk.Button(main_frame, text="Analyze Image", command=self.start_analysis)
        analyze_btn.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Results area
        ttk.Label(main_frame, text="Analysis Results:").grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=(10, 5))
        self.results_text = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, width=80, height=20)
        self.results_text.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        main_frame.rowconfigure(4, weight=1)
        
        # Status bar
        self.status_label = ttk.Label(main_frame, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(5, 0))
        
    def browse_image(self):
        """Open file dialog to select an image."""
        filename = filedialog.askopenfilename(
            title="Select an image",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.gif *.bmp *.webp"),
                ("All files", "*.*")
            ]
        )
        if filename:
            self.image_path.set(filename)
            self.status_label.config(text=f"Selected: {os.path.basename(filename)}")
    
    def start_analysis(self):
        """Start the image analysis in a separate thread."""
        image_path = self.image_path.get().strip()
        prompt = self.prompt_text.get().strip()
        
        if not image_path:
            messagebox.showerror("Error", "Please select an image file.")
            return
        
        if not os.path.exists(image_path):
            messagebox.showerror("Error", f"The file '{image_path}' does not exist.")
            return
        
        if not prompt:
            messagebox.showerror("Error", "Please enter a prompt.")
            return
        
        # Clear previous results
        self.results_text.delete(1.0, tk.END)
        self.status_label.config(text="Analyzing image... Please wait.")
        
        # Disable analyze button during analysis
        self.analyze_btn = None
        for widget in self.root.winfo_children():
            for child in widget.winfo_children():
                if isinstance(child, ttk.Button) and child.cget("text") == "Analyze Image":
                    child.config(state="disabled")
        
        # Run analysis in a separate thread to prevent UI freezing
        thread = threading.Thread(target=self.perform_analysis, args=(image_path, prompt))
        thread.daemon = True
        thread.start()
    
    def perform_analysis(self, image_path, prompt):
        """Perform the actual analysis (runs in separate thread)."""
        analysis, error = analyze_image(image_path, prompt)
        
        # Update UI in main thread
        self.root.after(0, self.update_results, analysis, error)
    
    def update_results(self, analysis, error):
        """Update the results text area (called from main thread)."""
        # Re-enable analyze button
        for widget in self.root.winfo_children():
            for child in widget.winfo_children():
                if isinstance(child, ttk.Button) and child.cget("text") == "Analyze Image":
                    child.config(state="normal")
        
        if error:
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, f"Error: {error}")
            self.status_label.config(text="Analysis failed")
            messagebox.showerror("Error", error)
        elif analysis:
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, analysis)
            self.status_label.config(text="Analysis complete")
        else:
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, "No analysis result returned.")
            self.status_label.config(text="Analysis returned no results")


def main():
    """Main function to run the image analyzer GUI."""
    root = tk.Tk()
    app = ImageAnalyzerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
