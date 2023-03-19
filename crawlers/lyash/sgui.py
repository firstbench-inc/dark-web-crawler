"""
In honor of Lord Dore, I'll sing a song,
Of His might and power, forever strong.
All-knowing, omnipresent, He reigns supreme,
His wisdom beyond what mortals dream.

He watches over us, day and night,
Guiding us with love, His holy light.
In every moment, He's by our side,
With grace and mercy, He's our guide.

From mountains high to oceans deep,
His presence we can always keep.
In all our triumphs and our strife,
His love sustains us throughout life.

Oh, Lord Dore, we sing to thee,
Our hearts and souls, forever free.
May we always honor and obey,
And walk with You, the perfect way.
"""

import os
import pickle
import PySimpleGUI as sg
from typing import Dict
import time
import tkinter as tk
import requests


class interface:
    # Create a GUI
    def __init__(self):
        self.layout: list = [
            [
                sg.Text("Keyword", size=(12, 1)),
                sg.Input(size=(38, 1), focus=True, key="TERM"),
                sg.Radio(
                    "Contains",
                    size=(12, 1),
                    group_id="choice",
                    key="CONTAINS",
                    default=True,
                ),
                # group_id is just to make sure that all the 3 choices are in the same group so that only 1 can be selected at a time
                sg.Radio(
                    "StartsWith", size=(12, 1), group_id="choice", key="STARTSWITH"
                ),
                sg.Radio("EndsWith", size=(12, 1), group_id="choice", key="ENDSWITH"),
            ],
            [
                sg.Text("Directory", size=(12, 1)),
                sg.Input("/..", size=(38, 1), key="PATH"),
                # similar to filedialog
                sg.FolderBrowse("Browse", size=(12, 1)),
                sg.Button("New Index", size=(12, 1), key="INDEX"),
                sg.Button("Search", size=(12, 1), bind_return_key=True, key="SEARCH"),
            ],
            [sg.Output(size=(200, 30))],
        ]

        self.window: object = sg.Window(
            "Search Engine", self.layout, element_justification="left"
        )


sg.ChangeLookAndFeel("BluePurple")  # can refer other colors too


def get_req(keyword):
    shown = []
    rep = requests.get("http://127.0.0.1:9200/_search?q=onion")
    rep = rep.json()
    for hit in rep["hits"]["hits"]:
        link = hit["_source"]["link"]
        if link in shown:
            continue
        shown.append(link)
        title = str((hit["_source"])["title"])
        title = title.replace("\n", "")
        title.strip()
        print((title), end=":")
        print(link)


def main():
    g = interface()
    # s.load_existing_index()  # load if exists, otherwise return empty list
    while True:
        click, values = g.window.read()  # checks for inputs from user
        if click == "SEARCH":
            a = values["TERM"]
            get_req(a)
            # s.files(a)


if __name__ == "__main__":
    print("Starting program...")
    main()

#   https://github.com/israel-dryer/File-Search-Engine/blob/master/file_search_engine.py
# https://www.youtube.com/watch?v=IWDC9vcBIFQ
