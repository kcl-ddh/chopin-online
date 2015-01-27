class ChopinOnlineRouter(object):
    """
    A router to control all database operations on models in the project.
    """

    def db_for_read(self, model, **hints):
        """
        Attempts to read ocve models go to ocve_db.
        """
        if model._meta.app_label == 'ocve':
            return 'ocve_db'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write ocve models go to ocve_db.
        """
        if model._meta.app_label == 'ocve':
            return 'ocve_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the ocve app is involved.
        """
        if obj1._meta.app_label == 'ocve' or \
           obj2._meta.app_label == 'ocve':
           return True
        return None

    def allow_migrate(self, db, model):
        """
        Make sure the ocve app only appears in the 'ocve_db'
        database.
        """
        if db == 'ocve_db':
            return model._meta.app_label == 'ocve'
        elif model._meta.app_label == 'ocve':
            return False
        return None
