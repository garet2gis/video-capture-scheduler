from tkinter import *
import pygame

TIRED = "tired"
AWAKE = "awake"
FINE = "fine"

choices = {
    TIRED: "Устал",
    AWAKE: "Бодр",
    FINE: "Нормально",
}

condition = FINE
pygame.mixer.init()


def init_popup() -> str:
    def play():
        pygame.mixer.music.load("aboba.mp3")
        pygame.mixer.music.play(loops=0)

    play()
    root = Tk()
    root.title('Оценка усталости')
    root.geometry("250x150")
    root.eval('tk::PlaceWindow . center')
    my_frame = Frame(root)
    my_frame.pack(pady=5)

    yes = Button(my_frame, text=choices[AWAKE], command=lambda: choice(AWAKE))
    yes.grid(row=1, column=0, pady=10)

    no = Button(my_frame, text=choices[FINE], command=lambda: choice(FINE))
    no.grid(row=2, column=0, pady=10)

    no = Button(my_frame, text=choices[TIRED], command=lambda: choice(TIRED))
    no.grid(row=3, column=0, pady=10)

    def choice(option):
        global condition
        if option == TIRED:
            condition = TIRED
        elif option == FINE:
            condition = FINE
        elif option == AWAKE:
            condition = AWAKE
        root.destroy()

    root.mainloop()

    return condition
