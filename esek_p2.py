#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 17:10:57 2022

@author: fil
"""

import math
import decimal
import pandas as pd
import geopandas as gpd
  
# Διαβάζεται το αρχειο shapefile
gdf = gpd.read_file("paradotea2/blocks_p1.shp", encoding='UTF-8')

# Δημιουργούνται τα κεντροειδή των πολυγώνων
gdf["x"] = gdf.centroid.x
gdf["y"] = gdf.centroid.y

# Υπολογίζεται η έκταση των πολυγώνων
gdf["pol_area"] = gdf.area


# Αντικαθίστανται οι κενές τιμές όπου χρειάζεται για τους υπολογισμούς
gdf["dom_adom"].fillna(0, inplace=True)

gdf["pop"].fillna(0, inplace=True)

gdf["kat_gps"].fillna(0, inplace=True)

gdf["kx_kf_cat"].fillna(0, inplace=True)


# Μετατρέπονται οι στήλες του DataFrame σε λίστες
uid = gdf["id"].to_list()

pop = gdf["pop"].to_list()

pol_en= gdf["pol_en"].to_list()

pol_en_id = gdf["pol_en_id"].to_list()

pol_area = gdf["pol_area"].to_list()

x = gdf["x"].to_list()

y = gdf["y"].to_list()

kx_kf_sel = gdf["kx_kf_sel"].to_list()

kx_kf_cat = gdf["kx_kf_cat"].to_list()

category = gdf["category"].to_list()

ulop = gdf["ulop"].to_list()

dom_adom = gdf["dom_adom"].to_list()

kat_gps = gdf["kat_gps"].to_list()

krisi_mel = gdf["krisi_mel"].to_list()

necess_rate = gdf["necess_rat"].to_list()


#Δημιουργείται λιστα με τις μοναδικές τιμές των Πολεοδομικών ενοτήτων
pol_len_id_un = list(set(pol_en_id))


# ------------------------------------------------#
# 1. Πληθυσμιακη πυκνότητα
# ------------------------------------------------#


def index_1_method(
    uid=uid,
    gdf=gdf,
    pol_en_id_un=pol_len_id_un,
    pol_en_id=pol_en_id,
    pol_area=pol_area,
    pop=pop):


    index_1 = ['NULL' for x in range(len(uid))]

    index_1_d = ['NULL' for x in range(len(uid))]

    # Iterate

    for it in pol_len_id_un:

        total_area = []

        total_pop_DE = 0

        i = 0

        while i < len(uid):

            if pol_en_id[i] == it:

                total_area.append(pol_area[i])
                
                if pop[i] > 0:

                    total_pop_DE = pop[i]
                    
                else:
                    
                    pass

            i += 1


        foo = round((total_pop_DE / ((sum(total_area) / 10_000) * 1.35)), 2)

        k = 0

        while k < len(uid):

            if pol_en_id[k] == it:

                index_1[k] = foo

            k += 1   
    

    #Δημιουργείται η αναγκαιότητα

    i = 0

    while i < len(index_1):

        if index_1[i] < 100:

            index_1_d[i] = 1

        elif (index_1[i] >= 100) and (index_1[i] < 400):

            index_1_d[i] = 3

        else:

            index_1_d[i] = 5

        i += 1

    gdf["index_1"] = index_1  # add list to dataframe

    gdf["index_1_d"] = index_1_d  # add list to dataframe


# ------------------------------------------------#
# 2. Χρήσεις γης ΚΧ-ΚΦ
# ------------------------------------------------#

def index_2_method(uid=uid,
                    gdf=gdf,
                    pol_en_id_un=pol_len_id_un,
                    pol_en_id=pol_en_id,
                    pol_area=pol_area,
                    pop=pop):


    index_2 = ['NULL' for x in range(len(uid))]
    
    index_2_d = ['NULL' for x in range(len(uid))]
        
    
    #Υπολογισμός των κατηγοριών 1 και 3
    
    def cat_1_3(use_cat, pol_en_id_un=pol_len_id_un, 
                kx_kf_cat=kx_kf_cat, ulop=ulop):
    
        for it in pol_len_id_un:
        
            total_area = []
        
            total_pop_DE = 0
        
            i = 0
        
            while i < len(uid):
            
                if (pol_en_id[i] == it) and (kx_kf_cat[i] == use_cat) and (ulop[i] == 1):

                    total_area.append(pol_area[i])
            
                    total_pop_DE = pop[i]
            
                i += 1
        
        
            if (sum(total_area) == 0) or (total_pop_DE == 0):
                    
                foo = 0
                    
            else:
            
                foo = round(sum(total_area) / total_pop_DE, 2)
                
        
                
            k = 0
            
            while k < len(uid):
            
                if (pol_en_id[k] == it) and (kx_kf_cat[k] == use_cat):
            
                    index_2[k] = foo
                    
                    if use_cat == 1:
                        
                        if foo < 100:
                            
                            index_2_d[k] = 1
                            
                        elif (foo >= 100) and (foo < 400):
                            
                            index_2_d[k] = 3
                            
                        else:
                            
                            index_2_d[k] = 5
                            
                    else:
                        
                        if foo < 5.5:
                            
                            index_2_d[k] = 4
                            
                        else:
                            
                            index_2_d[k] = 2               
                           
                k += 1
            
        
    #Υπολογισμός της κατηγορίας 2: Σχολικές μονάδες
    
    def education(cat, perc, thres, pol_en_id_un=pol_len_id_un, pol_area=pol_area, 
                  pop=pop, pol_en_id=pol_en_id,kx_kf_cat=kx_kf_cat, ulop=ulop,
                  index_2=index_2, index_2_d=index_2_d):
    
        for it in pol_len_id_un:
            
            total_area = []
        
            total_pop_DE = 0
        
            i = 0
        
            while i < len(uid):
            
                if (pol_en_id[i] == it) and (kx_kf_cat[i] == cat) and (ulop[i] == 1):
            
                    total_area.append(pol_area[i])
            
                    total_pop_DE = pop[i]
            
                i += 1
                
            users = perc * total_pop_DE
        
            k = 0
            
            while k < len(uid):
                
                if (krisi_mel[k] > 0):
                    
                    index_2[k] = krisi_mel[k]
                    
                    index_2_d[k] = krisi_mel[k]
            
                elif (pol_en_id[k] == it) and (kx_kf_cat[k] == cat):
            
                    if sum(total_area) == 0:
                        
                        index_2[k] = 0
                        
                        index_2_d[k] = 5
                        
                    else:
                        
                        foo = round(sum(total_area) / users, 2)
                        
                        index_2[k] = foo
                        
                        if foo < thres:
                            
                            index_2_d[k] = 4
                            
                        else:
                            
                            index_2_d[k] = 2
                            
                
    
            
                k += 1
                
    #Υπολογισμός για τις υπόλοιπες κατηγορίες
    
    def rest_categories(uid=uid, kx_kf_cat=kx_kf_cat,index_2=index_2, index_2_d=index_2_d):
        
        i = 0
        
        while i < len(uid):
        
            if (kx_kf_cat[i] > 3) and (kx_kf_cat[i] < 20) and (krisi_mel[i] > 0):
        
                index_2[i] = krisi_mel[i]
                
                index_2_d[i] = krisi_mel[i]
        
            i += 1
                
        
    cat_1_3(1)
    cat_1_3(3)
    
    education(21, 0.02, 15)
    education(22, 0.1, 8)
    education(23, 0.09, 8)
    
    rest_categories()
    
    #Προσθέτουμς τις λίστες στο DataFrame
    gdf["index_2"] = index_2 
    gdf["index_2_d"] = index_2_d 
    
# ------------------------------------------------#
# 3. Απόσταση ΚΧ-ΚΦ από άλλους υλοποιημένους ΚΧ-ΚΦ
# ------------------------------------------------#


def index_3_method(uid=uid, gdf=gdf, kx_kf_cat=kx_kf_cat, x=x, y=y):

    index_3_KX_KX = ['NULL' for x in range(len(uid))]
    
    index_3_KX_KF = ['NULL' for x in range(len(uid))]
    
    index_3_KF_KF = ['NULL' for x in range(len(uid))]
    
    index_3_KX_KX_d = ['NULL' for x in range(len(uid))]
    
    index_3_KX_KF_d = ['NULL' for x in range(len(uid))]
    
    index_3_KF_KF_d = ['NULL' for x in range(len(uid))]
    

    index_3_d = ['NULL' for x in range(len(uid))]
    
    
    #Υπολογισμός της ευκλίδειας απόστασης μεταξύ δύο σημείων
    
    def eucl_dist(x1, y1, x2, y2):

        return math.sqrt(((x2 - x1) ** 2) + ((y2 - y1) ** 2))
    

    #Καταχώριση όλων των ΚΧ-ΚΦ

    kx_id = []

    kx_coords = []

    kf_id = []

    kf_coords = []

    i = 0

    while i < len(uid):

        if kx_kf_cat[i] == 1:

            kx_id.append(uid[i])

            kx_coords.append([x[i], y[i]])

        elif kx_kf_cat[i] > 1:

            kf_id.append(uid[i])

            kf_coords.append([x[i], y[i]])

        i += 1

    #Καταχώριση όλων των υλοποιημένων ΚΧ-ΚΦ

    kx_id_u = []

    kx_coords_u = []

    kf_id_u = []

    kf_coords_u = []

    i = 0

    while i < len(uid):

        if (kx_kf_cat[i] == 1) and (ulop[i] == 1):

            kx_id_u.append(uid[i])

            kx_coords_u.append([x[i], y[i]])

        elif (kx_kf_cat[i] > 1) and (ulop[i] == 1):

            kf_id_u.append(uid[i])

            kf_coords_u.append([x[i], y[i]])

        i += 1

    #Υπολογισμός της ελάχιστης απόστασης από ΚΧ σε ΚΧ

    if len(kx_id) == 0:

        pass

    elif len(kx_id) == 1:

        uid_index = uid.index(kx_id[0])

        index_3_KX_KX[uid_index] = 0

    else:

        i = 0

        while i < len(kx_id):

            dis = []

            base_point = kx_coords[i]

            base_point_index = kx_id[i]

            k = 0

            while k < len(kx_id_u):

                if kx_id_u[k] == base_point_index:

                    pass

                else:

                    foo = eucl_dist(
                        base_point[0],
                        base_point[1],
                        kx_coords_u[k][0],
                        kx_coords_u[k][1],
                    )

                    dis.append(foo)

                k += 1

            uid_index = uid.index(base_point_index)

            index_3_KX_KX[uid_index] = round(min(dis), 2)

            i += 1
            
    #Υπολογισμός της ελάχιστης απόστασης από ΚΧ σε ΚΦ

    if len(kx_id) == 0:

        pass

    elif len(kx_id) == 1:

        uid_index = uid.index(kx_id[0])

        index_3_KX_KF[uid_index] = 0

    else:

        i = 0

        while i < len(kx_id):

            dis = []

            base_point = kx_coords[i]

            base_point_index = kx_id[i]

            k = 0

            while k < len(kf_id_u):

                if kf_id_u[k] == base_point_index:

                    pass

                else:

                    foo = eucl_dist(
                        base_point[0],
                        base_point[1],
                        kf_coords_u[k][0],
                        kf_coords_u[k][1],
                    )

                    dis.append(foo)

                k += 1

            uid_index = uid.index(base_point_index)

            index_3_KX_KF[uid_index] = round(min(dis), 2)

            i += 1

    #Υπολογισμός της ελάχιστης απόστασης από ΚΦ σε ΚΦ

    if len(kf_id) == 0:

        pass

    elif len(kf_id) == 1:

        uid_index = uid.index(kf_id[0])

        index_3_KF_KF[uid_index] = 0

    else:

        i = 0

        while i < len(kf_id):

            dis = []

            base_point = kf_coords[i]

            base_point_index = kf_id[i]

            k = 0

            while k < len(kf_id_u):

                if kf_id_u[k] == base_point_index:

                    pass

                else:

                    foo = eucl_dist(
                        base_point[0],
                        base_point[1],
                        kf_coords_u[k][0],
                        kf_coords_u[k][1],
                    )

                    dis.append(foo)

                k += 1

            uid_index = uid.index(base_point_index)

            index_3_KF_KF[uid_index] = round(min(dis), 2)

            i += 1

        #Δημιουργείται η αναγκαιότητα για ΚΧ - ΚΧ
        
        i = 0

        while i < len(index_3_KX_KX):

            if index_3_KX_KX[i] == "NULL":

                pass
            
            elif index_3_KX_KX[i] == 0:
                
                index_3_KX_KX_d[i] = 5

            else:

                if index_3_KX_KX[i] < 500:

                    index_3_KX_KX_d[i] = 1

                elif (index_3_KX_KX[i] >= 500) and (index_3_KX_KX[i] < 1500):

                    index_3_KX_KX_d[i] = 3

                else:

                    index_3_KX_KX_d[i] = 5

            i += 1
            
        #Δημιουργείται η αναγκαιότητα για ΚΧ - ΚΦ
        
        i = 0

        while i < len(index_3_KX_KF):

            if index_3_KX_KF[i] == "NULL":

                pass
            
            elif index_3_KX_KF[i] == 0:
                
                index_3_KX_KF_d[i] = 5

            else:

                if index_3_KX_KF[i] < 500:

                    index_3_KX_KF_d[i] = 5

                elif (index_3_KX_KF[i] >= 500) and (index_3_KX_KF[i] < 1500):

                    index_3_KX_KF_d[i] = 3

                else:

                    index_3_KX_KF_d[i] = 1

            i += 1
        
            
        #Δημιουργείται η αναγκαιότητα για ΚΦ - ΚΦ
        
        i = 0

        while i < len(index_3_KF_KF):

            if index_3_KF_KF[i] == "NULL":

                pass
            
            elif index_3_KF_KF[i] == 0:
                
                index_3_KF_KF_d[i] = 5

            else:

                if index_3_KF_KF[i] < 500:

                    index_3_KF_KF_d[i] = 1

                elif (index_3_KF_KF[i] >= 500) and (index_3_KF_KF[i] < 1500):

                    index_3_KF_KF_d[i] = 3

                else:

                    index_3_KF_KF_d[i] = 5

            i += 1
            
    #Υπολογίζεται η τελική αναγκαιότητα
    
    i = 0

    while i < len(index_3_d):

        if (index_3_KX_KX_d[i] == "NULL") and (index_3_KX_KF_d[i] == "NULL"):

            pass

        else:

            index_3_d[i] = math.ceil((index_3_KX_KX_d[i] + index_3_KX_KF_d[i]) / 2)
            
        if (index_3_KF_KF_d[i] == "NULL"):

            pass

        else:

            index_3_d[i] = index_3_KF_KF_d[i]

        i += 1
        
    
    gdf["index_3_KX_KX"] = index_3_KX_KX 
    
    gdf["index_3_KX_KX_d"] = index_3_KX_KX_d 
     
    gdf["index_3_KX_KF"] = index_3_KX_KF 
    
    gdf["index_3_KX_KF_d"] = index_3_KX_KF_d 

    gdf["index_3_KF_KF"] = index_3_KF_KF

    gdf["index_3_KF_KF_d"] = index_3_KF_KF_d
    
    gdf["index_3_d"] = index_3_d





# ------------------------------------------------#
# 4. Σημερινή κατάσταση (Δομημένο - Αδόμητο)
# ------------------------------------------------#


def index_4_method(uid=uid, dom_adom=dom_adom, kx_kf_sel=kx_kf_sel):

    index_4_d = ['NULL' for x in range(len(uid))]

    i = 0

    while i < len(index_4_d):

        if (dom_adom[i] == 0) and (kx_kf_sel[i] == 1):

            index_4_d[i] = 5

        elif (dom_adom[i] == 1) and (kx_kf_sel[i] == 1):

            index_4_d[i] = 1

        i += 1

    gdf["index_4_d"] = index_4_d  # add list to dataframe




# ------------------------------------------------#
# 5. Κατεύθυνση απο ΓΠΣ
# ------------------------------------------------#


def index_5_method(uid=uid, kat_gps=kat_gps, kx_kf_sel=kx_kf_sel):

    index_5_d = ['NULL' for x in range(len(uid))]


    i = 0

    while i < len(index_5_d):

        if (kat_gps[i] == 0) and (kx_kf_sel[i] == 1):

            index_5_d[i] = 1

        elif (kat_gps[i] == 1) and (kx_kf_sel[i] == 1):

            index_5_d[i] = 5

        i += 1

    gdf["index_5_d"] = index_5_d  # add list to dataframe


# Call funtions
index_1_method()

index_2_method()

index_3_method()

index_4_method()

index_5_method()

#Δημιουργία τελικής στήλης αναγκαιότητας

def final_calc(gdf=gdf, uid=uid):
    
    index_1_d = gdf["index_1_d"].to_list()
    
    index_2_d = gdf["index_2_d"].to_list()
    
    index_3_d = gdf["index_3_d"].to_list()
    
    index_4_d = gdf["index_4_d"].to_list()
    
    index_5_d = gdf["index_5_d"].to_list()
    

    i = 0
    
    while i<len(uid):
        
        total = []
        
        def calc(index, c):
        
            if type(index[c]) == int:
                
                if index[c] > 0:
                
                    total.append(index[c] * 0.2)
                
        calc(index_1_d, i)
        
        calc(index_2_d, i)
        
        calc(index_3_d, i)
        
        calc(index_4_d, i)
        
        calc(index_5_d, i)
    
        if (sum(total) % 2) > 0.5:
            
            necess_rate[i] = math.ceil(sum(total))
            
        else:
            
            necess_rate[i] = math.floor(sum(total))
            
        
        i+=1
    
    gdf.drop(columns = ["necess_rat"], inplace=True)
    
    gdf["necess_rate"] = necess_rate 


final_calc()



#Εξάγονται τα παραδοτέα αρχεία shapefiles


#All_blocks
all_blocks = gdf[['id', 'geometry', 'kaek', 'ot', 'pol_tomeas', 'pol_en', 'gen_use', 'sp_use', 'fek']].copy()

all_blocks.to_file("paradotea2/Β1.shp", encoding='UTF-8')



#all_kx_kf
all_kx_kf = gdf.loc[gdf['kx_kf_sel'] == 1].copy()

all_kx_kf = all_kx_kf[['id', 'geometry', 'kaek', 'ot', 'pol_tomeas', 'pol_en', 'gen_use', 'sp_use', 'fek']].copy()

all_kx_kf.to_file("paradotea2/Β_1_1_Εγκεκριμένου_Ρυμοτομικού_Σχεδίου.shp", encoding='UTF-8')


#arsi_apallotriosis
arsi_apallotriosis = gdf.loc[gdf['apallotr'] == 1].copy()

arsi_apallotriosis = arsi_apallotriosis[['id', 'geometry', 'kaek', 'ot','pol_en', 
                                         'pol_tomeas', 'gen_use', 'sp_use', 'cat_date', 'cat_notes', 
                                         'enforce_cn','necess_rate', 'necess_not']].copy()

arsi_apallotriosis.to_file("paradotea2/Β_1_2_Κοινόχρηστοι_και_Κοινωφελείς_Χώροι_που_δεν_έχουν_απαλλοτριωθεί.shp", encoding='UTF-8')




















