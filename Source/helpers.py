def phone_filter(phones, minSize, maxSize, OS, camera, SIM, multitouch, NFC, year):

    # Filter by size.
    if minSize and maxSize:
        phones = [phone for phone in phones if
        float(phone['size'][:3])>=float(minSize) and float(phone['size'][:3]) <= float(maxSize)]

    # Filter by Operating System.
    if OS == 'iOS':
        phones = [phone for phone in phones if 'os' in phone and phone['os'][:3]=='iOS' and phone['os'][:5]!='watch']
    elif OS == 'Android':
        phones = [phone for phone in phones if 'os' in phone and phone['os'][:7]=='Android']

    # Filter by camera type.
    if camera == 'Dual':
        phones = [phone for phone in phones if 'primary_' in phone and phone['primary_'][:4]=='Dual']
    elif camera == 'normal':
        phones = [phone for phone in phones if 'primary_' in phone and phone['primary_'][:4]!='Dual']

    # Filter by SIM type.
    if SIM == 'Single':
        phones = [phone for phone in phones if 'sim' in phone and phone['sim'][:5]=='Single']
    elif SIM == 'Dual':
        phones = [phone for phone in phones if 'sim' in phone and phone['sim'][:4]=='Dual']
    elif SIM == 'Hybrid':
        phones = [phone for phone in phones if 'sim' in phone and phone['sim'][:6]=='Hybrid']

    # Filter by Multitouch.
    if multitouch == 'True':
        phones = [phone for phone in phones if 'multitouch' in phone and phone['multitouch'][:3]=='Yes']
    elif multitouch == 'False':
        phones = [phone for phone in phones if 'multitouch' not in phone or phone['multitouch'][:2]=='No']

    # Filter by NFC.
    if NFC == 'True':
        phones = [phone for phone in phones if 'nfc' in phone and phone['nfc'][:3]=='Yes']
    elif NFC == 'False':
        phones = [phone for phone in phones if 'nfc' not in phone or phone['nfc'][:2]=='No']

    # Filter by announce year.
    if year:
        phones = [phone for phone in phones if phone['announced'][:4] == year]

    # Return result.
    return phones
