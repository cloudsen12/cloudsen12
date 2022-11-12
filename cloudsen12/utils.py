import datetime
import math

import pystac
import shapely.geometry

__description = """
    CloudSEN12 is a LARGE dataset (~1 TB) for cloud semantic understanding that
    consists of 49,400 image patches (IP) that are evenly spread throughout all
    continents except Antarctica. Each IP covers 5090 x 5090 meters and contains
    data from Sentinel-2 levels 1C and 2A, hand-crafted annotations of thick and
    thin clouds and cloud shadows, Sentinel-1 Synthetic Aperture Radar (SAR), 
    digital elevation model, surface water occurrence, land cover classes, and
    cloud mask results from six cutting-edge cloud detection algorithms.
"""


def create_collection():
    init_date = datetime.datetime(2018, 1, 1, tzinfo=datetime.timezone.utc)
    last_date = datetime.datetime(2020, 12, 31, tzinfo=datetime.timezone.utc)
    py_collection = Client(
        id="CloudSEN12",
        title="A Benchmark Dataset for Cloud Semantic Understanding",
        description=__description,
        license="CC-BY-4.0",
        providers=[
            pystac.Provider(
                name="EcoHidro",
                roles=["producer", "licensor"],
                url="https://vrip.unmsm.edu.pe/category/ecohidro/",
            )
        ],
        extent=pystac.Extent(
            spatial=pystac.SpatialExtent([[-180, -90, 180, 90]]),
            temporal=pystac.TemporalExtent([[init_date, last_date]]),
        ),
        keywords=[
            "cloud detection",
            "deep learning",
            "semantic segmentation",
            "Sentinel-2",
            "Sentinel-1",
        ],
    )
    return py_collection


def translate_op(operator):
    if operator == "eq":
        operator = "=="
    elif operator == "neq":
        operator = "!="
    elif operator == "gt":
        operator = ">"
    elif operator == "gte":
        operator = ">="
    elif operator == "lt":
        operator = "<"
    elif operator == "lte":
        operator = "<="
    else:
        raise ValueError("Operator not supported")
    return operator


def translate_query_simple(variable, q):
    # is a number?
    if isinstance(variable, (int, float)):
        if math.isnan(variable):
            return False

    operator, value = list(q.items())[0]
    operator = translate_op(operator)

    if isinstance(value, str):
        return eval(f"'{variable}' {operator} '{value}'")

    return eval(f"{variable} {operator} {value}")


def translate_query_list(variable, q):
    operator, value = list(q.items())[0]
    operator = translate_op(operator)

    for v in value:
        if eval(f"'{variable}' {operator} '{v}'"):
            return True
    return False


def translate_query_double(variable, q):
    if math.isnan(variable):
        return False
    # support for multiple operators
    operators = [translate_op(op) for op in q.keys()]
    ranges = [v for v in q.values()]

    conditions = []
    for operator, value in zip(operators, ranges):
        conditions.append(eval(f"{variable} {operator} {value}"))
    return conditions[0] and conditions[1]


def translate_query(item, query, join="and"):
    conditions = []
    for key, value in query.items():

        # check if the value have two keys
        if len(value) != 2:
            val = next(iter(value.values()))
            if isinstance(val, list):
                condition = translate_query_list(variable=item.properties[key], q=value)
                conditions.append(condition)
            else:
                condition = translate_query_simple(
                    variable=item.properties[key], q=value
                )
                conditions.append(condition)
        else:
            condition = translate_query_double(variable=item.properties[key], q=value)
            conditions.append(condition)

    if join == "and":
        # any true?
        return all(conditions)
    elif join == "or":
        # all true?
        return any(conditions)
    else:
        raise ValueError("join must be 'and' or 'or'")


class Client(pystac.Collection):
    def __init__(self, *args, **kwargs):
        super(Client, self).__init__(*args, **kwargs)

    def search(self, bbox=None, datetime=None, query=None):
        # Creat a cloudsen12 collection
        newcollection = self.clone()
        newcollection.clear_items()

        # Convert dict to shapely
        subset_container = list()
        for item in self.get_all_items():
            # filter according to datetime
            if datetime is not None:
                if not (
                    (item.datetime >= datetime[0]) and (item.datetime < datetime[1])
                ):
                    continue

            # filter according to query
            if query is not None:
                if not translate_query(item, query, join="and"):
                    continue

            # filter according to space
            if bbox is not None:
                # from dict to shapely
                sp_intersects = shapely.geometry.shape(bbox)

                # is the point inside the polygon?
                coordxy = list(item.properties["proj:centroid"].values())
                coordxy.reverse()
                item_point = shapely.geometry.Point(coordxy)

                if not item_point.intersects(sp_intersects):
                    continue

            subset_container.append(item)
        newcollection.add_items(subset_container)

        return newcollection
