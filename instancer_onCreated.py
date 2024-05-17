# Created by Paul Colton for Rebelway Cinematic Lighting in Houdini class
# Based on script from https://www.toadstorm.com/blog/?p=1012
# v1.0.1

import hou
import traceback
import time
import threading

primitiveName = "/$OS"
destinationPrimitivePath = '`chs("category")``chs("subcategory")``chs("primname")`'

categories = [
    "/env",
    "/fx",
    "/prop",
    "/veh",
    "/asset"
]

subCategories = [
    "/hero",
    "/secondary",
    "/fg",
    "/mg",
    "/bg",
    "/scatter",
    "/volume",
    "/water"
]

# get the node that was just created
me = kwargs['node']

def delayedSet():
    time.sleep(0.01)
    me.parm("primpath").set(destinationPrimitivePath)
    me.parm("protoindexsrc").set("nameattr")
    me.parm("protopattern").set("%kind:component")    

try:
    if me.parm("category") is None:

        # create spare parameter.
        # first get the ParmTemplateGroup of the HDA. this is the overall parameter layout.
        parm_group = me.parmTemplateGroup()
     
        # we'll put this new spare parm right before the "Destination Primitive" parameter, named "primpath".
        primpath_template = parm_group.find("primpath")

         # Code for parameter template
        hou_parm_template = hou.MenuParmTemplate("category", "Category", menu_items=(categories), menu_labels=(categories))
        hou_parm_template.setJoinWithNext(True)
        parm_group.insertBefore(primpath_template, hou_parm_template)

        # Code for parameter template
        hou_parm_template = hou.MenuParmTemplate("subcategory", "Sub-Category", menu_items=([""] + subCategories), menu_labels=(["None"] + subCategories))
        parm_group.insertBefore(primpath_template, hou_parm_template)

        hou_parm_template = hou.StringParmTemplate(name="primname", label="Primitive Name", num_components=1, default_value=([primitiveName]))
        parm_group.insertBefore(primpath_template, hou_parm_template)

        # now we need to write this modified ParmTemplateGroup back to the individual node's ParmTemplateGroup.
        # this is effectively how you add a spare parm to a node without modifying the HDA itself.
        me.setParmTemplateGroup(parm_group)

        threading.Thread(target=delayedSet).start()

except Exception as err:
    # just in case a ROP Alembic Output SOP is created as a locked node by something else. don't need to see errors.
    print("ERR: " + err)
    pass