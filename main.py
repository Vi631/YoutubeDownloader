# Import tkinter, pytube, ttk and filedialog libraries
import tkinter as tk
from pytube import YouTube
from tkinter import ttk, filedialog


# Define a global variable to store the selected folder path
folder_path = ''

# Define a function to update the progress bar
def progress_function(stream, chunk, bytes_remaining):
    # Calculate the percentage of downloaded video
    percentage = (stream.filesize - bytes_remaining) / stream.filesize * 100

    # Update the progress bar with the percentage
    progress_bar['value'] = percentage

# Define a function to download and save a YouTube video
def download_video():
    # Get the url and the video name from the text boxes
    url = text_box_1.get()
    video_name = text_box_2.get()

    # Create a YouTube object with the url
    youtube = YouTube(url, progress_function)

    # Get the first stream of the YouTube object
    stream = youtube.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()

    # Download and save the stream with the video name in the selected folder path
    stream.download(output_path=folder_path, filename=video_name)

# Define a function to select a folder using filedialog and store its path in the global variable
def select_folder():
    global folder_path

    # Ask the user to select a folder using filedialog and store its path in folder_path
    folder_path = filedialog.askdirectory()

# Define a function to resize the font size according to the window's size
def resize_font(event):
    # Get the width and height of the window
    width = event.width
    height = event.height

    # Calculate the font size based on a ratio of 1/50 of the window's width
    font_size = int(width / 13)

    # Create a font object with the calculated font size
    font = ('Arial', font_size)

    # Configure the text boxes and button to use the font object
    text_box_1.config(font=font)
    text_box_2.config(font=font)
    button.config(font=font)
    file_select_button.config(font=font)
    mp3_button.config(font=font)

# Define a function to clear the ghost text when the user clicks on a text box
def clear_ghost_text(event):
    # Get the widget that triggered the event
    widget = event.widget

    # Get the current text of the widget
    current_text = widget.get()

    # If the current text is equal to the ghost text, delete it and change the foreground color to black
    if current_text == 'YouTube URL' or current_text == 'Video Name':
        widget.delete(0, tk.END)
        widget.config(fg='black')

# Define a function to restore the ghost text when the user leaves a text box empty
def restore_ghost_text(event):
    # Get the widget that triggered the event
    widget = event.widget

    # Get the current text of the widget
    current_text = widget.get()

    # If the current text is empty, insert the ghost text and change the foreground color to grey
    if current_text == '':
        if widget == text_box_1:
            widget.insert(0, 'YouTube URL')
        elif widget == text_box_2:
            widget.insert(0, 'Video Name')
        widget.config(fg='grey')

# Define a function to download only the mp3 of a YouTube video
def download_mp3():
    # Get the url and the video name from the text boxes
    url = text_box_1.get()
    video_name = text_box_2.get()

    # Create a YouTube object with the url
    youtube = YouTube(url)

    # Get the audio stream of the YouTube object
    stream = youtube.streams.filter(only_audio=True).first()

    # Download and save the audio stream with the video name in the selected folder path
    stream.download(output_path=folder_path, filename=video_name)

# Create a window object and set its background color to light blue and title to YouTube Downloader
window = tk.Tk()

window.config(bg='light blue')
window.title('YouTube Downloader')

# Change the tkinter icon
#photo = PhotoImage(file = "youtubelogo.png")
#window.iconphoto(False, photo)

# Create a button to download mp3
mp3_button = tk.Button(window, text="Download MP3", command=download_mp3, bg='green', fg='white')
mp3_button.grid(row=5, column=0, sticky='nsew')

# Create two text boxes and set their background color to white and sticky option to expand in both directions
text_box_1 = tk.Entry(window, bg='white')
text_box_2 = tk.Entry(window, bg='white')
text_box_1.grid(row=0, column=0, sticky='nsew')
text_box_2.grid(row=1, column=0, sticky='nsew')

# Insert ghost text into both text boxes and change their foreground color to grey
text_box_1.insert(0, 'YouTube URL')
text_box_2.insert(0, 'Video Name')
text_box_1.config(fg='grey')
text_box_2.config(fg='grey')

# Bind restore_ghost_text function to both text boxes when they are left empty (focus out event)
text_box_1.bind('<FocusOut>', restore_ghost_text)
text_box_2.bind('<FocusOut>', restore_ghost_text)

# Create a button and set its background color to green and foreground color to white and sticky option to expand in both directions
button = tk.Button(window, text="Download", command=download_video, bg='green', fg='white')
button.grid(row=2, column=0, sticky='nsew')

# Create a progress bar and set its initial value to 0 and sticky option to expand in both directions
progress_bar = ttk.Progressbar(window, orient='horizontal', length=200, mode='determinate')
progress_bar['value'] = 0
progress_bar.grid(row=3, column=0, sticky='nsew')

# Create a file select button and set its background color to green and foreground color to white and sticky option to expand in both directions
file_select_button = tk.Button(window, text="Select Folder", command=select_folder, bg='green', fg='white')
file_select_button.grid(row=4, column=0, sticky='nsew')

# Configure the weight of the grid rows and columns to make them scale with the window size
window.grid_rowconfigure(0, weight=1)
window.grid_rowconfigure(1, weight=1)
window.grid_rowconfigure(2, weight=1)
window.grid_rowconfigure(3, weight=1)
window.grid_rowconfigure(4, weight=1)
window.grid_columnconfigure(0, weight=1)

# Bind the resize_font function to the window's configure event
window.bind('<Configure>', resize_font)

# Start the main loop of the window
window.mainloop()