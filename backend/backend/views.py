from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Utilisateur


@csrf_exempt  # Temporaire pour les tests, à retirer en production
def register(request):
    if request.method == 'POST':
        try:
            # Pour requêtes POST JSON (recommandé)
            if request.content_type == 'application/json':
                import json
                data = json.loads(request.body)
            else:  # Pour données form-urlencoded
                data = request.POST

            # Création avec mot de passe hashé automatiquement
            Utilisateur.objects.create(
                nom=data.get('nom'),
                email=data.get('email'),
                # Sera hashé via la méthode save()
                motDePasse=data.get('password'),
                role=data.get('role', 'joueur')   # Valeur par défaut
            )
            return JsonResponse({"status": "success", "message": "Utilisateur créé"})

        except Exception as e:
            return JsonResponse(
                {"status": "error", "message": str(e)},
                status=400
            )

    return JsonResponse(
        {"status": "error", "message": "Méthode non autorisée"},
        status=405
    )
