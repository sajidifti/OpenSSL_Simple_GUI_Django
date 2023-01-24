import os
import random
import platform
from django.shortcuts import render, redirect
from gui.myOpenSSL import *
from django.contrib import messages

# Create your views here.

def home(request):
    if request.method == 'POST':
        emailAddress = request.POST['email']
        commonName = request.POST['common']
        countryName = request.POST['country']
        localityName = request.POST['local']
        stateOrProvinceName = request.POST['state']
        organizationName = request.POST['org']
        organizationUnitName = request.POST['orgunit']
        serialNumber = random.random()
        serialNumber = int(serialNumber)
        validityInDays = request.POST['validity']
        validityInDays = int(validityInDays)
        validityEndInSeconds = validityInDays*24*60*60

        algorithmNameValue = request.POST['algo']
        algorithmName = "TYPE_RSA"

        if algorithmNameValue == 1:
            algorithmName = "TYPE_RSA"
        elif algorithmNameValue == 2:
            algorithmName = "TYPE_DSA"

        hashFunctionNameValue = request.POST['hash']
        hashFunctionName = "sha256"

        if hashFunctionNameValue == 1:
            hashFunctionName = "sha256"
        elif hashFunctionNameValue == 2:
            hashFunctionName = "sha512"

        bitLengthValue = request.POST['bitlen']
        bitLength = 2048

        if bitLengthValue == 1:
            bitLength = 2048
        elif bitLengthValue == 2:
            bitLength = 4096
        
        folderPath = request.POST['folder']
        folderPath = os.path.abspath(folderPath)
        KEY_FILE_Name = request.POST['keyname']
        CERT_FILE_Name = request.POST['crtname']     
        CERT_FILE_Name = request.POST['crtname']
        KEY_FILE_Name2 = ""
        CERT_FILE_Name2 = ""
        
        hasPath = False

        if request.POST['folder'] and os.path.exists(folderPath):
            KEY_FILE_Name2 = folderPath + "/" + KEY_FILE_Name + ".key"
            CERT_FILE_Name2 = folderPath + "/" + CERT_FILE_Name + ".crt"
            hasPath = True
        else:
            if not os.path.exists("certificates/"):
                os.mkdir("certificates/")
                
            KEY_FILE_Name2 = "certificates/" + KEY_FILE_Name + ".key"
            CERT_FILE_Name2 = "certificates/" + CERT_FILE_Name + ".crt"

        cert_gen(emailAddress, commonName, countryName, localityName, stateOrProvinceName, organizationName, organizationUnitName,
                 serialNumber, validityEndInSeconds, algorithmName, hashFunctionName, bitLength, KEY_FILE_Name2, CERT_FILE_Name2)

        if hasPath:
            messages.success(request, f"The {KEY_FILE_Name}.key and {CERT_FILE_Name}.crt has been generated and saved to the '{folderPath}' folder")
        else:
            messages.success(request, f"The folder path to save the files has not been specified or invalid.\nDeafulting to '/opensslgui/certificates' folder.\n\nThe '{KEY_FILE_Name}.key' and '{CERT_FILE_Name}.crt' has been generated and saved to the '/opensslgui/certificates' folder")

        return redirect('home')
    
    opsys = platform.system()
    
    dictionary = {
        'opsys': opsys
    }

    return render(request, 'home.html', context=dictionary)
