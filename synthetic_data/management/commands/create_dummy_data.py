from django.core.management.base import BaseCommand
from arches.app.models import models
from arches.app.models.tile import Tile
import uuid


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("-ng", "--nodegroup")

    def handle(self, **options):
        dest = uuid.UUID(options["nodegroup"])
        self.create_dummy_tiles(dest)

    def create_dummy_tiles(self, dest):
        group_node = models.Node.objects.filter(nodegroup_id=dest).first()
        graphid = group_node.graph_id
        publication_id = group_node.graph.publication_id
        nodes = models.Node.objects.filter(nodegroup_id=dest).exclude(datatype='semantic').values('nodeid', 'datatype')
        resources = []
        tiles = []
        tile_model = Tile()
        for i in range(20000):
            resource = models.ResourceInstance(pk=uuid.uuid1(), graph_id=graphid, graph_publication_id=publication_id)
            new_tile = tile_model.get_blank_tile_from_nodegroup_id(dest)
            new_tile_instance = models.TileModel(
                pk=new_tile.pk,
                resourceinstance_id=str(resource.pk),
                data=new_tile.data,
                nodegroup_id=new_tile.nodegroup_id
            )
            for node in nodes:
                match node['datatype']:
                    case 'string':
                        new_tile_instance.data[str(node['nodeid'])] = {"en": {"value": "cat","direction": "ltr"}}
                    case 'boolean':
                        new_tile_instance.data[str(node['nodeid'])] = True if i % 2 else False

            tiles.append(new_tile_instance)
            resources.append(resource)
        print('data generated')
        models.ResourceInstance.objects.bulk_create(resources, batch_size=500)
        print('resources saved')
        models.TileModel.objects.bulk_create(tiles, batch_size=500)
        print('tiles saved')



