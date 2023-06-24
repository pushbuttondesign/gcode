# anim_rotateselected.py CamBam

if view.SelectedEntities.Length > 0:
    for dd in range (1,360):
        for ent in view.SelectedEntities:
            ent.Transform.RotZ(Math.PI/90.0)
#				ent.Transform.Translate(0,2,0)
#			Repaint the view

        view.RefreshView()

#			slow things down so we can see
        app.Sleep(1)
		
