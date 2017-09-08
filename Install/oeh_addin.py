import pythonaddins
from os.path import dirname, realpath, join, isfile


def get_toolbox():

    script_path = dirname(realpath(__file__))
    toolbox = join(script_path, "oeh_tools.pyt")

    if not isfile(toolbox):
        raise ValueError("OEH Addin Toolbox not found: {}".format(toolbox))

    return toolbox


class AddLayerButton(object):
    """Implementation for thickOutline_addin.button (Button)"""

    def onClick(self):

        try:

            pythonaddins.GPToolDialog(get_toolbox(), "OehLayersTool")

        except Exception as e:

            pythonaddins.MessageBox("Error: {}".format(e), "Add Layer")

        return
