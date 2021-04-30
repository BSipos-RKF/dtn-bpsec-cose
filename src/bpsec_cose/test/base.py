''' Common test behavior.
'''
import unittest
import cbor2
from bpsec_cose.bp import EndpointId
from bpsec_cose.bpsec import SecurityBlockData
from bpsec_cose.util import decode_protected, encode_diagnostic


class BaseTest(unittest.TestCase):

    def _get_primary_item(self):
        return [
            7,
            0,
            0,
            EndpointId('dtn://dst/svc').encode_item(),
            EndpointId('dtn://src/').encode_item(),
            EndpointId('dtn://src/').encode_item(),
            [0, 40],
            1000000
        ]

    def _get_target_item(self):
        return [
            1,  # type code: payload
            1,  # always #1
            0,
            0,
            cbor2.dumps("hello")
        ]

    def _block_identity(self, item):
        ''' Block identity is the first three fields of canonical block array.
        '''
        return item[:3]

    def _get_aad_item(self, addl_protected:bytes=b''):
        ''' Get the AAD-structure item.

        :param addl_protected: The additional-protected parameters encoded.
        '''
        return [
            self._get_primary_item(),  # primary-ctx
            self._block_identity(self._get_target_item()),  # target-ctx
            None,  # asb-ctx
            addl_protected,
        ]

    def _get_asb_item(self, result):
        return SecurityBlockData(
            targets=[1],
            context_id=0,  # TBD
            security_source=EndpointId('dtn://src/').encode_item(),
            parameters=[
                [5, 0x03],
            ],
            results=[
                [  # target block #1
                    result,
                ],
            ],
        ).encode_item()

    def _get_asb_enc(self, asb_dec):
        ''' Encode ASB array as unframed CBOR sequence.
        '''
        return b''.join(cbor2.dumps(item) for item in asb_dec)

    def _get_bpsec_item(self, block_type, asb_dec=None):
        return [
            block_type,
            3,
            0,
            0,
            self._get_asb_enc(asb_dec or [])
        ]

    def _assemble_bundle(self, blocks_enc):
        return b'\x9f' + b''.join(blocks_enc) + b'\xff'

    def _print_headers(self, item, name: str):
        ''' Print COSE Headers from a decoded item.
        '''
        phdr_enc = item[0]
        phdr_dec = decode_protected(phdr_enc)
        uhdr_dec = item[1]
        print('{} Protected: {}'.format(name, encode_diagnostic(phdr_dec)))
        print('{} Encoded: {}'.format(name, encode_diagnostic(phdr_enc)))
        print('{} Unprotected: {}'.format(name, encode_diagnostic(uhdr_dec)))

    def _print_message(self, item, recipient_idx=None):
        ''' Print a top-level COSE message.
        '''
        print('Message: {}'.format(encode_diagnostic(item)))
        self._print_headers(item, 'Layer-1')
        if recipient_idx and recipient_idx in item:
            for (ix, rcpt) in enumerate(item[recipient_idx]):
                self._print_headers(rcpt, 'Layer-2 #{}'.format(ix))
