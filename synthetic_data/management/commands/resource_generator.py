from arches.app.models import models
import csv
from datetime import datetime
from django.contrib.gis.geos import GEOSGeometry
from django.core.management.base import BaseCommand
import json
from random import randrange, uniform
import uuid


class Command(BaseCommand):
    """
    Command for creating performance evaluation data

    """

    def add_arguments(self, parser):
  
        parser.add_argument(
            "-d",
            "--dest",
            action="store",
            dest="dest",
            default=""        
            )
        
        parser.add_argument(
            "-r",
            "--resources",
            action="store",
            dest="resources",
            default=""        
            )

    created = []


    def handle(self, *args, **options):
        self.minx, self.miny, self.maxx, self.maxy = self.get_project_bounds()
        self.write_file(options["dest"], int(options["resources"]))

    def get_project_bounds(self):
        settings_geom_node = "0e8ffbcf-4148-11e7-a95a-c4b301baab9f"
        settings_geom_nodegroup = "0e8fdef0-4148-11e7-8330-c4b301baab9f"
        project_bounds_tile = models.TileModel.objects.get(nodegroup_id=settings_geom_nodegroup)
        project_bounds = project_bounds_tile.data[settings_geom_node]
        bounds_geom = GEOSGeometry(json.dumps(project_bounds["features"][0]["geometry"]))
        return bounds_geom.extent
    
    def get_concept_values(self, valueid=True):

        sql = """select * from relations c join values v on c.conceptidto = v.conceptid 
                    where c.conceptidfrom = 'a4cfe974-0e0c-4c67-9854-c1bd0c625c09' 
                    and v.valuetype = 'prefLabel'"""

        if id:
            options = [c.valueid for c in models.Value.objects.raw(sql)]
        else:
            options = [c.value for c in models.Value.objects.raw(sql)]
        return options[randrange(len(options))]

    def get_domain_list_value(self):
        options = ["6f34cecb-c148-4b1a-a591-8eaf543811bb","c1d7434f-dc22-41ca-bb66-e1f8108271d9","f29d36a2-ee37-495e-afe5-b8a664ae835c"]
        # options = ['uno', 'dos', 'tres']
        # print(options)
        return options[randrange(len(options))]

    def get_date_value(self):
        return datetime.strftime(datetime.now(), "%Y-%m-%d")

    def get_resource_instance_list_value(self, resources=[]):
        if len(resources) > 1:
            result = json.dumps([{
                "resourceId": resources[randrange(len(resources))],
                "ontologyProperty": "",
                "resourceXresourceId": "",
                "inverseOntologyProperty": ""
                }])
        
        else:
            result = ""
        
        return result
    
    def get_geojson(self, minx=-122, maxx=-120, miny=32, maxy=39):
        x = uniform(self.minx, self.maxx) 
        y = uniform(self.miny, self.maxy)
        return f"GEOMETRYCOLLECTION (POINT ({x} {y}))"

    def get_edtf(self, min=1000, max=2024):
        range = [randrange(min, max), randrange(min, max)]
        range.sort()
        return f"{range[0]}/{range[1]}"

    def create_resource(self, resourceid, record):
        self.created.append(resourceid)
        return {
            "resource-instance": self.get_resource_instance_list_value(self.created),
            "url": '{"url": "https://en.wikipedia.org/wiki/The_Animals", "url_label": "wikipedia"}',
            "annotation": "",
            "edtf": self.get_edtf(),
            "node-value": "",
            "number": randrange(1, 999),
            "geojson": self.get_geojson(),
            "file-list": "",
            "concept-list": self.get_concept_values(valueid=True),
            "concept": self.get_concept_values(valueid=False),
            "date": self.get_date_value(),
            "string": f"Resource {record}",
            'domain': self.get_domain_list_value(),
            'domain-list': self.get_domain_list_value(),
            'resource-instance-list': self.get_resource_instance_list_value(self.created),
            'resourceid': resourceid,
        }
    
    def write_file(self, dest, resource_count):
        with open(dest, "w") as f:
            headers = ["number",
                "resource-instance",
                "url",
                "annotation",
                "edtf",
                "node-value",
                "geojson",
                "file-list",
                "concept-list",
                "concept",
                "date",
                "string",
                "resource-instance-list",
                "domain",
                "domain-list",
                "resourceid"
            ]

            csvwriter = csv.DictWriter(f, delimiter=",", fieldnames=headers)
            csvwriter.writeheader()
            for record in range(resource_count):
                resourceid = str(uuid.uuid4())
                csvwriter.writerow(self.create_resource(resourceid, record))

