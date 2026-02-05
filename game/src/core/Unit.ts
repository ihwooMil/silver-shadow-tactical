export interface DefenseStats {
  block: number;      // 소모형 보호막 (데미지 입으면 감소)
  armor: number;      // 피해 감소 수치 (데미지 입어도 수치 유지)
  armorDuration: number; // 방어력 유지 횟수 (피격 시마다 감소)
}

export class Unit {
  id: string;
  name: string;
  hp: number;
  maxHp: number;
  defense: DefenseStats;

  constructor(id: string, name: string, hp: number) {
    this.id = id;
    this.name = name;
    this.hp = hp;
    this.maxHp = hp;
    this.defense = { block: 0, armor: 0, armorDuration: 0 };
  }

  // 피해를 입을 때의 로직
  takeDamage(amount: number) {
    let finalDamage = amount;

    // 1. 방어력(Armor) 적용: 피해 감쇄
    if (this.defense.armorDuration > 0) {
      finalDamage = Math.max(0, finalDamage - this.defense.armor);
      this.defense.armorDuration -= 1; // 피격 횟수 차감
      console.log(`${this.name}의 방어력 작동! 남은 횟수: ${this.defense.armorDuration}`);
    }

    // 2. 방어도(Block) 적용: 보호막 소모
    if (this.defense.block > 0) {
      if (this.defense.block >= finalDamage) {
        this.defense.block -= finalDamage;
        finalDamage = 0;
      } else {
        finalDamage -= this.defense.block;
        this.defense.block = 0;
      }
    }

    // 3. 남은 피해 체력에서 차감
    this.hp = Math.max(0, this.hp - finalDamage);
    return finalDamage;
  }

  addBlock(amount: number) {
    this.defense.block += amount;
  }

  addArmor(value: number, duration: number) {
    this.defense.armor = value;
    this.defense.armorDuration = duration;
  }
}
