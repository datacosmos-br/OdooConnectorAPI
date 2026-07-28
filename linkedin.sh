#!/bin/bash

# r_ads - AQStPvPHb2cdd3-ec0xckoCjkZV2B7NvhPDuW_XEpDdG6xisv60XmXIjQzTn141CEpL5fjMaQtjIl6cH4Js3jV1fTfyxai8eFHV-xJdYD55q9ytyaynSLgVIXStmaBEaKbDG_MYv74d7iEYIleKFrvxZ5aSZRup7T5kagHIFhezhKD-yUBDFJLNPoTLiRX2FssoTjkO9iwS9fbSeVNY
# r_ads_reporting  AQTeFlljC_kkB1HrdM_6GGnzICX4czu3EVPYeYQvcWHFdsVlMVMDHgAY2UP2-tG0wdiJwQHDUL87zAfbsipajczPfbfIDzh0h4pRDra8Berf1Rb8p6DTiOTv2k2pxxmyWjVhaxUD71JMQUiWvepGFjiwNqwvMwSeoWVd6yl92k32m9DyjacNw0GfigD_7-jwlGQ8cXyTNSkBwtPQIC0
# r_organization_admin AQSc6FHxL1tmcmSSc3dBMbxjfH3voCM6GPgdb1oR1nMjgXdcwjd1s-BY8Oz_25A4-bwldXhbt-MkNaT-yF_GBQ2Grt30WHHaa1jn5aR3sv8FiAPDKICLy-FbBmCJW637YEsh6hSRwc8sZ0pITk2yISpTC2v_6Q3DWUpzqaOItJ4ExtcUORc7UdQb1-ApK8E4NM7xzgDwesXmCiwVk2c
# r_organization_social AQSCZ6GuMgDo0PtgBasr58FktGpC7MAx6JuH0OHhzhMsA6HImAG5VZZIKKRycb4ny10DyuMTnaWCvstDOblc5yQHYS9x850DfP3sJBbxzQkrchrJamvC-Y_MWqHDXiko6RLRb6mKImabp3GXyZCQAPzDLr2ZDodlVHZDh2UCsojtaNkGEHWKxvTKrXeIjGlORN-AB6__z7rZ5BdGN5M
# rw_ads AQQcl1aGHRXfBGxFuuWhkt1SGhRgU9C7yLwjAUu0VnprQxu9TeMkV4t8Z0pST3jX5uHksoC-a27aHvAiJCDtI2K7ZauALM0kuDGBdU3VYxJAuVR51-NQh76ai1w35woxSq4T3lyBzdXJLfVbdp_iQ5T8YBa5YlFIZVRtA90kscDlta69JSdHBcbdiCK1ced2X1YzRpgfViDzenqzuX8
# rw_organization_admin AQTKujajM6zcEoq7BGijmHVa0dU7ctMPEAyJyaTsQGSTcha9CcwNpIWJH8C56e6FmcJa5GIQUSlbp-MR0aM5h4auBGliSMzucpk-ZrrHmcOPrB0rqWfjnupjJ5bs5EKqXT2igOfJhnEtowo2vDDxRQBOCTMcGaFNCN8PJUUPT2TGy321HLe2TqOtj7roKvEkZgmm5JmcSARfJRWWM7Y
# w_member_social AQTr9j8yEY2VSIxqdIHtlqklenjXuf7hicn0V9SRfNZHR9VaKpisccotSMGk996XhJGD3R6jv9RkIxVQPa7ij_N_TQGxYWS5spsIFPcJ9IlMyAwdTimPamxzjnPRf_zB2eBggBQ9Ej0CqOIuoxXfnDL_VryzwV3FMYoqtM0x0MfvfwvtIybNdMHQ0eBHAjNjud4l6e_uGFPhoh8u8Ds
# w_organization_social - marlon.costa@datacosmos.com.br - AQQOpWHPoWNKqL8RPZq7sxpNMrkSp6zQmZADy2NCIJfAiuU3Sz-ss1gC55avqkPY6X_p9i7xtcA16BgNXbUgB1rkEz5A2ILYuSNGjsJv3r4G1mUDwDF4I7fh-ipHzzLyfKCTMU5WM4CvgRygeWIBn5AK_BWV4S96XyO5LeP--FQlqEizpdNaLGU7gMSSyQdByOCxuSFCo8xH6Pa_WdM

echo "Script para obter o Access Token do LinkedIn e fazer uma chamada de API."

# Variáveis necessárias
client_id="77dez837cubhff"
client_secret="iKejMK0ys7BTsjSv"
redirect_uri="https://datacosmos.com.br"
scope="r_organization_admin" # Modifique conforme necessário

# Passo 1: Instrução para obter o código de autorização
authorization_url="https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=$client_id&redirect_uri=$redirect_uri&scope=$scope"
echo "Primeiro, você precisa obter um código de autorização. Acesse o seguinte URL em seu navegador:"
echo $authorization_url
echo "Depois de autorizar o aplicativo, você será redirecionado. Copie o código de autorização da URL."

# Usuário insere o código de autorização
read -p "Insira o código de autorização aqui: " authorization_code

# Passo 2: Trocar o código de autorização por um token de acesso
access_token_url="https://www.linkedin.com/oauth/v2/accessToken"
response=$(curl -s --request POST --url $access_token_url \
--header "Content-Type: application/x-www-form-urlencoded" \
--data-urlencode "grant_type=authorization_code" \
--data-urlencode "code=$authorization_code" \
--data-urlencode "redirect_uri=$redirect_uri" \
--data-urlencode "client_id=$client_id" \
--data-urlencode "client_secret=$client_secret")

# Extrair o token de acesso da resposta
access_token=$(echo $response | jq -r '.access_token')

if [ "$access_token" != "null" ]; then
  echo "Token de acesso obtido com sucesso!"

  # Passo 3: Fazer uma chamada de API usando o token de acesso
  api_url="https://api.linkedin.com/v2/me"
  api_response=$(curl -s --request GET --url $api_url --header "Authorization: Bearer $access_token")

  echo "Resposta da API do LinkedIn:"
  echo $api_response
else
  echo "Falha ao obter o token de acesso. Verifique os detalhes e tente novamente."
fi
