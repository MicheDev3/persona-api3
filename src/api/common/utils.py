

def to_dict(model, to_be_excluded=None):
    # using vars I get also this attr
    # _sa_instance_state which I do need
    excludeds = ['id', '_sa_instance_state']
    if to_be_excluded:
        excludeds.append(to_be_excluded)
    attributes = vars(model)
    for excluded in excludeds:
        if excluded in attributes:
            attributes.pop(excluded)

    return attributes
