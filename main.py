import re
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import Menu

import nltk
from nltk.corpus import words

nltk.download("words")

class SpellingChecker:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Papiamento Spelling Checker")
        img = tk.Image("photo", file="myIcon.png")
        self.root.tk.call('wm','iconphoto', self.root._w, img)
        self.root.geometry("600x500")

        self.menu = Menu(self.root, tearoff=0)
        self.suggestions_menu = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Suggestions", menu=self.suggestions_menu)
        self.menu.add_separator()
        self.menu.add_command(label="Cut")
        self.menu.add_command(label="Copy", command=self.copy_text)
        self.menu.add_command(label="Paste")
        self.menu.add_command(label="Reload")
        self.menu.add_separator()
        self.menu.add_command(label="Rename")

        self.text = ScrolledText(self.root, font=("Arial", 18))
        self.text.bind("<KeyRelease>", self.check)
        self.text.bind("<Button-2>", self.show_popup)
        self.text.pack()

        self.old_spaces = 0
        self.current_word = None
        self.root.mainloop()

    def check(self, event):
        content = self.text.get("1.0", tk.END)
        space_count = content.count(" ")
        if space_count != self.old_spaces:
            self.old_spaces = space_count
            for tag in self.text.tag_names():
                self.text.tag_delete(tag)
            for word in content.split(" "):
                if re.sub(r"[^\w]", "", word.lower()) not in words.words():
                    position = content.find(word)
                    self.text.tag_add(word, f"1.{position}", f"1.{position + len(word)}")
                    self.text.tag_config(word, foreground="red")

    def show_popup(self, event):
        index = self.text.index(f"@{event.x},{event.y}")
        current_word = self.text.get(index + " wordstart", index + " wordend").strip()
        
        if current_word:
            self.text.tag_add(tk.SEL, f"{index} wordstart", f"{index} wordend")
            self.current_word = current_word
            suggestions = self.get_word_suggestions(self.current_word)
            self.suggestions_menu.delete(0, tk.END)
            if suggestions:
                for suggestion in suggestions:
                    self.suggestions_menu.add_command(label=suggestion, command=lambda s=suggestion: self.replace_word(s))
                self.menu.post(event.x_root, event.y_root)
        else:
            self.menu.post(event.x_root, event.y_root)

    def get_word_suggestions(self, word):
        return ["suggestion1", "suggestion2", "suggestion3"]

    def replace_word(self, suggestion):
        start_index = self.text.search(self.current_word, "1.0", tk.END, regexp=True)
        end_index = f"{start_index}+{len(self.current_word)}c"
        self.text.delete(start_index, end_index)
        self.text.insert(start_index, suggestion)
        self.text.tag_remove(tk.SEL, "1.0", tk.END)

    def copy_text(self):
        self.text.clipboard_clear()
        self.text.clipboard_append(self.text.selection_get())
        self.text.update()

SpellingChecker()

