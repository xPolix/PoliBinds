import pygame
import pygame._sdl2 as sdl2
from pygame import mixer
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import colorchooser
import os
import re
from pynput.keyboard import Listener, Key
import requests
devices = []
#pygame.mixer.init()
path = '%s\\Poli binds\\' %  os.environ['APPDATA']
icon = path+"\\Poli_Binds_icon.ico"
if not os.path.exists(path):
    print("Lokalizacja: " + path + ' nie istnieje! Tworze ja...')
    os.makedirs(path)
if not os.path.exists(path+"\\config.txt"):
    open(path+"\\config.txt","a")
if not os.path.exists(path+"\\config_audio.txt"):
    open(path+"\\config_audio.txt","a")
if not os.path.exists(path+"\\keys.txt"):
    open(path+"\\keys.txt","a")
if not os.path.exists(path+"\\stopothers.txt"):
    open(path+"\\stopothers.txt","a")
    open(path+"\\stopothers.txt","w").write('0')
if not os.path.exists(path+"\\stopothers2.txt"):
    open(path+"\\stopothers2.txt","a")
    open(path+"\\stopothers2.txt","w").write('0')
if not os.path.exists(path+"\\channels_data.txt"):
    open(path+"\\channels_data.txt","a")
if not os.path.exists(path+"\\stop.txt"):
    open(path+"\\stop.txt","a")
if not os.path.exists(path+"\\volume.txt"):
    open(path+"\\volume.txt","a")
if not os.path.exists(icon):
    try:
        iconLink = 'https://xpolix.github.io/polibinds/Poli_Binds_icon.ico'
        r2 = requests.get(iconLink, allow_redirects=True)
        open(icon, 'wb').write(r2.content)
        print('Downloading icon complete!')
    except:
        print("Error while downloading icon!")
def DownloadReplaceKeys():
    ReplaceKeysLink = 'https://xpolix.github.io/polibinds/replace_keys.txt'
    r = requests.get(ReplaceKeysLink, allow_redirects=True)
    open(path+"\\replace_keys.txt", 'wb').write(r.content)
    print('Downloading file complete!')
    askWindowDownload.destroy()
def skipDownloading():
    askWindowDownload.destroy()
if not os.path.exists(path+"\\replace_keys.txt"):
    print("You don't have replace_keys.txt in program directory, do you want to download it?")
    askWindowDownload = Tk()
    askWindowDownload.iconbitmap(icon)
    askWindowDownload.geometry("300x300")
    askWindowDownload.title("File not found!")
    askWindowDownload.resizable(0, 0)
    askWindowLabel = Label(askWindowDownload, text="You don't have replace_keys.txt\nin program directory, do you\nwant to download it?")
    askWindowLabel.place(relx=0.5, rely=0.4, anchor=CENTER)
    askWindowLabel.config(font=("Courier", 11), fg='black')
    YesAskWindowButton = Button(askWindowDownload, text="Download it!", command=DownloadReplaceKeys, bg="lime")
    YesAskWindowButton.place(relx=0.1, rely=0.7, anchor=W)
    NoAskWindowButton = Button(askWindowDownload, text="nahh, next time!", command=skipDownloading, bg="red")
    NoAskWindowButton.place(relx=0.9, rely=0.7, anchor=E)
    askWindowDownload.mainloop()
def DownloadReplaceKeys():
    ReplaceKeysLink = 'https://xpolix.github.io/polibinds/replace_keys.txt'
    r = requests.get(ReplaceKeysLink, allow_redirects=True)
    open(path+"\\replace_keys.txt", 'wb').write(r.content)
    print('Downloading song complete!')

def closeApp():
    print("Nie wyjdziesz :D")
    
def PrintDevices():
    pygame.init()
    is_capture = 0  # zero to request playback devices, non-zero to request recording devices
    num = sdl2.get_num_audio_devices(is_capture)
    names = [str(sdl2.get_audio_device_name(i, is_capture), encoding="utf-8") for i in range(num)]
    #print("\n".join(names))
    pygame.quit()
    return names

