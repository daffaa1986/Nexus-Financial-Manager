"""
Bank Detector
==============
Mendeteksi jenis bank dari teks mutasi rekening.
"""


def detect_bank(teks_mentah):
    """Auto-detect bank from statement text."""
    teks_upper = teks_mentah.upper()
    
    if 'BCA' in teks_upper or 'BANK CENTRAL ASIA' in teks_upper:
        return 'BCA'
    if 'MANDIRI' in teks_upper or 'BANK MANDIRI' in teks_upper:
        return 'MANDIRI'
    if 'BRI' in teks_upper or 'BANK RAKYAT' in teks_upper:
        return 'BRI'
    if 'BNI' in teks_upper or 'BANK NEGARA' in teks_upper:
        return 'BNI'
    if 'BSI' in teks_upper or 'BANK SYARIAH' in teks_upper:
        return 'BSI'
    
    return 'BCA'
