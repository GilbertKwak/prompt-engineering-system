# 🧮 PE-ICD · Semiconductor Schematic & Design Agent System v1.0

> **Status**: ✅ Active | **Created**: 2026-04-27 | **Manager**: GilbertKwak
> **Notion SSOT**: [PE-ICD Notion Page](https://www.notion.so/34f55ed436f081e3be64ff8dbad0e845)
> **Parent**: T-09 프롬프트 엔지니어링 시스템 Mother Page (C-09)

---

## 개요

반도체 회로도·설계도를 AI로 생성하기 위한 표준 프롬프트 + 멀티에이전트 시스템 정의입니다.

## 파일 구조

```
PE-ICD/
├── README.md
├── semiconductor_schematic_prompt.xml    # Prompt 1: 단일 프롬프트 (SSOT 원본)
├── design_agent_system.xml               # Prompt 2: 5-Agent 멀티에이전트 시스템
└── usage_examples.md                     # 사용 예시 템플릿
```

## 5-Agent 워크플로우

| Agent ID | Role | 핵심 체크 |
|----------|------|----------|
| architect | Chief Semiconductor Architect | 시스템 아키텍처 정의 |
| circuit_designer | Senior Circuit Designer | 상세 회로 설계 |
| rtl_engineer | RTL/Structural Engineer | Verilog 구조 생성 |
| verification | Verification & Validation Engineer | 논리 검증 |
| power_timing | Power & Timing Specialist | 전원/타이밍 검토 |

## 지원 설계 레벨

- Target Level: System / Block / Gate / Transistor
- Domain: Digital / Analog / Mixed-Signal
- Process Node: 180nm ~ 5nm CMOS
- Output: ASCII / Mermaid / Verilog / Step-by-step

## 연동

- **PE-11**: ICD-AGENT 네임스페이스로 5개 에이전트 정의 삽입 가능
- **PE-MEM**: HBM/LPDDR/NAND 회로 설계 시 SSOT로 활용
- **SPU**: 저장 및 캐시 회로 설계 시 활용

---
*Last updated: 2026-04-27 | Version: v1.0*
