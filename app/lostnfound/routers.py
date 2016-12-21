#Radhika Mattoo, rm3485@nyu.edu
#Routers for MySQL sharding
import random
from models import Item
from django.contrib.auth.models import User
NUM_LOGICAL_SHARDS = 16
NUM_PHYSICAL_SHARDS = 2

LOGICAL_TO_PHYSICAL = (
  'db1', 'default', 'db1', 'default', 'db1', 'default', 'db1', 'default',
  'db1', 'default', 'db1', 'default', 'db1', 'default', 'db1', 'default',
)

def logical_to_physical(logical):
    if logical >= NUM_LOGICAL_SHARDS or logical < 0:
        raise Exception("shard out of bounds " + str(logical))
    print "Performing action on database: " + LOGICAL_TO_PHYSICAL[logical]
    return LOGICAL_TO_PHYSICAL[logical]

def logical_shard_for_user(user_id):
    print "User id is: " + str(user_id) + " and maps to shard: " + str(user_id % NUM_LOGICAL_SHARDS)
    return user_id % NUM_LOGICAL_SHARDS

class UserRouter(object):
    def _database_of(self, user_id):
        return logical_to_physical(logical_shard_for_user(user_id))

    def _db_for_read_write(self, model, **hints):
        print(model._meta.app_label)
        if model._meta.app_label == 'auth':
          return 'auth_db'
        # For now, sessions are stored on the auth sub-system, too.
        if model._meta.app_label == 'sessions':
          return 'auth_db'

        db = None
        if model._meta.app_label == 'lostnfound':
            try: #Item
                instance = hints['instance']
                db = self._database_of(instance.owner)
            except AttributeError: #User
                db = self._database_of(instance.id)
            except KeyError: #Yikes, no instance in hints. Check the owner!
                try:
                    db = self._database_of(int(hints['owner']))
                except KeyError:
                    print "No instance in hints"
        return db

    def db_for_read(self, model, **hints):
        return self._db_for_read_write(model, **hints)

    def db_for_write(self, model, **hints):

        return self._db_for_read_write(model, **hints)

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model=None, **hints):
        return True
