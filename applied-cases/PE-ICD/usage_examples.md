# 📚 PE-ICD 사용 예시 템플릿

> SSOT: https://www.notion.so/34f55ed436f081e3be64ff8dbad0e845

---

## 기본 사용 템플릿

```
[Design Scope]
Target level: Gate | Domain: Digital | Process: 28nm | Voltage: 0.9V core

[Circuit]
4-bit synchronous counter

[Output Format]
Mermaid diagram
```

## 예시 1: SRAM Cell (6T)

```
[Design Scope]
Target level: Transistor | Domain: Digital | Process: 65nm | Voltage: 1.0V

[Circuit]
6-Transistor SRAM Cell with read/write ports
Key components: NMOS pass-gate, CMOS inverter pair

[Output Format]
ASCII schematic + step-by-step explanation
```

## 예시 2: 연산 증폭기 (Op-Amp)

```
[Design Scope]
Target level: Block | Domain: Analog | Process: 180nm | Voltage: 1.8V core, 3.3V I/O

[Circuit]
Two-stage CMOS Op-Amp
Key components: Differential pair, current mirror, output stage
Power: Low-power priority (< 1mW total)

[Output Format]
Verilog-style structural description
```

## 예시 3: Mixed-Signal ADC 인터페이스

```
[Design Scope]
Target level: Block | Domain: Mixed-Signal | Process: 28nm | Voltage: 0.9V/1.8V

[Circuit]
SAR ADC 12-bit interface
Key components: DAC, comparator, SAR logic
Timing: 100MHz clock, 1ns setup/hold

[Output Format]
Mermaid diagram
```

## PE-11 Agent Router 호출 예시

```javascript
// manufacturing 도메인 감지 시 PE-ICD 자동 선택
if (domain === 'semiconductor' || domain === 'ic-design') {
  agent = 'PE-ICD';
  prompt = load_prompt('applied-cases/PE-ICD/semiconductor_schematic_prompt.xml');
  // 5-Agent 실행: architect -> circuit_designer -> rtl_engineer -> verification -> power_timing
}
```

---
*Last updated: 2026-04-27 | SSOT: Notion PE-ICD Page*
