from django.shortcuts import render

from . import util

import markdown2

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def display_entry(request, entry_title):
    list_entries = util.list_entries()
    if entry_title in list_entries:
        entry_content = markdown2.markdown(util.get_entry(entry_title))
        return render(request, "encyclopedia/entry.html", {
            "entry_title": entry_title,
            "entry_content": entry_content
        })
    else:
        return render(request, "encyclopedia/not_found.html")


