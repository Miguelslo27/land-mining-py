echo | openssl s_client -servername tributos.imcanelones.gub.uy -connect tributos.imcanelones.gub.uy:8443 |\
sed -ne '/-BEGIN CERTIFICATE-/,/-END CERTIFICATE-/p' > imc.crt