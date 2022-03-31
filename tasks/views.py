from django.shortcuts import render
from django import forms
from django.forms import formset_factory
from django.urls import reverse
from django.http import HttpResponseRedirect
import uuid

PURPLE = {"primary":"#7c62c5", "primary_mid": "#8151cf", "primary_dark": "#7e4fd4", "primary_light":"#f1e6ff", "primary_light_mid":"#e1cffa" , "id":0}
BLUE = {"primary":"#5f8ee4", "primary_mid": "#507cda", "primary_dark": "#587cdf", "primary_light":"#e6f0ff", "primary_light_mid":"#cfe3fa" , "id":1}
ORANGE = {"primary":"#e47a5f", "primary_mid": "#da7750", "primary_dark": "#df5d58", "primary_light":"#ffe8d6", "primary_light_mid":"#fcc8a6" , "id":2}
PINK = {"primary":"#e45fa8", "primary_mid": "#da5090", "primary_dark": "#df58a2", "primary_light":"#fce4ed", "primary_light_mid":"#fccee4" , "id":3}
GREEN = {"primary":"#6ac588", "primary_mid": "#60b97b", "primary_dark": "#63bd81", "primary_light":"#e4f3e0", "primary_light_mid":"#b9e9b7" , "id":4}


COLORS = [PURPLE,BLUE,ORANGE, PINK,GREEN]

def init_session(session):
    if "tasks" not in session:
        session["tasks"] = []
    if "list_title" not in session:
        session["list_title"] = "TO DO:"
    if "active_color" not in session:
        session["active_color"] = 0
    return session

def index(request) :
    if (request.method == "POST"):
        toggle_form = ToggleTaskForm(request.POST)
        add_form = NewTaskForm(request.POST)
        if(toggle_form.is_valid()):
            def toggle_completed(task):
                task["completed"] = not task["completed"]
                return task
            request.session["tasks"] = list(map(lambda task : toggle_completed(task) if task["id"] == toggle_form.cleaned_data["task_id"] else task, request.session["tasks"]))

        elif(add_form.is_valid()):
            new_task = {"completed":False, "text":add_form.cleaned_data["new_task"], "id":str(uuid.uuid4())}
            request.session["tasks"] += [new_task]
        return HttpResponseRedirect(reverse("tasks:index"))
    else:
        request.session = init_session(request.session)
        return render(request, "tasks/index.html", {"tasks":request.session["tasks"], "new_task":NewTaskForm(), "title":"Tasks", "list_title":request.session["list_title"], "colors":COLORS, "active_color":COLORS[request.session["active_color"]]})

def edit(request):
    if (request.method == "POST"):
        delete_id_form = DeleteTaskForm(request.POST)
        rename_form = RenameForm(data=request.POST,tasks=request.session["tasks"])
        delete_completed_form = DeleteCompletedForm(request.POST)
        color_form = ChangeColorForm(request.POST)
        if(delete_id_form.is_valid()):
            request.session["tasks"] = list(filter(lambda task : task["id"] != delete_id_form.cleaned_data["task_id"], request.session["tasks"]))
        elif(delete_completed_form.is_valid()):
            request.session["tasks"] = list(filter(lambda task : not task["completed"], request.session["tasks"]))
        elif(rename_form.is_valid()):
            def rename(task, text):
                task["text"] = text 
                return task
            request.session["tasks"] = list(map(lambda task : rename(task, rename_form.cleaned_data[task["id"]]), request.session["tasks"]))
            request.session["list_title"] = rename_form.cleaned_data["list_title"]
        elif(color_form.is_valid()):
            request.session["active_color"] = color_form.cleaned_data["color_id"]
            
        return HttpResponseRedirect(reverse("tasks:edit"))
    else:
        request.session = init_session(request.session)
        return render(request, "tasks/edit.html", {"tasks":request.session["tasks"], "title":"Edit Tasks", "list_title":request.session["list_title"], "colors":COLORS, "active_color":COLORS[request.session["active_color"]]})


class NewTaskForm(forms.Form):
    new_task = forms.CharField(label="New Task")
    form_identifier = forms.BooleanField(widget=forms.HiddenInput(), required=False)


class ToggleTaskForm(forms.Form):
    task_id = forms.CharField(label="task_item")

class DeleteTaskForm(forms.Form):
    task_id = forms.CharField(label="task_item")

class DeleteCompletedForm(forms.Form) :
    delete_completed = forms.BooleanField(label="delete_completed")

class RenameForm(forms.Form):
    list_title = forms.CharField()
    def __init__(self, tasks, *args, **kwargs):
        super(RenameForm, self).__init__(*args, **kwargs)
        for task in tasks:
            self.fields[task["id"]] = forms.CharField()

class ChangeColorForm(forms.Form):
    color_id = forms.IntegerField()