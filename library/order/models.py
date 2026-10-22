from django.db import models
from django.utils import timezone


def _current_time():
    return timezone.now()


class Order(models.Model):
    user = models.ForeignKey('authentication.CustomUser', on_delete=models.CASCADE, related_name='orders')
    book = models.ForeignKey('book.Book', on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(default=_current_time)
    plated_end_at = models.DateTimeField(default=_current_time)
    end_at = models.DateTimeField(default=None, null=True, blank=True)

    def __str__(self):
        end_at_val = f"'{self.end_at}'" if self.end_at else "None"
        return (f"'id': {self.id}, 'user': {repr(self.user)}, 'book': {repr(self.book)}, "
                f"'created_at': '{self.created_at}', 'end_at': {end_at_val}, 'plated_end_at': '{self.plated_end_at}'")

    def __repr__(self):
        """
        This magic method is redefined to show class and id of Order object.
        :return: class, id
        """
        return f'Order(id={self.id})'

    def to_dict(self):
        """
        :return: dict contains order id, book id, user id, order created_at, order end_at, order plated_end_at
        :Example:
        | {
        |   'id': 8,
        |   'book': 8,
        |   'user': 8',
        |   'created_at': 1509393504,
        |   'end_at': 1509393504,
        |   'plated_end_at': 1509402866,
        | }
        """
        return {
            'id': self.id,
            'book': self.book.id,
            'user': self.user.id,
            'created_at': self.created_at,
            'end_at': self.end_at,
            'plated_end_at': self.plated_end_at,
        }

    @staticmethod
    def create(user, book, plated_end_at):
        """
        :param user: the user who took the book
        :type user: CustomUser
        :param book: the book they took
        :type book: Book
        :param plated_end_at: planned return of data
        :type plated_end_at: int (timestamp)
        :return: a new order object which is also written into the DB
        """
        if user._state.adding or book._state.adding:
            return None
        if book.orders.filter(end_at__isnull=True).count() >= book.count:
            return None

        order = Order(
            user=user,
            book=book,
            plated_end_at=plated_end_at
        )
        order.save()
        return order

    @staticmethod
    def get_by_id(order_id):
        """
        :param order_id:
        :type order_id: int
        :return:  the object of the order, according to the specified id or null in case of its absence
        """
        try:
            return Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return None

    def update(self, plated_end_at=None, end_at=None):
        """
        Updates order in the database with the specified parameters.\n
        :param plated_end_at: new plated_end_at
        :type plated_end_at: int (timestamp)
        :param end_at: new end_at
        :type plated_end_at: int (timestamp)
        :return: None
        """
        if plated_end_at is not None:
            self.plated_end_at = plated_end_at
        if end_at is not None:
            self.end_at = end_at
        self.save()

    @staticmethod
    def get_all():
        """
        :return: all orders
        """
        return list(Order.objects.all())

    @staticmethod
    def get_not_returned_books():
        """
        :return:  all orders that do not have a return date (end_at)
        """
        return list(Order.objects.filter(end_at__isnull=True))

    @staticmethod
    def delete_by_id(order_id):
        """
        :param order_id: an id of a user to be deleted
        :type order_id: int
        :return: True if object existed in the db and was removed or False if it didn't exist
        """
        try:
            order = Order.objects.get(id=order_id)
            order.delete()
            return True
        except Order.DoesNotExist:
            return False    
