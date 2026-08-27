# Imagem → PDF

Aplicativo Android (Python + Kivy) que converte imagens (JPG, JPEG,
PNG, WEBP) em um único arquivo PDF — **tudo processado localmente no
aparelho**, sem servidores ou APIs externas.

## Estrutura do projeto

```
imagem_pdf_app/
├── main.py                       # ponto de entrada
├── buildozer.spec                # configuração de build Android
├── requirements.txt              # dependências Python (dev)
├── screens/
│   └── main_screen.py            # tela principal (lógica)
├── widgets/
│   ├── rounded_button.py         # botão com cantos arredondados
│   └── image_card.py             # card de cada imagem selecionada
├── services/
│   ├── pdf_service.py            # geração do PDF (Pillow)
│   ├── image_picker_service.py   # seleção de imagens (plyer)
│   ├── share_service.py          # salvar/compartilhar (androidstorage4kivy)
│   ├── permissions_service.py    # permissões Android
│   └── ads_service.py            # AdMob (kivmob)
├── utils/
│   └── constants.py              # cores, textos e IDs de teste do AdMob
└── kv/
    └── main_screen.kv            # layout visual (Kivy Language)
```

## Bibliotecas usadas e por quê

| Necessidade                         | Biblioteca            |
|--------------------------------------|------------------------|
| Interface                           | Kivy                   |
| Geração do PDF localmente           | Pillow                 |
| Seletor nativo de imagens (múltiplo)| Plyer (`filechooser`)  |
| Chamadas a APIs nativas do Android  | PyJNIus                |
| Salvar em pasta pública / compartilhar (Scoped Storage + FileProvider automático) | `androidstorage4kivy` |
| Anúncios AdMob (banner + interstitial) | `kivmob`             |

`androidstorage4kivy` foi escolhido porque cuida automaticamente da
configuração do `FileProvider` (necessária para compartilhar PDFs com
o WhatsApp, Gmail, Telegram etc. em Android 7+), evitando edição
manual do `AndroidManifest.xml`.

## Como rodar em desenvolvimento (desktop, antes de gerar o APK)

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install kivy pillow plyer
python main.py
```

No desktop, a seleção de imagens usa a caixa de diálogo padrão do
sistema operacional e o compartilhamento/salvamento público é
simulado (apenas via `print`) — essas funções reais dependem de APIs
Android e só funcionam no aparelho/emulador.

## Como gerar o APK (build de teste/debug)

1. Instale o Buildozer (Linux ou WSL é o ambiente recomendado):
   ```bash
   pip install buildozer cython==0.29.36
   sudo apt install -y git zip unzip openjdk-17-jdk python3-pip \
       autoconf libtool pkg-config zlib1g-dev libncurses5-dev \
       libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
   ```
2. Dentro da pasta do projeto:
   ```bash
   buildozer -v android debug
   ```
3. O APK gerado ficará em `bin/imagemparapdf-1.0.0-arm64-v8a_armeabi-v7a-debug.apk`.
4. Instale no aparelho para testar:
   ```bash
   adb install -r bin/*.apk
   ```

## Como gerar o APK de release (assinado)

1. Gere uma keystore (uma única vez, guarde-a com segurança):
   ```bash
   keytool -genkey -v -keystore imagemparapdf.keystore \
       -alias imagemparapdf -keyalg RSA -keysize 2048 -validity 10000
   ```
2. Configure a assinatura no `buildozer.spec` (seção `[app]`), adicionando:
   ```ini
   android.release_artifact = apk
   ```
   E defina as variáveis de ambiente antes do build (não coloque a
   senha diretamente no `buildozer.spec`):
   ```bash
   export P4A_RELEASE_KEYSTORE=/caminho/para/imagemparapdf.keystore
   export P4A_RELEASE_KEYSTORE_PASSWD="sua_senha"
   export P4A_RELEASE_KEYALIAS=imagemparapdf
   export P4A_RELEASE_KEYALIAS_PASSWD="sua_senha"
   ```
3. Gere o release:
   ```bash
   buildozer -v android release
   ```
   O `.apk` assinado ficará em `bin/`.

## Como gerar o AAB (Android App Bundle) para a Google Play

A Google Play exige o formato `.aab` para novos apps:

```bash
android.release_artifact = aab
buildozer -v android release
```

O arquivo `.aab` assinado será gerado em `bin/`.

## Onde configurar versão e Application ID

No `buildozer.spec`:

```ini
package.domain = com.seudominio      # -> forma o Application ID: com.seudominio.imagemparapdf
package.name = imagemparapdf
version = 1.0.0
```

> **Atenção:** o `package.domain` + `package.name` (Application ID)
> **não pode ser alterado depois de publicado** na Google Play.
> Escolha-o com cuidado antes do primeiro envio.

## Trocando os IDs de teste do AdMob pelos IDs reais

Antes de publicar, troque os 3 valores a seguir:

1. **`utils/constants.py`**
   ```python
   ADMOB_APP_ID = "SEU_APP_ID_REAL"
   BANNER_AD_UNIT_ID = "SEU_BANNER_ID_REAL"
   INTERSTITIAL_AD_UNIT_ID = "SEU_INTERSTITIAL_ID_REAL"
   ```

2. **`buildozer.spec`** (meta-data do AndroidManifest):
   ```ini
   android.meta_data = com.google.android.gms.ads.APPLICATION_ID=SEU_APP_ID_REAL
   ```

Gere os IDs reais em https://apps.admob.com, dentro do seu app
cadastrado. **Nunca teste com os IDs reais** — use sempre os IDs de
teste durante o desenvolvimento, e só troque na build final antes de
enviar para a Google Play.

## Permissões solicitadas (e por quê)

- `READ_MEDIA_IMAGES` (Android 13+) / `READ_EXTERNAL_STORAGE` (versões
  anteriores): ler as imagens escolhidas na galeria.
- `WRITE_EXTERNAL_STORAGE`: necessário apenas em versões antigas do
  Android para salvar o PDF fora da pasta privada do app.
- `INTERNET` / `ACCESS_NETWORK_STATE`: exigidas pelo SDK do Google
  Mobile Ads (AdMob) para carregar os anúncios — não são usadas para
  a conversão de imagens em si, que continua 100% offline.

## Publicando na Google Play (checklist)

1. Crie a conta de desenvolvedor Google Play (taxa única).
2. Gere o `.aab` de release assinado (ver seção acima).
3. Configure a ficha da loja (nome, descrição, capturas de tela, ícone).
4. Preencha o questionário de classificação de conteúdo.
5. Preencha a seção "Segurança dos dados" — declare a coleta feita
   pelo AdMob (identificadores de publicidade).
6. Envie o `.aab` em uma faixa de teste interno antes da produção.
7. Depois de validado, promova para produção.
