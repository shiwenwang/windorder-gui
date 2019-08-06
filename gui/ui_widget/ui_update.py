

def combobox_update(combobox, new_items, checkbox, full_items):
    current_item = combobox.currentText()
    combobox.clear()
    if checkbox.isChecked():
        combobox.addItems(full_items)
    else:
        combobox.addItems(new_items)
    
    combobox.setCurrentText(current_item)

def listWidget_update(listWidget, new_items):
    listWidget.clear()
    listWidget.addItems(new_items)

def list_upper(lst):
    return [d.upper() for d in lst]
