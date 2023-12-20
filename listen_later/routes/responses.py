import listen_later.constants as constants


def obj_created(obj):
    return f"Created {obj} successfully.", 201


def obj_updated(obj_type, obj_id, updated_vals):
    return f"Updated {obj_type}({constants.ID}={obj_id}) successfully with the following values:<br />{updated_vals}.", 200


def obj_deleted(obj_type, obj_id):
    return f"Deleted {obj_type}({constants.ID}={obj_id}) successfully.", 200


def not_found_error(obj_type, obj_id):
    return {constants.ERRORS: f"{obj_type}({constants.ID}={obj_id}) could not be found."}, 404


def not_implemented_error():
    return {constants.ERRORS: "Not implemented."}, 501
