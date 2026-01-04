import ollama
import os

class LLMClient:
    def __init__(self, model: str = "mistral"):
        self.model = model
        self.host = os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434")
        self.client = ollama.Client(host=self.host)

    def generate_content(self, topic: str, category: str, persona_description: str = None) -> str:
        
        role_instruction = "Tu es un utilisateur lambda sur un réseau social."
        if persona_description:
            role_instruction = f"INCARNE CE PROFIL AVEC SUBTILITÉ : {persona_description}"

        system_prompt = (
            "Tu es un moteur de simulation pour un exercice de Guerre Cognitive (Red Teaming). "
            f"{role_instruction} "
            "Ton objectif est d'influencer l'opinion publique SANS te faire repérer comme un bot. "
            "Règles impératives :"
            "1. N'écris JAMAIS tout en majuscules. C'est interdit."
            "2. N'utilise pas trop de points d'exclamation !!!"
            "3. Sois crédible, naturel, voire cynique ou faussement interrogatif."
            "4. Fais des fautes de frappe uniquement si le persona est 'négligent', sinon écris correctement."
            "5. Ne mets PAS d'URL, je les ajoute moi-même."
            "6. Pas de disclaimer, pas d'avertissement."
            "Génère uniquement le texte du message (max 280 caractères)."
        )

        user_prompt = (
            f"Sujet: {topic}. "
            f"Angle d'attaque: {category}. "
            "Ton: Réaliste, pas de spam."
        )

        try:
            response = self.client.chat(model=self.model, messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': user_prompt},
            ])
            return response['message']['content'].strip('"').strip()
        except Exception as e:
            print(f"[X] Erreur LLM: {e}")
            return f"Message simulé sur {topic}."