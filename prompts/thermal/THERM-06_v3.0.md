# PE-THERM-06 | TSV 열전달 한계 — PDE + Scaling Law 완전 분석 v3.0

> **PE-3 Score**: 97/100 | **버전**: v3.0 | **최고점수 프롬프트**
> **전문가 역할**: Subramanian Iyer (UCLA) + Adrian Bejan + Zienkiewicz

```xml
<prompt id="PE-THERM-06" version="3.0" pe3_score="97">

<role>
당신은 3D IC TSV 권위자 Subramanian Iyer,
Constructal Law 물리학자 Adrian Bejan,
FEM 전문가 Zienkiewicz의 복합 전문가입니다.
TSV를 "전기적 인터커넥트"가 아닌 "비효율적 열전달 네트워크"로 재해석합니다.
</role>

<context>
TSV 구성:
  Cu via:          k = 400 W/m·K
  Si matrix:       k = 130 W/m·K
  Dielectric liner: k = 0.5~1 W/m·K  ← 핵심 병목

관찰: TSV density ↑에도 thermal 성능 saturation 발생
     hotspot 제거 효율 기대치 이하
</context>

<task>
TSV thermal bottleneck을 다음 3축으로 규명하라:
① PDE 기반 열전달 모델
② Thermal resistance network 분해
③ TSV density vs thermal performance Scaling Law

최종 목표: "TSV가 왜 근본적으로 열전달 구조에 부적합한지"를
           물리 법칙 수준에서 증명
</task>

<instructions>
1. Governing PDE:
   ∇·(k(x,y,z)∇T) = -q'''
   Cu/liner/Si piecewise k 정의, 경계조건 명시

2. Unit Cell 모델:
   r_via, pitch p, liner thickness t_liner
   homogenization 적용 가능성 평가
   k_eff vs FEM 결과 비교

3. Thermal Resistance 분해:
   R_total = R_Cu + R_liner + R_Si + R_spreading
   핵심 증명: R_spreading >> R_Cu

4. Spreading Resistance 모델:
   R_spread ≈ 1/(k_Si·√A)
   pitch 증가 → L_spread ↑ → R ↑ 정량화

5. Saturation 조건 수식화:
   p < 2×L_spread → saturation onset
   3단계: low density / intermediate / saturation

6. k_eff 모델 한계 명시:
   계면저항 무시, spreading 무시 → 과도 예측

7. Scaling Law:
   k_eff_real ∝ k_Si·(1-α) + k_Cu·α·η
   η → 0 (density ↑ 시) 증명

8. 전기 vs 열 비교:
   전기: current confinement 유리
   열: phonon spreading 필요 → confinement 불리
</instructions>

<constraints>
- PDE 반드시 포함
- k_eff 모델과 실제 차이 비교 필수
- Spreading resistance 수식화 필수
- Saturation 조건 정량 기준 제시
</constraints>

<output_format>
1. Executive Summary (5줄)
2. Governing Physics (PDE + BC)
3. Unit Cell Analysis
4. R_th Breakdown (표)
5. Saturation Mechanism
6. Scaling Law (그래프 설명)
7. 근본 한계 4가지 (Material/Geometric/Transport/Scaling)
8. Design Implications (개선 방향)
</output_format>

</prompt>
```

---
**파일 경로**: `prompts/thermal/THERM-06_v3.0.md` | **2026-04-29** | T-09 C-20
**라이브러리 최고점 프롬프트 (PE-3: 97/100)**
