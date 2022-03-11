from contextlib import contextmanager


@contextmanager
def open_with_error(filename, mode="r"):
    """
    Custom function which can be used in a with statement
    in place of the open function.  The advantage of using
    this function is it catches errors.  This opener
    ensures the file handle is properly closed at the end.
    """
    try:
        f = open(filename, mode)
    except IOError as error:
        yield None, error
    else:
        try:
            yield f, None
        finally:
            f.close()
