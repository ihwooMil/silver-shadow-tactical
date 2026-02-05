export interface Unit {
  id: string;
  name: string;
  speed: number;
  hp: number;
  maxHp: number;
  position: number; // 0 to 100 on timeline
  energy: number;
  side: 'player' | 'enemy';
}

export class BattleEngine {
  units: Unit[];
  onTurnStart: (unit: Unit) => void;

  constructor(units: Unit[], onTurnStart: (unit: Unit) => void) {
    this.units = units;
    this.onTurnStart = onTurnStart;
  }

  // 타임라인 업데이트 (Tick)
  update(deltaTime: number) {
    for (const unit of this.units) {
      if (unit.hp <= 0) continue;
      
      // 속도에 비례해 타임라인 전진
      unit.position += unit.speed * deltaTime;

      if (unit.position >= 100) {
        unit.position = 0; // 초기화 (혹은 초과분 유지)
        this.onTurnStart(unit);
        return unit; // 이번 틱에 턴을 잡은 유닛 반환
      }
    }
    return null;
  }
}
