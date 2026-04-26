#!/usr/bin/env python3
"""
P6: ExaFLOPS 통합 자원모델
HBM · Glass Substrate · 전력(SMR) · 패키징(OSAT) → 단일 TCO 엔진

Usage:
    python exaflops_resource_model.py
    python exaflops_resource_model.py --scenario smr_full
    python exaflops_resource_model.py --system SYS_C --dry-run
"""

import argparse
import json
import math
import os
import sys
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
import yaml

# ────────────────────────────────────────
# 데이터 구조 정의
# ────────────────────────────────────────

@dataclass
class HBMLayer:
    """HBM 자원 레이어 계산 결과"""
    system_id: str
    hbm_gen: str
    stacks_total: int
    capacity_total_tb: float
    unit_cost_usd: float
    gross_cost_usd_m: float
    yield_adj_cost_usd_m: float
    salvage_value_usd_m: float
    net_cost_usd_m: float
    cost_per_exaflops_usd_m: float

@dataclass
class GlassLayer:
    """Glass Substrate 자원 레이어 계산 결과"""
    system_id: str
    gpu_model: str
    adoption_scenario: str
    substrates_glass: int
    substrates_abf: int
    glass_cost_usd_m: float
    abf_cost_usd_m: float
    total_cost_usd_m: float
    premium_vs_allabf_usd_m: float
    cost_per_exaflops_usd_m: float

@dataclass
class PowerLayer:
    """전력 자원 레이어 계산 결과"""
    system_id: str
    smr_scenario: str
    total_power_mw: float
    annual_energy_gwh: float
    grid_cost_10y_usd_m: float
    smr_capex_usd_m: float
    smr_opex_10y_usd_m: float
    blended_lcoe_usd_per_mwh: float
    total_power_tco_10y_usd_m: float
    saving_vs_grid_usd_m: float
    cost_per_exaflops_usd_m: float

@dataclass
class PackagingLayer:
    """패키징(OSAT) 자원 레이어 계산 결과"""
    system_id: str
    gpu_model: str
    cowos_area_m_mm2: float
    packaging_cost_usd_m: float
    yield_loss_cost_usd_m: float
    total_cost_usd_m: float
    lead_time_weeks: int
    capacity_constrained: bool
    cost_per_exaflops_usd_m: float

@dataclass
class IntegratedTCO:
    """통합 TCO 최종 결과"""
    system_id: str
    system_name: str
    exaflops: float
    smr_scenario: str
    glass_scenario: str
    lifetime_years: int

    # 레이어별 CAPEX
    capex_hbm_usd_m: float
    capex_glass_pkg_usd_m: float
    capex_power_infra_usd_m: float
    capex_gpu_other_usd_m: float
    total_capex_usd_m: float

    # OPEX (lifetime)
    opex_power_usd_m: float
    opex_maintenance_usd_m: float
    opex_staffing_usd_m: float
    opex_other_usd_m: float
    total_opex_usd_m: float

    # TCO 합계
    total_tco_usd_m: float
    tco_per_exaflops_usd_m: float
    tco_per_exaflops_per_year_usd_m: float
    npv_tco_usd_m: float

    # 절감 분석
    saving_vs_grid_only_usd_m: float
    moic_contribution: float

    # 레이어 객체
    hbm: HBMLayer = field(default=None)
    glass: GlassLayer = field(default=None)
    power: PowerLayer = field(default=None)
    packaging: PackagingLayer = field(default=None)


# ────────────────────────────────────────
# 핵심 계산 엔진
# ────────────────────────────────────────

