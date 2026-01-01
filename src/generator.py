import json
import random
import os
from faker import Faker
from src.models import SocialMediaPost, SocialMediaUser
from src.llm_client import LLMClient
class ThreatGenerator:
    def __init__(self, scenario_file: str = "scenarios.json"):
        self.fake = Faker()
        self.scenarios = self._load_scenarios(scenario_file)
        self.llm_client = LLMClient()

    def _load_scenarios(self, path: str) -> list:
        """Charge les scénarios depuis le JSON"""
        if not os.path.exists(path):
            print(f"[WARN] Scénarios introuvables ({path}). Mode aléatoire activé.")
            return []
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get("scenarios", [])
        except Exception as e:
            print(f"[X] Erreur lecture scénarios : {e}")
            return []

    def _generate_user(self) -> SocialMediaUser:
        """(Méthode inchangée, garde ton code existant ici)"""
        return SocialMediaUser(
            pseudo=f"@{self.fake.user_name()}",
            average_daily_posts=random.uniform(0.1, 10.0),
            reputation_score=random.randint(0, 100)
        )

    def _pick_scenario(self):
        """Choisit un scénario selon les probabilités (poids)"""
        if not self.scenarios:
            return None
        
        weights = [s.get("weight", 1.0) for s in self.scenarios]
        selected_scenario = random.choices(self.scenarios, weights=weights, k=1)[0]
        return selected_scenario

    def _generate_dynamic_content(self, template: str) -> str:
        """Remplit les trous {url}, {bank} avec de fausses données"""

        return template.format(
            url=f"http://{self.fake.domain_name()}/{self.fake.uri_path()}",
            domain=self.fake.domain_name(),
            bank=self.fake.random_element(["Chase", "BNP", "Société Générale"]),
            company=self.fake.company(),
            project_name=self.fake.bs().split(" ")[0],
            ip=self.fake.ipv4(),
            hash=self.fake.sha256()
        )

    def generate_posts(self, count: int = 10) -> list[SocialMediaPost]:
            posts = []
            print(f"   [*] Génération de {count} posts (Mode IA Hybride)...")

            for _ in range(count):
                scenario = self._pick_scenario()
                
                if scenario:
                    if "ai_topic" in scenario:
                        base_content = self.llm_client.generate_content(
                            topic=scenario["ai_topic"],
                            category=scenario["category"]
                        )
                    else:
                        base_content = self.fake.text()

                    malicious_link = f" http://{self.fake.domain_name()}/{self.fake.uri_path()}"
                    malicious_ip = f" (IP: {self.fake.ipv4()})"
                    full_content = f"{base_content} {malicious_link} {malicious_ip}"
                    
                else:
                    full_content = self.fake.text()

                post = SocialMediaPost(
                    platform=self.fake.random_element(elements=("Twitter", "BlueSky", "Mastodon")),
                    author=self._generate_user(),
                    content=full_content,
                    created_at=self.fake.date_time_between(start_date="-1h", end_date="now")
                )
                posts.append(post)
                
            return posts