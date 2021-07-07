import geopandas as gpd

from Level_zero_classes_main import LevelZeroClass

source1 = gpd.read_file(r"C:\Amol_Parande\9_Python_Project\level_Zero\1_MDS\1_Admin_Area\Lavel_Zero.gdb", layer='Source', driver='FileGDB')

edges = gpd.read_file(r"C:\Amol_Parande\9_Python_Project\level_Zero\1_MDS\1_Admin_Area\Lavel_Zero.gdb", layer='Edges', driver='FileGDB')


def test():
    levelzero = LevelZeroClass(source1, edges)

    result = levelzero.final_level_zero_logic()
    result.to_file(r"C:\Amol_Parande\8_MIS\New folder\mmmmcc.shp")
    return result

test()
