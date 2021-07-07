import geopandas as gpd
from shapely import ops


class LevelZeroClass:

    def __init__(self, polygon, polyline):
        self.polygon = polygon
        self.polyline = polyline

    def polygon_to_polyline(self):
        """
        # Convert Polygons to line
        # line string to geodatafram
        # Make Noding on interesection
        # Sheplay Multiline to geodatafram
        # explode Multiline string
        # Line Merge

        :param polygon:
        :return:
        """
        source = self.polygon.boundary
        boundry_lineString = gpd.GeoDataFrame(crs="EPSG:4326", geometry=source)
        line = boundry_lineString.unary_union
        geom = [line]
        Multiline_string = gpd.GeoDataFrame(crs="EPSG:4326", geometry=geom)
        explode = Multiline_string.explode()
        multiLineGeom = ops.linemerge(explode.unary_union)
        gdf = gpd.GeoDataFrame(geometry=[line for line in multiLineGeom], crs='EPSG:4326')
        return gdf


    def source_polygon_intersecting_edges(self):
        dissolve = self.polygon_buffer_dissolve()
        intersection_edges = gpd.sjoin(self.polyline, dissolve, how="inner", op='intersects')
        return intersection_edges

    def polygon_buffer_dissolve(self, distance=50):
        """
        # Convert Polygons to line
        # Reproject GCS to PCS (Meter)
        # Buffer 5 Meter
        # Reproject Back to WGS 84
        # GeoSeries to GeoDataFrame
        # Dissolve Buffer
        :param :polygon
        :return:
        """
        source_boundary = self.polygon.boundary
        reproject_meter = source_boundary.to_crs(epsg=900913)
        buffer = reproject_meter.buffer(distance)
        reproject_WGS84 = buffer.to_crs(epsg=4326)
        buffer_GDF = gpd.GeoDataFrame(geometry=reproject_WGS84.geometry)
        dissolve_s = buffer_GDF.dissolve()
        return dissolve_s

    def polyline_buffer_dissolve(self ,distance=5):
        """
        # Convert Polygons to line
        # Buffer 5 Meter
        # Reproject Back to WGS 84
        # GeoSeries to GeoDataFrame
        # Dissolve Buffer

        :param :polyline
        :param : distance
        :return:
        """
        polyline= self.source_polygon_intersecting_edges()
        reproject_meter = polyline.to_crs(epsg=900913)
        buffer = reproject_meter.buffer(distance)
        reproject_WGS84 = buffer.to_crs(epsg=4326)
        buffer_GDF = gpd.GeoDataFrame(geometry=reproject_WGS84.geometry)
        dissolve_s = buffer_GDF.dissolve()
        return dissolve_s

    def line_merger(self):
        """
        # Sheplay Multiline to geodatafram
        # explode Multiline string
        # Line Merge
        :return:
        """
        line = self.polyline.unary_union
        geom = [line]
        Multiline_string = gpd.GeoDataFrame(crs="EPSG:4326", geometry=geom)
        explode = Multiline_string.explode()
        multiLineGeom = ops.linemerge(explode.unary_union)
        gdf = gpd.GeoDataFrame(geometry=[line for line in multiLineGeom], crs='EPSG:4326')
        return gdf

    def source_split_with_edgs(self):
        """
        # Add colume data type integer 1
        # Merge Line layers
        # Drop unwanted Index
        # Final Source Boundrys Lines
        # Drop new Index
        # Create Columne and assing Index Values
        :return:
        """
        source_line = self.polygon_to_polyline()
        source_line["POPS"]= 1
        intersection_edges = self.source_polygon_intersecting_edges()
        union_d = gpd.overlay(source_line, intersection_edges, how='union', keep_geom_type=True).explode()
        union_d.drop('index_right', axis=1, inplace=True)
        source_line = union_d.loc[union_d["POPS"] == 1]
        source_line.reset_index(drop=True, inplace=True)
        source_line['Uniqq'] = source_line.index
        return source_line

    def final_level_zero_logic(self):
        """
        # Spatil join get with in polyline
        # get the inverse means not with in the area
        :return:
        """
        source_split = self.source_split_with_edgs()
        edgs_5m_buffer = self.polyline_buffer_dissolve()
        gpd_sJoin = gpd.sjoin(source_split, edgs_5m_buffer , how='inner', op='within')
        result = source_split[~source_split['Uniqq'].isin(gpd_sJoin['Uniqq'].unique())]
        return result




