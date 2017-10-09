import pythonaddins
from os.path import dirname, realpath, join, isfile


def get_toolbox():

    script_path = dirname(realpath(__file__))
    toolbox = join(script_path, "core_layers_tools.pyt")

    if not isfile(toolbox):
        raise ValueError("Core Layers Addin Toolbox not found: {}".format(toolbox))

    return toolbox


class AddLayerButton(object):
    """Implementation for thickOutline_addin.button (Button)"""

    def onClick(self):

        try:

            pythonaddins.GPToolDialog(get_toolbox(), "AddCoreLayersTool")

        except Exception as e:

            pythonaddins.MessageBox("Error: {}".format(e), "Add Layer")

        return
