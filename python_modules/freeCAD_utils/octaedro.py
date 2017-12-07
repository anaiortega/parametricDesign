import FreeCAD, FreeCADGui, Part

class Octahedron:
      def __init__(self, obj):
         "Add some custom properties to our box feature"
         obj.addProperty("App::PropertyLength","Length","Octahedron","Length of the octahedron").Length=1.0
         obj.addProperty("App::PropertyLength","Width","Octahedron","Width of the octahedron").Width=1.0
         obj.addProperty("App::PropertyLength","Height","Octahedron", "Height of the octahedron").Height=1.0
         obj.addProperty("Part::PropertyPartShape","Shape","Octahedron", "Shape of the octahedron")
         obj.Proxy = self

      def execute(self, fp):
         # Define six vetices for the shape
         v1 = FreeCAD.Vector(0,0,0)
         v2 = FreeCAD.Vector(fp.Length,0,0)
         v3 = FreeCAD.Vector(0,fp.Width,0)
         v4 = FreeCAD.Vector(fp.Length,fp.Width,0)
         v5 = FreeCAD.Vector(fp.Length/2,fp.Width/2,fp.Height/2)
         v6 = FreeCAD.Vector(fp.Length/2,fp.Width/2,-fp.Height/2)
         
         # Make the wires/faces
         f1 = self.make_face(v1,v2,v5)
         f2 = self.make_face(v2,v4,v5)
         f3 = self.make_face(v4,v3,v5)
         f4 = self.make_face(v3,v1,v5)
         f5 = self.make_face(v2,v1,v6)
         f6 = self.make_face(v4,v2,v6)
         f7 = self.make_face(v3,v4,v6)
         f8 = self.make_face(v1,v3,v6)
         shell=Part.makeShell([f1,f2,f3,f4,f5,f6,f7,f8])
         solid=Part.makeSolid(shell)
         fp.Shape = solid

      # helper mehod to create the faces
      def make_face(self,v1,v2,v3):
         wire = Part.makePolygon([v1,v2,v3,v1])
         face = Part.Face(wire)
         return face

class ViewProviderOctahedron:
      def __init__(self, obj):
         "Set this object to the proxy object of the actual view provider"
         obj.addProperty("App::PropertyColor","Color","Octahedron","Color of the octahedron").Color=(1.0,0.0,0.0)
         obj.Proxy = self

      def attach(self, obj):
         "Setup the scene sub-graph of the view provider, this method is mandatory"
         self.shaded = coin.SoGroup()
         self.wireframe = coin.SoGroup()
         self.scale = coin.SoScale()
         self.color = coin.SoBaseColor()

         self.data=coin.SoCoordinate3()
         self.face=coin.SoIndexedLineSet()

         self.shaded.addChild(self.scale)
         self.shaded.addChild(self.color)
         self.shaded.addChild(self.data)
         self.shaded.addChild(self.face)
         obj.addDisplayMode(self.shaded,"Shaded");
         style=coin.SoDrawStyle()
         style.style = coin.SoDrawStyle.LINES
         self.wireframe.addChild(style)
         self.wireframe.addChild(self.scale)
         self.wireframe.addChild(self.color)
         self.wireframe.addChild(self.data)
         self.wireframe.addChild(self.face)
         obj.addDisplayMode(self.wireframe,"Wireframe");
         self.onChanged(obj,"Color")

      def updateData(self, fp, prop):
         "If a property of the handled feature has changed we have the chance to handle this here"
         # fp is the handled feature, prop is the name of the property that has changed
         if prop == "Shape":
            s = fp.getPropertyByName("Shape")
            self.data.point.setNum(6)
            cnt=0
            for i in s.Vertexes:
               self.data.point.set1Value(cnt,i.X,i.Y,i.Z)
               cnt=cnt+1
            
            self.face.coordIndex.set1Value(0,0)
            self.face.coordIndex.set1Value(1,1)
            self.face.coordIndex.set1Value(2,2)
            self.face.coordIndex.set1Value(3,-1)

            self.face.coordIndex.set1Value(4,1)
            self.face.coordIndex.set1Value(5,3)
            self.face.coordIndex.set1Value(6,2)
            self.face.coordIndex.set1Value(7,-1)

            self.face.coordIndex.set1Value(8,3)
            self.face.coordIndex.set1Value(9,4)
            self.face.coordIndex.set1Value(10,2)
            self.face.coordIndex.set1Value(11,-1)

            self.face.coordIndex.set1Value(12,4)
            self.face.coordIndex.set1Value(13,0)
            self.face.coordIndex.set1Value(14,2)
            self.face.coordIndex.set1Value(15,-1)

            self.face.coordIndex.set1Value(16,1)
            self.face.coordIndex.set1Value(17,0)
            self.face.coordIndex.set1Value(18,5)
            self.face.coordIndex.set1Value(19,-1)

            self.face.coordIndex.set1Value(20,3)
            self.face.coordIndex.set1Value(21,1)
            self.face.coordIndex.set1Value(22,5)
            self.face.coordIndex.set1Value(23,-1)

            self.face.coordIndex.set1Value(24,4)
            self.face.coordIndex.set1Value(25,3)
            self.face.coordIndex.set1Value(26,5)
            self.face.coordIndex.set1Value(27,-1)

            self.face.coordIndex.set1Value(28,0)
            self.face.coordIndex.set1Value(29,4)
            self.face.coordIndex.set1Value(30,5)
            self.face.coordIndex.set1Value(31,-1)

      def getDisplayModes(self,obj):
         "Return a list of display modes."
         modes=[]
         modes.append("Shaded")
         modes.append("Wireframe")
         return modes

      def getDefaultDisplayMode(self):
         "Return the name of the default display mode. It must be defined in getDisplayModes."
         return "Shaded"

      def setDisplayMode(self,mode):
         return mode

      def onChanged(self, vp, prop):
         "Here we can do something when a single property got changed"
         FreeCAD.Console.PrintMessage("Change property: " + str(prop) + "\n")
         if prop == "Color":
            c = vp.getPropertyByName("Color")
            self.color.rgb.setValue(c[0],c[1],c[2])

      def getIcon(self):
         return """
            /* XPM */
            static const char * ViewProviderBox_xpm[] = {
            "16 16 6 1",
            "    c None",
            ".   c #141010",
            "+   c #615BD2",
            "@   c #C39D55",
            "#   c #000000",
            "$   c #57C355",
            "        ........",
            "   ......++..+..",
            "   .@@@@.++..++.",
            "   .@@@@.++..++.",
            "   .@@  .++++++.",
            "  ..@@  .++..++.",
            "###@@@@ .++..++.",
            "##$.@@$#.++++++.",
            "#$#$.$$$........",
            "#$$#######      ",
            "#$$#$$$$$#      ",
            "#$$#$$$$$#      ",
            "#$$#$$$$$#      ",
            " #$#$$$$$#      ",
            "  ##$$$$$#      ",
            "   #######      "};
            """

      def __getstate__(self):
         return None

      def __setstate__(self,state):
         return None


FreeCAD.newDocument()
a=FreeCAD.ActiveDocument.addObject("App::FeaturePython","Octahedron")
Octahedron(a)
ViewProviderOctahedron(a.ViewObject)
