import re
from django.http.response import HttpResponse
from django.shortcuts import render
from django import forms

from . import util

import markdown2

class searchEntry(forms.Form):
    entry = forms.CharField(label="Search Encyclopedia", widget=forms.TextInput(attrs={'class': "search"}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "search_form": searchEntry()
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


def search(request):
    form = searchEntry(request.POST)
    if form.is_valid():
        entry_name = form.cleaned_data["entry"]

        for entry in util.list_entries():
            if entry_name == entry:
                return display_entry(request, entry_name)

        def related_entry(entry):
            if entry_name in entry:
                return True
            return False

        related_entries = list(filter(related_entry, util.list_entries()))
        if related_entries:
            return render(request, "encyclopedia/search.html", {
                "related_entries": related_entries
            })

    return render(request, "encyclopedia/not_found.html")