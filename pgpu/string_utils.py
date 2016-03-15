def print_to_var(*args, **kw):
    """
    Returns strings like those the Python3 print() function writes to file
    objects.
    """
    sep = str(kw.pop('sep', ' '))
    end = str(kw.pop('end', '\n'))
    if kw:
        raise TypeError(
            "'%s' is an invalid keyword argument for this function"
            % kw.keys()[0]
        )

    return sep.join(str(a) for a in args) + end
