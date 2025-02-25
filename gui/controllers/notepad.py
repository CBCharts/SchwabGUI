import os
import json
import datetime
from PySide6.QtWidgets import (
    QMessageBox, QInputDialog, QMenu, QTextEdit, QToolButton
)
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt

class NotepadController:
    def __init__(self, ui):
        """
        ui: The Ui_MainWindow object containing:
          - textEdit_4          : QTextEdit used as the notepad editor.
          - clear_notes_button  : QPushButton to clear the current note.
          - np_save_button      : QPushButton to initiate saving.
          - np_prev_button      : QPushButton to load the previous note.
          - np_next_button      : QPushButton to load the next note.
          - np_new_button       : QPushButton to create a new note or journal entry.
          - np_edit_button      : QPushButton (checkable) to lock/unlock editing.
          - np_toolbutton       : QToolButton with dropdown options.
        """

        self.ui = ui

        # Base folders for notes and journal
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.notes_folder = os.path.normpath(os.path.join(current_dir, "..", "..", "configs", "notes"))
        self.journal_folder = os.path.normpath(os.path.join(current_dir, "..", "..", "configs", "journal"))
        os.makedirs(self.notes_folder, exist_ok=True)
        os.makedirs(self.journal_folder, exist_ok=True)

        # We'll use textEdit_4 as the editor
        self.editor = self.ui.textEdit_4
        self.editor.setAcceptRichText(True)  # allow rich text formatting if desired

        # We maintain a list of file paths (for navigation) and the current file pointer
        self.current_file = None
        self.file_list = []
        self.current_file_index = -1

        # Setup the UI connections
        self.setup_connections()
        self.setup_toolbutton_menu()

    def setup_connections(self):
        self.ui.clear_notes_button.clicked.connect(self.clear_editor)
        self.ui.np_save_button.clicked.connect(self.save_popup)
        self.ui.np_prev_button.clicked.connect(self.load_prev)
        self.ui.np_next_button.clicked.connect(self.load_next)
        self.ui.np_new_button.clicked.connect(self.new_entry_prompt)

        # np_edit_button is checkable: toggles read-only state of textEdit_4
        self.ui.np_edit_button.setCheckable(True)
        self.ui.np_edit_button.toggled.connect(self.toggle_lock)

    def setup_toolbutton_menu(self):
        """
        Build a dropdown menu on np_toolbutton with two submenus: "Journal" and "Notes".
        Each submenu lists the files in the corresponding folder.
        """
        menu = QMenu(self.ui.np_toolbutton)
        journal_menu = QMenu("Journal", menu)
        notes_menu = QMenu("Notes", menu)

        # Populate journal submenu
        for f in self.get_files_in_folder(self.journal_folder):
            act = QAction(os.path.basename(f), journal_menu)
            act.triggered.connect(lambda checked, path=f: self.load_file(path))
            journal_menu.addAction(act)

        # Populate notes submenu
        for f in self.get_files_in_folder(self.notes_folder):
            act = QAction(os.path.basename(f), notes_menu)
            act.triggered.connect(lambda checked, path=f: self.load_file(path))
            notes_menu.addAction(act)

        menu.addMenu(journal_menu)
        menu.addMenu(notes_menu)
        self.ui.np_toolbutton.setMenu(menu)
        # If your version of PySide6 doesn't allow instance-based access to MenuButtonPopup:
        # from PySide6.QtWidgets import QToolButton
        # self.ui.np_toolbutton.setPopupMode(QToolButton.MenuButtonPopup)
        self.ui.np_toolbutton.setPopupMode(QToolButton.InstantPopup)

    def get_files_in_folder(self, folder):
        """Return a sorted list of file paths in the specified folder."""
        if not os.path.isdir(folder):
            return []
        files = [
            os.path.join(folder, fname)
            for fname in os.listdir(folder)
            if os.path.isfile(os.path.join(folder, fname))
        ]
        return sorted(files)

    def clear_editor(self):
        """Clear the content of the editor."""
        self.editor.clear()

    def save_popup(self):
        """
        Display a popup with options:
          - Save: overwrite current file
          - Save as Journal Entry: use today's date, appending if exists
          - Save As: prompt for filename in notes folder
          - Cancel: do nothing
        """
        msg = QMessageBox()
        msg.setWindowTitle("Save Options")
        msg.setText("Choose a save option:")
        btn_save = msg.addButton("Save", QMessageBox.AcceptRole)
        btn_journal = msg.addButton("Save as Journal Entry", QMessageBox.AcceptRole)
        btn_saveas = msg.addButton("Save As", QMessageBox.AcceptRole)
        btn_cancel = msg.addButton("Cancel", QMessageBox.RejectRole)
        msg.exec()
        clicked = msg.clickedButton()
        if clicked == btn_save:
            self.save_current_entry()
        elif clicked == btn_journal:
            self.save_as_journal()
        elif clicked == btn_saveas:
            self.save_as()
        else:
            return

    def save_current_entry(self):
        """
        Overwrite the current file with the editor's content.
        If no file is currently loaded, default to saving in the notes folder with a 'default_note.html' name.
        """
        content = self.editor.toHtml()
        if not self.current_file:
            default_path = os.path.join(self.notes_folder, "default_note.html")
            self.current_file = default_path
            self.file_list.append(default_path)
            self.current_file_index = len(self.file_list) - 1
        try:
            with open(self.current_file, "w", encoding="utf-8") as f:
                f.write(content)
            QMessageBox.information(None, "Notepad", f"Note saved to {os.path.abspath(self.current_file)}")
        except Exception as e:
            QMessageBox.critical(None, "Save Error", f"Error saving note:\n{e}")

    def save_as_journal(self):
        """
        Save as a journal entry using today's date as filename. 
        If today's journal exists, append. Otherwise, create new.
        """
        today = datetime.date.today().isoformat()
        filename = f"{today}_journal.html"
        filepath = os.path.join(self.journal_folder, filename)
        content = self.editor.toHtml()
        if os.path.exists(filepath):
            try:
                with open(filepath, "a", encoding="utf-8") as f:
                    f.write("<hr>")
                    f.write(content)
            except Exception as e:
                QMessageBox.critical(None, "Save Error", f"Error appending to journal:\n{e}")
                return
        else:
            try:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content)
            except Exception as e:
                QMessageBox.critical(None, "Save Error", f"Error creating journal entry:\n{e}")
                return
        self.current_file = filepath
        if filepath not in self.file_list:
            self.file_list.append(filepath)
            self.current_file_index = len(self.file_list) - 1
        QMessageBox.information(None, "Notepad", f"Journal entry saved to {os.path.abspath(filepath)}")

    def save_as(self):
        """
        Prompt for a filename and save the current content in the notes folder.
        """
        new_name, ok = QInputDialog.getText(
            None, "Save As", "Enter new filename (e.g. my_note.html):"
        )
        if ok and new_name.strip():
            filepath = os.path.join(self.notes_folder, new_name.strip())
            content = self.editor.toHtml()
            try:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content)
            except Exception as e:
                QMessageBox.critical(None, "Save Error", f"Error saving note as:\n{e}")
                return
            self.current_file = filepath
            if filepath not in self.file_list:
                self.file_list.append(filepath)
                self.current_file_index = len(self.file_list) - 1
            QMessageBox.information(None, "Notepad", f"Note saved as {os.path.abspath(filepath)}")
        else:
            return

    def load_file(self, filepath):
        """Load a note file (HTML) into textEdit_4."""
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            self.editor.setHtml(content)
            self.current_file = filepath
            if filepath not in self.file_list:
                self.file_list.append(filepath)
                self.current_file_index = len(self.file_list) - 1
            else:
                self.current_file_index = self.file_list.index(filepath)
        except Exception as e:
            QMessageBox.critical(None, "Load Error", f"Error loading note:\n{e}")

    def load_prev(self):
        """Navigate to the previous note in file_list."""
        if self.current_file_index > 0:
            self.current_file_index -= 1
            self.load_file(self.file_list[self.current_file_index])
        else:
            QMessageBox.information(None, "Notepad", "This is the first note.")

    def load_next(self):
        """Navigate to the next note in file_list."""
        if self.current_file_index < len(self.file_list) - 1:
            self.current_file_index += 1
            self.load_file(self.file_list[self.current_file_index])
        else:
            QMessageBox.information(None, "Notepad", "This is the last note.")

    def toggle_lock(self, locked):
        """
        Toggle the editor's read-only state.
        If np_edit_button is checked, we lock the editor.
        """
        self.editor.setReadOnly(locked)
        if locked:
            self.ui.np_edit_button.setText("Locked")
        else:
            self.ui.np_edit_button.setText("Edit")

    def new_entry_prompt(self):
        """
        Ask whether to create a Journal entry or a Note.
        Based on the choice, clear the editor and update current_file.
        """
        msg = QMessageBox()
        msg.setWindowTitle("New Entry")
        msg.setText("Create a new entry:")
        journal_btn = msg.addButton("Journal", QMessageBox.AcceptRole)
        note_btn = msg.addButton("Note", QMessageBox.AcceptRole)
        cancel_btn = msg.addButton("Cancel", QMessageBox.RejectRole)
        msg.exec()
        clicked = msg.clickedButton()
        if clicked == journal_btn:
            today = datetime.date.today().isoformat()
            filename = f"{today}_journal.html"
            filepath = os.path.join(self.journal_folder, filename)
            self.current_file = filepath
            if filepath not in self.file_list:
                self.file_list.append(filepath)
                self.current_file_index = len(self.file_list) - 1
            self.editor.clear()
        elif clicked == note_btn:
            self.current_file = None
            self.editor.clear()
        else:
            return
