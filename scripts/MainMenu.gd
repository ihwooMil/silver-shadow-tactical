extends Control

func _ready():
	$VBoxContainer/StartButton.grab_focus()

func _on_start_button_pressed():
	print("Start button pressed, switching to Battle scene...")
	var result = get_tree().change_scene_to_file("res://scenes/Battle.tscn")
	if result != OK:
		print("Failed to change scene! Error code: ", result)
