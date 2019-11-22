from tkinter import *
import time, random
import win32api, win32con

root = Tk()

canvas1 = Canvas(root, width=400, height=300)

# MAIN LABEL
mainLabel = Label(root, text='Point your cursor to clicking point')
mainLabel.configure(font=('helvetica', 14, 'bold'))
canvas1.create_window(200, 25, window=mainLabel)

# Checkbox for the random
randomCursor = IntVar()
randomCursorCheckBox = Checkbutton(root, text="RandomCursor", variable=randomCursor)
canvas1.create_window(300, 75, window=randomCursorCheckBox)

# Cursor explanation image
randomCursorImg = PhotoImage(file='cursor.png')
canvas1.create_image(125, 75, image=randomCursorImg)

# Speed label and intervals
speedLabel = Label(root, text='Define ticking speed interval in seconds')
speedLabel.configure(font=('helvetica', 12, 'bold'))
canvas1.create_window(200, 125, window=speedLabel)

T1_lbl = Label(root, text='T1:')
canvas1.create_window(25, 150, window=T1_lbl)
entryT1 = Entry(root)
canvas1.create_window(110, 150, window=entryT1)

T2_lbl = Label(root, text='T2:')
canvas1.create_window(225, 150, window=T2_lbl)
entryT2 = Entry(root)
canvas1.create_window(310, 150, window=entryT2)

state = False


def get_cursor_pos(x, y):
    if randomCursor.get() == 1:
        x_n = random.randint(x - 5, x + 5)
        y_n = random.randint(y - 5, y + 5)
        win32api.SetCursorPos((x_n, y_n))
        print('new random +-5 x_n: %s y_n: %s' % (x_n, y_n))
        root.update()
        return x_n, y_n
    else:
        print('Exact pos x: %s y: %s' % (x, y))
        root.update()
        return x, y


def mouseClickLeft(x, y):
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    time.sleep(0.005)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)


def mouseClickRight(x, y):
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, x, y, 0, 0)
    time.sleep(0.005)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, x, y, 0, 0)


def generate_random_time():
    T1 = entryT1.get()
    T2 = entryT2.get()
    root.update()
    return random.uniform(float(T1), float(T2))


# Clicking button dropdown list
OPTIONS = ['LeftMouse',
           'RightMouse']
buttonListVar = StringVar()
buttonListVar.set(OPTIONS[0])
buttonListMenu = OptionMenu(root, buttonListVar, *OPTIONS)
canvas1.create_window(200, 200, window=buttonListMenu)


def press_button_input():
    button = buttonListVar.get()
    root.update()
    return button


def start(event=None):
    global state
    state = True
    startTime = time.time()
    x, y = win32api.GetCursorPos()
    while state == True:
        try:
            get_cursor_pos(x, y)
            timeDelay = generate_random_time()
            root.after(round(timeDelay * 1000), None)
            # Click the button
            if 'Left' in press_button_input():
                mouseClickLeft(x, y)
            elif 'Right' in press_button_input():
                mouseClickRight(x, y)
            print('Clicker is on with time delay:%s' % timeDelay)
            elapsedTime = time.time() - startTime
            print('Elapsed time: %s seconds' % elapsedTime)
        except ValueError:
            print('Something is not provided. Check data.')
            break


def stop(event=None):
    print('Stop')
    global state
    state = False
    root.update()


# START STOP buttons and labels, with keybind explanations
startLabel = Label(root, text='(Press F3 or button)')
canvas1.create_window(75, 200, window=startLabel)
startButton = Button(text='START!', bg='green', fg='white',
                     font=('helvetica', 9, 'bold'), command=start)
canvas1.create_window(75, 220, window=startButton)

stopLabel = Label(root, text='(Press F4 or button)')
canvas1.create_window(325, 200, window=stopLabel)
stopButton = Button(text='STOP!', bg='red', fg='white',
                    font=('helvetica', 9, 'bold'), command=stop)
canvas1.create_window(325, 220, window=stopButton)

root.bind('<F3>', start)
root.bind('<F4>', stop)
canvas1.pack()

root.mainloop()
