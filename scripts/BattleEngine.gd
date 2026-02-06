extends Node2D

var turn_count = 0

func _ready():
	print("Battle Started")
	new_turn()

func new_turn():
	turn_count += 1
	$CanvasLayer/TurnLabel.text = "Turn: %d" % turn_count
	$CanvasLayer/LogLabel.text = "Player Turn Started..."

func _on_attack_button_pressed():
	$CanvasLayer/LogLabel.text = "Player used Strike! Dealt 6 Damage."
	await get_tree().create_timer(1.0).timeout
	enemy_turn()

func enemy_turn():
	$CanvasLayer/LogLabel.text = "Enemy Turn..."
	await get_tree().create_timer(1.0).timeout
	$CanvasLayer/LogLabel.text = "Enemy Attacked! Took 5 Damage."
	await get_tree().create_timer(1.0).timeout
	new_turn()
