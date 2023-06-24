# In Place Resize

scale=0.5

if view.SelectedEntities.Length > 0:
    for ent in view.SelectedEntities:
        cp = ent.GetCentroid()
        ent.Transform.Translate(-cp.X,-cp.Y,-cp.Z)
        ent.Transform.Scale(scale,scale,scale)
        ent.Transform.Translate(cp.X,cp.Y,cp.Z)

	