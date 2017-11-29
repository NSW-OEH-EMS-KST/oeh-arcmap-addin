import arcpy
import pandas as pd
from os.path import exists


LAYERS_CSV = None
LAYERS_CSV_1 = "P:\Region\Other\Tools\CoreLayers\layers.csv"
LAYERS_CSV_2 = "P:\Corporate\Tools\Software\Corporate\CoreLayers\layers.csv"


def layer_specs_from_csv(csv):

    try:
        df = pd.read_csv(csv)

        # df['Display'] = df[["Type", "Category", "Title"]].apply(lambda x: "{} | {} | {}".format(*x), axis=1)
        df['Display'] = df[["Category", "Title"]].apply(lambda x: "{} | {}".format(*x), axis=1)

        layer_specs = zip(df["Category"], df["Title"], df["Datasource"], df["Display"])

        del df
    except:
        layer_specs = [["CSV error", "CSV error", "CSV error", "CSV error", "CSV error"]]

    return layer_specs


class AddCoreLayersTool(object):

    def __init__(self):

        self.label = "Add Core Layers"
        self.description = "Add core layers to the map"
        self.canRunInBackground = False

        global LAYERS_CSV

        if not exists(LAYERS_CSV_1):
            if not exists(LAYERS_CSV_2):
                LAYERS_CSV = "Neither '{}' nor '{}' could be found on the system".format(LAYERS_CSV_1, LAYERS_CSV_2)
            else:
                LAYERS_CSV = LAYERS_CSV_2
        else:
            LAYERS_CSV = LAYERS_CSV_1

        self.layers = layer_specs_from_csv(LAYERS_CSV)
        self.layer_dict = {display: source for cat, ti, source, display in self.layers}

    def getParameterInfo(self):

        param0 = arcpy.Parameter(
            displayName="Layer list in use",
            name="layers_list",
            datatype="DEFile",
            parameterType="Required",
            direction="Input")

        param0.filter.list = ['csv']
        param0.value = LAYERS_CSV
        param0.enabled = False

        param1 = arcpy.Parameter(
            displayName="Target Dataframe",
            name="target_dataframe",
            datatype="GPString",
            parameterType="Required",
            direction="Input",
            multiValue=False)
        try:
            param1.filter.list = [f.name for f in arcpy.mapping.ListDataFrames(arcpy.mapping.MapDocument("CURRENT"))]
            param1.value = param1.filter.list[0]
        except:
            param1.filter.list = ["No Dataframe"]  # e.g. To load in ArcCatalog
            param1.value = param1.filter.list[0]

        param2 = arcpy.Parameter(
            displayName="Target Position",
            name="target_position",
            datatype="GPString",
            parameterType="Required",
            direction="Input",
            multiValue=False)
        param2.filter.list = ["TOP", "BOTTOM", "AUTO_ARRANGE"]
        param2.value = param2.filter.list[0]

        param3 = arcpy.Parameter(
            displayName="Available Layers",
            name="available_layers",
            datatype="GPString",
            parameterType="Required",
            direction="Input",
            multiValue=True)

        param3.filter.list = [display for cat, ti, src, display in self.layers]

        return [param0, param1, param2, param3]

    def execute(self, parameters, messages):

        messages.AddMessage("Executing...")
        df = arcpy.mapping.ListDataFrames(arcpy.mapping.MapDocument("CURRENT"), parameters[1].valueAsText)[0]
        df_name = df.name

        pos = parameters[2].valueAsText

        lyrs = [v.strip().strip("'") for v in parameters[3].ValueAsText.split(";")]

        if lyrs:
            messages.AddMessage("Adding layers...")

            for lyr in lyrs:
                src = self.layer_dict[lyr]

                messages.AddMessage("... adding layer '{}' from '{}' to dataframe '{}' at position '{}'".format(lyr, src, df_name, pos))
                try:
                    layer = arcpy.mapping.Layer(src)
                    layer.visible = False
                    arcpy.mapping.AddLayer(df, layer, pos)

                except Exception as e:
                    messages.AddErrorMessage(e.message)

        else:
            messages.AddMessage("No layers selected")

        return


class Toolbox(object):

    def __init__(self):

        self.label = "OEH"
        self.alias = "oeh_tools"
        self.tools = [AddCoreLayersTool]

        return
