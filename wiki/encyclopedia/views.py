from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from markdown2 import markdown

from django import forms
from . import util
import random

class SearchForm(forms.Form):
    search_title = forms.CharField(label='', widget=forms.TextInput(attrs={
        "class": "search",
        "placeholder": "Search Wiki"}))

class CreateForm(forms.Form):
    form_title = forms.CharField(label="Title", widget=forms.TextInput(attrs={
        "class": "form-control",
        "id": "title", 
        "name": "title", 
        "placeholder": "Title for entry"}))
    form_content = forms.CharField(label="Content", widget=forms.Textarea(attrs={
        "class": "form-control",
        "id": "content",
        "name": "content",
        "placeholder": "Write content for the entry in this text area."}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "search_request": SearchForm(),
    })

def go_to_entry(request, title):
    return render(request, "encyclopedia/entry.html", {
        "entry": markdown(util.get_entry(title)),
        "title": title,
        "search_request": SearchForm(),
    })

def search(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            search_title = form.cleaned_data["search_title"]
            entry = util.get_entry(search_title)
            if entry:
                return redirect(reverse('entry', args=[search_title]))
            else:
                entries = util.list_entries()
                related_entries = []
                for entry in entries:
                    if search_title.lower() in entry.lower():
                        related_entries.append(entry)

                return render(request, "encyclopedia/search.html", {
                    "search_title": search_title,
                    "related_entries": related_entries,
                    "search_request": SearchForm()
                })
        return redirect(reverse('index')) 
    
def create_new_page(request):
    if request.method == "POST":
        form = CreateForm(request.POST)
        if form.is_valid():    
            title = form.cleaned_data["form_title"]
            content = form.cleaned_data["form_content"]
            if title in util.list_entries():
                messages.error(request,'Entry with this title already exists. Try again with a different title!')
            else:
                util.save_entry(title, content)
                return redirect("entry", title=title)
    return render(request, "encyclopedia/create.html", {
        "create_form": CreateForm()
    })
    
def edit_page(request, title):
    entry = util.get_entry(title.strip())

    if request.method == "POST":
        entry = request.POST.get("content")
        util.save_entry(title, entry)
        return redirect("entry", title=title)  

    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "entry": entry
    })

def random_page(request):
    title = random.choice(util.list_entries())

    return render(request, "encyclopedia/entry.html", {
        "entry": markdown(util.get_entry(title)),
        "title": title,
        "search_request": SearchForm(),
    })
