from django.db import models


class Author(models.Model):
    """
        This class represents an Author. \n
        Attributes:
        -----------
        param name: Describes name of the author
        type name: str max_length=20
        param surname: Describes last name of the author
        type surname: str max_length=20
        param patronymic: Describes middle name of the author
        type patronymic: str max_length=20

    """
    name = models.CharField(max_length=20, default=None, null=True, blank=True)
    surname = models.CharField(max_length=20, default=None, null=True, blank=True)
    patronymic = models.CharField(max_length=20, default=None, null=True, blank=True)

    def __str__(self):
        """
        Magic method is redefined to show all information about Author.
        :return: author id, author name, author surname, author patronymic
        """
        return f"'id': {self.id}, 'name': '{self.name}', 'surname': '{self.surname}', 'patronymic': '{self.patronymic}'"

    def __repr__(self):
        """
        This magic method is redefined to show class and id of Author object.
        :return: class, id
        """
        return f"Author(id={self.id})"

    @staticmethod
    def get_by_id(author_id):
        """
        :param author_id: SERIAL: the id of a Author to be found in the DB
        :return: author object or None if a user with such ID does not exist
        """
        try:
            return Author.objects.get(id=author_id)
        except Author.DoesNotExist:
            return None

    @staticmethod
    def delete_by_id(author_id):
        """
        :param author_id: an id of a author to be deleted
        :type author_id: int
        :return: True if object existed in the db and was removed or False if it didn't exist
        """
        try:
            author = Author.objects.get(id=author_id)
            author.delete()
            return True
        except Author.DoesNotExist:
            return False
        
    @staticmethod
    def create(name, surname, patronymic):
        """
        param name: Describes name of the author
        type name: str max_length=20
        param surname: Describes surname of the author
        type surname: str max_length=20
        param patronymic: Describes patronymic of the author
        type patronymic: str max_length=20
        :return: a new author object which is also written into the DB
        """
        if name and len(name) > 20:
            return None
        if surname and len(surname) > 20:
            return None
        if patronymic and len(patronymic) > 20:
            return None

        author = Author(
            name=name,
            surname=surname,
            patronymic=patronymic
        )
        author.save()
        return author

    def to_dict(self):
        """
        :return: author id, author name, author surname, author patronymic
        :Example:
        | {
        |   'id': 8,
        |   'name': 'fn',
        |   'surname': 'mn',
        |   'patronymic': 'ln',
        | }
        """
        return {
            'id': self.id,
            'name': self.name,
            'surname': self.surname,
            'patronymic': self.patronymic,
        }

    def update(self,
               name=None,
               surname=None,
               patronymic=None):
        """
        Updates author in the database with the specified parameters.
        param name: Describes name of the author
        type name: str max_length=20
        param surname: Describes surname of the author
        type surname: str max_length=20
        param patronymic: Describes patronymic of the author
        type patronymic: str max_length=20
        :return: None
        """
        if name is not None:
            if len(name) > 20:
                return
            self.name = name
        if surname is not None:
            if len(surname) > 20:
                return
            self.surname = surname
        if patronymic is not None:
            if len(patronymic) > 20:
                return
            self.patronymic = patronymic

        self.save()

    @staticmethod
    def get_all():
        """
        returns data for json request with QuerySet of all authors
        """
        return Author.objects.all()
