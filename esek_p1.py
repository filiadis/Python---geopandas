# -*- coding: utf-8 -*-
"""
Created on Sat Oct 15 18:27:20 2022

@author: fil
"""
import geopandas as gpd

    
# Read shapefile

gdf = gpd.read_file("final/blocks.shp", encoding='ISO-8859-7')


gdf2 = gpd.GeoDataFrame()


#Column creation

gdf2['id'] = int()

gdf2['geometry'] = gdf['geometry']

gdf2['kaek'] = str()

gdf2['ot'] = gdf['ARITHMOS_O']

gdf2['fek'] = gdf['FEK']

gdf2['pol_en'] = str()

gdf2['pol_en_id'] = int()

gdf2['pol_tomeas'] = str()

gdf2['gen_use'] = str()

gdf2['sp_use'] = str()

gdf2['kx_kf_cat'] = int()

gdf2['kx_kf_sel'] = int()

gdf2['category'] = int()

gdf2['cat_date'] = str()

gdf2['cat_notes'] = str()

gdf2['enforce_cnt'] = int()

gdf2['apallotr'] = int()

gdf2['pop'] = int()

gdf2['necess_rate'] = int()

gdf2['necess_notes'] = str()

gdf2['ulop'] = int()

gdf2['dom_adom'] = int()

gdf2['kat_gps'] = int()

gdf2['krisi_mel'] = int()


#Shapefile export
gdf2.to_file("final/blocks_p1.shp", encoding='ISO-8859-7')
    










