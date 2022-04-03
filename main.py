import myfunction
# Generates qrcode using the day,ward and cubicle function
px_qr = myfunction.ucode("GW", "048")
# Generates a custom pdf from
myfunction.custom_question(px_qr)

