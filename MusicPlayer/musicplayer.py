from tkinter import *
from tkinter import filedialog, ttk
import pygame
import time
from mutagen.mp3 import MP3

root = Tk()

root.title("MP3 Player")
root.geometry("450x350")

# Initialize pygame.
pygame.mixer.init()


# Create a function to deal with time.
def play_time():
    # Check to see if song is stopped.
    if stopped:
        return
    # Grab current song time.
    current_time = pygame.mixer.music.get_pos() / 1000
    # Convert current song time to user friendly format.
    converted_current_time = time.strftime('%M:%S', time.gmtime(current_time))
    # Reconstruct song with directory structure
    song = playlist_box.get(ACTIVE)
    song = f'E:/Stash/{song}.mp3'
    # Find current song length.
    song_mut = MP3(song)
    global song_length
    song_length = song_mut.info.length

    # Convert to time format.
    converted_song_length = time.strftime('%M:%S', time.gmtime(song_length))

    # # Set slider length to song length.
    # song_slider.config(to=song_length)
    # my_label.config(text=song_slider.get())

    if int(song_slider.get()) == int(song_length):
        stop()
    elif paused:
        # Check to sse if paused.
        pass
    else:
        # Move slider along one second at a time.
        next_time = int(song_slider.get()) + 1
        # Output new time value to slider and to length of song.
        song_slider.config(to=song_length, value=next_time)

        # Convert slider position to time format.
        converted_current_time = time.strftime('%M:%S', time.gmtime(int(song_slider.get())))

        # Output slider.
        status_bar.config(text=f'Time Elapsed: {converted_current_time} of {converted_song_length}  ')

    # Add current time to status bar.
    if current_time >= 1:
        status_bar.config(text=f'Time Elapsed: {converted_current_time} of {converted_song_length}  ')
    # Loop for every second.
    status_bar.after(1000, play_time)


# Create function to add one song to playlist
def add_song():
    song = filedialog.askopenfilename(initialdir='E:/Stash', title="Choose a song:",
                                      filetypes=(("mp3 Files", "*.mp3"),))
    # Strip out directory structure and .mp3 from file
    song = song.replace('E:/Stash/', '')
    song = song.replace('.mp3', '')
    playlist_box.insert(END, song)


# Create function to add many songs.
def add_many_songs():
    songs = filedialog.askopenfilenames(initialdir='E:/Stash', title="Choose songs:",
                                        filetypes=(("mp3 Files", "*.mp3"),))
    # Loop through and replace directory structure and .mp3 from file
    for song in songs:
        # Strip out directory structure and .mp3 from file
        song = song.replace('E:/Stash/', '')
        song = song.replace('.mp3', '')
        # Add to end of playlist.
        playlist_box.insert(END, song)


# Create function to delete one song from playlist.
def delete_song():
    # Delete highlighted song from playlist.
    playlist_box.delete(ANCHOR)


def delete_all_songs():
    playlist_box.delete(0, END)


# Create play function.
def play():
    # Set stopped to false.
    global stopped
    stopped = False
    # Reconstruct song with directory structure
    song = playlist_box.get(ACTIVE)
    song = f'E:/Stash/{song}.mp3'

    # Load song with pygame mixer.
    pygame.mixer.music.load(song)
    # Play song with pygame mixer.
    pygame.mixer.music.play(loops=0)
    # Get song time.
    play_time()


# Create stopped variable
global stopped
stopped = False


def stop():
    # Stop the song.
    pygame.mixer.music.stop()
    # Clear playlist bar.
    playlist_box.selection_clear(ACTIVE)

    status_bar.config(text='')
    # Set stop variable to True.
    global stopped
    stopped = True


# Create paused variable.
global paused
paused = False


# Create pause function.
def pause(is_paused):
    global paused
    paused = is_paused

    if paused:
        # Unpause
        pygame.mixer.music.unpause()
        paused = False
    else:
        # Pause
        pygame.mixer.music.pause()
        paused = True


# Create function to play the next song.
def next_song():
    # Reset slider position and status bar.
    status_bar.config(text='')
    song_slider.config(value=0)
    # Get current song number.
    next_one = playlist_box.curselection()
    # Add one to the current song number.
    next_one = next_one[0] + 1

    # Grab the song title from the playlist.
    song = playlist_box.get(next_one)
    # Add directory structure.
    song = f'E:/Stash/{song}.mp3'
    # Load song with pygame mixer.
    pygame.mixer.music.load(song)
    # Play song with pygame mixer.
    pygame.mixer.music.play(loops=0)

    # Clear active bar in playlist.
    playlist_box.selection_clear(0, END)

    # Move active bar to the next song.
    playlist_box.activate(next_one)

    # Set the active bar to the next song.
    playlist_box.selection_set(next_one, last=None)