class ExaFLOPSResourceModel:
    def __init__(self, config_path: str = None):
        config_path = config_path or Path(__file__).parent / "exaflops_config.yaml"
        with open(config_path, "r", encoding="utf-8") as f:
            self.cfg = yaml.safe_load(f)
        self.results: List[IntegratedTCO] = []

    # ── 1. HBM 레이어 ──────────────────────
    def calc_hbm(self, sys: dict, year_offset: int = 0) -> HBMLayer:
        gpu_model = sys["gpu_model"]
        hbm_gen   = sys["hbm_gen"]
        n_gpu     = sys["gpu_count"]
        exaflops  = sys["exaflops"]
        h = self.cfg["hbm"]

        stacks_per_gpu = h["stacks_per_gpu"][gpu_model]
        stacks_total   = n_gpu * stacks_per_gpu
        cap_per_stack  = h["capacity_per_stack_gb"][hbm_gen]
        cap_total_tb   = stacks_total * cap_per_stack / 1000

        # 연도별 단가 적용
        unit_cost = h["unit_cost_usd"][hbm_gen] * (
            (1 - h["annual_price_decline_pct"]) ** year_offset
        )
        yield_rate    = h["yield_rate"][hbm_gen]
        gross_cost_m  = stacks_total * unit_cost / 1e6
        yield_adj_m   = gross_cost_m / yield_rate

        # Salvage
        s = h["salvage"]
        salvageable   = int(stacks_total * s["recovery_rate"])
        salvage_val_m = (salvageable * unit_cost * s["salvage_value_pct"]
                         - salvageable * s["reconditioning_cost_usd_per_stack"]) / 1e6
        salvage_val_m = max(salvage_val_m, 0)
        net_cost_m    = yield_adj_m - salvage_val_m

        return HBMLayer(
            system_id=sys["id"],
            hbm_gen=hbm_gen,
            stacks_total=stacks_total,
            capacity_total_tb=round(cap_total_tb, 1),
            unit_cost_usd=round(unit_cost, 0),
            gross_cost_usd_m=round(gross_cost_m, 2),
            yield_adj_cost_usd_m=round(yield_adj_m, 2),
            salvage_value_usd_m=round(salvage_val_m, 2),
            net_cost_usd_m=round(net_cost_m, 2),
            cost_per_exaflops_usd_m=round(net_cost_m / exaflops, 2),
        )

    # ── 2. Glass Substrate 레이어 ──────────
    def calc_glass(self, sys: dict, glass_scenario: str = "base") -> GlassLayer:
        gpu_model  = sys["gpu_model"]
        n_gpu      = sys["gpu_count"]
        exaflops   = sys["exaflops"]
        g = self.cfg["glass_substrate"]
        year_offset = self.cfg["glass_substrate"]["current_year"] - \
                      self.cfg["glass_substrate"]["adoption_start_year"]

        adoption_rate  = g["adoption_scenario"][glass_scenario]
        n_glass        = int(n_gpu * adoption_rate)
        n_abf          = n_gpu - n_glass

        # Glass 단가 (연도별 개선)
        base_glass_cost = g["unit_cost_usd"]["glass_2026"]
        glass_unit = base_glass_cost * (
            (1 - g["yield_improvement_pct"]) ** year_offset
        )
        abf_unit   = g["unit_cost_usd"]["standard"]

        glass_cost_m   = n_glass * glass_unit / 1e6
        abf_cost_m     = n_abf   * abf_unit   / 1e6
        total_cost_m   = glass_cost_m + abf_cost_m
        all_abf_cost_m = n_gpu * abf_unit / 1e6
        premium_m      = total_cost_m - all_abf_cost_m

        return GlassLayer(
            system_id=sys["id"],
            gpu_model=gpu_model,
            adoption_scenario=glass_scenario,
            substrates_glass=n_glass,
            substrates_abf=n_abf,
            glass_cost_usd_m=round(glass_cost_m, 2),
            abf_cost_usd_m=round(abf_cost_m, 2),
            total_cost_usd_m=round(total_cost_m, 2),
            premium_vs_allabf_usd_m=round(premium_m, 2),
            cost_per_exaflops_usd_m=round(total_cost_m / exaflops, 2),
        )

    # ── 3. 전력(SMR) 레이어 ───────────────
    def calc_power(self, sys: dict, smr_scenario: str = "grid_only") -> PowerLayer:
        gpu_model  = sys["gpu_model"]
        n_gpu      = sys["gpu_count"]
        pue        = sys["pue"]
        region     = sys["region"]
        exaflops   = sys["exaflops"]
        p = self.cfg["power"]
        scenario   = p["smr_scenarios"][smr_scenario]
        dr         = self.cfg["tco"]["discount_rate"]

        # IT 전력
        gpu_tdp_w      = p["gpu_tdp_w"][gpu_model]
        it_power_mw    = n_gpu * gpu_tdp_w * p["system_overhead_multiplier"] / 1e6
        total_power_mw = it_power_mw * pue
        annual_gwh     = total_power_mw * 8760 / 1000

        grid_price     = p["grid_price_usd_per_mwh"][region]
        smr_pct        = scenario["smr_pct"]
        smr_lcoe       = scenario["lcoe_usd_per_mwh"] or grid_price
        smr_capex_m    = scenario["capex_usd_m"]
        cf             = p["capacity_factor"]

        # 연간 전력비 계산
        annual_grid_portion  = annual_gwh * (1 - smr_pct)
        annual_smr_portion   = annual_gwh * smr_pct
        annual_cost_grid_m   = annual_grid_portion * grid_price / 1e3
        annual_cost_smr_m    = annual_smr_portion  * smr_lcoe  / 1e3

        # 10Y NPV 전력비
        def npv_annuity(annual, years, rate, escalation=0.03):
            return sum(
                annual * ((1 + escalation) ** t) / ((1 + rate) ** (t + 1))
                for t in range(years)
            )

        lifetime = sys["lifetime_years"]
        grid_10y_m = npv_annuity(annual_cost_grid_m, lifetime, dr)
        smr_10y_m  = npv_annuity(annual_cost_smr_m,  lifetime, dr)

        # 전체 그리드 대비 절감
        all_grid_m = npv_annuity(
            annual_gwh * grid_price / 1e3, lifetime, dr
        )
        total_power_tco_m = grid_10y_m + smr_10y_m + smr_capex_m
        saving_m = all_grid_m + 0 - total_power_tco_m

        blended_lcoe = (
            (1 - smr_pct) * grid_price + smr_pct * smr_lcoe
        )

        return PowerLayer(
            system_id=sys["id"],
            smr_scenario=smr_scenario,
            total_power_mw=round(total_power_mw, 1),
            annual_energy_gwh=round(annual_gwh, 1),
            grid_cost_10y_usd_m=round(grid_10y_m, 1),
            smr_capex_usd_m=smr_capex_m,
            smr_opex_10y_usd_m=round(smr_10y_m, 1),
            blended_lcoe_usd_per_mwh=round(blended_lcoe, 1),
            total_power_tco_10y_usd_m=round(total_power_tco_m, 1),
            saving_vs_grid_usd_m=round(saving_m, 1),
            cost_per_exaflops_usd_m=round(total_power_tco_m / exaflops, 1),
        )

    # ── 4. 패키징(OSAT) 레이어 ───────────
    def calc_packaging(self, sys: dict) -> PackagingLayer:
        gpu_model  = sys["gpu_model"]
        n_gpu      = sys["gpu_count"]
        exaflops   = sys["exaflops"]
        pk = self.cfg["packaging"]["process_per_gpu"][gpu_model]
        oc = self.cfg["packaging"]["osat_capacity_constraint"]

        cowos_area_m  = n_gpu * pk["CoWoS_size_mm2"] / 1e6
        gross_pkg_m   = n_gpu * pk["cost_usd"] / 1e6
        yield_rate    = pk["yield_rate"]
        yield_loss_m  = gross_pkg_m * (1 - yield_rate) / yield_rate
        total_pkg_m   = gross_pkg_m + yield_loss_m

        # 용량 제약 확인
        pe7_wafers_k  = oc["annual_cowos_wafer_starts_k"] * oc["pe7_allocation_pct"]
        req_wafers    = n_gpu * pk["CoWoS_size_mm2"] / (300**2 * math.pi / 4) / 1000
        constrained   = req_wafers > pe7_wafers_k

        return PackagingLayer(
            system_id=sys["id"],
            gpu_model=gpu_model,
            cowos_area_m_mm2=round(cowos_area_m, 1),
            packaging_cost_usd_m=round(gross_pkg_m, 1),
            yield_loss_cost_usd_m=round(yield_loss_m, 1),
            total_cost_usd_m=round(total_pkg_m, 1),
            lead_time_weeks=pk["lead_time_weeks"],
            capacity_constrained=constrained,
            cost_per_exaflops_usd_m=round(total_pkg_m / exaflops, 1),
        )

    # ── 5. 통합 TCO 계산 ──────────────────
    def calc_integrated_tco(
        self,
        sys: dict,
        smr_scenario: str = "grid_only",
        glass_scenario: str = "base",
    ) -> IntegratedTCO:
        exaflops = sys["exaflops"]
        lifetime = sys["lifetime_years"]
        dr = self.cfg["tco"]["discount_rate"]
        cbd = self.cfg["tco"]["capex_breakdown"]
        oap = self.cfg["tco"]["opex_annual_pct"]

        hbm  = self.calc_hbm(sys)
        gls  = self.calc_glass(sys, glass_scenario)
        pwr  = self.calc_power(sys, smr_scenario)
        pkg  = self.calc_packaging(sys)

        # GPU + 기타 CAPEX 역산 (HBM, Substrate/Packaging 비율에서)
        pkg_substrate_m = gls.total_cost_usd_m + pkg.total_cost_usd_m
        # HBM 비율로부터 총 시스템 CAPEX 역산
        total_system_capex_m = hbm.net_cost_usd_m / cbd["hbm"]
        gpu_other_m = total_system_capex_m * cbd["gpu_die"]
        net_infra_m = total_system_capex_m * cbd["facility_infra"]
        net_nwk_m   = total_system_capex_m * cbd["networking"]
        smr_capex_m = pwr.smr_capex_usd_m
        power_infra_m = total_system_capex_m * cbd["power_infra"] + smr_capex_m

        total_capex_m = (
            gpu_other_m + hbm.net_cost_usd_m + pkg_substrate_m
            + net_infra_m + net_nwk_m + power_infra_m
        )

        # OPEX (NPV, lifetime)
        def npv_annuity(annual, years, rate, esc=0.03):
            return sum(
                annual * ((1 + esc) ** t) / ((1 + rate) ** (t + 1))
                for t in range(years)
            )

        opex_maint_m   = npv_annuity(total_capex_m * oap["maintenance"], lifetime, dr)
        opex_staff_m   = npv_annuity(total_capex_m * oap["staffing"],     lifetime, dr)
        opex_sw_m      = npv_annuity(total_capex_m * oap["software_license"], lifetime, dr)
        opex_cool_m    = npv_annuity(total_capex_m * oap["cooling_fluid"],    lifetime, dr)
        opex_power_m   = pwr.total_power_tco_10y_usd_m - smr_capex_m

        total_opex_m   = opex_power_m + opex_maint_m + opex_staff_m + opex_sw_m + opex_cool_m
        total_tco_m    = total_capex_m + total_opex_m
        npv_tco_m      = total_tco_m   # 이미 NPV 기반

        tco_per_exa_m        = total_tco_m / exaflops
        tco_per_exa_yr_m     = tco_per_exa_m / lifetime

        # Grid Only 대비 절감 (전력 절감만)
        saving_m = pwr.saving_vs_grid_usd_m

        # MOIC 기여 (절감액 / 투자 CAPEX 대비 단순 배수)
        moic_contribution = 1 + (saving_m / total_capex_m) if total_capex_m > 0 else 1.0

        return IntegratedTCO(
            system_id=sys["id"],
            system_name=sys["name"],
            exaflops=exaflops,
            smr_scenario=smr_scenario,
            glass_scenario=glass_scenario,
            lifetime_years=lifetime,
            capex_hbm_usd_m=round(hbm.net_cost_usd_m, 1),
            capex_glass_pkg_usd_m=round(pkg_substrate_m, 1),
            capex_power_infra_usd_m=round(power_infra_m, 1),
            capex_gpu_other_usd_m=round(gpu_other_m + net_infra_m + net_nwk_m, 1),
            total_capex_usd_m=round(total_capex_m, 1),
            opex_power_usd_m=round(opex_power_m, 1),
            opex_maintenance_usd_m=round(opex_maint_m, 1),
            opex_staffing_usd_m=round(opex_staff_m, 1),
            opex_other_usd_m=round(opex_sw_m + opex_cool_m, 1),
            total_opex_usd_m=round(total_opex_m, 1),
            total_tco_usd_m=round(total_tco_m, 1),
            tco_per_exaflops_usd_m=round(tco_per_exa_m, 1),
            tco_per_exaflops_per_year_usd_m=round(tco_per_exa_yr_m, 2),
            npv_tco_usd_m=round(npv_tco_m, 1),
            saving_vs_grid_only_usd_m=round(saving_m, 1),
            moic_contribution=round(moic_contribution, 3),
            hbm=hbm,
            glass=gls,
            power=pwr,
            packaging=pkg,
        )

    # ── 6. 전체 시나리오 실행 ─────────────
    def run_all(
        self,
        system_filter: str = None,
        smr_scenarios: List[str] = None,
        glass_scenarios: List[str] = None,
    ) -> List[IntegratedTCO]:
        smr_s   = smr_scenarios   or ["grid_only", "smr_partial", "smr_full"]
        glass_s = glass_scenarios or ["base"]
        systems = self.cfg["systems"]
        if system_filter:
            systems = [s for s in systems if s["id"] == system_filter]

        results = []
        for sys in systems:
            for smr in smr_s:
                for gls in glass_s:
                    r = self.calc_integrated_tco(sys, smr, gls)
                    results.append(r)
                    print(f"  ✓ {sys['id']} | SMR={smr} | Glass={gls} "
                          f"→ TCO ${r.total_tco_usd_m:,.0f}M | "
                          f"${r.tco_per_exaflops_usd_m:,.0f}M/ExaFLOPS")
        self.results = results
        return results

    # ── 7. Excel 출력 ─────────────────────
    def to_excel(self, results: List[IntegratedTCO] = None, path: str = None) -> str:
        results = results or self.results
        path    = path    or self.cfg["output"]["excel_filename"]
        rows = []
        for r in results:
            rows.append({
                "System ID":         r.system_id,
                "System Name":       r.system_name,
                "ExaFLOPS":          r.exaflops,
                "SMR Scenario":      r.smr_scenario,
                "Glass Scenario":    r.glass_scenario,
                "Lifetime (Y)":      r.lifetime_years,
                "CAPEX HBM ($M)":    r.capex_hbm_usd_m,
                "CAPEX Glass/Pkg ($M)": r.capex_glass_pkg_usd_m,
                "CAPEX Power Infra ($M)": r.capex_power_infra_usd_m,
                "CAPEX GPU/Other ($M)": r.capex_gpu_other_usd_m,
                "Total CAPEX ($M)":  r.total_capex_usd_m,
                "OPEX Power ($M)":   r.opex_power_usd_m,
                "OPEX Maintenance ($M)": r.opex_maintenance_usd_m,
                "OPEX Staffing ($M)": r.opex_staffing_usd_m,
                "OPEX Other ($M)":   r.opex_other_usd_m,
                "Total OPEX ($M)":   r.total_opex_usd_m,
                "Total TCO ($M)":    r.total_tco_usd_m,
                "TCO/ExaFLOPS ($M)": r.tco_per_exaflops_usd_m,
                "TCO/ExaFLOPS/Yr ($M)": r.tco_per_exaflops_per_year_usd_m,
                "NPV TCO ($M)":      r.npv_tco_usd_m,
                "Saving vs Grid ($M)": r.saving_vs_grid_only_usd_m,
                "MOIC Contribution": r.moic_contribution,
                # HBM
                "HBM Stacks":        r.hbm.stacks_total if r.hbm else None,
                "HBM Net Cost ($M)": r.hbm.net_cost_usd_m if r.hbm else None,
                "HBM Salvage ($M)":  r.hbm.salvage_value_usd_m if r.hbm else None,
                # Power
                "Total Power (MW)":  r.power.total_power_mw if r.power else None,
                "Annual Energy (GWh)": r.power.annual_energy_gwh if r.power else None,
                "Blended LCOE ($/MWh)": r.power.blended_lcoe_usd_per_mwh if r.power else None,
                # Packaging
                "CoWoS Area (M mm²)": r.packaging.cowos_area_m_mm2 if r.packaging else None,
                "Pkg Constrained":   r.packaging.capacity_constrained if r.packaging else None,
            })
        df = pd.DataFrame(rows)
        df.to_excel(path, index=False)
        print(f"\n📊 Excel → {path}")
        return path

    # ── 8. JSON 출력 ──────────────────────
    def to_json(self, results: List[IntegratedTCO] = None, path: str = None) -> str:
        results = results or self.results
        path    = path    or "p6_exaflops_tco.json"

        def default_serializer(obj):
            if hasattr(obj, '__dataclass_fields__'):
                return asdict(obj)
            return str(obj)

        data = [asdict(r) for r in results]
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, default=default_serializer)
        print(f"📄 JSON  → {path}")
        return path

    # ── 9. 요약 테이블 출력 ───────────────
    def print_summary(self, results: List[IntegratedTCO] = None):
        results = results or self.results
        print("\n" + "=" * 90)
        print(" P6 ExaFLOPS 통합 TCO 요약 (단위: $M)")
        print("=" * 90)
        header = f"{'System':12} {'SMR':12} {'Glass':10} {'CAPEX':>10} {'OPEX':>10} {'TCO':>10} {'$/EF':>10} {'Save':>8}"
        print(header)
        print("-" * 90)
        for r in results:
            print(f"{r.system_id:12} {r.smr_scenario:12} {r.glass_scenario:10} "
                  f"{r.total_capex_usd_m:>10,.0f} {r.total_opex_usd_m:>10,.0f} "
                  f"{r.total_tco_usd_m:>10,.0f} {r.tco_per_exaflops_usd_m:>10,.0f} "
                  f"{r.saving_vs_grid_only_usd_m:>8,.0f}")
        print("=" * 90)


