import arcpy
import pandas as pd

LAYERS_CSV = "p:\Corporate\Tools\Software\Corporate\CoreLayers\layers.csv"


def layer_specs_from_csv(csv):

    df = pd.read_csv(csv)

    df['Display'] = df[["Type", "Category", "Title"]].apply(lambda x: "{} | {} | {}".format(*x), axis=1)

    layer_specs = zip(df["Type"], df["Category"], df["Title"], df["Datasource"], df["Display"])

    del df

    return layer_specs


class AddCoreLayersTool(object):

    def __init__(self):

        self.label = "Add Core Layers"
        self.description = "Add core layers to the map"
        self.canRunInBackground = False

        self.layers = layer_specs_from_csv(LAYERS_CSV)
        self.layer_dict = {display: source for ty, cat, ti, source, display in self.layers}

    def getParameterInfo(self):

        param0 = arcpy.Parameter(
            displayName="Target Dataframe",
            name="target_dataframe",
            datatype="GPString",
            parameterType="Required",
            direction="Input",
            multiValue=False)
        try:
            param0.filter.list = [f.name for f in arcpy.mapping.ListDataFrames(arcpy.mapping.MapDocument("CURRENT"))]
            param0.value = param0.filter.list[0]
        except:
            param0.filter.list = ["No Dataframe"]  # e.g. To load in ArcCatalog
            param0.value = param0.filter.list[0]

        param1 = arcpy.Parameter(
            displayName="Available Layers",
            name="available_layers",
            datatype="GPString",
            parameterType="Required",
            direction="Input",
            multiValue=True)

        param1.filter.list = [display for ty, cat, ti, src, display in self.layers]

        return [param0, param1]

    def execute(self, parameters, messages):

        messages.AddMessage("Executing...")
        df = arcpy.mapping.ListDataFrames(arcpy.mapping.MapDocument("CURRENT"), parameters[0].valueAsText)[0]
        df_name = df.name

        lyrs = [v.strip().strip("'") for v in parameters[1].ValueAsText.split(";")]

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

        self.label = "Core Layers"
        self.alias = "core_layers_tools"
        self.tools = [AddCoreLayersTool]

        return