def setAudioDevice(value):
    pygame.mixer.pre_init(devicename=value)

def StopAudio():
    UnPauseAudio()
    pygame.mixer.quit()
    scale.config(state="normal",troughcolor='lime',activebackground='lime')
    label_stopsounds.config(text="",bg='SystemButtonFace')
def PauseAudio():
    try:
        StopTextAudio = open(path+"\\stopothers.txt","r").read()
        if StopTextAudio == "1":
            pygame.mixer.Channel(main_channel_to_play).pause()
            Bx3.config(text="Play Sound",command=UnPauseAudio,bg="lime", activebackground="green")
    except:
        print("1pygame.error: mixer not initialized")
def UnPauseAudio():
    try:
        pygame.mixer.Channel(main_channel_to_play).unpause()
        Bx3.config(text="Pause Sound",command=PauseAudio, bg="red", activebackground="red")
    except:
        print("2pygame.error: mixer not initialized")
global idChannel
idChannel = 0
def ChannelSetUnSet(number):
    global idChannel
    idChannel = idChannel+1
    return idChannel

channels_for_bind = 5
Playidx = 0
def prepareChannels():
    binds_count = len(open(path+"\\config.txt","r").readlines())
    all_channels = binds_count*channels_for_bind
    #print("x\n\nSTART:",all_channels)
    #print("##########")
    def changeIdx():
        global Playidx
        Playidx = Playidx+1
    open(path+"\\channels_data.txt","w").write('')
    for i in range(binds_count):
        #print("bind:",i)
        dfg = i+1
        to_cosxd = dfg*channels_for_bind-channels_for_bind
        open(path+"\\channels_data.txt","a").write(str(i)+':'+str(to_cosxd)+'\n')
        for x in range (channels_for_bind):
            #print("chanID:",Playidx)
            changeIdx()
    print("Channel for all binds:",all_channels)
    changeChannelsSettings(0,all_channels)

main_channel_to_play = 0
def changeChannelsSettings(number, zmiana):
    if number == 0:
        global main_channel_to_play
        main_channel_to_play = zmiana
def PlayAudio(audio_loc,bindID):
    UnPauseAudio()
    scale.config(state="disabled",troughcolor='red',activebackground='red')
    label_stopsounds.config(text="STOP SOUNDS TO\nCHANGE VOLUME",bg='red')
#BINDS#

    channel_to_play_multi_list = open(path+"\\channels_data.txt","r").readlines()
    #print(channel_to_play_multi_list[int(bindID)])
    channel_to_play_multi = channel_to_play_multi_list[int(bindID)]
    channel_to_play_multi = channel_to_play_multi.replace(str(bindID)+":","")
    channel_to_play_multi = channel_to_play_multi.replace("\n","")
    chanToPlay = int(channel_to_play_multi)+1
    bindIDx = int(bindID)
    bindIDx = bindIDx+1
    if chanToPlay > bindIDx*channels_for_bind-1:
        chanToPlay = bindIDx*channels_for_bind-channels_for_bind
        print('restart chanToPlay',chanToPlay)
    channel_to_play_multi_list[int(bindID)] = str(bindID)+":"+str(chanToPlay)+"\n"
    #print(channel_to_play_multi_list[int(bindID)])
    open(path+"\\channels_data.txt","w").writelines(channel_to_play_multi_list)

    pygame.mixer.init()
    pygame.mixer.set_num_channels(main_channel_to_play+1)
    #pygame.mixer.music.load(audio_loc)
    StopTextAudio = open(path+"\\stopothers.txt","r").read()
    StopTextAudio2 = open(path+"\\stopothers2.txt","r").read()
    global sound
    if StopTextAudio == "0" and StopTextAudio2 == "0":
        kanal_zero = bindIDx*channels_for_bind-1
        sound = pygame.mixer.Sound(audio_loc)
        sound.set_volume(v_float)
        pygame.mixer.Channel(kanal_zero).play(sound)
        print(kanal_zero)
        return
    elif StopTextAudio == "0":
        sound = pygame.mixer.Sound(audio_loc)
        sound.set_volume(v_float)
        pygame.mixer.Channel(chanToPlay).play(sound)
        print(chanToPlay,"derluegrfho")
    elif StopTextAudio == "1":
        pygame.mixer.quit()
        pygame.mixer.init()
        pygame.mixer.set_num_channels(main_channel_to_play+1)
        sound = pygame.mixer.Sound(audio_loc)
        sound.set_volume(v_float)
        pygame.mixer.Channel(main_channel_to_play).play(sound)
        print(main_channel_to_play)
