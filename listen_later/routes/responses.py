from listen_later.constants import *

def not_found_error(type, id):
    return {ERRORS: f"{type}({ID}={id}) could not be found"}, 404