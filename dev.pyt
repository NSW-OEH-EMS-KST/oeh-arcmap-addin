import arcpy
import pandas as pd
from os.path import realpath, split, join

# SHAPE_CSV = "p:\Corporate\Tools\Software\Corporate\CoreLayers\shape.csv"
# IMAGE_CSV = "p:\Corporate\Tools\Software\Corporate\CoreLayers\grid.csv"
# GRID_CSV = "p:\Corporate\Tools\Software\Corporate\CoreLayers\image.csv"
SHAPE_CSV = join(split(realpath(__file__))[0], "shape.csv")
IMAGE_CSV = join(split(realpath(__file__))[0], "image.csv")
GRID_CSV = join(split(realpath(__file__))[0], "grid.csv")


def layer_specs_from_csv(csv):

    try:
        df = pd.read_csv(csv)
    except Exception as e:
        return [("Error", "Error", e.message, "Error")]

    df["Display"] = df["Category"] + " - " + df["Title"]

    layer_specs = zip(df["Category"], df["Title"], df["Datasource"], df["Display"])

    del df

    return layer_specs


class OehLayersTool(object):

    def __init__(self):

        self.label = "Add OEH Layers"
        self.description = "Add corporate layers to the map"
        self.canRunInBackground = True

        self.layers_by_category = [("Shape", layer_specs_from_csv(SHAPE_CSV)),
                                   ("Image", layer_specs_from_csv(IMAGE_CSV)),
                                   ("Grid", layer_specs_from_csv(GRID_CSV))]

        self.layer_dict = {}

        for cat, layers in self.layers_by_category:
            for _, __, source, display in layers:
                self.layer_dict[display] = source

    def getParameterInfo(self):

        param = arcpy.Parameter(
            displayName="Target Dataframe",
            name="target_dataframe",
            datatype="GPString",
            parameterType="Required",
            direction="Input",
            multiValue=False)

        param.filter.list = [f.name for f in arcpy.mapping.ListDataFrames(arcpy.mapping.MapDocument("CURRENT"))]
        param.value = param.filter.list[0]

        params = [param]

        for category, layer_specs in self.layers_by_category:
            param = arcpy.Parameter(
                displayName="{} Layers".format(category),
                name="layers_{}".format(category),
                datatype="GPString",
                parameterType="Optional",
                direction="Input",
                multiValue=True,
                category=category)

            param.filter.list = [display_name for _, __, ___, display_name in layer_specs]

            params.append(param)

        return params

    def isLicensed(self):

        return True

    def updateParameters(self, parameters):

        return

    def updateMessages(self, parameters):

        return

    def execute(self, parameters, messages):

        df = arcpy.mapping.ListDataFrames(arcpy.mapping.MapDocument("CURRENT"), parameters[0].valueAsText)[0]
        df_name = df.name

        lyrs = []

        for p in parameters[1:]:

            try:
                v = [v.strip().strip("'") for v in p.ValueAsText.split(";")]

            except AttributeError:
                continue

            lyrs.extend(v)

        if lyrs:
            messages.AddMessage("Adding layers...")

            for lyr in lyrs:
                src = self.layer_dict[lyr]

                messages.AddMessage("... adding layer '{}' from '{}' to dataframe '{}'".format(lyr, src, df_name))
                try:
                    layer = arcpy.mapping.Layer(src)
                    layer.visible = False
                    arcpy.mapping.AddLayer(df, layer, "BOTTOM")

                except Exception as e:
                    messages.AddErrorMessage(e.message)

        else:
            messages.AddMessage("No layers selected")

        return


class Toolbox(object):
    def __init__(self):
        self.label = "OEH Layers"
        self.alias = "oeh_layers"
        self.tools = [OehLayersTool]

        return

# code to add to the addin ...
# def onClick(self):
#
#     pa.GPToolDialog(configure.Configuration().toolbox, "ConfigureTool")
#
#     return
