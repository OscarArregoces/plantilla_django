from django.db.models import Manager


class UserManagers(Manager):
    def user_for_facultad(self, facultad):
        return self.filter(persons__program__faculty_id=facultad)
