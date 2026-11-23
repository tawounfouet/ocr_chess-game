# P4 OpenClassrooms - R00-R01 - Compte rendu d'implémentation et validation

**Date :** 23 novembre 2026
**Projet :** Chess Tournament Manager
**Dépôt :** https://github.com/tawounfouet/ocr_chess-game
**Branche :** recovery/p4-r00-r01
**Commit source main :** 43a9910ec3ae0ab6651519ac8e2d5c5ecb3e4c3b
**Pull Request en brouillon :** https://github.com/tawounfouet/ocr_chess-game/pull/1
**Statut R01 :** PASS en CI
**Statut R00 :** PARTIEL - conservation de la référence Git distante vérifiée ; sauvegarde des fichiers locaux du Mac à effectuer.

## 1. Modifications livrées

| Fichier | Résultat |
|---|---|
| controllers/app.py | Imports portables, sans dépendance au dossier parent |
| views/view_app.py | Choix principaux 1, 2, 4 ; sortie cohérente |
| controllers/tournament.py | Choix 6 : retour ; choix 4 : consultation puis maintien dans le menu tournoi |
| views/tournament.py | UUID transmis depuis input, recherches par UUID, affichages défensifs de données historiques |
| requirements.txt | Ajout de rich==13.5.2 |
| tests/test_navigation.py | 13 tests unitaires et d'intégration |
| .github/workflows/p4-r00-r01.yml | Exécution automatisée des tests sur Python 3.12 |

Une modification de périmètre a été retenue : le workflow CI a été ajouté pour pouvoir valider réellement les tests sans dépendre de la machine locale.

Aucun changement apporté aux fichiers models/*.py, data/*.json, .venv, __pycache__ ou aux fichiers .pyc suivis.

## 2. Résultat des tests

**Run GitHub Actions :** https://github.com/tawounfouet/ocr_chess-game/actions/runs/45139722832

**Job :** navigation-tests - Ubuntu / Python 3.12
**Commande :** PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s tests -v
**Sortie confirmée :** Ran 13 tests in 0.579s ; OK

| ID | Cas testé | Statut |
|---|---|---|
| NAV-T01 | Sortie du menu principal via 4 | PASS |
| NAV-T02 | Option cachée 3 refusée au menu principal | PASS |
| NAV-T03 | Retour du menu joueurs via 5 | PASS |
| NAV-T04 | Retour du menu tournois via 6 | PASS |
| NAV-T05 | Option cachée 5 refusée au menu tournois | PASS |
| NAV-T06 | Saisie UUID retournée et nettoyée | PASS |
| NAV-T07 | Consultation d'un tournoi existant par UUID | PASS |
| NAV-T08 | UUID absent dans les détails sans exception | PASS |
| NAV-T09 | Consultation des rondes par UUID et maintien du menu | PASS |
| NAV-T10 | UUID absent dans les rondes sans exception | PASS |
| NAV-T11 | Navigation de bout en bout et sortie normale | PASS |
| NAV-T12 | Aucun octet modifié dans les deux JSON après consultations | PASS |
| NAV-T13 | Démarrage depuis un répertoire de travail indépendant | PASS |

Les fichiers de données originaux du dépôt conservent leurs SHA Git :
- data/players.json : 3132ef28ee7122e74b227445be7d873ceb6d21e7
- data/tournaments.json : bfb5ca516a7fefb75c99ccf796f139d4dcf96bf4

## 3. R00 - Ce qui a été réalisé et ce qui reste

| Tâche | Statut |
|---|---|
| Identifier le commit main et les JSON historiques publiés | PASS |
| Créer la branche distante recovery/p4-r00-r01 | PASS |
| Travailler sans modifier main | PASS |
| Installer l'environnement propre et isoler les données dans GitHub Actions | PASS |
| Inventorier le git status et les fichiers non suivis du Mac | À faire localement |
| Sauvegarder les modifications locales, le bundle Git et CODEBASE_ANALYSIS.md | À faire localement |
| Cloner la branche dans un nouveau répertoire sur le Mac | À faire localement |

Le dépôt original sur le Mac comprend des fichiers modifiés non commités et un fichier views/base.py historiquement non suivi. Le connecteur GitHub ne donne pas accès à ces changements locaux. Aucun reset, pull ou nettoyage n'a été effectué sur ce dossier.

## 4. Procédure locale non destructive

Depuis le dossier historique chess_game, avant de mettre à jour quoi que ce soit :

~~~bash
pwd
git remote -v
git status --short --untracked-files=all
git rev-parse HEAD

BACKUP_DIR="$(mktemp -d /tmp/p4-original-archive.XXXXXX)"
git diff --binary > "$BACKUP_DIR/working-tree.patch"
git diff --cached --binary > "$BACKUP_DIR/index.patch"
git bundle create "$BACKUP_DIR/repository.bundle" --all
git bundle verify "$BACKUP_DIR/repository.bundle"
mkdir -p "$BACKUP_DIR/snapshot"
rsync -a --exclude='.git/' --exclude='.venv/' \
  --exclude='__pycache__/' --exclude='*.pyc' \
  ./ "$BACKUP_DIR/snapshot/"
echo "$BACKUP_DIR"
~~~

Vérifier que les fichiers non suivis et les documents Markdown sont bien présents dans snapshot. La sauvegarde doit ensuite être conservée dans un emplacement durable, et non uniquement dans un répertoire temporaire.

Depuis un autre dossier, cloner la branche de reprise :

~~~bash
git clone --branch recovery/p4-r00-r01 --single-branch \
  https://github.com/tawounfouet/ocr_chess-game.git chess_game_r00_r01
cd chess_game_r00_r01
python3 -m venv ../p4_r00_r01_env
../p4_r00_r01_env/bin/python -m pip install -r requirements.txt
PYTHONDONTWRITEBYTECODE=1 ../p4_r00_r01_env/bin/python \
  -m unittest discover -s tests -v
~~~

Ne pas lancer de création de joueur ou de tournoi avec les bases historiques.

## 5. Périmètre non implémenté

- R02 : insertion des joueurs, conversion des identifiants TinyDB.
- R03-R04 : modèles, sérialisation et mise à jour persistante des tournois.
- R05-R08 : tableaux de résultats, scores, machine à états et appariements.
- R09-R16 : rapports, qualité et livrables de soutenance.

**Décision :** R01 est techniquement validé en CI. Avant fusion ou nouvelle modification du dossier local, terminer R00-02 sur le Mac et revoir la PR. Aucun merge automatique vers main n'a été réalisé.
