import logging
from flask_restplus import Resource
from api.repositories.products_repo import get_sectors
from api.restplus import api
from api.cache import cache

log = logging.getLogger(__name__)

ns = api.namespace('products/sectors', description='Operations related to Product sectors')


@ns.route('/')
class SectorCollection(Resource):
    def get(self):
        """
        Returns a list of available price sectors.
        """
        rv = cache.get('sectorsList')
        if rv is None:
            rv = get_sectors()
            cache.set('sectorsList', rv, timeout=5 * 60)
        return rv, 200
