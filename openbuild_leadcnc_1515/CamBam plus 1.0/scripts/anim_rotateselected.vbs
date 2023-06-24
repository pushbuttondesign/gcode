' anim_rotateselected.vbs CamBam
sub main

	if view.SelectedEntities.Length > 0 then

		for dd as single = 1 to 360 step 2

			for each ent as Entity in view.SelectedEntities
				ent.Transform.RotZ(Math.PI/90f)
				' ent.Transform.Translate(0,2,0)
			next ent

			'// Repaint the view
			view.RefreshView()

			'// Slow things down so we can see
			app.Sleep(1)
			'System.Windows.Forms.Application.DoEvents  

		next dd
	
	end if

end sub
