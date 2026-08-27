[app]

# ---------------------------------------------------------------------------
# INFORMAÇÕES BÁSICAS DO APP
# ---------------------------------------------------------------------------
title = Imagem para PDF
package.name = imagemparapdf

# Altere para um domínio/identificador único seu antes de publicar
# (ex.: com.suaempresa.imagemparapdf). Não altere depois de publicar
# na Google Play — o package name é definitivo.
package.domain = com.seudominio

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,webp

version = 1.0.0

requirements = python3,kivy==2.3.0,pillow,plyer,pyjnius,androidstorage4kivy,kivmob

# ---------------------------------------------------------------------------
# ÍCONES E TELA DE ABERTURA (opcional — adicione seus arquivos em assets/)
# ---------------------------------------------------------------------------
# icon.filename = %(source.dir)s/assets/icon.png
# presplash.filename = %(source.dir)s/assets/presplash.png

orientation = portrait
fullscreen = 0

# ---------------------------------------------------------------------------
# PERMISSÕES ANDROID (apenas as estritamente necessárias)
# ---------------------------------------------------------------------------
# READ_MEDIA_IMAGES  -> Android 13+ (API 33+)
# READ_EXTERNAL_STORAGE / WRITE_EXTERNAL_STORAGE -> Android < 13
# INTERNET / ACCESS_NETWORK_STATE -> exigidos pelo SDK do AdMob para
# carregar os anúncios.
android.permissions = READ_MEDIA_IMAGES,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,INTERNET,ACCESS_NETWORK_STATE

# ---------------------------------------------------------------------------
# ADMOB APP ID
# ---------------------------------------------------------------------------
# O SDK do AdMob exige que o ADMOB_APP_ID esteja declarado como
# meta-data no AndroidManifest.xml. O valor abaixo é o ID DE TESTE
# oficial do Google.
#
# >>> TROQUE AQUI pelo seu ADMOB_APP_ID real antes de publicar <<<
android.meta_data = com.google.android.gms.ads.APPLICATION_ID=ca-app-pub-3940256099942544~3347511713

# ---------------------------------------------------------------------------
# CONFIGURAÇÃO ANDROID / SDK / ARQUITETURAS
# ---------------------------------------------------------------------------
android.api = 34
android.minapi = 24
android.ndk = 25b
android.archs = arm64-v8a,armeabi-v7a
android.accept_sdk_license = True

# Necessário para o SDK do Google Play Services (AdMob).
android.gradle_dependencies = com.google.android.gms:play-services-ads:23.0.0

# AndroidX é exigido pelas bibliotecas modernas (AdMob, androidstorage4kivy).
android.enable_androidx = True

[buildozer]
log_level = 2
warn_on_root = 1
