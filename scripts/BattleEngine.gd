extends Node

class_name BattleEngine

signal turn_started(unit_data)

var units = []
var is_active = false

func setup(unit_list: Array):
	units = unit_list
	is_active = true

func _process(delta):
	if not is_active: return
	
	if units.is_empty():
		print("WARNING: BattleEngine has no units!")
		is_active = false
		return
		
	for unit in units:
		if unit.hp <= 0: continue
		
		# 속도에 비례해 position (0~100) 증가
		unit.position += unit.speed * delta
		
		if unit.position >= 100:
			unit.position = 0
			is_active = false # 턴 처리 중 정지
			emit_signal("turn_started", unit)
			return

func resume():
	is_active = true
