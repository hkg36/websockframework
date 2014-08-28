import apnsclient
import OpenSSL.crypto
import apnsclient.certificate

class P12Certificate(apnsclient.certificate.BaseCertificate):
    def  load_context(self, cert_string=None, cert_file=None, key_string=None, key_file=None, passphrase=None):
        context = OpenSSL.SSL.Context(OpenSSL.SSL.SSLv3_METHOD)
        p12=OpenSSL.crypto.load_pkcs12(file(cert_file,'rb').read(),passphrase)
        cert =p12.get_certificate()
        context.use_certificate(cert)
        key=p12.get_privatekey()
        context.use_privatekey(key)
        context.check_privatekey()
        return context, cert
    def dump_certificate(self, raw_certificate):
        return OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM, raw_certificate)
    def dump_digest(self, raw_certificate, digest):
        return raw_certificate.digest(digest)
