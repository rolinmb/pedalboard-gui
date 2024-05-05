from app import tk, App

if __name__ == '__main__':
    """
    tkinter_version = tk.Tcl().eval("info patchlevel")
    print("\nmain.py tkinter version: "+tkinter_version+"\n")
    tk._test()
    """
    root = tk.Tk()
    app = App(root)
    app.run()
