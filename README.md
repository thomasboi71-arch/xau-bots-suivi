# Suivi public — bots XAU (démo)

Page de suivi en lecture seule pour 3 bots de trading tournant en compte
démo (aucun argent réel) : Claude V1, Claude V2 (NU5, candidat forward non
prouvé) et Donchian.

Publiée via GitHub Pages : https://thomasboi71-arch.github.io/xau-bots-suivi/

`index.html` est régénéré périodiquement par `generate.py`, qui lit le
panneau de contrôle local (`127.0.0.1:8765`, jamais accessible depuis
Internet) et republie un instantané — numéros de compte retirés, soldes et
historique des trades conservés.

Aucune action possible depuis cette page : c'est un instantané statique, pas
un accès au panneau local.
