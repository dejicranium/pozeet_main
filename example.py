VERBS = {
    "COMMENT": "commented on",
    "LIKE": "liked",
    "VOTE": "voted",
    "ADD": "added",

}

class BaseActivity:
    """Use this to verify whether an object is an activity"""
    pass

class Activity:
    """Class for creating an activity

        An activity is made up of an actor, object, verb and source.

        As its name implies, an 'actor' refers to the user or entity who
        triggered the activity.

        An 'object' is the entity on which an action by an actor is carred out
        The 'verb' is the name of the action carried out
        A 'source', as its name implies, signifies the source of the object

        For example::

        In "Deji Atoyebi commented on Iyabo Atoyebi's poll":

        Actor: Deji Atoyebi
        Verb: Commented on
        Object: Poll
        Source: A poll by Iyabo Atoyebi in the list of polls

        In this class, the ids of the actor and source, rather than the actual
        objects, are needed.

    """

    #the class in which we query to get our actor. Needs to be changed
    actor_class = None

    def __init__(self, actor_id, verb, object, source_id):
        self.actor_id = actor_id
        self.verb = verb if verb in VERBS.keys() else None
        self.object = object
        self.source_id = source_id

        def get_actor_id(self):
            return self.actor_id

        def get_actor(self, request):
            actor = self.get_entity_from_class(request, actor_class, actor_id)
            return actor



        def get_entity_from_class(self, request, clss, entity_id):
            entity = request.dbsession.query(clss).filter(clss.id==entity_id).first()
            return entity
