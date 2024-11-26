from arrow import Arrow
from ..exceptions import ImproperlyConfigured
from .enriched_datetime import ArrowDateTime
from .enriched_datetime.enriched_datetime_type import EnrichedDateTimeType

arrow = None
try:
    import arrow
except ImportError:
    pass


class ArrowType(EnrichedDateTimeType):
    """
    ArrowType provides way of saving Arrow_ objects into database. It
    automatically changes Arrow_ objects to datetime objects on the way in and
    datetime objects back to Arrow_ objects on the way out (when querying
    database). ArrowType needs Arrow_ library installed.

    .. _Arrow: https://github.com/arrow-py/arrow

    ::

        from datetime import datetime
        from sqlalchemy_utils import ArrowType
        import arrow


        class Article(Base):
            __tablename__ = 'article'
            id = sa.Column(sa.Integer, primary_key=True)
            name = sa.Column(sa.Unicode(255))
            created_at = sa.Column(ArrowType)



        article = Article(created_at=arrow.utcnow())


    As you may expect all the arrow goodies come available:

    ::


        article.created_at = article.created_at.replace(hours=-1)

        article.created_at.humanize()
        # 'an hour ago'

    """

    cache_ok = True

    def __init__(self, *args, **kwargs):
        if not arrow:
            raise ImproperlyConfigured("'arrow' package is required to use 'ArrowType'")

        super().__init__(datetime_processor=ArrowDateTime, *args, **kwargs)

        @property
        def python_type(self):
            return Arrow
