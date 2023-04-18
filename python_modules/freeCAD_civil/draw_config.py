import FreeCAD as App
import Draft
# These variables will be substitutted  by layers in   all  modules
colorRebars=(0.00,1.00,0.00) # green (color 3 Autocad)
colorSectBars= (1.00,0.00,0.00) # red (color 1 Autocad)
colorConcrete=(0.00,1.00,1.00) #cyan (color 4 Autocad)
colorRebarSketch=(0.50,0.50,0.00) # olive (color 54 Autocad)
colorRefLines=(1.00,1.00,0.00) # yellow (color 2 Autocad)
colorArrows=(1.00,0.00,1.00) #magenta (color 6 Autocad)
colorTextLeft=(0.00,0.00,1.00) #blue (color 5 Autocad)
colorTextCenter=(0.50,0.50,0.50) #gray (color 9 Autocad)
colorTextRight=(0.50,0.00,0.50) #purple (color 214 Autocad)
colorFrames=(0.00,0.00,0.00) # black (color 7 Autocad)
colorLinesTables=(1.00,0.50,0.50)# gray (color 11 Autocad)
colorHidden=(0.5058,0.00,0.00) # color 14 Autocad
colorAxis=(0.31,0.00,0.00) # color 12 AutoCad


class reinfConf(object):
    '''
    Generic parameteters to be used as default values for several 
    attributes of different rebar families.

    :ivar cover:   minimum cover
    :ivar texSize: generic text size to label rebar families in the 
          drawings. Defaults to 0.125
    :ivar Code: code on structural concrete that applies (defaults to 'EC2') 
    :ivar xcConcr: XC concrete material object (ex: EC2_materials.C25)
    :ivar xcSteel: XC steel material object (ex: EC2_materials.S500C)

    :ivar dynamEff: 'Y' 'yes' 'Yes' ... if dynamic effects may occur (defaults 
          to 'N') 
    :ivar decLengths: decimal positions to calculate and express lengths and
                      their derivated magnitudes, like weight  (defaults to 2).
    :ivar decSpacing: decimal positions to express the spacing (defaults to 2)
                      if spacing has more than decSpacing positions, the 
                      full number is written.
    :ivar sketchScale: scale of the sketch that represents the rebar in the text
                       relative to the text size (defaults to 5)
    :ivar factPosLabelSectReb: factor to locate labels of section-rebars (defaults to 2/3)
    :ivar factDispReflinSectReb: factor to locate reference lines of section-rebars (defaults to 1)
    '''
    def __init__(self,cover,xcConcr,xcSteel,texSize=0.125,Code='EC2',dynamEff='N',decLengths=2,decSpacing=2,sketchScale=5,factPosLabelSectReb=2/3,factDispReflinSectReb=1.0):
        self.cover=cover
        self.texSize=texSize
        self.xcConcr=xcConcr
        self.xcSteel=xcSteel
        self.dynamEff=dynamEff
        self.decLengths=decLengths
        self.decSpacing=decSpacing
        self.sketchScale=sketchScale
        self.factPosLabelSectReb=factPosLabelSectReb
        self.factDispReflinSectReb=factDispReflinSectReb
        if Code == 'EC2':
            from materials.ec2 import EC2_limit_state_checking as Lcalc # doesn't work if only imported here

            
class tableConf(object):
    '''Parameters to configure the geometry of tables

    :ivar wColumns:  list with the width of the columns
    :ivar hRows: rows height 
    :ivar hText: text height 
    '''
    def __init__(self,wColumns,hRows,hText):
        self.wColumns=wColumns
        self.hRows=hRows
        self.hText=hText

setoutCfg=tableConf(wColumns=[15,25,25,18],hRows=5,hText=2.5)

class scheduleConf(tableConf):
     '''  Parameters to configure the geometry of  a rebars schedule
   
    :ivar wColumns: width of the columns [identifier,sketch, diam. and spacing., 
                        Number of bars, length of each bar, total weight of the family]
                        (defaults to [10,28,20,10,12,12])
    :ivar hRows: rows height (defaults to 12)
    :ivar htText: text height (defaults to 2.5)
    :ivar hTextSketch: text height for the sketch (defaults to 2.0).
    '''
     def __init__(self,wColumns,hRows,hText,hTextSketch):
         super(scheduleConf,self).__init__(wColumns,hRows,hText)
         self.hTextSketch=hTextSketch

        
XC_scheduleCfg=scheduleConf(wColumns=[10,30,20,10,12,12],hRows=12,hText=2.5,hTextSketch=2.0)







