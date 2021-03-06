import izi
from sqlalchemy.orm.session import Session

from demo.context import SqlalchemyContext


@izi.directive()
class SqlalchemySession(Session):

    def __new__(cls, *args, context: SqlalchemyContext=None, **kwargs):
        return context.db
