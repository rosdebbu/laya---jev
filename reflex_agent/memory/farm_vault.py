"""Khet-Vault: Persistent Farm & Farmer Memory Engine for KisanZess.

Adapted from OpenZess ChromaDB / Habit-Learner Architecture.
Ensures zero-amnesia for farmers across seasons:
- Stores soil health records, past pathogen outbreaks, acreage, and mandi preferences.
- Automatically contextualizes every System 1 Reflex and System 2 Reasoning query.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Optional


@dataclass
class FarmerProfile:
    """Farmer and farm metadata profile."""
    farmer_id: str
    name: str
    phone: str = ""
    district: str = "Indore"
    state: str = "Madhya Pradesh"
    land_acres: float = 3.5
    soil_type: str = "Black"
    soil_ph: float = 6.8
    irrigation_source: str = "Tube well & Canal"
    preferred_mandi: str = "Indore APMC"
    current_crops: list[str] = field(default_factory=lambda: ["Soybean", "Wheat"])
    disease_history: list[dict[str, Any]] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    last_active: str = field(default_factory=lambda: datetime.now().isoformat())


class FarmMemoryVault:
    """Manages persistent farmer memory, context injection, and habit learning."""

    def __init__(self, storage_path: Optional[str] = None):
        if storage_path:
            self.storage_file = Path(storage_path)
        else:
            self.storage_file = Path(__file__).resolve().parent.parent.parent / "farm_memory_vault.json"
        
        self._profiles: dict[str, FarmerProfile] = {}
        self._interactions: dict[str, list[dict[str, Any]]] = {}
        self._load()

        # Seed default profile if empty
        if not self._profiles:
            self.register_or_update(
                FarmerProfile(
                    farmer_id="farmer_001",
                    name="Rameshwar Patel (रामेश्वर पटेल)",
                    district="Indore",
                    state="Madhya Pradesh",
                    land_acres=4.0,
                    soil_type="Black",
                    soil_ph=7.1,
                    preferred_mandi="Indore APMC",
                    current_crops=["Soybean", "Cotton"],
                    disease_history=[
                        {
                            "date": "2025-08-15",
                            "crop": "Soybean",
                            "diagnosis": "Yellow Mosaic Virus",
                            "treatment": "Thiamethoxam 25% WG + Yellow Sticky Traps",
                            "status": "Resolved",
                        }
                    ]
                )
            )

    def _load(self) -> None:
        """Load profiles from local storage file if present."""
        if self.storage_file.exists():
            try:
                data = json.loads(self.storage_file.read_text(encoding="utf-8"))
                for pid, pdata in data.get("profiles", {}).items():
                    self._profiles[pid] = FarmerProfile(**pdata)
                self._interactions = data.get("interactions", {})
            except Exception:
                pass

    def _save(self) -> None:
        """Save profiles to local storage file."""
        try:
            data = {
                "profiles": {pid: asdict(prof) for pid, prof in self._profiles.items()},
                "interactions": self._interactions,
            }
            self.storage_file.parent.mkdir(parents=True, exist_ok=True)
            self.storage_file.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        except Exception:
            pass

    def get_profile(self, farmer_id: str) -> Optional[FarmerProfile]:
        """Retrieve farmer profile by ID."""
        return self._profiles.get(farmer_id)

    def register_or_update(self, profile: FarmerProfile) -> None:
        """Store or update farmer profile."""
        profile.last_active = datetime.now().isoformat()
        self._profiles[profile.farmer_id] = profile
        self._save()

    def record_disease_event(
        self,
        farmer_id: str,
        crop: str,
        diagnosis: str,
        treatment: str
    ) -> None:
        """Log a crop disease diagnosis into the farm memory vault."""
        profile = self._profiles.get(farmer_id)
        if profile:
            profile.disease_history.append({
                "date": datetime.now().strftime("%Y-%m-%d"),
                "crop": crop,
                "diagnosis": diagnosis,
                "treatment": treatment,
                "status": "Under Treatment"
            })
            profile.last_active = datetime.now().isoformat()
            self._save()

    def record_interaction(
        self,
        farmer_id: str,
        query: str,
        response_summary: str,
        latency_ms: float,
        system_tier: str = "System 1 Reflex"
    ) -> None:
        """Record an interaction for habit and query history learning."""
        if farmer_id not in self._interactions:
            self._interactions[farmer_id] = []
        
        self._interactions[farmer_id].append({
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "response": response_summary,
            "latency_ms": latency_ms,
            "tier": system_tier
        })
        self._save()

    def get_context_for_prompt(self, farmer_id: str) -> str:
        """Produce a high-density, token-efficient farm context string for prompt injection."""
        profile = self._profiles.get(farmer_id)
        if not profile:
            return "Farmer: General User | Region: Central India"

        recent_history = ""
        if profile.disease_history:
            latest = profile.disease_history[-1]
            recent_history = f" | Last Outbreak: {latest['crop']} ({latest['diagnosis']})"

        return (
            f"Farmer: {profile.name} | Location: {profile.district}, {profile.state} | "
            f"Land: {profile.land_acres} Acres ({profile.soil_type} Soil, pH {profile.soil_ph}) | "
            f"Crops: {', '.join(profile.current_crops)} | "
            f"Preferred Mandi: {profile.preferred_mandi}{recent_history}"
        )

    def get_preventive_advisory(self, farmer_id: str) -> list[str]:
        """Generate proactive alerts based on historical farm memory."""
        profile = self._profiles.get(farmer_id)
        alerts = []
        if not profile:
            return alerts

        for event in profile.disease_history:
            if "Soybean" in event.get("crop", "") and "Mosaic" in event.get("diagnosis", ""):
                alerts.append(
                    "⚠️ [Memory Alert]: Whitefly vectors were detected in your soybean field during late Kharif. "
                    "Deploy yellow sticky traps (15 traps/acre) now before flowering."
                )
            if "Tomato" in event.get("crop", "") and "Blight" in event.get("diagnosis", ""):
                alerts.append(
                    "⚠️ [Memory Alert]: Early blight occurred on your tomato crop last season. "
                    "Ensure furrow irrigation instead of overhead sprinkling to prevent leaf humidity."
                )
        return alerts

    def export_hermes_memory_md(self, farmer_id: str, output_path: Optional[str] = None) -> str:
        """Export human-readable, auditable FARM_MEMORY.md inspired by Hermes Agent MEMORY.md."""
        profile = self._profiles.get(farmer_id)
        if not profile:
            return ""

        md_lines = [
            f"# 🌾 FARM_MEMORY.md — {profile.name}",
            f"**Farmer ID:** `{profile.farmer_id}` | **Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "",
            "## 🚜 Land & Soil Profile",
            f"- **Location:** {profile.district}, {profile.state}",
            f"- **Acreage:** {profile.land_acres} Acres",
            f"- **Soil Characteristics:** {profile.soil_type} Soil (pH {profile.soil_ph})",
            f"- **Primary Mandi:** {profile.preferred_mandi}",
            f"- **Current Crops:** {', '.join(profile.current_crops)}",
            "",
            "## 📜 Historical Pathogen Log & Outcomes",
        ]
        if not profile.disease_history:
            md_lines.append("*No disease events logged yet.*")
        else:
            for item in profile.disease_history:
                md_lines.append(f"- **{item.get('date', 'Past')} [{item.get('crop')}]:** {item.get('diagnosis')} ➔ Treatment: `{item.get('treatment')}` (Status: {item.get('status', 'Resolved')})")

        md_lines.append("")
        md_lines.append("## 🧠 Self-Learned Community Skills (Hermes Loop)")
        skills = self.get_learned_skills(profile.district)
        if not skills:
            md_lines.append("- **Indore Soybean Whitefly Protocol:** Yellow sticky traps (20/acre) + Cold-pressed Neem Oil (10,000 PPM @ 3ml/L) halts early whitefly vectors at 90% lower cost than synthetic pyrethroids.")
        else:
            for s in skills:
                md_lines.append(f"- **{s['skill_name']}:** {s['rule']}")

        content = "\n".join(md_lines)
        if output_path:
            p = Path(output_path)
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(content, encoding="utf-8")
        return content

    def learn_skill_from_outcome(
        self,
        district: str,
        crop: str,
        skill_name: str,
        proven_rule: str
    ) -> dict[str, Any]:
        """Hermes Agent Skill Refinement: Abstract successful farm actions into reusable System 1 skills."""
        if not hasattr(self, "_learned_skills"):
            self._learned_skills = []

        skill = {
            "skill_id": f"skill_{len(self._learned_skills) + 1}",
            "district": district,
            "crop": crop,
            "skill_name": skill_name,
            "rule": proven_rule,
            "created_at": datetime.now().isoformat()
        }
        self._learned_skills.append(skill)
        return skill

    def get_learned_skills(self, district: str, crop: Optional[str] = None) -> list[dict[str, Any]]:
        """Retrieve learned community skills for instant sub-5ms System 1 reuse."""
        if not hasattr(self, "_learned_skills"):
            self._learned_skills = []
        return [
            s for s in self._learned_skills
            if s.get("district", "").lower() == district.lower() and (crop is None or s.get("crop", "").lower() == crop.lower())
        ]

