from django.http.response import HttpResponse
from django.shortcuts import render
from django import forms

from . import util

import markdown2

class SearchEntry(forms.Form):
    entry = forms.CharField(label="Search Encyclopedia", widget=forms.TextInput(attrs={'class': "search"}))

class NewPage(forms.Form):
    entry_title = forms.CharField(label="Title")
    entry_body = forms.CharField(label="Body", widget=forms.Textarea)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "search_form": SearchEntry()
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
    form = SearchEntry(request.POST)
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

def new_page(request):
    if request.method == "POST":
        form = NewPage(request.POST)
        if form.is_valid():
            entry_title = form.cleaned_data["entry_title"]
            entry_body = form.cleaned_data["entry_body"]

            if util.get_entry(entry_title):
                return HttpResponse("ENTRY ALREADY EXISTS!")
            
            util.save_entry(entry_title, entry_body)
            return display_entry(request, entry_title)

    return render(request, "encyclopedia/new_page.html", {
        "new_page_form": NewPage()
    })

def edit_page(request, entry_title):
    if request.method == "POST":
        form = NewPage(request.POST)
        if form.is_valid():
            entry_title = form.cleaned_data["entry_title"]
            entry_body = form.cleaned_data["entry_body"]

            util.save_entry(entry_title, entry_body)
            return display_entry(request, entry_title)

    return render(request, "encyclopedia/edit_page.html", { 
        "edit_entry_form": NewPage(
            initial={ 
                'entry_title': entry_title,
                'entry_body': util.get_entry(entry_title)
                })
        })
