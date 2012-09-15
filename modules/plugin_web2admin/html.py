# -*- coding: utf-8 -*-

from gluon import TABLE, DIV, BUTTON, H3, UL, TR, TD, LI
from gluon import current

def build_field_details(db, tables):
    T = current.T
    field_details = DIV(_id="field-details")
    for tablename in tables:
        tbl = TABLE(_class="table table-hover table-condensed table-bordered")
        for fieldname in db[tablename].fields:
            field = db[tablename][fieldname]
            field_props = dict(unique=field.unique, notnull=field.notnull, default=field.default,
                               required=field.required, compute=field.compute, requires=field.requires,
                               represent=field.represent, readable=field.readable, writable=field.writable,
                               label=field.label, comment=field.comment)
            if field.type == "upload":
                field_props["uploadfolder"] = field.uploadfolder     
                field_props["uploadfield"] = field.uploadfield
                field_props["uploadseparate"] = field.uploadseparate
                field_props["uploadfolder"] = field.uploadfolder                         
            tbl.append(TR(TD( "%s (%s - %s)" % (field.name, field.type, field.length)),
                          TD(UL(*[LI(str(key) + " = " + str(value)) for key,value in field_props.iteritems()]))))
        
        # BOOTSTRAP MODAL
        modal_div = DIV(_class="modal hide fade", _id="details_" + tablename, _tabindex="-1", _role="dialog",
                        **{"_aria-labelledby": tablename, "_aria-hidden": "true"})
        modal_div.append(DIV(BUTTON("x", _type="close", _class="button hidden",
                             **{"_data-dismiss": "modal", "_aria-hidden": "true"}),
                             H3(tablename, _id="details_" + tablename + "Label"),
                             _class="modal-header"))
        modal_div.append(DIV(tbl, _class="modal-body"))
        modal_div.append(DIV(BUTTON(T("Close"),_class="btn btn-primary", **{"_data-dismiss": "modal", "_aria-hidden": "true"}),
                             _class="modal-footer"))
        # /MODAL

        field_details.append(modal_div)

    return field_details  