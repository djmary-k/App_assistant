"""
These classes are required to perform editing of records in the address book.
"""
class ChangeType:
    """
    This class represents types of possible changes
    which can be performed for a record in the address book.
    """
    EDIT_NAME, EDIT_PHONE, EDIT_EMAIL, ADD_PHONE, ADD_EMAIL, REMOVE_PHONE, REMOVE_EMAIL, EDIT_BIRTHDAY, REMOVE_BIRTHDAY = range(9)


class Change:
    """
    This class stores information about a change
    which has to be performed for a record in the address book.
    """

    def __init__(self, changetype: ChangeType, name: str, **kwargs):
        self.name = name  # name of the contact for which the record has to be changed
        self.changetype = changetype  # type of the change which has to be performed
        self.kwargs = kwargs  # key word arguments needed to conduct the change (e.g. "new_name" if the name has to be edited)

    def get_name(self) -> str:
        """
        Returns the name of the contact which has to be changed.
        :return: name of the contact.
        """
        return self.name

    def get_changetype(self) -> ChangeType:
        """
        Returns the type of the change which has to be performed.
        :return: the type of the change.
        """
        return self.changetype

    def get_kwargs(self):
        """
        Returns all the arguments required to perform the change.
        :return: key word arguments for the change.
        """
        return self.kwargs