# ────────────────────────────────────────
# CLI 엔트리포인트
# ────────────────────────────────────────

def parse_args():
    parser = argparse.ArgumentParser(description="P6 ExaFLOPS 통합 자원모델")
    parser.add_argument("--system",   default=None, help="시스템 ID 필터 (SYS_A/B/C)")
    parser.add_argument("--scenario", default=None,
                        choices=["grid_only", "smr_partial", "smr_full", "all"],
                        help="SMR 시나리오 선택")
    parser.add_argument("--glass",    default="base",
                        choices=["conservative", "base", "aggressive"],
                        help="Glass substrate 채택 시나리오")
    parser.add_argument("--dry-run",  action="store_true", help="Excel/JSON 미저장")
    parser.add_argument("--config",   default=None, help="설정 파일 경로")
    return parser.parse_args()


def main():
    args = parse_args()
    print("\n🚀 P6 ExaFLOPS 통합 자원모델 시작")
    print(f"   System: {args.system or 'ALL'} | SMR: {args.scenario or 'ALL'} | Glass: {args.glass}")
    print("-" * 60)

    model = ExaFLOPSResourceModel(config_path=args.config)

    smr_scenarios = None
    if args.scenario and args.scenario != "all":
        smr_scenarios = [args.scenario]

    results = model.run_all(
        system_filter=args.system,
        smr_scenarios=smr_scenarios,
        glass_scenarios=[args.glass],
    )

    model.print_summary(results)

    if not args.dry_run:
        model.to_excel(results)
        model.to_json(results)
        print("\n✅ P6 완료")
    else:
        print("\n[DRY RUN] 파일 저장 생략")

    return results


if __name__ == "__main__":
    main()
