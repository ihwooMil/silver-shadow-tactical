extends Control

func _ready():
	$VBoxContainer/StartButton.grab_focus()

func _on_start_button_pressed():
	print("Start button pressed! Event received.")
	$VBoxContainer/StartButton.disabled = true
	$VBoxContainer/StartButton.text = "Loading..."
	
	# 리소스 존재 여부 확인 로그
	print("Checking scenes/Battle.tscn exists: ", ResourceLoader.exists("res://scenes/Battle.tscn"))
	
	var result = get_tree().change_scene_to_file("res://scenes/Battle.tscn")
	if result != OK:
		print("Failed to change scene! Error code: ", result)
		$VBoxContainer/StartButton.disabled = false
		$VBoxContainer/StartButton.text = "Start Battle (Error: " + str(result) + ")"
