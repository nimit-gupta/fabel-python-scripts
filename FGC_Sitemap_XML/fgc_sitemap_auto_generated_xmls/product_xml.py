#!/usr/bin/env python39 python310
#coding:utf-8

from IPython.core.display import display
import pandas as pd
import contactlenses_xml
import eyecare_xml
import glasses_xml
import solutions_xml 
import sunglasses_xml 

def read_scripts():

    df_contact_lenses = contactlenses_xml.beautiful_soup()

    df_eye_care = eyecare_xml.beautiful_soup()

    df_glasses = glasses_xml.beautiful_soup()

    df_solutions = solutions_xml.beautiful_soup()

    df_sunglasses = sunglasses_xml.beautiful_soup()

    df_product = pd.concat([df_contact_lenses,df_eye_care,df_glasses,df_solutions,df_sunglasses], axis = 0)

    return df_product