# Create function to play previous song.
def previous_song():
    # Reset slider position and status bar.
    status_bar.config(text='')
    song_slider.config(value=0)
    # Get current song number.
    next_one = playlist_box.curselection()
    # Subtract one to the current song number.
    next_one = next_one[0] - 1

    # Grab the song title from the playlist.
    song = playlist_box.get(next_one)
    my_label.config(text=song)
    # Add directory structure.
    song = f'E:/Stash/{song}.mp3'
    # Load song with pygame mixer.
    pygame.mixer.music.load(song)
    # Play song with pygame mixer.
    pygame.mixer.music.play(loops=0)

    # Clear active bar in playlist.
    playlist_box.selection_clear(0, END)

    # Move active bar to the next song.
    playlist_box.activate(next_one)

    # Set the active bar to the next song.
    playlist_box.selection_set(next_one, last=None)


# Create volume function.
def volume(x):
    pygame.mixer.music.set_volume(volume_slider.get())


# Create a slide function for song positioning.
def slide(x):
    # Reconstruct song with directory structure
    song = playlist_box.get(ACTIVE)
    song = f'E:/Stash/{song}.mp3'

    # Load song with pygame mixer.
    pygame.mixer.music.load(song)
    # Play song with pygame mixer.
    pygame.mixer.music.play(loops=0, start=song_slider.get())


# Create main frame.
main_frame = Frame(root)
main_frame.pack(pady=20)

# Create Playlist Box.
playlist_box = Listbox(main_frame, bg='black', fg='red', width=50, selectbackground='red', selectforeground='black')
playlist_box.grid(row=0, column=0)

# Create volume slider frame
volume_frame = LabelFrame(main_frame, text="Volume")
volume_frame.grid(row=0, column=1, padx=15)
# Create volume slider.
volume_slider = ttk.Scale(volume_frame, from_=1, to=0, orient=VERTICAL, length=125, value=0.5, command=volume)
volume_slider.grid(pady=10)
# Create song slider.
song_slider = ttk.Scale(main_frame, from_=0, to=100, orient=HORIZONTAL, length=360, value=0, command=slide)
song_slider.grid(row=2, column=0, pady=20)

# Define Button Images for Controls.
back_btn_img = PhotoImage(file='Images/back50.png')
forward_btn_img = PhotoImage(file='Images/forward50.png')
play_btn_img = PhotoImage(file='Images/play50.png')
pause_btn_img = PhotoImage(file='Images/pause50.png')
stop_btn_img = PhotoImage(file='Images/stop50.png')

# Create Buttons Frame.
control_frame = Frame(main_frame)
control_frame.grid(row=1, column=0, pady=20)

# Create Buttons.
back_button = Button(control_frame, image=back_btn_img, borderwidth=0, command=previous_song)
forward_button = Button(control_frame, image=forward_btn_img, borderwidth=0, command=next_song)
play_button = Button(control_frame, image=play_btn_img, borderwidth=0, command=play)
pause_button = Button(control_frame, image=pause_btn_img, borderwidth=0, command=lambda: pause(paused))
stop_button = Button(control_frame, image=stop_btn_img, borderwidth=0, command=stop)
back_button.grid(row=0, column=0, padx=10)
pause_button.grid(row=0, column=1, padx=10)
play_button.grid(row=0, column=2, padx=10)
forward_button.grid(row=0, column=3, padx=10)
stop_button.grid(row=0, column=4, padx=10)

# Create Menu.
my_menu = Menu(root)
root.config(menu=my_menu)

# Create add song menu.
add_song_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Add Songs", menu=add_song_menu)
# Add one song to playlist.
add_song_menu.add_command(label="Add one song to playlist.", command=add_song)
# Add many songs to playlist.
add_song_menu.add_command(label="Add many songs to playlist.", command=add_many_songs)

# Create delete song menu dropdowns.
remove_song_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Remove songs", menu=remove_song_menu)
remove_song_menu.add_command(label='Delete a song from playlist', command=delete_song)
remove_song_menu.add_command(label='Delete all songs from playlist', command=delete_all_songs)

# Create status bar.
status_bar = Label(root, text='', bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)

# Temporary Label.
my_label = Label(root, text='')
my_label.pack(pady=20)

root.mainloop()
