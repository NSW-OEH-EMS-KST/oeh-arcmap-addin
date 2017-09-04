import arcpy
import pythonaddins
import os

class activeLayerComboBoxClass(object):
    """Implementation for activeLayer_addin.combobox (ComboBox)"""
    def __init__(self):
        self.editable = True
        self.enabled = True
        self.dropdownWidth = 'WWWWWWWWWWWWWWWWWW'
        self.width = 'WWWWWWWWWWWWWWWWWW'
	
    def onSelChange(self, selection):

	global toolPath
	global layer
	global FeatureLayer
	global shpType
	global thicklyrfile
	global thinlyrfile
	
    	layer = arcpy.mapping.ListLayers(self.mxd, selection)[0]
	
	if layer.isFeatureLayer:
	    FeatureLayer = True
	else:
	    FeatureLayer = False
	toolPath = os.path.dirname(os.path.abspath(__file__))
	desc = arcpy.Describe(layer.dataSource)
	shpType = desc.shapeType
	if shpType == 'Polygon':
	    thicklyrfile = toolPath + '/Symbology/Thick_polygon_outline.lyr'
	    thinlyrfile = toolPath + '/Symbology/Thin_polygon_outline.lyr'	    
	elif shpType == 'Polyline':
	    thicklyrfile = toolPath + '/Symbology/Thick_polyline_outline.lyr'
	    thinlyrfile = toolPath + '/Symbology/Thin_polyline_outline.lyr'	    
	else:
	    pass

    def onEditChange(self, text):
        pass
    # When the combo box has focus, update the combo box with the list of layer names.
    def onFocus(self, focused):
	if focused:
		self.mxd = arcpy.mapping.MapDocument('current')
		layers = arcpy.mapping.ListLayers(self.mxd)
		self.items = []
		for layer in layers:
			self.items.append(layer.name)        

    def onEnter(self):
        pass
    def refresh(self):
        pass

class addIDClass(object):
    """Implementation for addID_addin.button (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        if FeatureLayer == True:
	    # Check if field name already exists, if it does it will be deleted and recreated.
	    fieldList = arcpy.ListFields (layer)
	    fieldExist = 0
	    for field in fieldList:
		if str(field.name) == 'IDField':
		    fieldExist = 1
		else:
		    pass
	    if fieldExist == 1:
		pythonaddins.MessageBox('Field of name IDField already exists it will be deleted and recreated', 'IDField Exists', 0)
		arcpy.DeleteField_management (layer, 'IDField') 
	    arcpy.AddField_management(layer, 'IDField', 'DOUBLE', 11, 12, 3)
	    # Create update cursor for feature class 
	    x = 0
	    with arcpy.da.UpdateCursor(layer, ('IDField')) as cursor:
		# For each row, evaluate the WELL_YIELD value (index position 
		#  of 0), and update WELL_CLASS (index position of 1)
		#
		for row in cursor:
		    row[0] = x + 1
		    x = x + 1
		    # Update the cursor with the updated list
		    #
		    cursor.updateRow(row)

	else:
	    pythonaddins.MessageBox('The Add ID field can not be added as the current selection is not a feature layer', 'Add ID', 0)
	    

class thickOutlineButtonClass(object):
    """Implementation for thickOutline_addin.button (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
	if shpType <> ('Polygon') and (shpType <> 'Polyline'):
	    pythonaddins.MessageBox('A polygon or polyline theme needs to be selected', 'Thick Outline', 0)
	else:
	    arcpy.ApplySymbologyFromLayer_management(layer, thicklyrfile)


class thinOutlineButtonClass(object):
    """Implementation for thinOutline_addin.button (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
	if (shpType <> 'Polygon') and (shpType <> 'Polyline'):
	    pythonaddins.MessageBox('A polygon or polyline theme needs to be selected', 'Thin Outline', 0)
	else:
	    arcpy.ApplySymbologyFromLayer_management(layer, thinlyrfile)

class updateAreaHaClass(object):
    """Implementation for updateAreaHa.button (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):

	# Check that the current layer is a featurelayer of type polygon.
	if FeatureLayer == True:
	    # Check if the selected featurelayer is type polygon.
	    if shpType <> 'Polygon':
		# Do nothing as area can't be calculated.
		pythonaddins.MessageBox('A polygon theme needs to be selected', 'Update Area', 0)
	    else:
		# Get the spatial reference.
		spatialReference = arcpy.Describe(layer).spatialReference
		strSpatialReference = str(spatialReference.name)
		if strSpatialReference[:3] == 'GCS':
		    # Project the layer and store in memory.
		    pythonaddins.MessageBox(str(layer) + ' is not projected so area calculations will not take place.', 'Not projected', 0)
		else:
		    # Commence with the calculations
		    pythonaddins.MessageBox(str(layer) + ' is projected so area calculations will commence.', 'Projected', 0)
		    # Check if 'Area' field already exists, if not it will be added.
		    fieldList = arcpy.ListFields (layer)
		    fieldExist = 0
		    for field in fieldList:
			if str(field.name) == 'AreaHa':
			    fieldExist = 1
			else:
			    pass
		    # If field 'area' does not exist it will be added.
		    if fieldExist == 0:
			arcpy.AddField_management(layer, 'AreaHa', 'DOUBLE', 11, 12, 3)
		    # The area calculations.
		    arcpy.CalculateField_management(layer, 'AreaHa', '!shape.area@hectares!', 'PYTHON_9.3')
			

class updateAreaSqMClass(object):
    """Implementation for updateAreaSqM_addin.button (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):

	# Check that the current layer is a featurelayer of type polygon.
	if FeatureLayer == True:
	    # Check if the selected featurelayer is type polygon.
	    if shpType <> 'Polygon':
		# Do nothing as area can't be calculated.
		pythonaddins.MessageBox('A polygon theme needs to be selected', 'Update Area', 0)
	    else:
		# Get the spatial reference.
		spatialReference = arcpy.Describe(layer).spatialReference
		strSpatialReference = str(spatialReference.name)
		if strSpatialReference[:3] == 'GCS':
		    # Project the layer and store in memory.
		    pythonaddins.MessageBox(str(layer) + ' is not projected so area calculations will not take place.', 'Not projected', 0)
		else:
		    # Commence with the calculations
		    pythonaddins.MessageBox(str(layer) + ' is projected so area calculations will commence.', 'Projected', 0)
		    # Check if 'Area' field already exists, if not it will be added.
		    fieldList = arcpy.ListFields (layer)
		    fieldExist = 0
		    for field in fieldList:
			if str(field.name) == 'AreaSqM':
			    fieldExist = 1
			else:
			    pass
		    # If field 'area' does not exist it will be added.
		    if fieldExist == 0:
			arcpy.AddField_management(layer, 'AreaSqM', 'DOUBLE', 12, 4, 20)
		    # The area calculations.
		    arcpy.CalculateField_management(layer, 'AreaSqM', '!shape.area@meters!', 'PYTHON_9.3')
			


