renderer = slicer.app.layoutManager().threeDWidget(0).threeDView().renderWindow().GetRenderers().GetFirstRenderer()
imagex = 800
imagey = 600
imageGrid = vtk.vtkImageGridSource()
imageGrid.SetGridSpacing(50,50,0)
imageGrid.SetGridOrigin(0,0,0)
imageGrid.SetDataExtent(0,imagex,0,imagey,0,0)
imageGrid.SetDataScalarTypeToUnsignedChar()

table = vtk.vtkLookupTable()
table.SetTableRange(0,1)
table.SetAlphaRange(0,1)
table.SetHueRange(.15,.15)
table.SetSaturationRange(1,1)
table.SetValueRange(0,1)
table.Build()


alpha = vtk.vtkImageMapToColors()
alpha.SetInputConnection( imageGrid.GetOutputPort() )
alpha.SetLookupTable( table )

reader = vtk.vtkJPEGReader()
reader.SetFileName('C:\\Users\\chene\\Downloads\\temp\\AIP_W18_Notebooks\\data\\images\\monkey.jpg')
reader.Update()


blend = vtk.vtkImageBlend()
blend.AddInputConnection( 0, reader.GetOutputPort() )
blend.AddInputConnection( 0, alpha.GetOutputPort() )

p1 = vtk.vtkPoints()
p1.SetNumberOfPoints( 5 )
p1.SetPoint( 0, 324,  imagey-499, 0)
p1.SetPoint( 1, 378,  imagey-540, 0)
p1.SetPoint( 2, 451,  imagey-510, 0)
p1.SetPoint( 3, 343,  imagey-234, 0)
p1.SetPoint( 4, 452,  imagey-229, 0)
p2 = vtk.vtkPoints()
p2.SetNumberOfPoints( 5 )
p2.SetPoint( 0, 324,  imagey-540, 0)
p2.SetPoint( 1, 378,  imagey-540, 0)
p2.SetPoint( 2, 451,  imagey-540, 0)
p2.SetPoint( 3, 343,  imagey-234, 0)
p2.SetPoint( 4, 452,  imagey-229, 0)
   
transform = vtk.vtkThinPlateSplineTransform()
transform.SetSourceLandmarks( p1 )
transform.SetTargetLandmarks( p2 )
transform.SetBasisToR2LogR()
transform.Inverse()

reslice = vtk.vtkImageReslice()
reslice.SetInputConnection( blend.GetOutputPort() )
reslice.SetResliceTransform( transform )
reslice.SetInterpolationModeToLinear()

map = vtk.vtkImageMapper()
map.SetInputConnection( reslice.GetOutputPort() )
map.SetColorWindow( 255.0 )
map.SetColorLevel( 127.5 )
map.SetZSlice( 0 )

act = vtk.vtkActor2D()
act.SetMapper( map )
act.SetPosition(0,0)
renderer.AddActor( act )