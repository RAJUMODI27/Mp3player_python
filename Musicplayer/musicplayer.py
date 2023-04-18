from tkinter import *
import pygame
from tkinter import filedialog
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk

root = Tk()
root.title("Royplayer")
root.geometry("700x500")


pygame.mixer.init()


#grab song length time info
def play_time():
    if stopped:
        return
    #grab current song elaspe time
    current_time=pygame.mixer.music.get_pos()/1000


    #thrwo temp label to get data
    # slider_label.config(text=f"slider:{int(my_slider.get(  ))} and Song pos:{int(current_time)}")

    #conver to time format
    converted_current_time=time.strftime("%H:%M:%S",time.gmtime(current_time))

    #get currently playing song
    current_song = song_box.curselection()
    song = song_box.get(ACTIVE)


    # Load song with mutagen
    song_mut=MP3(song)

    #get song length
    global song_length
    song_length=song_mut.info.length
    #conver to time format
    converted_song_length=time.strftime("%H:%M:%S",time.gmtime(song_length))

    #increase current time by 1 sec
    current_time += 1

    if int(my_slider.get())==int(song_length):
        status_bar.config(text=f'Time elasped:  {converted_song_length}  of  {converted_song_length}  ')

    elif paused:
        pass
    elif int(my_slider.get())== int(current_time):
        # update slider to position
        slider_position = int(song_length)
        my_slider.config(to=slider_position, value=int(current_time))

    else:
        slider_position = int(song_length)
        my_slider.config(to=slider_position, value=int(my_slider.get()))

        # conver to time format
        converted_current_time = time.strftime("%H:%M:%S", time.gmtime(int(my_slider.get())))

        # output time to status bar
        status_bar.config(text=f'Time elasped:  {converted_current_time}  of  {converted_song_length}  ')

        #move this thing along by one second
        next_time=int(my_slider.get())+1
        my_slider.config(value=next_time)



    #updating slider
    # my_slider.config(value=int(current_time))

    #  #output time to status bar
    # status_bar.config(text=f'Time elasped:  {converted_current_time}  of  {converted_song_length}  ')


    #update time
    status_bar.after(1000,play_time)


def slide(x):
    # slider_label.config(text=int(my_slider.get()))
    song = song_box.get(ACTIVE)
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(start=int(my_slider.get()))



#play selected song
def play():
    stopped = False
    song=song_box.get(ACTIVE)
    pygame.mixer.music.load(song)
    pygame.mixer.music.play()


    #call the play_time function to get the song length
    play_time()

    # #update slider to position
    # slider_position=int(song_length)
    # my_slider.config(to=slider_position,value=0)

global stopped
stopped = False

#stop playing current song
def stop():
    # song=song_box.get(ACTIVE)
    # pygame.mixer.music.stop()
    #rest slider and status bar
    status_bar.config(text="")
    my_slider.config(value=0)
    #stop song from playing
    pygame.mixer.music.stop()
    song_box.selection_clear(ACTIVE)

    #clear the status bar
    status_bar.config(text="")

    #set stop variable to true
    global stopped
    stopped = True

def next_song():
    status_bar.config(text="")
    my_slider.config(value=0)
    #get current tuple song number
    next_one = song_box.curselection()
    #add 1 to current song number
    next_one = next_one[0]+1
    song = song_box.get(next_one)
    pygame.mixer.music.load(song)
    pygame.mixer.music.play()
    #clear Activate bar  in playlist listbox
    song_box.selection_clear(0,END)
    #activate new songbar
    song_box.activate(next_one)
    #set Activate bar to next song
    song_box.select_set(next_one)




def previous_song():
    status_bar.config(text="")
    my_slider.config(value=0)
    # get current tuple song number
    prev_one = song_box.curselection()
    # add 1 to current song number
    prev_one = prev_one[0] - 1
    song = song_box.get(prev_one)
    pygame.mixer.music.load(song)
    pygame.mixer.music.play()
    # clear Activate bar  in playlist listbox
    song_box.selection_clear(0, END)
    # activate new songbar
    song_box.activate(prev_one)
    # set Activate bar to next song
    song_box.select_set(prev_one)




global paused
paused = False

def pause(is_paused):
    global paused
    paused = is_paused

    if paused:
        # unpause
        pygame.mixer.music.unpause()
        paused=False
    else:
        #pause
        pygame.mixer.music.pause()
        paused=True


def add_song():
    song = filedialog.askopenfilename(title="Choose Song",filetypes=(("mp3 Files","*.mp3"),))
    #Adding song to listbox
    song_box.insert(END,song)



# Create label and center it
l = Label(root, text="Music player", font=32,borderwidth=0)
l.pack()

#create listbox of songs
song_box=Listbox(root,bg="black",fg="green",width=100,height=10,selectbackground="grey",selectforeground="black")
song_box.pack(pady=20)

#creating frame for buttons
f1=Frame(root)
f1.pack()

#creating buttons for music player
f_b=Button(f1,text="Previous",borderwidth=1,command=previous_song)
b_b=Button(f1,text="forward",borderwidth=1,command=next_song)
p_b=Button(f1,text="Play",borderwidth=1,command=play)
pa_b=Button(f1,text="Pause",borderwidth=1,command=lambda: pause(paused))
s_b=Button(f1,text="Stop",borderwidth=1,command=stop)

f_b.grid(row=0,column=0,padx=25)
b_b.grid(row=0,column=1,padx=25)
p_b.grid(row=0,column=2,padx=25)
pa_b.grid(row=0,column=3,padx=25)
s_b.grid(row=0,column=4,padx=25)

#create menu
my_menu =Menu(root)
root.config(menu=my_menu)

#Add song menu
add_song_menu =Menu(my_menu)
my_menu.add_cascade(label="Add songs",menu=add_song_menu)
add_song_menu.add_command(label="Add One song to playlist",command=add_song)


#create satus bar
status_bar = Label(root,text="",bd=1,relief=GROOVE,anchor=E)
status_bar.pack(fill=X,side=BOTTOM)

#create Music  position slider
my_slider = ttk.Scale(root,from_=0,to=100,orient=HORIZONTAL,value=0,command=slide,length=360)
my_slider.pack(pady=20)

#temperary label for slider
# slider_label = Label(root,text="0")
# slider_label.pack(pady=10)

root.mainloop()
