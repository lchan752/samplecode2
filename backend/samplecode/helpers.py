import attr


def is_equal(this, that):
    if this.__class__ != that.__class__:
        return False
    dataclass = this.__class__
    for attribute in attr.fields(dataclass):
        if getattr(this, attribute.name) != getattr(that, attribute.name):
            return False
    return True
