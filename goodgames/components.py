
import os

from django.core.files.storage import FileSystemStorage

from mySite import settings


class OverwriteStorage(FileSystemStorage):

    def get_available_name(self, name, max_length=500):
        # If the filename already exists, remove it as if it was a true file system
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name


def path_and_rename(path):
    def wrapper(instance, filename):

        ext = filename.split('.')[-1]
        name = "%s" % (instance.short_name,)

        # get filename
        if instance.pk:
            filename = '{}.{}'.format(name, ext)
        else:
            # set filename as random string
            # random_id = "rid_%s" % (uuid4().hex,)
            filename = '{}.{}'.format(name, ext)
            # return the whole path to the file

        return os.path.join(path, filename)

    return wrapper
    # return ''


def path_and_rename_match(path):
    def wrapper(instance, filename):

        ext = filename.split('.')[-1]
        name = "%s" % (instance.pk,)
        # get filename
        if instance.pk:
            filename = '{}.{}'.format(name, ext)
        else:
            # set filename as random string
            # random_id = "rid_%s" % (uuid4().hex,)
            filename = '{}.{}'.format(name, ext)
            # return the whole path to the file

        return os.path.join(path, filename)

    return wrapper
    # return ''