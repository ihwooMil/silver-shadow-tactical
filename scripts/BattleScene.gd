extends Node2D

@onready var engine = $BattleEngine

func _ready():
	var data = load_json("res://data/units.json")
	var units = data["units"]
	
	# 초기화: 모든 유닛의 position을 0으로 설정
	for unit in units:
		unit["position"] = 0.0
	
	engine.setup(units)
	engine.turn_started.connect(_on_turn_started)

func load_json(path):
	var file = FileAccess.open(path, FileAccess.READ)
	var content = file.get_as_text()
	return JSON.parse_string(content)

func _on_turn_started(unit):
	$CanvasLayer/LogLabel.text = "[%s]의 턴! (Speed: %d)" % [unit.name, unit.speed]
	
	# 타임바 시각화를 위해 잠시 대기 후 재개 (실제론 카드 선택 대기)
	await get_tree().create_timer(1.0).timeout
	engine.resume()

func _process(_delta):
	# 타임라인 시각화 (간이)
	var status = ""
	for unit in engine.units:
		status += "%s: %.1f%% | " % [unit.name, unit.position]
	$CanvasLayer/TurnLabel.text = status
