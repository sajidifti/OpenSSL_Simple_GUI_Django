from OpenSSL import crypto

def cert_gen(
    emailAddress="admin@example.com",
    commonName="example.com",
    countryName="BD",
    localityName="AFTABNAGAR",
    stateOrProvinceName="DHK",
    organizationName="EWUBD",
    organizationUnitName="ADMIN",
    serialNumber=0,
    validityEndInSeconds=365*24*60*60,
    algoType="TYPE_RSA",
    hashType="sha512",
    bitlength=4096,
    KEY_FILE = r"server.key",
    CERT_FILE= r"ca.crt"):

    # Key Pair
    k = crypto.PKey()

    if algoType == "TYPE_RSA":
        k.generate_key(crypto.TYPE_RSA, bitlength)
    if algoType == "TYPE_DSA":
        k.generate_key(crypto.TYPE_DSA, bitlength)
    
    # create a self-signed cert
    cert = crypto.X509()
    cert.get_subject().C = countryName
    cert.get_subject().ST = stateOrProvinceName
    cert.get_subject().L = localityName
    cert.get_subject().O = organizationName
    cert.get_subject().OU = organizationUnitName
    cert.get_subject().CN = commonName
    cert.get_subject().emailAddress = emailAddress
    cert.set_serial_number(serialNumber)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(validityEndInSeconds)
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(k)
    cert.sign(k, hashType)

    with open(CERT_FILE, "wt") as f:
        f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert).decode("utf-8"))
    with open(KEY_FILE, "wt") as f:
        f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, k).decode("utf-8"))