def soundVolumeChangeTest(v):
    open(path+"\\volume.txt","w").write(v)
    try:
        v = int(v)
        global v_float
        v_float = v/100
    except:
        return
def callback(value):
    print(value)
    open(path+"\\config_audio.txt","w").write(value)
    setAudioDevice(value)

devices = PrintDevices()
print("Possible devices: " + str(len(devices)))

def LoadBindButton(name, i, color,btn):
    Button(newWindow, text=name, command=lambda m=str(i): readFileToPlayMusic(m),bg=color, activebackground=color).pack()
    #print(i)
    Button(newWindow, text=name+" options", command=lambda idb=str(i): optionsButton(idb, name, color,btn),bg=color, activebackground=color).place(relx=1, y=i*26, anchor=NE)#.pack(pady=10,anchor=NE)
    if btn == "":
        btn = "None"
    try:
        keys_lines = open(path+"\\replace_keys.txt", 'r').readlines()
        for f in range(len(keys_lines)):
            if btn in keys_lines[f]:
                char = btn
                if len(char) > 3:
                    btn = re.search(':(.*?),', keys_lines[f])
                    btn = btn.group(1)
                    #print(btn)
                    break
    except:
        print("File replace_keys.txt does not exist, you can download it")
        print("from: xpolix.github.io/PoliBind/replace_keys")

    Label(newWindow, text="Bind button: "+btn, bg=color).place(relx=0, y=i*26, anchor=NW)
    
def LoadData():
    open(path+"\\keys.txt", "w")
    #print("04370743902")
    lines = len(open(path+"\\config.txt","r").readlines())
    for i in range(lines):
        data = open(path+"\\config.txt", "r").read()
        data = str(data)
        m = re.search(str(i)+': Name: (.*?),', data)
        data_color = re.search(str(i)+'c:(.*?),', data)
        data_btn = re.search(str(i)+'btn:(.*?),', data)
        if m:
            found = m.group(1)
            color = data_color.group(1)
            if(data_btn == None):
                btn = ""
            else:
                btn = data_btn.group(1)
                key_data = open(path+"\\keys.txt", "a").write(":"+btn+";"+str(i)+",\n")
            LoadBindButton(found, i, color, btn)
        #print(str(i) + ": " + m.group(1))
    setBindNameNumber()
    prepareChannels()
def readFileToPlayMusic(value):
    data = open(path+"\\config.txt", "r").read()
    data = str(data)
    bind_name = re.search(value+': Name: (.*?),', data)
    if bind_name:
        found = bind_name.group(1)
    bind_file = re.search(str(value)+': Name: '+str(found)+', File: (.*?).mp3###', data)
    exit_file = bind_file.group(1)+".mp3"
    
    #print(value +": "+ exit_file)
    #try:
    PlayAudio(exit_file,value)
    #except:
     #   print("Error while trying to play music.")
#print(test)

