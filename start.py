
fbOrTik=input('Please choose where to download videos from. Type "1" for Facebook or "2" for TikTok: ')
if fbOrTik=='1':
    import fb_dl

elif fbOrTik=='2':
    import tik_dl
    
else:
    print('You can only choose between "1" or "2". No other options available. Which option do you choose: \n')
    fbOrTik=input('Which option "1" or "2"?: ')
    if fbOrTik=='1':
        import fb_dl

    elif fbOrTik=='2':
        import tik_dl
    
    