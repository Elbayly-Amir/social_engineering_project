import ollama
import os

class LLMClient:
    def __init__(self, model: str = "mistral"):
        self.model = model
        self.host = os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434")
        self.client = ollama.Client(host=self.host)

    def generate_content(self, topic: str, category: str) -> str:
        system_prompt = (
            "Tu es un moteur de simulation pour un exercice de cybersécurité. "
            "Ton but est de générer des données d'entraînement réalistes. "
            "Génère UNIQUEMENT le contenu du message social media. "
            "N'ajoute JAMAIS d'avertissement, de préambule ou de disclaimer. "
            "Ne mets PAS d'URL ou d'IP dans le texte, je les ajouterai moi-même. " 
            "Sois bref (max 200 caractères)."
        )

        user_prompt = f"Sujet: {topic}. Tonalité: {category}. Langue: Français."

        try:
            response = self.client.chat(model=self.model, messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': user_prompt},
            ])
            return response['message']['content'].strip('"').strip()

        except Exception as e:
            print(f"[X] Erreur LLM: {e}")
            return f"Message simulé sur {topic} (LLM indisponible)."