def removeBind(RidBind):
    data_text = open(path+"\\config.txt", "r").read()
    lines = len(open(path+"\\config.txt","r").readlines())
    linia_do_kasacji = open(path+"\\config.txt", "r").readlines()[int(RidBind)]
    linia_do_kasacji = linia_do_kasacji.replace("\n","")
    #print(linia_do_kasacji)
    #data_text = data_text.replace(linia_do_kasacji+"\n", "")
    #print(data_text)
    print("==============")
    for i in range(lines):
        if i > int(RidBind):
            print(i)
            linia_do_zmiany = open(path+"\\config.txt", "r").readlines()[i]
            #print(linia_do_zmiany)
            nr_do_zmiany = re.search('(.*?):', linia_do_zmiany)
            nr_do_zmiany = nr_do_zmiany.group(1)
            nowa_linia = linia_do_zmiany.replace(nr_do_zmiany+": ",str(int(nr_do_zmiany)-1)+": ")
            nowa_linia = nowa_linia.replace(nr_do_zmiany+"c:",str(int(nr_do_zmiany)-1)+"c:")
            nowa_linia = nowa_linia.replace(nr_do_zmiany+"btn:",str(int(nr_do_zmiany)-1)+"btn:")
            print(linia_do_zmiany+"//"+nowa_linia)
            data_text = data_text.replace(linia_do_zmiany,nowa_linia)

            open(path+"\\config.txt", "w").write(data_text)
            print("Saved: "+data_text+": END")
    data_text = open(path+"\\config.txt", "r").readlines()
    data_text[int(RidBind)] = ""
    open(path+"\\config.txt", "w").writelines(data_text)
    for widget in newWindow.winfo_children():
        widget.destroy()
    close_top()
    LoadData()

def character_limit(entry_text):
        ##entry_text = StringVar()
        ##entry_text.trace("w", lambda *args: character_limit(entry_text))
    if len(entry_text.get()) > 0:
        entry_text.set(entry_text.get()[-1])

def changeHearTrue():
    global HearForNewBind
    HearForNewBind = True
def changeHearFalse():
    global HearForNewBind
    HearForNewBind = False
global HearForNewBind
HearForNewBind = False

optionsWindow = None
def close_top():
    global optionsWindow
    optionsWindow.destroy()
    optionsWindow = None
    close_hearingButton()
    
chooseButtonWindow = None
def close_hearingButton():
    global chooseButtonWindow
    try:
        chooseButtonWindow.destroy()
    except:
        print("Changing bind button window does not exist.")
    chooseButtonWindow = None
def data_btn_save(btn):
    global buttonik
    buttonik = btn
