import arcpy
import pandas as pd
from os.path import realpath, split, join

shape_csv = "p:\Corporate\Tools\Software\Corporate\CoreLayers\shape.csv"
grid_csv = "p:\Corporate\Tools\Software\Corporate\CoreLayers\grid.csv"
image_csv = "p:\Corporate\Tools\Software\Corporate\CoreLayers\image.csv"


class OehLayersTool(object):

    def __init__(self):

        self.label = "Add OEH Layers"
        self.description = "Add corporate layers to the map"
        self.canRunInBackground = False

        self.df = pd.read_csv(join(split(realpath(__file__))[0], "shape2.csv"))
        self.unique_category = list(self.df["Category"].unique())
        self.layer_dict = {k.strip(): v.strip() for k, v in zip(self.df["Title"], self.df["Datasource"])}

        return

    def getParameterInfo(self):

        params = []

        for u in self.unique_category:

            df = self.df[(self.df["Category"] == u)]

            choices = list(df["Title"].unique())

            v = u.replace(" ", "_")

            param = arcpy.Parameter(
                displayName="{} Layers".format(v),
                name="layers_{}".format(v),
                datatype="GPString",
                parameterType="Optional",
                direction="Input",
                multiValue=True,
                category=u)

            param.filter.list = choices
            params.append(param)

        return params

    def isLicensed(self):

        return True

    def updateParameters(self, parameters):

        return

    def updateMessages(self, parameters):

        return

    def execute(self, parameters, messages):

        df = arcpy.mapping.ListDataFrames(arcpy.mapping.MapDocument("CURRENT"), "*")[0]

        lyrs = []

        for p in parameters:
            try:
                v = [v.strip().strip("'") for v in p.ValueAsText.split(";")]
            except AttributeError:
                continue

            lyrs.extend(v)

        if lyrs:
            messages.AddMessage("Adding layers...")

            for lyr in lyrs:

                ds = self.layer_dict[lyr]

                messages.AddMessage("... adding '{}' from '{}'".format(lyr, ds))

                addlayer = arcpy.mapping.Layer(ds)

                addlayer.visible = False

                arcpy.mapping.AddLayer(df, addlayer, "BOTTOM")

        else:
            messages.AddMessage("No layers selected")

        return


class Toolbox(object):

    def __init__(self):

        self.label = "OEH Layers"
        self.alias = "oeh_layers"
        self.tools = [OehLayersTool]

        return

