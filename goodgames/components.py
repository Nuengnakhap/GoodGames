import os
from uuid import uuid4


def path_and_rename(path):
    def wrapper(instance, filename):
        ext = filename.split('.')[-1]
        name = "%s" % (instance.short_name,)
        # get filename
        if instance.pk:
            filename = '{}.{}'.format(name, ext)
        else:
            # set filename as random string
            random_id = "rid_%s" % (uuid4().hex,)
            filename = '{}.{}'.format(name, ext)
            # return the whole path to the file
        return os.path.join(path, filename)

    return wrapper


def path_and_rename_match(path):
    def wrapper(instance, filename):
        ext = filename.split('.')[-1]
        name = "%s" % (instance.pk,)
        # get filename
        if instance.pk:
            filename = '{}.{}'.format(name, ext)
        else:
            # set filename as random string
            random_id = "rid_%s" % (uuid4().hex,)
            filename = '{}.{}'.format(name, ext)
            # return the whole path to the file
        return os.path.join(path, filename)

    return wrapper