def optionsButton(idBind, name, color, btn):
    if btn == "":
        btn = "None"
    def chooseButton():
        def chooseButtonClose():
            close_hearingButton()
            changeHearFalse()
            global xchooseButtonWindow
            xchooseButtonWindow = None
        def closeTwoWindows():
            chooseButtonClose()
            try:
                saveBtn()
            except:
                print("Error while trying to save bind button")
        def saveBtn():
            data_read = open(path+"\\config.txt", "r").read()
            old_btn = re.search(idBind+"btn:(.*?),", data_read)
            old_btn = old_btn.group(1)
            print(old_btn)
            data_read = open(path+"\\config.txt", "r").read()
            data_read = data_read.replace(idBind+'btn:'+old_btn+",",idBind+'btn:'+str(buttonik)+",")
            open(path+"\\config.txt", "w").write(data_read)
            print(data_read)
            for widget in newWindow.winfo_children():
                widget.destroy()
            close_top()
            LoadData()
        global xchooseOptionsLabel
        global chooseButtonWindow
        if chooseButtonWindow == None:
            global xchooseButtonWindow
            try:
                xchooseButtonWindow.destroy()
            except:
                xchooseButtonWindow = 769
            chooseButtonWindow = Toplevel(optionsWindow)
            chooseButtonWindow.iconbitmap(icon)
            chooseButtonWindow.geometry('250x250')
            chooseButtonWindow.configure(bg="white")
            chooseButtonWindow.protocol("WM_DELETE_WINDOW", chooseButtonClose)
            chooseButtonWindow.title("Bind Options: "+name+", BUTTON")
            chooseButtonWindow.attributes('-toolwindow', True)
            chooseButtonWindow.attributes('-topmost', True)
            xchooseOptionsLabel = Label(chooseButtonWindow, text = "Press any key to\nchange it", bg='white')
            xchooseOptionsLabel.place(relx=0.5, rely=0.3, anchor=CENTER)
            xchooseOptionsLabel.config(font=("Courier", 12), fg='red')
            chooseOptionsLabel = Label(chooseButtonWindow, text = "Current Button: "+btn, bg='white')
            chooseOptionsLabel.place(relx=0.5, rely=0.5, anchor=CENTER)
            chooseOptionsLabel.config(width=20)
            XsaveButton = Button(chooseButtonWindow, text = "Save", command = closeTwoWindows, bg='yellow', activebackground='#808000')
            XsaveButton.place(relx=0.5, rely=0.9, anchor=S)
            changeHearTrue()
    if color == "RETURN":
        xchooseOptionsLabel.config(text="Press any key to\nchange it: "+btn)
        data_btn_save(btn)
        return
    def chooseColor():
        try:
            NewColor = colorchooser.askcolor()
            Decolor = str(NewColor)
            print(Decolor)
            Decolor = re.search("'(.*?)'", Decolor)
            NewColor = Decolor.group(1)
            #ChooseColorButton.config(bg=color)
            data_read = open(path+"\\config.txt", "r").read()
            data_read = data_read.replace(idBind+'c:'+color,idBind+'c:'+NewColor)
            print(data_read)
            open(path+"\\config.txt", "w").write(data_read)
            for widget in newWindow.winfo_children():
                widget.destroy()
            LoadData()
            close_top()
        except:
            print("Error while setting color")
    def saveName():
        linie_names = open(path+"\\config.txt", "r").read()
        new_text = linie_names.replace(idBind+": Name: "+name+",",idBind+": Name: "+nameEntry.get()+",")
        open(path+"\\config.txt", "w").write(new_text)
        for widget in newWindow.winfo_children():
            widget.destroy()
        close_top()
        LoadData()
    global optionsWindow
    if optionsWindow is None:
        optionsWindow = Toplevel(app)
        optionsWindow.iconbitmap(icon)
        optionsWindow.protocol("WM_DELETE_WINDOW", close_top)
        optionsWindow.geometry('250x250')
        optionsWindow.configure(bg=color)
        optionsWindow.title("Bind Options: "+name)
        #optionsWindow.attributes('-toolwindow', True)
        optionsWindow.resizable(0, 0)
        ChooseColorButton = Button(optionsWindow, text = "Color", command = chooseColor, bg='yellow', activebackground='#808000')
        ChooseColorButton.place(relx=0.5, rely=0.9, anchor=CENTER)
        deleteButton = Button(optionsWindow, text = "Delete", command=lambda xd=idBind: removeBind(xd), bg='red', activebackground='red')
        deleteButton.place(relx=0, rely=0.45, anchor=W)
        changeButton = Button(optionsWindow, text = "Change Button", command = chooseButton, bg='yellow', activebackground='#808000')
        changeButton.place(relx=0.5, rely=0.1, anchor=N)
        NameButton = Button(optionsWindow, text = "Save", command = saveName, bg='yellow', activebackground='#808000')
        NameButton.place(relx=1, rely=0.675, anchor=E)
        optionsLabel = Label(optionsWindow, text = "Button: "+btn, bg='white')
        optionsLabel.place(relx=0.5, rely=0.45, anchor=CENTER)
        optionsLabel.config(width=20)
        nameEntry = Entry(optionsWindow, bg='white')
        nameEntry.insert(0,name)
        nameEntry.place(relx=0.5, rely=0.675, anchor=CENTER)
        nameEntry.config(width=24)
        #optionsLabel.insert(0, btn)
    else:
        print("Toplevel already exists")
        close_top()
        optionsButton(idBind, name, color, btn)
  
