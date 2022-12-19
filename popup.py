from tkinter import *

TIRED = "tired"
AWAKE = "awake"
FINE = "fine"

choices = {
    TIRED: "Устал",
    AWAKE: "Бодр",
    FINE: "Нормально",
}

condition = FINE


def init_popup() -> str:
    root = Tk()

    def choice(option):
        global condition
        if option == TIRED:
            condition = TIRED
        elif option == FINE:
            condition = FINE
        elif option == AWAKE:
            condition = AWAKE
        root.quit()

    root.title('Оценка усталости')
    root.geometry("250x150")
    root.eval('tk::PlaceWindow . center')

    Button(root, text=choices[AWAKE], command=lambda: choice(AWAKE)).pack(expand=True)
    Button(root, text=choices[FINE], command=lambda: choice(FINE)).pack(expand=True)
    Button(root, text=choices[TIRED], command=lambda: choice(TIRED)).pack(expand=True)

    root.mainloop()

    return condition
