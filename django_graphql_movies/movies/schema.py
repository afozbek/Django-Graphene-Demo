import graphene
from graphene_django.types import DjangoObjectType, ObjectType
from django_graphql_movies.movies.models import Actor, Movie

# Create a Graphql type for the actor model
class ActorType(DjangoObjectType):
    class Meta:
        model = Actor


# Create a Graphql type for the movie model
class MovieType(DjangoObjectType):
    class Meta:
        model = Movie


# Create Input Object Types
class ActorInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()


class MovieInput(graphene.InputObjectType):
    id = graphene.ID()
    title = graphene.String()
    actors = graphene.List(ActorInput)
    year = graphene.Int()


# Create mutations for actorss
class CreateActor(graphene.Mutation):
    class Arguments:
        input = ActorInput(required=True)

    ok = graphene.Boolean()
    actor = graphene.Field(ActorType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        actor_instance = Actor(name=input.name)
        actor_instance.save()
        return CreateActor(ok=ok, actor=actor_instance)


class UpdateActor(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = ActorInput(required=True)

    ok = graphene.Boolean()
    actor = graphene.Field(ActorType)

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        actor_intance = Actor.objects.get(pk=id)
        if actor_intance:
            ok = True
            actor_intance.name = input.name
            actor_intance.save()
            return UpdateActor(ok=ok, actor=actor_intance)

        return UpdateActor(ok=ok, actor=None)


# query of the models
class Query(ObjectType):
    actor = graphene.Field(ActorType, id=graphene.Int())
    movie = graphene.Field(MovieType, id=graphene.Int())
    actors = graphene.List(ActorType)
    movies = graphene.List(MovieType)

    # add resolvers
    def resolve_actor(self, info, **kwargs):
        id = kwargs.get("id")

        if id is not None:
            return Actor.objects.get(pk=id)

        return None

    def resolve_movie(self, info, **kwargs):
        id = kwargs.get("id")

        if id is not None:
            return Movie.objects.get(pk=id)

        return None

    def resolve_movie(self, info, **kwargs):
        return Actor.objects.all()

        return None

    def resolve_movies(self, info, **kwargs):
        return Movie.objects.all()
