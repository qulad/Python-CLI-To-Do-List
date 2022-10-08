from configparser import ConfigParser
import json
from venv import create
from utils import take_input
import database as db
from datetime import datetime

def initialize_app() -> None:
    """
    Makes initial configuration loadings.
    """
    global config
    config = ConfigParser()
    config.read("config.ini")
    global lang
    lang = config["CONFIG"]["LANGUAGE"]
    global texts
    texts = json.load(open(f"languages\{lang}.json", encoding="utf-8"))

def opening_screen() -> None:
    """
    Prints things that needs to be printed only once at the beginning of the program.
    """
    print(texts["app_name"])
    print(texts["welcome_text"])

def main_menu() -> None:
    """
    The main menu.
    """
    print(texts["main_menu"]["menu"])

    print("1) " + texts["main_menu"]["new_item"])
    print("2) " + texts["main_menu"]["view_items"])
    print("3) " + texts["main_menu"]["edit_item"])
    print("4) " + texts["main_menu"]["delete_item"])
    print("5) " + texts["main_menu"]["settings"])
    print("6) " + texts["main_menu"]["about"])
    print("7) " + texts["main_menu"]["exit"])

    selected = take_input(input_text=texts["ask_input"], low=1, high=7)
    funcs = {"1": new_note_menu, "2": all_notes_menu, "3": edit_notes_menu, "4": delete_notes_menu, "5": settings_menu, "6": about_menu, "7": exit_app}
    funcs[str(selected)]()

def new_note_menu() -> None:
    """
    The menu to add new notes.
    """
    print(texts["new_item_menu"]["menu"])

    print(texts["new_item_menu"]["item_name"])
    note_name = input()
    print(texts["new_item_menu"]["item_text"])
    note_text = input()

    db.insert_new_note(note_name=note_name, note_text=note_text)

    print(texts["new_item_menu"]["added_item"])

    end_of_menu()


def all_notes_menu() -> None:
    """
    The menu to view all notes.
    """
    print(texts["all_notes_menu"]["menu"])

    print(texts["all_notes_menu"]["description"])
    notes = db.all_notes()
    for i in range(len(notes)):
        created = notes[i][1]
        updated = notes[i][2]
        title = notes[i][3]
        text = notes[i][4]
        print(f"\n{i+1}) " + texts["all_notes_menu"]["item_name"] + title)
        print(texts["all_notes_menu"]["item_text"] + text)
        print(texts["all_notes_menu"]["created"] + created)
        if created != updated:
            print(texts["all_notes_menu"]["updated"] + updated)
    
    end_of_menu()

def edit_notes_menu() -> None:
    """
    The menu to edit notes.
    """
    print(texts["edit_notes_menu"]["menu"])

    print(texts["edit_notes_menu"]["description"])
    notes = db.all_notes()
    for i in range(len(notes)):
        created = notes[i][1]
        updated = notes[i][2]
        title = notes[i][3]
        text = notes[i][4]
        print(f"\n{i+1}) " + texts["edit_notes_menu"]["item_name"] + title)
        print(texts["edit_notes_menu"]["item_text"] + text)
        print(texts["edit_notes_menu"]["created"] + created)
        if created != updated:
            print(texts["edit_notes_menu"]["updated"] + updated)
    
    selected_index = take_input(texts["ask_input"], 1, len(notes)) - 1
    selected_note_id = notes[selected_index][0]

    print(texts["edit_notes_menu"]["new_item_name"])
    new_note_name = input()
    print(texts["edit_notes_menu"]["new_item_text"])
    new_note_text = input()

    db.update_note(note_id=selected_note_id, note_name=new_note_name, note_text=new_note_text)

    print(texts["edit_notes_menu"]["edited"])

    end_of_menu()

def delete_notes_menu() -> None:
    """
    The menu to delete notes.
    """
    print(texts["delete_notes_menu"]["menu"])

    print(texts["delete_notes_menu"]["description"])
    notes = db.all_notes()
    for i in range(len(notes)):
        created = notes[i][1]
        updated = notes[i][2]
        title = notes[i][3]
        text = notes[i][4]
        print(f"\n{i+1}) " + texts["delete_notes_menu"]["item_name"] + title)
        print(texts["delete_notes_menu"]["item_text"] + text)
        print(texts["delete_notes_menu"]["created"] + created)
        if created != updated:
            print(texts["delete_notes_menu"]["updated"] + updated)
    
    selected = take_input(texts["ask_input"], 1, len(notes)) - 1
    db.delete_note(notes[selected][0])

    print(texts["delete_notes_menu"]["deleted"])

    end_of_menu()

def settings_menu() -> None:
    """
    The settings menu.
    """
    print(texts["settings_menu"]["menu"])

    print(texts["settings_menu"]["text"])
    print("1) " + texts["settings_menu"]["language"]["en"])
    print("2) " + texts["settings_menu"]["language"]["tr"])

    selected = take_input(input_text=texts["ask_input"], low=1, high=2)
    if selected == 1:
        config["CONFIG"]["LANGUAGE"] = "en"
    elif selected == 2:
        config["CONFIG"]["LANGUAGE"] = "tr"
    with open("config.ini", "w") as configfile:
        config.write(configfile)
    initialize_app()

    print(texts["settings_menu"]["changed"])

    end_of_menu()

def about_menu() -> None:
    """
    The menu about the app.
    """
    print(texts["about_menu"]["menu"])

    print(texts["about_menu"]["creator"])
    print(texts["about_menu"]["version"])
    print(texts["about_menu"]["about"])
    print(texts["about_menu"]["social"]["github"])
    print(texts["about_menu"]["social"]["instagram"])

    end_of_menu()

def exit_app() -> None:
    """
    Exit app
    """
    db.close_db()
    print(texts["exit_menu"]["exit_text"])
    quit()

def end_of_menu() -> None:
    """
    In the end of a menu, asks user to go to main menu or exit app.
    """
    print("\n1) " + texts["about_menu"]["main_menu"])
    print("2) " + texts["about_menu"]["exit"])
    selected = take_input(input_text=texts["ask_input"], low=1, high=2)
    funcs = {"1": main_menu, "2": exit_app}
    funcs[str(selected)]()

if __name__ == "__main__":
    initialize_app()
    db.initialize_db()
    opening_screen()
    main_menu()
