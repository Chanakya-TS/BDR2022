import tkinter as tk
import customtkinter as ctk

import os
import time

from neurosity import neurosity_sdk

THRESHOLD = 0.8

class RaceApp:

    def __init__(self):
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.root.title("BDR 2022 | Controller")
        self.root.geometry("1000x800")

        self.neurosity = 0
        self.deviceID = ""
        self.email = ""
        self.password = ""

        self.deviceStatus = tk.StringVar(value="Offline")

        self.leftProbability = tk.StringVar(value="N/A")
        self.leftSubscription = 0
        self.rightProbability = tk.StringVar(value="N/A")
        self.rightSubscription = 0

        self.instructionNum = -1
        self.instruction = tk.StringVar(value="N/A")

        self.raceStarted = False
        self.startRaceButton = tk.StringVar(value="Start Race")

        self.titleFont = ctk.CTkFont("Century Gothic", 20, "bold")
        self.textFont = ctk.CTkFont("Century Gothic", 18)
        self.textBFont = ctk.CTkFont("Century Gothic", 18, "bold")
        self.textTrialBFont = ctk.CTkFont("Century Gothic", 70, "bold")
        self.textTrialFont = ctk.CTkFont("Century Gothic", 150)

        self.title = ctk.CTkLabel(self.root, text="BDR 2022 | Controller", pady=10, font=self.titleFont)
        self.title.pack()

        container = ctk.CTkFrame(self.root)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (LoginPage, RacePage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="news")

        self.show_frame("LoginPage")

        self.root.mainloop()

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def next_instruction(self):
        self.instructionNum += 1
        if self.instructionNum % 3 == 0:
            self.instruction.set("Imagine moving your left arm")
        elif self.instructionNum % 3 == 1:
            self.instruction.set("Imagine moving your right arm")
        elif self.instructionNum % 3 == 2:
            self.instruction.set("Drone moving forward")
            # MOVE DRONE FORWARD
            time.sleep(3)
            self.next_instruction()

    def right_callback(self, data):
        global THRESHOLD
        if self.instructionNum % 3 == 1:
            prob = data['predictions'][0]['probability']
            print("RIGHT PROB: ", prob)
            prob /= THRESHOLD
            prob *= 100
            prob = min(prob, 100)
            self.rightProbability.set(f'prob:.3f%')
            if prob >= 100:
                self.next_instruction()

    def left_callback(self, data):
        global THRESHOLD
        if self.instructionNum % 3 == 0:
            prob = data['predictions'][0]['probability']
            print("LEFT PROB: ", prob)
            prob /= THRESHOLD
            prob *= 100
            prob = min(prob, 100)
            self.leftProbability.set(f'prob:.3f%')
            if prob >= 100:
                self.next_instruction()


class LoginPage(ctk.CTkFrame):

    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller

        self.loginFrame = ctk.CTkFrame(self)
        self.loginFrame.place(anchor='c', relx=0.5, rely=0.5)

        tk.Grid.rowconfigure(self.loginFrame, tuple(range(5)), weight=1)
        tk.Grid.columnconfigure(self.loginFrame, tuple(range(2)), weight=1)

        self.emailLabel = ctk.CTkLabel(self.loginFrame, text="Email: ", font=controller.textBFont)
        self.emailLabel.grid(row=1, column=0, pady=(20, 0), sticky="NEWS", padx=(10, 0))

        self.emailInput = ctk.CTkEntry(self.loginFrame, placeholder_text="johndoe@xyz.com", font=controller.textFont,
                                       width=250, height=10)
        self.emailInput.grid(row=1, column=1, pady=(20, 0), padx=(10, 10))

        self.passwordLabel = ctk.CTkLabel(self.loginFrame, text="Password: ", font=controller.textBFont)
        self.passwordLabel.grid(row=2, column=0, pady=(20, 0), sticky="NEWS", padx=(10, 10))

        self.passwordInput = ctk.CTkEntry(self.loginFrame, show="*", font=controller.textFont, width=250, height=10)
        self.passwordInput.grid(row=2, column=1, pady=(20, 0), sticky="NEWS", padx=(10, 10))

        self.deviceIDLabel = ctk.CTkLabel(self.loginFrame, text="Device ID: ", font=controller.textBFont)
        self.deviceIDLabel.grid(row=3, column=0, pady=(20, 20), sticky="NEWS", padx=(10, 10))

        self.deviceIDInput = ctk.CTkEntry(self.loginFrame, font=controller.textFont, width=250, height=10)
        self.deviceIDInput.grid(row=3, column=1, pady=(20, 20), sticky="NEWS", padx=(10, 10))

        self.loginButton = ctk.CTkButton(self.loginFrame, width=50, command=self.login, text="Login",
                                         font=controller.textFont)
        self.loginButton.grid(row=4, column=0, columnspan=5, sticky="NEWS")

    def login(self):

        self.controller.deviceID = self.deviceIDInput.get()
        self.controller.email = self.emailInput.get()
        self.controller.password = self.passwordInput.get()

        self.controller.neurosity = neurosity_sdk({
            "device_id": self.controller.deviceID
        })

        # self.controller.neurosity = neurosity_sdk({
        #     "device_id": "ff682da876c9f86787dba4d9930663cb"
        # })

        self.controller.neurosity.login({
            "email": self.controller.email,
            "password": self.controller.password
        })

        # self.controller.neurosity.login({
        #     "email": "jsspringer@crimson.ua.edu",
        #     "password": "BDR_dev2"
        # })

        status = self.controller.neurosity.status_once()
        if status['state'] == "online":
            self.controller.deviceStatus.set("Online")

        self.controller.show_frame("RacePage")


