import logging
from app.extensions import get_mysql_connection

class BillService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    