def add_new_bind(name, file):
    lines = len(open(path+"\\config.txt","r").readlines())
    lines = str(lines)
    #print(lines)
    open(path+"\\config.txt","a").write(lines+": Name: "+name+", File: "+file+"###"+lines+"c:#ffffff,"+lines+"btn:,\n")
    Button(newWindow, text=name, command=lambda m=lines: optionsButton(m, name)).pack()
    for widget in newWindow.winfo_children():
        widget.destroy()
    LoadData()
    file_selected = None

def selectFile():
    print('Choose location!')
    global file_selected
    file_selected = filedialog.askopenfilename(filetypes=[("Select sound: ", "*.mp3")])
    e2.delete(0, 'end')
    e2.insert(0, file_selected)
def newBindClick():
    try:
        if not file_selected == "":
            #print("###"+file_selected+"###")
            add_new_bind(e1.get(), file_selected)
            print("Successed added new bind!")
        else:
            selectFile()
    except:
        if messagebox.askokcancel(title="Error", message="No file selected."):
            selectFile()
            #global file_selected
            if not file_selected == "":
                add_new_bind(e1.get(), file_selected)
            #file_selected = None
            #newBindClick()
        else:
            print("Cancel")
hearOnly = False
def hearOnlyForStopSoundsTrue():
    global hearOnly
    hearOnly = True
def hearOnlyForStopSoundsFalse():
    global hearOnly
    hearOnly = False
def on_press(key):
    global listen 
    if listen:
        key = str(key).replace("'","")
        data_keys = open(path+"\\keys.txt", "r").readlines()
        #print(str(len(data_keys)))
        stop_bind = open(path+"\\stop.txt","r").read()
        if stop_bind == key:
            StopAudio()
            return
        if HearForNewBind == True:
            print(key)
            if hearOnly == False:
                optionsButton(1, 1, "RETURN", key)
            else:
                xhearForStopSounds("RETURN", key)
                return
            #changeHearFalse()
        else:
            gdfdfg = 1
        for i in range(len(data_keys)):
            line = open(path+"\\keys.txt", "r").readlines()[i]
            loaded_key = re.search(':(.*?);', line)
            loaded_key = loaded_key.group(1)
            value = re.search(";(.*?),", line)
            value = value.group(1)
            if str(key) == loaded_key:
                readFileToPlayMusic(value)
xchooseButtonWindow = None
def returnToStartValue():
    global xchooseButtonWindow
    xchooseButtonWindow = None
    global chooseButtonWindow
    chooseButtonWindow = None
def hearForStopSounds():
    xhearForStopSounds("fwf", "")