class RacePage(ctk.CTkFrame):

    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller

        self.statusFrame = ctk.CTkFrame(self)
        self.statusFrame.pack(fill=tk.X, expand=False)
        tk.Grid.rowconfigure(self.statusFrame, tuple(range(1)), weight=1)
        tk.Grid.columnconfigure(self.statusFrame, tuple(range(2)), weight=1)

        self.statusLabel = ctk.CTkLabel(self.statusFrame, text="Status: ", font=controller.textBFont)
        self.statusLabel.grid(row=0, column=0, pady=(10, 10), sticky="NES", padx=(10, 10))

        self.connectionLabel = ctk.CTkLabel(self.statusFrame, textvariable=self.controller.deviceStatus, font=controller.textFont)
        self.connectionLabel.grid(row=0, column=1, pady=(10, 10), padx=(10, 10), sticky="NWS")

        self.logoutButton = ctk.CTkButton(self.statusFrame, text="Logout", command=self.logout,
                                          font=controller.textFont)
        self.logoutButton.grid(row=1, column=0, columnspan=2, pady=(10, 10), padx=(10, 10))

        self.raceFrame = ctk.CTkFrame(self)
        self.raceFrame.pack(fill=tk.BOTH, expand=True)
        tk.Grid.rowconfigure(self.raceFrame, tuple(range(3)), weight=1)
        self.raceFrame.rowconfigure(0, weight=1)
        self.raceFrame.rowconfigure(2, weight=4)
        self.raceFrame.rowconfigure(1, weight=1)
        tk.Grid.columnconfigure(self.raceFrame, tuple(range(3)), weight=1)

        self.startRaceButton = ctk.CTkButton(self.raceFrame, textvariable=self.controller.startRaceButton, command=self.start_race,
                                             font=controller.textFont)
        self.startRaceButton.grid(row=0, column=0, columnspan=3, pady=(10, 10), padx=(10, 10))

        self.leftProb = ctk.CTkLabel(self.raceFrame, textvariable=self.controller.leftProbability, font=controller.textTrialFont)
        self.leftProb.grid(row=1, column=0, sticky="NEWS")

        self.leftLabel = ctk.CTkLabel(self.raceFrame, text="LEFT", font=controller.textTrialBFont)
        self.leftLabel.grid(row=2, column=0, sticky="NEWS")

        self.rightProb = ctk.CTkLabel(self.raceFrame, textvariable=self.controller.rightProbability, font=controller.textTrialFont)
        self.rightProb.grid(row=1, column=2, sticky="NEWS")

        self.rightLabel = ctk.CTkLabel(self.raceFrame, text="RIGHT", font=controller.textTrialBFont)
        self.rightLabel.grid(row=2, column=2, sticky="NEWS")

        self.instructionLabel = ctk.CTkLabel(self.raceFrame, textvariable=self.controller.instruction, font=controller.textTrialBFont)
        self.instructionLabel.grid(row=1, column=1, rowspan=2)

    def logout(self):
        self.controller.show_frame("LoginPage")

    def start_race(self):
        if not self.controller.raceStarted:
            self.controller.raceStarted = True
            self.controller.next_instruction()
            self.controller.rightSubscription = self.controller.neurosity.kinesis("rightArm", self.controller.right_callback)
            self.controller.leftSubscription = self.controller.neurosity.kinesis("leftArm", self.controller.left_callback)
            self.controller.startRaceButton.set("End Race")
        else:
            self.controller.raceStarted = False
            self.controller.instructionNum = -1
            self.controller.rightSubscription()
            self.controller.leftSubscription()
            self.controller.startRaceButton.set("Start Race")


RaceApp()
