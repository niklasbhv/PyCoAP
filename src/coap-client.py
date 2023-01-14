# Implementation eines CoAP clients, primaer zum Testen des CoAP Servers
# Versendet die unten angegebene Nachricht an den CoAP Server

import logging
import asyncio

from tkinter import *
from aiocoap import *

logging.basicConfig(level=logging.INFO)

class Gui:
    def startGui():
        gui = Gui()
    
    def send():
        pass
    
    def get_input(self, text):
        return text.get("1.0", END)

    def set_input(self, text, value):
        text.delete("1.0", END)
        text.insert(END, value)

    def __init__(self):
        self.root=Tk()
        self.root.geometry('800x600')
        self.root.resizable(0, 0)
        self.root.title("CoAP Client")

        self.command = StringVar()
        self.destination = StringVar()
        self.confirm = BooleanVar()

        Label(self.root, text="Nachricht:").pack()
        self.message = Text(self.root, width=60, height=10)
        self.message.pack()
        
        self.command.set("GET")
        Label(self.root, text="Befehl:").pack()
        Entry(self.root, textvariable=self.command, width=60).pack()

        self.confirm.set(True)
        Checkbutton(self.root, text="Bestätigung?", variable=self.confirm).pack()

        self.destination.set("coap://")
        Label(self.root, text="Ziel:").pack()
        Entry(self.root, textvariable=self.destination, width=60).pack()

        Label(self.root, text="Antwort:").pack()
        self.answer = Text(self.root, width=60, height=10)
        self.answer.pack()

        Button(self.root, text="Senden", command=lambda: asyncio.run(self.send())).pack()
        
        self.root.mainloop()
        
    async def send(self):
        if self.confirm.get():
            self.messagetype = 0
        else:
            self.messagetype = 1

        match self.command.get().upper():
            case "PUT":
                request = Message(code=PUT, mtype = self.messagetype, payload=str.encode(self.get_input(self.message)), uri=self.destination.get())
            case "GET":
                self.confirm.set(True)
                request = Message(code=GET, mtype = 0, uri=self.destination.get())
            case "POST":
                request = Message(code=POST, mtype = self.messagetype, payload=str.encode(self.get_input(self.message)), uri=self.destination.get())
            case _:
                self.set_input(self.answer, "Unbekannter Befehl: " + command.get())
                request = None
        
        if(request != None):
            context = await Context.create_client_context()
            await asyncio.sleep(2)
            response = await context.request(request).response
            if self.confirm.get():
                self.set_input(self.answer, "Result: %s\n%s"%(response.code, str(bytes.decode(response.payload))))
            else:
                self.set_input(self.answer, "Bestätigung deaktiviert")
           
if __name__ == "__main__":
    Gui.startGui()