def xhearForStopSounds(color, key):
    btn = key
    global xxchooseOptionsLabel
    dgfknj = open(path+"\\stop.txt","r").read()
    try:
        keys_lines = open(path+"\\replace_keys.txt", 'r').readlines()
        for f in range(len(keys_lines)):
            if dgfknj in keys_lines[f]:
                char = dgfknj
                if len(char) > 3:
                    dgfknj = re.search(':(.*?),', keys_lines[f])
                    dgfknj = dgfknj.group(1)
                    #print(btn)
                    break
    except:
        print("File replace_keys.txt does not exist, you can download it")
        print("from: xpolix.github.io/PoliBind/replace_keys")
    if color == "RETURN":
        xxchooseOptionsLabel.config(text="Press any key to\nchange it: "+btn)
        data_btn_save(btn)
    def xchooseButtonClose():
        changeHearFalse()
        hearOnlyForStopSoundsFalse()
        xchooseButtonWindow.destroy()
        returnToStartValue()
    def closeTwoWindows():
        try:
            if not buttonik == "":
                open(path+"\\stop.txt","w").write(buttonik)
                xchooseButtonWindow.destroy()
                xchooseButtonClose()
                changeStopSoundsBtn(buttonik)
            try:
                print("Save button")
            except:
                print("Error while trying to save bind button")
        except:
            xchooseButtonWindow.destroy()
            xchooseButtonClose()
    global xchooseButtonWindow
    if xchooseButtonWindow == None:
        global chooseButtonWindow
        chooseButtonWindow = 23904230
        xchooseButtonWindow = Toplevel(app)
        xchooseButtonWindow.iconbitmap(icon)
        xchooseButtonWindow.geometry('250x250')
        xchooseButtonWindow.configure(bg="white")
        xchooseButtonWindow.protocol("WM_DELETE_WINDOW", xchooseButtonClose)
        xchooseButtonWindow.title("Bind STOP Sounds Button")
        xchooseButtonWindow.attributes('-toolwindow', True)
        xchooseButtonWindow.attributes('-topmost', True)
        xxchooseOptionsLabel = Label(xchooseButtonWindow, text = "Press any key to\nchange it", bg='white')
        xxchooseOptionsLabel.place(relx=0.5, rely=0.3, anchor=CENTER)
        xxchooseOptionsLabel.config(font=("Courier", 12), fg='red')
        xchooseOptionsLabel = Label(xchooseButtonWindow, text = "Current Button: "+dgfknj, bg='white')
        xchooseOptionsLabel.place(relx=0.5, rely=0.5, anchor=CENTER)
        xchooseOptionsLabel.config(width=20)
        xXsaveButton = Button(xchooseButtonWindow, text = "Save", command = closeTwoWindows, bg='yellow', activebackground='#808000')
        xXsaveButton.place(relx=0.5, rely=0.9, anchor=S)
        hearOnlyForStopSoundsTrue()
        changeHearTrue()
    else:
        print("Destroyed!")
def changeStopSoundsBtn(txt):
    Bx2.config(text="Stop Btn: "+txt)
listen = True    
app = Tk()
listener = Listener(on_press=on_press)
listener.start()
app.geometry("300x300")
app.resizable(0, 0)
app.title("Main window")
app.iconbitmap(icon)
urzadzenie = open(path+"\\config_audio.txt","r").read()
print(urzadzenie)
id_data = 0
for i in range(len(devices)):
    if devices[i] == urzadzenie:
        print(str(i)+"/"+urzadzenie)
        id_data = i

variable = StringVar(app)
variable.set(devices[id_data]) # default value
setAudioDevice(devices[id_data])
SelectDevice = OptionMenu(app, variable, *devices, command=callback)
SelectDevice.pack()

B1 = Button(app, text = "Add new bind", command = newBindClick, bg='yellow', activebackground='#808000')
B1.place(relx=0.5, rely=0.9, anchor=CENTER)
B2 = Button(app, text = "Stop Sounds", command = StopAudio, bg='yellow', activebackground='#808000')
B2.place(relx=0.5, rely=0.2, anchor=CENTER)
xdgfknj = open(path+"\\stop.txt","r").read()
try:
    keys_lines = open(path+"\\replace_keys.txt", 'r').readlines()
    for f in range(len(keys_lines)):
        if xdgfknj in keys_lines[f]:
            char = xdgfknj
            if len(char) > 3:
                xdgfknj = re.search(':(.*?),', keys_lines[f])
                xdgfknj = xdgfknj.group(1)
                #print(btn)
                break
except:
    print("File replace_keys.txt does not exist, you can download it")
    print("from: xpolix.github.io/PoliBind/replace_keys")
