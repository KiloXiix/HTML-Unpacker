# Setting Up The Virtual Environment
# python -m venv .venv
# .venv\Scripts\activate

# Imports


#Main Code


import os
import re
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox


def process_html(source_file, output_dir):
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Read the source HTML file
    with open(source_file, "r", encoding="utf-8") as f:
        html_content = f.read()

    # Patterns for script and style tags
    script_pattern = re.compile(r"<script.*?>(.*?)</script>", re.DOTALL)
    style_pattern = re.compile(r"<style.*?>(.*?)</style>", re.DOTALL)

    # File counters
    script_count = 0
    style_count = 0

    # Process <script> tags
    def replace_script_tag(match):
        nonlocal script_count
        script_content = match.group(1).strip()
        script_file = os.path.join(output_dir, f"script_{script_count}.js")
        with open(script_file, "w", encoding="utf-8") as script_f:
            script_f.write(script_content)
        script_count += 1
        return f'<script src="{os.path.basename(script_file)}"></script>'

    # Process <style> tags
    def replace_style_tag(match):
        nonlocal style_count
        style_content = match.group(1).strip()
        style_file = os.path.join(output_dir, f"style_{style_count}.css")
        with open(style_file, "w", encoding="utf-8") as style_f:
            style_f.write(style_content)
        style_count += 1
        return f'<link rel="stylesheet" href="{os.path.basename(style_file)}">'

    # Replace script and style tags in the HTML content
    html_content = script_pattern.sub(replace_script_tag, html_content)
    html_content = style_pattern.sub(replace_style_tag, html_content)

    # Write the updated HTML to the output directory
    output_html = os.path.join(output_dir, "index.html")
    with open(output_html, "w", encoding="utf-8") as f:
        f.write(html_content)

    return output_dir  # Return the output directory


def zip_output_folder(folder_path, zip_file_path):
    # Create a zip file from the output folder
    shutil.make_archive(zip_file_path.replace('.zip', ''), 'zip', folder_path)


def select_file_and_generate_zip():
    # Open a file dialog to select an HTML file
    file_path = filedialog.askopenfilename(filetypes=[("HTML files", "*.html")])
    if not file_path:
        return

    # Create a temporary output folder in the same directory as the source file
    temp_output_dir = os.path.join(os.path.dirname(file_path), "temp_processed_files")

    try:
        # Process the selected HTML file
        process_html(file_path, temp_output_dir)

        # Prompt the user to save the ZIP file
        zip_file_path = filedialog.asksaveasfilename(
            defaultextension=".zip",
            filetypes=[("ZIP files", "*.zip")],
            title="Save ZIP File"
        )
        if not zip_file_path:
            # If the user cancels, exit the process
            shutil.rmtree(temp_output_dir)
            return

        # Create the ZIP file
        zip_output_folder(temp_output_dir, zip_file_path)

        # Clean up temporary files
        shutil.rmtree(temp_output_dir)

        # Show success message
        messagebox.showinfo("Success", f"ZIP file saved: {zip_file_path}")
    except Exception as e:
        shutil.rmtree(temp_output_dir, ignore_errors=True)
        messagebox.showerror("Error", f"An error occurred: {e}")


# GUI Setup
def main():
    root = tk.Tk()
    root.title("HTML Unpacker")

    # Add a button to select a file and generate the ZIP
    select_button = tk.Button(root, text="Select HTML File and Generate ZIP", command=select_file_and_generate_zip, width=40)
    select_button.pack(pady=20)

    # Run the Tkinter main loop
    root.mainloop()


if __name__ == "__main__":
    main()