# The following classes are written in order to substitute the colors' code
# by layers' code (for now, it has nor been achieved, see paramDesignBranch)
# Colors
red= (1.00,0.00,0.00) # red (color 1 Autocad)
yellow=(1.00,1.00,0.00) # yellow (color 2 Autocad)
green=(0.00,1.00,0.00) # green (color 3 Autocad)
magenta=(1.00,0.00,1.00) #magenta (color 6 Autocad)
cyan=(0.00,1.00,1.00) #cyan (color 4 Autocad)
blue=(0.00,0.00,1.00) #blue (color 5 Autocad)
gray=(0.50,0.50,0.50) #gray (color 9 Autocad)
purple=(0.50,0.00,0.50) #purple (color 214 Autocad)
olive=(0.50,0.50,0.00) # olive (color 54 Autocad)
black=(0.00,0.00,0.00) # black (color 7 Autocad)
gray=(1.00,0.50,0.50)# gray (color 11 Autocad)
color14=(0.5058,0.00,0.00) # color 14 Autocad
color12=(0.31,0.00,0.00) # color 12 AutoCad




class layerCfg(object):
    '''Config of layers and colors to be used in drawings
    :ivar lynameRebars: true-shape rebars' layer name
    :ivar colorRebars: true-shape rebars' color
    :ivar lynameSectBars: sectionned-rebars' layer name
    :ivar colorSectBars: sectionned-rebars' color
    :ivar lynameStirrups: stirrups layer name
    :ivar color Stirrups: stirrups color
    :ivar lynameRebarSketch: rebar-sketch's layer name
    :ivar colorRebarSketch: rebar-sketch's color
    :ivar lynameThinConcrete: concrete layer name (thin line)
    :ivar colorThinConcrete: concrete color (thin line)
    :ivar lynameThickConcrete: concrete layer name (thick line)
    :ivar colorThickConcrete: concrete color (thick line)
    :ivar lynameRefLines: reference lines layer name
    :ivar colorRefLines: reference lines color
    :ivar lynameArrows: arrows' layer name
    :ivar colorArrows: arrows' color
    :ivar lynameTextLeft: layer name for left justified text 
    :ivar colorTextLeft: color for left justified text 
    :ivar lynameTextCenter: layer name for center justified text 
    :ivar colorTextCenter: color for center justified text 
    :ivar lynameTextRight: layer name for right justified text 
    :ivar colorTextRight: color for right justified text
    :ivar lynameFrameLines: layer name for contour frames in tables
    :ivar colorFrameLines: color for contour frames in tables
    :ivar lynameGridLines: layer for grid lines in tables
    :ivar colorGridLines: color for grid lines in tables
    :ivar lynameHidden: hidden lines layer name
    :ivar colorHidden: hidden lines color
    :ivar lynameAxis: axis lines layer name
    :ivar colorAxis: axis lines color
    '''
    def __init__(self,lynameRebars='armadura',
                 colorRebars=cyan,
                 lynameSectBars='armadura_sect',
                 colorSectBars=yellow,
                 lynameStirrups='cercos',
                 colorStirrups=yellow,
                 lynameRebarSketch='armadura_croquis',
                 colorRebarSketch=green,
                 lynameThinConcrete='hormigon_fino',
                 colorThinConcrete=yellow,
                 lynameThickConcrete='hormigon_grueso',
                 colorThickConcrete=cyan,
                 lynameRefLines='lin_ref',
                 colorRefLines=red,
                 lynameArrows='simbolos',
                 colorArrows=red,
                 lynameTextLeft='textoL',
                 colorTextLeft=black,
                 lynameTextCenter='textoC',
                 colorTextCenter=black,
                 lynameTextRight='textoR',
                 colorTextRight=black,
                 lynameFrameLines='recuadro',
                 colorFrameLines=cyan,
                 lynameGridLines='lin_grid',
                 colorGridLines=red,
                 lynameHidden='oculto',
                 colorHidden=red,
                 lynameAxis='ejes',
                 colorAxis=red):
        self.lynameRebars=lynameRebars
        self.colorRebars=colorRebars
        self.lynameSectBars=lynameSectBars
        self.colorSectBars=colorSectBars
        self.lynameStirrups=lynameStirrups
        self.colorStirrups=colorStirrups
        self.lynameRebarSketch=lynameRebarSketch
        self.colorRebarSketch=colorRebarSketch
        self.lynameThinConcrete=lynameThinConcrete
        self.colorThinConcrete=colorThinConcrete
        self.lynameThickConcrete=lynameThickConcrete
        self.colorThickConcrete=colorThickConcrete
        self.lynameRefLines=lynameRefLines
        self.colorRefLines=colorRefLines
        self.lynameArrows=lynameArrows
        self.colorArrows=colorArrows
        self.lynameTextLeft=lynameTextLeft
        self.colorTextLeft=colorTextLeft
        self.lynameTextCenter=lynameTextCenter
        self.colorTextCenter=colorTextCenter
        self.lynameTextRight=lynameTextRight
        self.colorTextRight=colorTextRight
        self.lynameFrameLines=lynameFrameLines
        self.colorFrameLines=colorFrameLines
        self.lynameGridLines=lynameGridLines
        self.colorGridLines=colorGridLines
        self.lynameHidden=lynameHidden
        self.colorHidden=colorHidden
        self.lynameAxis=lynameAxis
        self.colorAxis=colorAxis        

    def createReinfLayers(self):
        '''Create layers for reinforcement elements
        '''
        try:
            getattr(self,'layerRebars')
        except AttributeError:
            self.layerRebars=Draft.make_layer(name=self.lynameRebars,line_color=self.colorRebars,draw_style='Solid')
            self.layerRebars.Group=list()
        try:
            getattr(self,'layerSectBars')
        except AttributeError:
            self.layerSectBars=Draft.make_layer(name=self.lynameSectBars,line_color=self.colorSectBars,draw_style='Solid')
            self.layerSectBars.Group=list()
        try:
            getattr(self,'layerStirrups')
        except AttributeError:
            self.layerStirrups=Draft.make_layer(name=self.lynameStirrups,line_color=self.colorStirrups,draw_style='Solid')
            self.layerStirrups.Group=list()
        try:
            getattr(self,'layerRebarSketch')
        except AttributeError:
            self.layerRebarSketch=Draft.make_layer(name=self.lynameRebarSketch,line_color=self.colorRebarSketch,draw_style='Solid')
            self.layerRebarSketch.Group=list()
        try:
            getattr(self,'layerRefLines')
        except AttributeError:
            self.layerRefLines=Draft.make_layer(name=self.lynameRefLines,line_color=self.colorRefLines,draw_style='Solid')
            self.layerRefLines.Group=list()
        try:
            getattr(self,'layerArrows')
        except AttributeError:
            self.layerArrows=Draft.make_layer(name=self.lynameArrows,line_color=self.colorArrows,draw_style='Solid')
            self.layerArrows.Group=list()
        try:
            getattr(self,'layerTextLeft')
        except AttributeError:
            self.layerTextLeft=Draft.make_layer(name=self.lynameTextLeft,line_color=self.colorTextLeft,draw_style='Solid')
            self.layerTextLeft.Group=list()
        try:
            getattr(self,'layerTextRight')
        except AttributeError:
            self.layerTextRight=Draft.make_layer(name=self.lynameTextRight,line_color=self.colorTextRight,draw_style='Solid')
            self.layerTextRight.Group=list()

    def createBarScheduleLayers(self):
        try:
            getattr(self,'layerTextCenter')
        except AttributeError:
            self.layerTextCenter=Draft.make_layer(name=self.lynameTextCenter,line_color=self.colorTextCenter,draw_style='Solid')
            self.layerTextCenter.Group=list()
        try:
            getattr(self,'layerFrameLines')
        except AttributeError:
            self.layerFrameLines=Draft.make_layer(name=self.lynameFrameLines,line_color=self.colorFrameLines,draw_style='Solid')
            self.layerFrameLines.Group=list()
        try:
            getattr(self,'layerGridLines')
        except AttributeError:
            self.layerGridLines=Draft.make_layer(name=self.lynameGridLines,line_color=self.colorGridLines,draw_style='Solid')
            self.layerGridLines.Group=list()
        try:
            getattr(self,'layerTextLeft')
        except AttributeError:
            self.layerTextLeft=Draft.make_layer(name=self.lynameTextLeft,line_color=self.colorTextLeft,draw_style='Solid')
            self.layerTextLeft.Group=list()
        try:
            getattr(self,'layerTextRight')
        except AttributeError:
            self.layerTextRight=Draft.make_layer(name=self.lynameTextRight,line_color=self.colorTextRight,draw_style='Solid')
        try:
            getattr(self,'layerRebarSketch')
        except AttributeError:
            self.layerRebarSketch=Draft.make_layer(name=self.lynameRebarSketch,line_color=self.colorRebarSketch,draw_style='Solid')
            self.layerRebarSketch.Group=list()
          
    def createConcreteLayers(self):
        try:
            getattr(self,'layerThinConcrete')
        except AttributeError:
            self.layerThinConcrete=Draft.make_layer(name=self.lynameThinConcrete,line_color=self.colorThinConcrete,draw_style='Solid')
            self.layerThinConcrete.Group=list()
        try:
            getattr(self,'layerThickConcrete')
        except AttributeError:
            self.layerThickConcrete=Draft.make_layer(name=self.lynameThickConcrete,line_color=self.colorThickConcrete,draw_style='Solid')
            self.layerThickConcrete.Group=list()


XC_layerCfg=layerCfg()
       
    




