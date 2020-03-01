from flask_login import login_required, current_user
from flask import Blueprint, render_template, request, redirect, url_for
import sys
from warehouse import Backend
main = Blueprint("main", __name__)

'''
Login page
Home page for the application
'''
@main.route("/")
def login_page():
    if current_user != None and current_user.is_authenticated:
        if current_user.isAdmin():
            return redirect(url_for("main.adminHomepage"))
        elif current_user.isManager():
            return redirect(url_for("main.managerHomepage"))
    return render_template("loginPage.html")

'''
Admin homepage page
Home page for the admin
'''
@main.route("/adminHomepage")
def adminHomepage():
    pageData = {
        "Name": Backend.getName(current_user.id),
        "Items": Backend.getItems(),
        "Sections": list(Backend.getSections())
    }
    managers = Backend.getManagers()
    sep = []
    for manager in managers:
        sectNames = ""
        for sect in manager["Sections"]:
            sectNames += Backend.getSectName(sect) + ", "
        manager["SectionNames"] = sectNames[:-2]
        sep.append(manager)
    pageData["Managers"] = sep
    return render_template("adminHomepage.html", pageData=pageData)


'''
Admin homepage page
Home page for the admin
'''
@main.route("/managerHomepage")
def managerHomepage():
    pageData = {
        "Name": Backend.getName(current_user.id),
    }
    sections = []
    for section in list(Backend.getSections()):
        if current_user.id in section["Managers"]:
            sections.append(section)
    pageData["Sections"] = sections

    return render_template("managerHomepage.html", pageData=pageData)

@main.route("/adminSectionPage", methods=['POST'])
def adminSectionPage():
    sID = request.form.get("sID")
    pageData = {
        "ID": sID,
        "Name": Backend.getSectName(sID),
        "AllItems": Backend.getItems()
    }

    items = []
    for item in Backend.getSectItems(sID):
        item["Name"] = Backend.getItemName(item["ID"])
        items.append(item)
    pageData["Items"] = items

    managerIDs = Backend.getSectManagers(sID)
    managerNames = []
    for mID in managerIDs:
        managerNames.append(Backend.getManagerName(mID))

    pageData["ManagerNames"] = managerNames
    return render_template("adminSectionPage.html", pageData=pageData)

@main.route("/managerSectionPage", methods=['POST'])
def managerSectionPage():
    sID = request.form.get("sID")
    pageData = {
        "ID": sID,
        "Name": Backend.getSectName(sID),
        "AllItems": Backend.getItems()
    }
    items = []
    for item in Backend.getSectItems(sID):
        item["Name"] = Backend.getItemName(item["ID"])
        items.append(item)
    pageData["Items"] = items

    managerIDs = Backend.getSectManagers(sID)
    managerNames = []
    for mID in managerIDs:
        managerNames.append(Backend.getManagerName(mID))

    pageData["ManagerNames"] = managerNames

    return render_template("managerSectionPage.html", pageData=pageData)

@main.route("/settings")
def settings():
    return render_template("settings.html")

@main.route("/createItem", methods=['POST'])
def createItem():
    # Get form data
    name = request.form.get("name")
    description = request.form.get("description")
    Backend.createItem(name, description)
    return '', 204

@main.route("/createSection", methods=["POST"])
def createSection():
    name = request.form.get("name")
    managerIds = []
    managers = Backend.getManagers()
    for manager in managers:
        managerIds.append(str(manager["ID"]))
    managersUsed = []
    for manager in managerIds:
        if request.form.get(manager) != None:
            managersUsed.append(int(manager))
    Backend.createSection(name, managersUsed)
    return '', 204

@main.route("/addItemToSection", methods=["POST"])
def addItemToSection():
    sID = int(request.form.get("sID"))
    itemID = int(request.form.get("Item"))
    Backend.addItemToSect(sID, itemID)
    return '', 204

@main.route("/changeItemAdmin", methods=["POST"])
def changeItemAdmin():
    print(request.form, file=sys.stderr)
    if request.form.get("change") != '':
        sID = int(request.form.get("sID"))
        itemId = int(request.form.get("ItemID"))
        change = int(request.form.get("change"))
        sign = int(request.form.get("sign"))
        proceed = True
        if sign == -1:
            current = Backend.getSectItems(sID)
            for c in current:
                if c["ID"] == itemId:
                    if c["Quantity"] < change:
                        proceed = False
        if proceed:
            Backend.changeSectItem(sID, itemId, sign*change)
    return '', 204



@main.route("/changeItemManager", methods=["POST"])
def changeItemManager():
    if request.form.get("change") != '':
        sID = int(request.form.get("sID"))
        itemId = int(request.form.get("ItemID"))
        change = int(request.form.get("change"))
        sign = int(request.form.get("sign"))
        proceed = True
        if sign == -1:
            current = Backend.getSectItems(sID)
            for c in current:
                if c["ID"] == itemId:
                    if c["Quantity"] < change:
                        proceed = False
        if proceed:
            Backend.changeSectItem(sID, itemId, sign*change)
    return '', 204

