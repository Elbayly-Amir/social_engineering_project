import re

class IndicatorManager:
    def __init__(self):
        # Dictionnaire des motifs à rechercher
        # Clé = Type STIX (approximatif pour notre usage interne), Valeur = Regex
        self.patterns = {
            "Domain-Name": r"https?://([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})",
            "IPv4-Addr": r"\b(?:\d{1,3}\.){3}\d{1,3}\b", # Détecte X.X.X.X
            "File-Hash-MD5": r"\b[a-fA-F0-9]{32}\b",     # 32 hex chars
            "File-Hash-SHA256": r"\b[a-fA-F0-9]{64}\b"   # 64 hex chars
        }

    def extract_indicators(self, content: str) -> list[dict]:
        """
        Scan le texte et retourne une liste d'indicateurs STIX potentiels.
        """
        indicators = []
        
        for stix_type, regex in self.patterns.items():
            matches = re.findall(regex, content)
            
            for match in set(matches):
                # Nettoyage spécifique pour les domaines (retirer slash final)
                clean_value = match.rstrip("/")
                
                # Pour les IPs, on pourrait valider que chaque bloc est <= 255
                # mais restons simples pour l'instant.
                
                indicators.append({
                    "type": stix_type,
                    "value": clean_value
                })
            
        return indicators