Bx2 = Button(app, text = "Stop Btn: "+xdgfknj, command = hearForStopSounds, bg='orange', activebackground='brown')
Bx2.place(relx=0, rely=0.2, anchor=W)
Bx3 = Button(app, text = "Pause Sound", command = PauseAudio, bg="red", activebackground="red")
Bx3.place(relx=0.5, rely=0.325, anchor=CENTER)
e1 = Entry(app)
e1.place(relx=0.5, rely=0.45, anchor=CENTER)

def readStopFile():
    StopText = open(path+"\\stopothers.txt","r").read()
    if StopText == '0': 
        chkValue.set(False)
    elif StopText == '1':
        chkValue.set(True)
    else:
        print("Some error exist! :readStopFile():")
def readStopFile2():
    StopText2 = open(path+"\\stopothers2.txt","r").read()
    if StopText2 == '0': 
        chkValue2.set(False)
    elif StopText2 == '1':
        chkValue2.set(True)
    else:
        print("Some error exist! :readStopFile2():")
def changeStopFile():
    StopTextx = open(path+"\\stopothers.txt","r").read()
    if StopTextx == '0':
        open(path+"\\stopothers.txt","w").write("1")
        StopAudio()
        C2.destroy()
    elif StopTextx == '1':
        open(path+"\\stopothers.txt","w").write("0")
        setC2()
    readStopFile()
def changeStopFile2():
    StopTextxx = open(path+"\\stopothers2.txt","r").read()
    if StopTextxx == '0':
        open(path+"\\stopothers2.txt","w").write("1")
    elif StopTextxx == '1':
        open(path+"\\stopothers2.txt","w").write("0")
        StopAudio()
    readStopFile2()
def setC2():
    global C2
    C2 = Checkbutton(app, text="Multiple\nsounds", command=changeStopFile2, variable = chkValue2, onvalue = 1, offvalue = 0, bg='pink', activebackground='magenta')
    C2.place(relx=0, rely=0.525, anchor=W)
chkValue = BooleanVar()
chkValue2 = BooleanVar() 
readStopFile()
readStopFile2()
C1 = Checkbutton(app, text="STOP other\nsounds", command=changeStopFile, variable = chkValue, onvalue = 1, offvalue = 0, bg='pink', activebackground='magenta')
C1.place(relx=0, rely=0.325, anchor=W)
ffef = open(path+"\\stopothers.txt","r").read()
if ffef == "1":
    print()
else:
    setC2()
#changeStopFile()
#changeStopFile()
def setBindNameNumber():
    e1.delete(0, 'end')
    number_bind = len(open(path+"\\config.txt","r").readlines())
    e1.insert(0, "Bind name "+str(number_bind))
setBindNameNumber()
e2 = Entry(app)
e2.place(relx=0.5, rely=0.55, anchor=CENTER)
e2.insert(0, "Location")
B3 = Button(app, text = "Select file", command = selectFile, bg='yellow', activebackground='#808000')
B3.place(relx=0.5, rely=0.7, anchor=CENTER)
v = DoubleVar()
scale_value = open(path+"\\volume.txt","r").read()
if scale_value == "":
    scale_value = 50
try:
    scale_value = int(scale_value)
except:
    scale_value = 50
    print("except")
scale = Scale(app,resolution=1,troughcolor='lime',activebackground='lime', variable = v, command=soundVolumeChangeTest, from_ = 100, to = 0)
scale.place(relx=1, rely=0.5, anchor=E)
scale.set(scale_value)
label_stopsounds = Label(app, text="")
label_stopsounds.place(relx=1, rely=0.225, anchor=E)
#BINDS#

newWindow = Toplevel(app)
newWindow.iconbitmap(icon)
newWindow.geometry('350x750')
newWindow.title("Binds")
#newWindow.attributes('-toolwindow', True)
newWindow.protocol("WM_DELETE_WINDOW", closeApp)
newWindow.resizable(0, 1)

LoadData()
#try:
#    LoadData()
#except:
#    print("Error while loading data!")
app.mainloop()
listener.stop()
