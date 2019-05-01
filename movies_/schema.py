import graphene
from graphene_django.types import DjangoObjectType, ObjectType
from .models import Movie, Actor, Furkan
# Create a Graphql type for the actor model


class ActorType(DjangoObjectType):
    class Meta:
        model = Actor


# Create a Graphql type for the movie model
class MovieType(DjangoObjectType):
    class Meta:
        model = Movie


class FurkanType(DjangoObjectType):
    class Meta:
        model = Furkan


class Query(ObjectType):
    actor = graphene.Field(ActorType, id=graphene.Int())
    movie = graphene.Field(MovieType, id=graphene.Int())
    furkan = graphene.Field(FurkanType, id=graphene.Int())
    actors = graphene.List(ActorType)
    movies = graphene.List(MovieType)
    furkans = graphene.List(FurkanType)

    def resolve_furkan(self, info, **kwargs):
        id = kwargs.get("id")

        if id is not None:
            return Furkan.objects.get(pk=id)
        return None

    def resolve_furkans(self, info, **kwargs):
        return Furkan.objects.all()

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

    def resolve_actors(self, info, **kwargs):
        return Actor.objects.all()

    def resolve_movies(self, info, **kwargs):
        return Movie.objects.all()


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
    message = graphene.String()
    actor = graphene.Field(ActorType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        message = "Furkan yeni bir actor oluşturdu"
        actor_instance = Actor(name=input.name)
        actor_instance.save()
        return CreateActor(ok=ok, actor=actor_instance, message=message)


class UpdateActor(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = ActorInput(required=True)

    ok = graphene.Boolean()
    actor = graphene.Field(ActorType)

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        actor_instance = Actor.objects.get(pk=id)
        if actor_instance:
            ok = True
            actor_instance.name = input.name
            actor_instance.save()
            return UpdateActor(ok=ok, actor=actor_instance)
        return UpdateActor(ok=ok, actor=None)


# Create mutations for movies
class CreateMovie(graphene.Mutation):
    class Arguments:
        input = MovieInput(required=True)

    ok = graphene.Boolean()
    message = graphene.String()
    movie = graphene.Field(MovieType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        message = "Furkan yeni bir Movie oluşturdu"
        actors = []
        for actor_input in input.actors:
            actor = Actor.objects.get(pk=actor_input.id)
            if actor is None:
                return CreateMovie(ok=False, movie=None)
            actors.append(actor)
        movie_instance = Movie(title=input.title, year=input.year)
        movie_instance.save()
        movie_instance.actors.set(actors)
        return CreateMovie(ok=ok, movie=movie_instance, message=message)


class UpdateMovie(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = MovieInput(required=True)

    ok = graphene.Boolean()
    movie = graphene.Field(MovieType)

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        movie_instance = Movie.objects.get(pk=id)
        if movie_instance:
            ok = True
            actors = []
            for actor_input in input.actors:
                actor = Actor.objects.get(pk=actor_input.id)
                if actor is None:
                    return CreateMovie(ok=False, movie=None)
                actors.append(actor)
            movie_instance = Movie(title=input.title, year=input.year)
            movie_instance.save()
            movie_instance.actors.set(actors)
            return UpdateMovie(ok=ok, movie=movie_instance)
        return UpdateMovie(ok=ok, movie=None)


# mutation of the models
class Mutation(graphene.ObjectType):
    create_actor = CreateActor.Field()
    update_actor = UpdateActor.Field()
    create_movie = CreateMovie.Field()
    update_movie = UpdateMovie.Field()


# query of the models

schema = graphene.Schema(query=Query, mutation=Mutation)
