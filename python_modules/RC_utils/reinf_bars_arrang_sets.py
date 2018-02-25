# -*- coding: iso-8859-1 -*-
from __future__ import division

__author__= "Ana Ortega (AO_O) "
__copyright__= "Copyright 2018, AO_O"
__license__= "GPL"
__version__= "1.0"
__email__= "ana.ortega@xcengineering.xyz "

#Coefficient m
coefM={
    'HA-25':{'B-400':1.2,'B-500':1.5},
    'HA-30':{'B-400':1.0,'B-500':1.3},
    'HA-35':{'B-400':0.9,'B-500':1.2},
    'HA-40':{'B-400':0.8,'B-500':1.1},
    'HA-45':{'B-400':0.7,'B-500':1.0},
    'HA-50':{'B-400':0.7,'B-500':1.0}
}

#Coefficient beta
coefBeta={
    'straight':{'tens':1.0,'compr':1.0},
    'hook':{'tens':0.7,'compr':1.0},
    'welded':{'tens':0.7,'compr':0.7}
}

def anchor_length_EHE(concrType,steelType,fi,position,anchType,stressState='compr',ratAs=1.0,dynamEff='N'):
    '''Return anchorage length [mm] of passive reinforcements according to
    art. 69.5.1 of EHE-08.
    Depending on the position occupied by the bar in the member, the following 
    cases may be distinguished:
    - Position I: good bonding, in the case of reinforcements that, during the 
    concreting, form with the horizontal an angle between 45 and 90 degrees 
    or if they form an angle smaller than 45 degress, are situated in the lower
    half of the section or at a distance equal to or greater than 30 cm from 
    the upper facing of a concreted layer.
    - Position II: inadequate bonding, in the case of reinforcements that, 
    during the concreting, do not fall within any of the aforementioned 
    categories.
    - If dynamic effects may occur, the anchorage lengths will be increased by 
    10fi.
    
    :param concrType: type of concrete ('HA-25','HA-30','HA-35,'HA-40',
           'HA-45' or 'HA-50')
    :param steelType: type of reinforcement steel ('B-400' or 'B-500')
    :param fi: rebar diameter in mm
    :param position: position occupied by the bar in the member ('I' or 'II')
    :param anchType: anchorage type ('straight': straight elongation, 
    'hook': pin, hook and U hook, 'welded': welded transverse bar)
    :param stressState: state of stress ('tens': tension, 
           'compr':compression). Defaults to 'compr' 
    :param ratAs: ratio between the necessary reinforcement by calculation 
           and the actually existing reinforcement in the section from which 
           the reinforcement is anchored. Defaults to 1
    :param dynamEff: ='Y' if dynamic effects may occur, 'N' otherwise.
           Defaults to  'N'
    '''
    fyk=eval(steelType[-3:])
    m=coefM[concrType][steelType]
    if position=='I':
        lb=max(m*fi**2,fyk/20.*fi)
    elif position=='II':
        lb=max(1.4*m*fi**2,fyk/14.*fi)
    else:
        print "Not valid value of rebar position (must be 'I' or 'II')"
    beta=coefBeta[anchType][stressState]
    lbneta=lb*beta*ratAs
    if dynamEff.upper() in 'SIYES':
        lbneta=lbneta+10*fi
    if stressState[:2].lower() == 'co':
        fact=2/3.
    else:
        fact=1/3.
    l_anc=max(lbneta,10*fi,150,fact*lb)
    return l_anc

def bend_rad_hooks_EHE(fi):
    '''Minimum bending radius of hooks, pins and U hooks, according to art. 69.3.4 of EHE-08.

    :param fi: rebar diameter in mm
    '''
    r= 4*fi/2. if fi <20 else 7*fi/2.
    return r


def bend_rad_curved_bars_EHE(steelType,fi):
    '''Minimum bending radius of bent and other curved bars, according to art. 69.3.4 of EHE-08.

    :param steelType: type of reinforcement steel ('B-400' or 'B-500')
    :param fi: rebar diameter in mm
    '''
    if '400' in steelType:
        r=10*fi/2. if fi <= 25 else 12*fi/2.
    else: 
        r=12*fi/2. if fi <= 25 else 14*fi/2.
    return r




