from django_elasticsearch_dsl import Document, Index, fields
from django_elasticsearch_dsl.registries import registry
from .models import Post

posts_index = Index('posts')


@registry.register_document
class PostDocument(Document):
    title = fields.TextField()
    description = fields.TextField()
    content = fields.TextField()

    class Index:
        name = 'posts'
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 0
        }

    class Django:
        model = Post

