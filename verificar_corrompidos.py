import os

# Caminho do site-packages do seu ambiente
site_packages_path = r"C:\Users\user\anaconda3\envs\streamlit-2025\Lib\site-packages"

# Lista tudo que está no site-packages
for item in os.listdir(site_packages_path):
    # Itens suspeitos: começam com ~ ou terminam com .dist-info estranho
    if item.startswith("~") or item.startswith("~treamlit"):
        print(f"[SUSPEITO] {item}")
